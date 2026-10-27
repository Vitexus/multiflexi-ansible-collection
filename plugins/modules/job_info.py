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
module: job_info
short_description: Get information about jobs from MultiFlexi
description:
  - Returns jobs from MultiFlexi using C(multiflexi-cli). Read-only, never reports a change.
options:
  id:
    description:
      - Numeric ID of the job.
      - When given, a single record is fetched instead of the list.
    type: int
  status:
    description: List only jobs with this status.
    type: str
    choices: ['failed', 'success', 'running', 'pending']
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
- name: List jobs
  vitexus.multiflexi.job_info:
  register: result

- name: Get a single record
  vitexus.multiflexi.job_info:
    id: 100
  register: result
"""

RETURN = """
jobs:
  description: List of records (when no selector is given).
  type: list
  elements: dict
  returned: when no selector is given
count:
  description: Number of returned records.
  type: int
  returned: when no selector is given
job:
  description: A single record, or C(null) if it was not found.
  type: dict
  returned: when a selector is given
  sample: {id: 100, runtemplate_id: 5, app_id: 12, exitcode: 0}
found:
  description: Whether the requested record exists.
  type: bool
  returned: when a selector is given
"""


def main():
    spec = info_argument_spec(selectors={'id': 'int'}, filters={'status': 'str'})
    spec['status']['choices'] = ['failed', 'success', 'running', 'pending']

    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    run_info(
        module,
        singular='job',
        plural='jobs',
        list_command='job:list',
        get_command='job:get',
        selectors={'id': '--id'},
        filters={'status': '--status'},
    )


if __name__ == "__main__":
    main()
