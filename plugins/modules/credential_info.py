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
module: credential_info
short_description: Get information about credentials from MultiFlexi
description:
  - Returns credentials from MultiFlexi using C(multiflexi-cli). Read-only, never reports a change.
options:
  id:
    description:
      - Numeric ID of the credential.
      - When given, a single record is fetched instead of the list.
    type: int
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
- name: List credentials
  vitexus.multiflexi.credential_info:
  register: result

- name: Get a single record
  vitexus.multiflexi.credential_info:
    id: 3
  register: result
"""

RETURN = """
credentials:
  description: List of records (when no selector is given).
  type: list
  elements: dict
  returned: when no selector is given
count:
  description: Number of returned records.
  type: int
  returned: when no selector is given
credential:
  description: A single record, or C(null) if it was not found.
  type: dict
  returned: when a selector is given
  sample: {id: 3, name: Demo AbraFlexi, company_id: 1, credential_type_id: 2}
found:
  description: Whether the requested record exists.
  type: bool
  returned: when a selector is given
"""


def main():
    spec = info_argument_spec(selectors={'id': 'int'}, filters={})

    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    run_info(
        module,
        singular='credential',
        plural='credentials',
        list_command='credential:list',
        get_command='credential:get',
        selectors={'id': '--id'},
        filters={},
    )


if __name__ == "__main__":
    main()
