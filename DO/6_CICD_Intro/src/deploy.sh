#!/bin/bash
set -Eeuo pipefail

USER="rankenfv"
HOST="192.168.64.42"

ART_DIR="src/ci_artifacts"
TARGET_DIR="/usr/local/bin"
TMP_DIR="/tmp/deploy_tmp"

SSH="ssh -o BatchMode=yes -p 22"
SCP="scp -P 22"

echo ">>> Deploy started: копируем артефакты на ${USER}@${HOST} <<<"

$SSH "${USER}@${HOST}" "/usr/bin/mkdir -p '${TMP_DIR}'"

if $SCP "${ART_DIR}/s21_cat" "${ART_DIR}/s21_grep" "${USER}@${HOST}:${TMP_DIR}/"; then
  echo ">>> Файлы скопированы во временный каталог ${TMP_DIR}"
else
  echo ">>> Ошибка при копировании во временный каталог"
  exit 1
fi

if $SSH "${USER}@${HOST}" "
  sudo /usr/bin/mkdir -p '${TARGET_DIR}' &&
  sudo /usr/bin/mv '${TMP_DIR}/s21_cat' '${TMP_DIR}/s21_grep' '${TARGET_DIR}/' &&
  sudo /usr/bin/chmod +x '${TARGET_DIR}/s21_cat' '${TARGET_DIR}/s21_grep' &&
  sudo /usr/bin/rm -rf '${TMP_DIR}'
"; then
  echo ">>> Файлы успешно развернуты в ${TARGET_DIR}"
else
  echo ">>> Ошибка при перемещении файлов в ${TARGET_DIR}"
  exit 1
fi

echo ">>> Deploy finished SUCCESS <<<"



