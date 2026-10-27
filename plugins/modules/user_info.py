#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vitexus.multiflexi.plugins.module_utils.multiflexi_cli import (
    info_argument_spec,
    run_info,
)

DOCUMENTATION = """
---
module: user_info
short_description: Get information about users from MultiFlexi
description:
  - Returns users from MultiFlexi using C(multiflexi-cli). Read-only, never reports a change.
options:
  id:
    description:
      - Numeric ID of the user.
      - When given, a single record is fetched instead of the list.
    type: int
  login:
    description:
      - Login of the user.
      - When given, a single record is fetched instead of the list.
    type: str
  email:
    description:
      - E-mail of the user.
      - When given, a single record is fetched instead of the list.
    type: str
  limit:
    description: Maximum number of records to return.
    type: int
  offset:
    description: Number of records to skip.
    type: int
  order:
    description: Sort order, C(A) ascending or C(D) descending.
    type: str
    choices: ['A', 'D']
  fields:
    description: Restrict the returned records to these fields.
    type: list
    elements: str
  multiflexi_cli_path:
    description: Path to the C(multiflexi-cli) executable.
    type: str
    default: multiflexi-cli
author:
  - Vitex (@Vitexus)
"""

EXAMPLES = """
- name: List users
  vitexus.multiflexi.user_info:
  register: result

- name: Get a single record
  vitexus.multiflexi.user_info:
    login: demo
  register: result
"""

RETURN = """
users:
  description: List of records (when no selector is given).
  type: list
  elements: dict
  returned: when no selector is given
count:
  description: Number of returned records.
  type: int
  returned: when no selector is given
user:
  description: A single record, or C(null) if it was not found.
  type: dict
  returned: when a selector is given
  sample: {id: 1, login: demo, email: demo@example.com, enabled: true}
found:
  description: Whether the requested record exists.
  type: bool
  returned: when a selector is given
"""


def main():
    spec = info_argument_spec(selectors={'id': 'int', 'login': 'str', 'email': 'str'}, filters={})

    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    run_info(
        module,
        singular='user',
        plural='users',
        list_command='user:list',
        get_command='user:get',
        selectors={'id': '--id', 'login': '--login', 'email': '--email'},
        filters={},
    )


if __name__ == "__main__":
    main()
