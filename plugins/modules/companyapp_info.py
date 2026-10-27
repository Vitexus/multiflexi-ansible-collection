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
module: companyapp_info
short_description: Get information about company/application assignments from MultiFlexi
description:
  - Returns company/application assignments from MultiFlexi using C(multiflexi-cli). Read-only, never reports a change.
options:
  company_id:
    description: List only assignments of this company ID.
    type: int
  app_id:
    description: List only assignments of this application ID.
    type: int
  app_uuid:
    description: List only assignments of this application UUID.
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
      - Without it only a short allowlist of non-secret fields is returned for credentials, tokens and event sources.
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
- name: List company/application assignments
  vitexus.multiflexi.companyapp_info:
  register: result
"""

RETURN = """
companyapps:
  description: List of records (when no selector is given).
  type: list
  elements: dict
  returned: when no selector is given
count:
  description: Number of returned records.
  type: int
  returned: when no selector is given
companyapp:
  description: A single record, or C(null) if it was not found.
  type: dict
  returned: when a selector is given
  sample: {id: 7, company_id: 1, app_id: 12}
found:
  description: Whether the requested record exists.
  type: bool
  returned: when a selector is given
"""


def main():
    spec = info_argument_spec(selectors={}, filters={'company_id': 'int', 'app_id': 'int', 'app_uuid': 'str'})

    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    run_info(
        module,
        singular='companyapp',
        plural='companyapps',
        list_command='company-app:list',
        get_command=None,
        selectors={},
        filters={'company_id': '--company_id', 'app_id': '--app_id', 'app_uuid': '--app_uuid'},
        safe_fields=None,
    )


if __name__ == "__main__":
    main()
