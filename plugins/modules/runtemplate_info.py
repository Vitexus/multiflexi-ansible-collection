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
module: runtemplate_info
short_description: Get information about run templates from MultiFlexi
description:
  - Returns run templates from MultiFlexi using C(multiflexi-cli). Read-only, never reports a change.
options:
  id:
    description:
      - Numeric ID of the run template.
      - When given, a single record is fetched instead of the list.
    type: int
  name:
    description:
      - Name of the run template.
      - When given, a single record is fetched instead of the list.
    type: str
  company:
    description: List only run templates of this company (slug).
    type: str
  app_uuid:
    description: List only run templates of this application UUID.
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
  show_secrets:
    description:
      - Return the content of secret fields (passwords, tokens, API keys) instead of masking it as C(***).
      - Keep it off; results end up in job logs.
    type: bool
    default: false
  multiflexi_cli_path:
    description: Path to the C(multiflexi-cli) executable.
    type: str
    default: multiflexi-cli
author:
  - Vitex (@Vitexus)
"""

EXAMPLES = """
- name: List run templates
  vitexus.multiflexi.runtemplate_info:
  register: result

- name: Get a single record
  vitexus.multiflexi.runtemplate_info:
    id: 5
  register: result
"""

RETURN = """
runtemplates:
  description: List of records (when no selector is given).
  type: list
  elements: dict
  returned: when no selector is given
count:
  description: Number of returned records.
  type: int
  returned: when no selector is given
runtemplate:
  description: A single record, or C(null) if it was not found.
  type: dict
  returned: when a selector is given
  sample: {id: 5, name: Daily invoices, app_id: 12, company_id: 1, interv: d}
found:
  description: Whether the requested record exists.
  type: bool
  returned: when a selector is given
"""


def main():
    spec = info_argument_spec(selectors={'id': 'int', 'name': 'str'}, filters={'company': 'str', 'app_uuid': 'str'})

    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    run_info(
        module,
        singular='runtemplate',
        plural='runtemplates',
        list_command='run-template:list',
        get_command='run-template:get',
        selectors={'id': '--id', 'name': '--name'},
        filters={'company': '--company', 'app_uuid': '--app_uuid'},
    )


if __name__ == "__main__":
    main()
