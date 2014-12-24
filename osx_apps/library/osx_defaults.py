#!/usr/bin/python
# -*- coding: utf-8 -*-

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

def get_value(module, domain, key):
    cmd = '/usr/bin/defaults read %s "%s"' % (domain, key)
    rc, stdout, stderr = module.run_command(cmd, check_rc=True)
    return stdout.strip()

def needs_update(module, domain, key, expected_value):
    current_value = get_value(module, domain, key)
    return not current_value == expected_value

def update_value(module, domain, key, key_type, value):
    if not needs_update(module, domain, key, value):
        return False
    if not module.check_mode:
        cmd = '/usr/bin/defaults write %s "%s" -%s %s' % (domain, key, key_type, value)
        rc, stdout, stderr = module.run_command(cmd, check_rc=True)
    return True

def main():

    module = AnsibleModule(
        argument_spec=dict(
            domain=dict(required=True),
            key=dict(required=True),
            key_type=dict(required=True),
            value=dict(required=True),
        ),
        supports_check_mode=True
    )

    if not os.path.exists('/usr/bin/defaults'):
        module.fail_json(msg='/usr/bin/defaults does not exist!')

    domain = module.params['domain']
    key = module.params['key']
    key_type = module.params['key_type']
    value = module.params['value']

    current_value = get_value(module, domain, key)
    changed_marker = update_value(module, domain, key, key_type, value)
    if changed_marker:
        msg = '%s updated from %s to %s' % (key, current_value, value)
    else:
        msg = '%s unchanged - value %s' % (key, value)

    module.exit_json(msg=msg, changed=changed_marker)

from ansible.module_utils.basic import *
main()
