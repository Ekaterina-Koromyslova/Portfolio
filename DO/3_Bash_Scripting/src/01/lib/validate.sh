#! /usr/bin/bash

is_number () {
    
    local input="$1"

    [[ "$input" =~ ^[+-]?[0-9]+([.,][0-9]+)?$ ]]
}