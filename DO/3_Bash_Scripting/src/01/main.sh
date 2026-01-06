#! /bin/bash

set -eu

source "./lib/validate.sh"

if [[ $# -ne 1 ]]; then
echo "Error: exactly one parameter is required"
exit 1
fi

argument="$1"

if is_number "$argument"; then
echo "Invalid input: parameter is a number. Should be text."
exit 1
fi

echo "$argument"