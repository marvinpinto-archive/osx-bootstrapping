#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: osx_scutil
short_description: Manage a subset of the system configuration parameters
description:
  - Manage a subset of the system configuration parameters
version_added: '1.2'
author: Marvin Pinto
notes:
  - Manage a subset of the system configuration parameters
requirements:
  - Mac OSX
options:
  key:
    description:
      - defaults key, e.g. ComputerName
    required: true
    default: null
    choices: []
    aliases: []
    version_added: 1.2
  value:
    description:
      - defaults value, e.g. my-mba
    required: true
    default: null
    choices: []
    aliases: []
    version_added: 1.2
'''

EXAMPLES = '''
- name: 'Set the OSX ComputerName'
  osx_scutil:
    key: 'ComputerName'
    value: 'marvin-mba'
'''

def get_value(module, key):
    cmd = '/usr/sbin/scutil --get %s' % key
    rc, stdout, stderr = module.run_command(cmd, check_rc=True)
    return stdout.strip()

def needs_update(current_value, expected_value):
    return not current_value == expected_value

def update_value(module, key, value):
    if not module.check_mode:
        cmd = '/usr/sbin/scutil --set %s "%s"' % (key, value)
        rc, stdout, stderr = module.run_command(cmd, check_rc=True)

def main():

    module = AnsibleModule(
        argument_spec=dict(
            key=dict(required=True),
            value=dict(required=True),
        ),
        supports_check_mode=True
    )

    if not os.path.exists('/usr/sbin/scutil'):
        module.fail_json(msg='/usr/sbin/scutil does not exist!')

    key = module.params['key']
    new_value = module.params['value']

    current_value = get_value(module, key)
    if needs_update(current_value, new_value):
        update_value(module, key, new_value)
        msg = '%s updated from %s to %s' % (key, current_value, new_value)
        changed_marker = True
    else:
        msg = '%s unchanged - value %s' % (key, new_value)
        changed_marker = False

    module.exit_json(msg=msg, changed=changed_marker)

from ansible.module_utils.basic import *
main()
