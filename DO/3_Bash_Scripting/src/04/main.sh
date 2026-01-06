#!/bin/bash

source ./lib/help_functions.sh
source ./config.conf

column1_background=${column1_background:-6}
column1_font_color=${column1_font_color:-1}
column2_background=${column2_background:-2}
column2_font_color=${column2_font_color:-4}

validate_params \
  "$column1_background" \
  "$column1_font_color" \
  "$column2_background" \
  "$column2_font_color"

NAME_BACKGROUND_COLOR=$(get_bg_color "$column1_background")
NAME_FONT_COLOR=$(get_font_color "$column1_font_color")
VALUE_BACKGROUND_COLOR=$(get_bg_color "$column2_background")
VALUE_FONT_COLOR=$(get_font_color "$column2_font_color")

source ./lib/assemble_data.sh
source ./lib/create_output.sh

print_scheme
