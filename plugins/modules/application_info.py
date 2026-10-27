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
module: application_info
short_description: Get information about applications from MultiFlexi
description:
  - Returns applications from MultiFlexi using C(multiflexi-cli). Read-only, never reports a change.
options:
  id:
    description:
      - Numeric ID of the application.
      - When given, a single record is fetched instead of the list.
    type: int
  uuid:
    description:
      - UUID of the application.
      - When given, a single record is fetched instead of the list.
    type: str
  name:
    description:
      - Name of the application.
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
- name: List applications
  vitexus.multiflexi.application_info:
  register: result

- name: Get a single record
  vitexus.multiflexi.application_info:
    uuid: 78fa718c-0000-0000-0000-000000000000
  register: result
"""

RETURN = """
applications:
  description: List of records (when no selector is given).
  type: list
  elements: dict
  returned: when no selector is given
count:
  description: Number of returned records.
  type: int
  returned: when no selector is given
application:
  description: A single record, or C(null) if it was not found.
  type: dict
  returned: when a selector is given
  sample: {id: 12, uuid: 78fa718c-..., name: AbraFlexi Contract Invoices, executable: abraflexi-contract-invoices}
found:
  description: Whether the requested record exists.
  type: bool
  returned: when a selector is given
"""


def main():
    spec = info_argument_spec(selectors={'id': 'int', 'uuid': 'str', 'name': 'str'}, filters={})

    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    run_info(
        module,
        singular='application',
        plural='applications',
        list_command='application:list',
        get_command='application:get',
        selectors={'id': '--id', 'uuid': '--uuid', 'name': '--name'},
        filters={},
    )


if __name__ == "__main__":
    main()
