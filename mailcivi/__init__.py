"""
Mailcivi command line tool
"""
__all__ = [
    'CiviMailTemplate',
    'mailcivi',
    'main',
    'readjson',
    'readlocal',
    'fetch_url',
    'connect_to_civi',
    'check_creator_exists',
    'create_template',
    'group_id_from_title',
    'creator_id_from_name',
]

from __main__ import mailcivi
from __main__ import CiviMailTemplate
from __main__ import connect_to_civi
from __main__ import check_creator_exists
from __main__ import create_template
from __main__ import creator_id_from_name
from __main__ import group_id_from_title
