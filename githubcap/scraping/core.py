import json
import re
import typing
import logging
import os
from typing import Optional

import bs4
import requests

from githubcap import Configuration


_LOG = logging.getLogger(__name__)
_TRANSLATE_VAR_TYPE = {
    'string': 'str',
    'integer': 'int',
    'boolean': 'bool',
    'array of integers': '[int]',
    'array of objects': '[object]',
    'array of strings': '[str]'
}


_PARAM_RE = re.compile(':([A-Za-z0-9-_]+)')
_NO_SCRAPE_SITES = frozenset((
    '/v3/',
    '/v3/api-previews/',
    '/v3/apps/available-endpoints/',
    '/v3/apps/marketplace/',
    '/v3/apps/marketplace/',
    '/v3/auth/',
    '/v3/enterprise/',
    '/v3/enterprise-admin/admin_stats/',
    '/v3/enterprise-admin/global_webhooks/',
    '/v3/enterprise-admin/ldap/',
    '/v3/enterprise-admin/license/',
    '/v3/enterprise-admin/management_console/',
    '/v3/enterprise-admin/orgs/',
    '/v3/enterprise-admin/pre_receive_environments/',
    '/v3/enterprise-admin/pre_receive_hooks/',
    '/v3/enterprise-admin/search_indexing/',
    '/v3/git/',
    '/v3/media/',
    '/v3/migration/',
    '/v3/misc/',
    '/v3/orgs/pre_receive_hooks/',
    '/v3/pre-release/',
    '/v3/previews/',
    '/v3/repos/pre_receive_hooks/',
    '/v3/search/legacy/',
    '/v3/troubleshooting/',
    '/v3/users/administration/',
    '/v3/versions/',
    # No support for activity yet
    '/v3/activity/',
    '/v3/activity/events/',
    '/v3/activity/events/types/',
    '/v3/activity/feeds/',
    '/v3/activity/notifications/',
    '/v3/activity/starring/',
    '/v3/activity/watching/',
))


def _get_item_href(item: bs4.element.Tag):
    return item['href'].split('#', maxsplit=1)


def _add_section(result: dict, link: str, text: typing.Tuple[str, typing.Union[None, str]]) -> None:
    """Add section to the resulting scraping section."""
    if link in _NO_SCRAPE_SITES:
        _LOG.debug("Skipping blacklisted section %s%s", Configuration().github_docs, link)
        return

    _LOG.debug("Found section to be scraped %r: %s%s",
               text, Configuration().github_docs, link)
    if link in result:
        raise ValueError
    result[link] = text


def _scrape_sections() -> dict:
    """Get listing of sections with their headings."""
    result = {}
    _LOG.debug("Scraping available sections")
    response = requests.get("{}/{}".format(Configuration().github_docs, Configuration().github_docs_version))
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    for topic in soup.find_all('li', {'class': 'js-topic'}):
        item = topic.h3.find_all('a')
        if not item or len(item) != 2:
            continue

        item = item[1]
        link = _get_item_href(item)
        if len(link) != 1:
            # Omit references to the same document e.g. '/v3/search/#search-repositories'
            _LOG.debug("Omitting in-document reference %r", link)
            continue

        _add_section(result, link[0], (item.text, None))

        for child in topic.findChildren():
            if child.name != 'li':
                continue

            link = _get_item_href(child.a)
            if link is None or len(link) != 1:
                # Omit references to the same document
                _LOG.debug("Omitting in-document reference %r", link)
                continue
            _add_section(result, link[0], (item.text, child.text))

    return result


def _where_location(record: dict, item: str, last_section_title: str, last_subsection_title: str) -> dict:
    """Get information where a parsed item should be stored in the resulting JSON."""
    where = record[item]

    if last_section_title:
        if last_section_title not in where:
            where['@sections'] = {}
        where = where['@sections']

        key = last_section_title
        if key not in where:
            where[key] = {}
        where = where[key]
    else:
        if '@top' not in where:
            where['@top'] = {}
        where = where['@top']

    if last_subsection_title:
        key = '@subsections'
        if key not in where:
            where[key] = {}
        where = where[key]
        if last_subsection_title not in where:
            where[last_subsection_title] = {}
        where = where[last_subsection_title]

    return where


def _get_last_desc_text(last_desc: bs4.element.Tag) -> typing.Union[None, str]:
    """Retrieve last description text if any provided."""
    if last_desc is None:
        return None

    text = last_desc.text.strip().replace('\n', ' ')
    if text:
        text = text[:-1] + '.'

    return text


def _parse_type_definition(table: bs4.element.Tag) -> list:
    """Parse type definition from table representation."""
    result = []
    for row in table.find_all('tr')[1:]:
        type_desc = tuple(column.text.strip() for column in row.find_all('td'))
        var_type = type_desc[1] if len(type_desc) == 3 else None
        if var_type and var_type.startswith('array of '):
            new_var_type = _TRANSLATE_VAR_TYPE.get(var_type)
            if new_var_type:
                var_type = new_var_type
            elif var_type.endswith('objects'):
                var_type = '[object]'
            else:
                raise ValueError("Unable to uniquely parse type %r assuming a list of objects" % var_type)

        result.append({
            '@name': type_desc[0],
            '@type': var_type,
            '@description': type_desc[2] if len(type_desc) == 3 else type_desc[1]
        })

    return result


def _parse_request_def(request_string: str, last_desc: str) -> dict:
    """Parse request endpoint description and method used."""
    method, endpoint = request_string.strip().split(' ', maxsplit=1)
    return {
        '@method': method,
        '@endpoint': re.sub(_PARAM_RE, r"{\1}", endpoint.strip()),
        '@description': _get_last_desc_text(last_desc)
    }


def _find_section_description(section: bs4.element.Tag) -> typing.Union[str, None]:
    """Find description of a section."""
    description = None
    tag = section.next_sibling
    while isinstance(tag, bs4.element.NavigableString):
        tag = tag.next_sibling

    if tag and tag.name == 'p':
        _LOG.debug('Found section description for %r', section.text)
        description = tag.text.replace('\n', ' ')
        if description and description[-1] == ':':
            description = description[:-1] + '.'

    return description


def _do_scrape(sections: dict, schemas_dir: Optional[str] = None, resources_dir: Optional[str] = None) -> dict:
    """Scrape remote documentation and return its parsed representation."""
    _LOG.debug("Creating directory %r for resources", resources_dir)
    os.makedirs(resources_dir, exist_ok=True)
    _LOG.debug("Creating directory %r for schemas", schemas_dir)
    os.makedirs(schemas_dir, exist_ok=True)

    all_items = {}
    for link, (item_tag, item_title) in sections.items():
        record = {}
        all_items[link] = record
        url = "{}{}".format(Configuration().github_docs, link)
        _LOG.debug("Scraping %r to automatically construct classes", url)
        response = requests.get(url)
        response.raise_for_status()

        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        content = soup.find_all('div', {'class': 'content'})
        if len(content) != 1:
            raise ValueError("Found multiple contents in %r", url)
        content = content[0]

        for obj in content.find_all('h2'):
            if obj is None or not isinstance(obj, bs4.element.Tag):
                continue

            if obj.name != 'h2':
                continue

            item = obj.text.strip()
            assert item not in record
            record[item] = {}
            last_desc = None
            last_section_title = None
            last_subsection_title = None
            for sibling in obj.next_siblings:
                if sibling.name == 'h2':
                    break

                if isinstance(sibling, bs4.element.NavigableString):
                    continue

                if sibling.name == 'p':
                    last_desc = sibling

                if sibling.name in 'h3':
                    last_section_title = sibling.text.strip()
                    last_subsection_title = None
                    _LOG.debug("Found new section %r in %r", last_section_title, item)

                if sibling.name in 'h4':
                    last_subsection_title = sibling.text.strip()
                    _LOG.debug("Found new sub-section %r in %r", last_subsection_title, item)

                if sibling.name == 'pre' and \
                        sibling.text.lstrip().startswith(('GET', 'DELETE', 'PATCH', 'POST', 'PUT', 'DELETE')):
                    where = _where_location(record, item, last_section_title, last_subsection_title)
                    if '@requests' not in where:
                        where['@requests'] = []
                    where['@requests'].append(_parse_request_def(sibling.text, last_desc))

                if sibling.name == 'table':
                    _LOG.debug("Found table describing types for %r (subsection %r) in %r",
                               last_section_title, last_subsection_title, item)
                    where = _where_location(record, item, last_section_title, last_subsection_title)
                    type_def = _parse_type_definition(sibling)
                    if '@types' in where:
                        var_name = last_desc.find('code').text
                        if '@subtypes' not in where:
                            where['@subtypes'] = []
                        where['@subtypes'].append({var_name: type_def})
                    else:
                        where['@types'] = type_def

                if sibling.name == 'pre' and 'highlight-json' in sibling.attrs.get('class', []):
                    _LOG.debug("Found JSON format in %r for %r, subsection %r",
                               last_section_title, item, last_subsection_title)
                    where = _where_location(record, item, last_section_title, last_subsection_title)
                    if '@json' not in where:
                        where['@json'] = []
                    where['@json'].append(json.loads(sibling.text))

                if sibling.name == 'pre' and 'highlight-headers' in sibling.attrs.get('class', []):
                    _LOG.debug("Found headers in %r for %r, subsection %r",
                               last_section_title, item, last_subsection_title)
                    where = _where_location(record, item, last_section_title, last_subsection_title)
                    if '@headers' not in where:
                        where['@headers'] = []
                    where['@headers'].append(sibling.text)

                if sibling.name == 'div' and 'note' in sibling.attrs.get('class', []):
                    for s in sibling.find_all('code'):
                        if s.name == 'code' and s.text.startswith('application/vnd.github.'):
                            where = _where_location(record, item, last_section_title, last_subsection_title)
                            assert '@additonal-headers' not in where, where
                            where['@additional-headers'] = s.text.strip()

            if not record[item]:
                _LOG.debug("No valuable data found for %r", item)
                record.pop(item)
            else:
                record[item]['@description'] = _find_section_description(obj)
                record[item]['@tag'] = item_tag
                record[item]['@title'] = item_title

    return all_items


def _convert2swagger(internal_representation: dict) -> dict:
    paths = {}
    for url, entries in internal_representation.items():
        for item_desc, value in entries.items():
            if not value or '@top' not in value:
                continue

            for request in value['@top'].get('@requests', []):
                if request['@endpoint'] not in paths:
                    paths[request['@endpoint']] = {}

                paths[request['@endpoint'].lower()] = {
                    request['@method'].lower(): {
                        'summary': request['@description'] or "",
                        'tags': [value['@tag']]
                    }
                }

    return {
        'paths': paths,
        "produces": [
            "application/json"
        ],
        "swagger": "2.0",
        "info": {
            "description": "GitHub API v3 swagger definition."
        },
        "host": Configuration().github_api,
        "basePath": "/{}".format(Configuration().github_docs_version),
        "schemes": "https"
    }


def scrape(schemas_dir: Optional[str] = None, resources_dir: Optional[str] = None) -> dict:
    """Scrape GitHub API v3 and autonomously construct schemas and resource classes."""
    sections = _scrape_sections()
    result = _do_scrape(sections, schemas_dir, resources_dir)
    result = _convert2swagger(result)
    return result
