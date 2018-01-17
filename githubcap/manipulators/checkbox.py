"""Manipulation with checkboxes."""

import typing

from githubcap.exceptions import UserInputError


class Checkbox:
    """A checkbox manipulator."""

    _CHECKED_CHECKBOX = ('* [x] ', '* [X] ', '- [x] ', '- [X] ')
    _UNCHECKED_CHECKBOX = ('* [ ] ', '- [ ] ')
    _CHECKBOX = _CHECKED_CHECKBOX + _UNCHECKED_CHECKBOX

    def __init__(self):
        """Not instantiable."""
        raise NotImplementedError

    @classmethod
    def _iterate_lines(cls, text) -> typing.Generator[str, None, None]:
        """Iterate over lines and yield line itself with info whether the given line represents a checkbox."""
        for line in text.split('\n'):
            yield line, line.lstrip().startswith(cls._CHECKBOX)

    @classmethod
    def _get_checkbox_title(cls, line: str) -> str:
        """Get title of a checkbox item."""
        return line.strip()[len('- [ ] '):]

    @classmethod
    def _do_checkbox_setting(cls, text: str, title: str, replace_args: tuple) -> typing.Tuple[str, bool, bool]:
        """Set or unset a checkbox tick in text based on checkbox title."""
        title = title.strip()

        lines = []
        found = False
        modified = False
        for line, is_checkbox in cls._iterate_lines(text):
            if is_checkbox and title == cls._get_checkbox_title(line):
                    found = True
                    lines.append(line.replace(*replace_args))
                    if line != lines[-1]:
                        modified |= True

                    continue

            lines.append(line)

        return "\n".join(lines), found, modified

    @classmethod
    def set(cls, text: str, title: str, graceful: bool = True) -> str:
        """Set a checkbox tick in text based on checkbox title.

        >>> Checkbox.set('# Foo\\n - [ ] bar', 'bar') # returns '# Foo\\n - [x] bar'
        """
        result, found, modified = cls._do_checkbox_setting(text, title, ('[ ]', '[x]', 1))

        if not found:
            raise UserInputError("Checkbox with title {!r} was not found in the provided text".format(title))

        if not graceful and not modified:
            raise UserInputError("Checkbox with title {!r} was already set".format(title))

        return result

    @classmethod
    def unset(cls, text: str, title: str, graceful: bool = True) -> str:
        """Unset a checkbox tick in text based on checkbox title.

        >>> Checkbox.unset('# Foo\\n - [x] bar', 'bar') # returns '# Foo\\n - [ ] bar'
        """
        result, found, modified = cls._do_checkbox_setting(text, title, ('[x]', '[ ]', 1))

        if not found:
            raise UserInputError("Checkbox with title {!r} was not found in the provided text".format(title))

        if not modified:
            # Try again with uppercase, we could optimize this to iterate only once.
            # This can resolve in a different behaviour on multiple runs with upper and lower case checkboxes,
            # but that is fine for now.
            result, found, modified = cls._do_checkbox_setting(text, title, ('[X]', '[ ]', 1))

        if not graceful and not modified:
            raise UserInputError("Checkbox with title {!r} was already unset".format(title))

        return result
