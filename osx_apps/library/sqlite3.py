#!/usr/bin/python
# -*- coding: utf-8 -*-

sqlite = '/usr/bin/sqlite3'

DOCUMENTATION = '''
---
module: osx_defaults
short_description: Access a subset of the Mac OS X user defaults system
description:
  - Access a subset of the Mac OS X user defaults system
version_added: '1.2'
author: Marvin Pinto
notes:
  - Access a subset of the Mac OS X user defaults system
requirements:
  - Mac OSX
options:
  domain:
    description:
      - defaults domain, e.g. com.apple.systemsound
    required: true
    default: null
    choices: []
    aliases: []
    version_added: 1.2
  key:
    description:
      - defaults key, e.g. com.apple.sound.uiaudio.enabled
    required: true
    default: null
    choices: []
    aliases: []
    version_added: 1.2
  key_type:
    description:
      - defaults key type, e.g. int, string
    required: true
    default: null
    choices: []
    aliases: []
    version_added: 1.2
  value:
    description:
      - defaults value, e.g. 0
    required: true
    default: null
    choices: []
    aliases: []
    version_added: 1.2
'''

EXAMPLES = '''
- name: 'Disable system UI sound effects'
  osx_defaults:
    domain: 'com.apple.systemsound'
    key: 'com.apple.sound.uiaudio.enabled'
    key_type: 'int'
    value: '0'
'''

def get_value(module, database, check_stmt):
    cmd = '%s "%s" "%s"' % (sqlite, database, check_stmt)
    rc, stdout, stderr = module.run_command(cmd, check_rc=False)
    if rc:
        return None
    return stdout.strip()

def update_value(module, database, update_stmt):
    if not module.check_mode:
        cmd = '%s "%s" "%s"' % (sqlite, database, update_stmt)
        rc, stdout, stderr = module.run_command(cmd, check_rc=True)

def needs_update(current_value, expected_value):
    return not current_value == expected_value

def main():

    module = AnsibleModule(
        argument_spec=dict(
            database=dict(required=True),
            check_stmt=dict(required=True),
            expected_check_output=dict(required=True),
            update_stmt=dict(required=True),
        ),
        supports_check_mode=True
    )

    database = module.params['database']
    check_stmt = module.params['check_stmt']
    expected_check_output = module.params['expected_check_output']
    update_stmt = module.params['update_stmt']

    for i in [sqlite, database]:
        if not os.path.exists(i):
            module.fail_json(msg='%s does not exist!' % i)

    if not os.access(database, os.W_OK):
        module.fail_json(msg='%s is not writable!' % database)

    current_value = get_value(module, database, check_stmt)

    if needs_update(current_value, expected_check_output):
        update_value(module, database, update_stmt)
        msg = '%s updated from %s to %s' % (database, current_value, expected_check_output)
        changed_marker = True
    else:
        msg = '%s unchanged - value %s' % (database, expected_check_output)
        changed_marker = False

    module.exit_json(msg=msg, changed=changed_marker)

from ansible.module_utils.basic import *
main()
