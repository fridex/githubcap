"""A clean library for manipulating with GitHub API v3 with CLI interface and bunch of useful things."""

from .configuration import Configuration
from .configuration import ConfigurationDefaults
from .enums import AuthorAssociation
from .enums import Filtering
from .enums import Sorting
from .enums import SortingDirection
from .enums import State
from .enums import UserType
from .token_management import Token
from .token_management import TokenManagement
from .utils import setup_logging

__version__ = '1.0.0rc1'
__title__ = 'githubcap'
__author__ = 'Fridolin Pokorny'
__license__ = 'ASL 2.0'
__copyright__ = 'Copyright 2018 Fridolin Pokorny'
