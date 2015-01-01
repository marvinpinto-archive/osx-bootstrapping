#!/usr/bin/awk -f
# Remove Skipped lines from Ansible output, and if a full TASK section has only skipped lines do not print TASK line
# Written by Todd Wells  todd@wells.ws
#
# If TASK line, put line in buffer and do not print
# Remove all skipping lines ( both with and without color coding)
# if TASK buffer empty, print line
# if TASK buffer is full and current line is blank, TASK was followed only by skipped lines.  Do not print TASK and clear buffer
# TASK buffer full and current line not blank.  TASK followed by a non-skipped line ( OK, Changed).  Print TASK, current line and clear buffer
#
# color coding can be preserved by using the environment variable option
# export ANSIBLE_FORCE_COLOR=true
# to preserve color in jenkins, https://major.io/2014/06/25/get-colorful-ansible-output-in-jenkins/

# This was shamelessly stolen (and slightly modified) from:
# https://github.com/ansible/ansible/issues/3324#issuecomment-55461675
# This definitely has some edge cases but I'm okay with this for now

/^TASK/ { TL=$0; next }
/^GATHERING FACTS/ { next }
/^skipping/ { next }
/^ok/ { next }
/^$/ { next }
{
  if ( TL== "" ){
       print }
  else if ( $0 == ""  ) {
       TL=""; next }
  else {
       print TL; print ; TL="" }
}
