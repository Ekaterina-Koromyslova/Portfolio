#!/bin/bash

source "./lib/help_functions.sh"
validate_params "$@"

NAME_BACKGROUND_COLOR=$(get_bg_color "$1")
NAME_FONT_COLOR=$(get_font_color "$2")
VALUE_BACKGROUND_COLOR=$(get_bg_color "$3")
VALUE_FONT_COLOR=$(get_font_color "$4")

source "./lib/assemble_data.sh"
source "./lib/create_output.sh"


