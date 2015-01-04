#!/bin/bash
SCRIPT=`/usr/local/bin/grealpath  ${0}`
SCRIPTDIR=`/usr/bin/dirname ${SCRIPT}`
DFVERSION=${SCRIPTDIR}/roles/common/files/dfversion
git -C "${SCRIPTDIR}" --no-pager rev-parse --short HEAD > "${DFVERSION}"
