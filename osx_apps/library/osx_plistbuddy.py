#!/usr/bin/python
# -*- coding: utf-8 -*-

plistbuddy = '/usr/libexec/plistbuddy'
defaults = '/usr/bin/defaults'

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

def get_value(module, key, plist_file):
    cmd = '%s -c "Print %s" %s' % (plistbuddy, key, plist_file)
    rc, stdout, stderr = module.run_command(cmd, check_rc=False)
    if rc:
        return None
    return stdout.strip()

def create_value(module, key, key_type, value, plist_file):
    if not module.check_mode:
        cmd = '%s -c "Add %s %s %s" %s' % (plistbuddy, key, key_type, value, plist_file)
        rc, stdout, stderr = module.run_command(cmd, check_rc=True)

def update_value(module, key, value, plist_file):
    if not module.check_mode:
        cmd = '%s -c "Set %s %s" %s' % (plistbuddy, key, value, plist_file)
        rc, stdout, stderr = module.run_command(cmd, check_rc=True)

def needs_update(current_value, expected_value):
    return not current_value == expected_value

def persist_value(module, persist_domain):
    # http://www.cnet.com/how-to/how-to-manually-edit-defaults-plist-files-in-mavericks
    if not module.check_mode:
        cmd = '%s read "%s"' % (defaults, persist_domain)
        rc, stdout, stderr = module.run_command(cmd, check_rc=True)

def main():

    module = AnsibleModule(
        argument_spec=dict(
            key=dict(required=True),
            key_type=dict(required=True),
            value=dict(required=True),
            plist_file=dict(required=True),
            persist_domain=dict(required=True),
            force=dict(default=False,choices=BOOLEANS),
        ),
        supports_check_mode=True
    )

    for i in [defaults, plistbuddy]:
        if not os.path.exists(i):
            module.fail_json(msg='%s does not exist!' % i)

    key = module.params['key']
    key_type = module.params['key_type']
    new_value = module.params['value']
    plist_file = module.params['plist_file']
    persist_domain = module.params['persist_domain']
    force = module.boolean(module.params['force'])

    current_value = get_value(module, key, plist_file)

    if (not force) and (current_value is None):
        msg = '%s does not exist and force not specified' % key
        module.fail_json(msg=msg)

    if current_value is None:
        create_value(module, key, key_type, new_value, plist_file)
        persist_value(module, persist_domain)
        msg = '%s successfully created' % key
        changed_marker = True
    elif needs_update(current_value, new_value):
        update_value(module, key, new_value, plist_file)
        persist_value(module, persist_domain)
        msg = '%s updated from %s to %s' % (key, current_value, new_value)
        changed_marker = True
    else:
        msg = '%s unchanged - value %s' % (key, new_value)
        changed_marker = False

    module.exit_json(msg=msg, changed=changed_marker)

from ansible.module_utils.basic import *
main()
