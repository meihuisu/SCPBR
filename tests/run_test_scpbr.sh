#!/bin/bash

if [[ -z "${UCVM_INSTALL_PATH}" ]]; then
  if [[ -f "${UCVM_INSTALL_PATH}/model/scpbr/lib" ]]; then
    env DYLD_LIBRARY_PATH=${UCVM_INSTALL_PATH}/model/scpbr/lib ./test_scpbr
    exit
  fi
fi
env DYLD_LIBRARY_PATH=../src ./test_scpbr
