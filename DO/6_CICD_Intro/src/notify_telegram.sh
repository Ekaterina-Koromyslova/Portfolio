#!/bin/bash
set -e

: "${TG_BOT_TOKEN:?missing TG_BOT_TOKEN in runner env}"
: "${TG_CHAT_ID:?missing TG_CHAT_ID in runner env}"

build_status="failed";  [ -f ci_status/build_ok ]  && build_status="passed"
style_status="failed";  [ -f ci_status/style_ok ]  && style_status="passed"
tests_status="failed";  [ -f ci_status/tests_ok ]  && tests_status="passed"

if [ -f ci_status/deploy_ok ]; then
  deploy_status="passed"
else
  if [ "${build_status}${style_status}${tests_status}" != "passedpassedpassed" ]; then
    deploy_status="not run"
  else
    deploy_status="skipped"
  fi
fi

message_text="$(printf '%s DO6 CI/CD\nCI: build=%s, style=%s, tests=%s\nCD: deploy=%s\n%s' \
  "${CI_PROJECT_PATH}" \
  "${build_status}" "${style_status}" "${tests_status}" \
  "${deploy_status}" \
  "${CI_PIPELINE_URL}")"

# отправка в Telegram
curl -sS -X POST "https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage" \
  -d chat_id="${TG_CHAT_ID}" \
  --data-urlencode "text=${message_text}" >/dev/null

echo "Telegram notification sent."
