#!/usr/bin/bash


# TIMEZONE
get_timezone_name() {
    timedatectl | grep "Time zone" | awk '{print $3}'
}

timezone_utc_offset() {
    local utc_raw_offset offset_sign hh mm

    utc_raw_offset="$(date +%z)"
    offset_sign="${utc_raw_offset:0:1}"
    hh="${utc_raw_offset:1:2}"
    mm="${utc_raw_offset:3:2}"

    if [[ "$mm" != "00" ]]; then
        echo "UTC ${offset_sign}${hh}:${mm}"
    else
        echo "UTC ${offset_sign}${hh}"
    fi
}

# MASK
get_mask() {
    local prefix mask
    prefix="$(ip -o -f inet addr show | awk '{print $4}' | head -n1 | cut -d/ -f2)"

    mask=$(printf "%d.%d.%d.%d" \
        $(( (0xffffffff << (32-prefix)) >> 24 & 255 )) \
        $(( (0xffffffff << (32-prefix)) >> 16 & 255 )) \
        $(( (0xffffffff << (32-prefix)) >> 8 & 255 )) \
        $(( (0xffffffff << (32-prefix)) >> 0 & 255 ))
    )

    echo "$mask"
}

# RAM_TOTAL
get_ram_total() {
    awk '/MemTotal/ {printf "%.3f GB", $2/1024/1024}' /proc/meminfo
}

# RAM_USED
get_ram_used() {
    awk '
        /MemTotal/    {total=$2}
        /MemAvailable/ {available=$2}
        END {
            used = total - available
            printf "%.3f GB", used/1024/1024
        }
    ' /proc/meminfo
}

#RAM_FREE
get_ram_free() {
    awk '
        /MemAvailable/ {
            printf "%.3f GB", $2/1024/1024
        }
    ' /proc/meminfo
}

# SPACE_ROOT / USED / FREE
get_space_root_value() {
    local field value

    case "$1" in
        size) field=2 ;;
        used) field=3 ;;
        free) field=4 ;;
        *) echo "Invalid parameter" >&2; return 1 ;;
    esac

    value=$(df -BM / | awk -v f="$field" 'NR==2 {
        v=$f
        sub(/M$/, "", v)
        printf "%.2f MB", v
    }')

    echo "$value"
}

# Part 3

validate_params() {
    # Проверяем что ровно 4 аргумента
    if [[ $# -ne 4 ]]; then
        echo "Error: script must be run with 4 parameters (1-6)."
        exit 1
    fi

    for param in "$@"; do
        if ! [[ "$param" =~ ^[1-6]$ ]]; then
            echo "Error: parameters must be numbers from 1 to 6."
            exit 1
        fi
    done

    if [[ "$1" -eq "$2" ]]; then
        echo "Error: background and font color for NAMES must not match."
        echo "Please run the script again with different parameters."
        exit 1
    fi

    if [[ "$3" -eq "$4" ]]; then
        echo "Error: background and font color for VALUES must not match."
        echo "Please run the script again with different parameters."
        exit 1
    fi
}

get_font_color() {
    case "$1" in
        1) echo "37" ;;
        2) echo "31" ;;
        3) echo "32" ;;
        4) echo "34" ;;
        5) echo "35" ;;
        6) echo "30" ;;
        *) echo "37" ;;
    esac
}

get_bg_color() {
    case "$1" in
        1) echo "47" ;;
        2) echo "41" ;;
        3) echo "42" ;;
        4) echo "44" ;;
        5) echo "45" ;;
        6) echo "40" ;;
        *) echo "47" ;;
    esac
}

print_colored_line() {
    local name="$1"
    local value="$2"

    local name_width=18
    local value_width=28

    local formatted_name
    local formatted_value

    formatted_name=$(printf "%-${name_width}s" "$name")
    formatted_value=$(printf "%-${value_width}s" "$value")

    printf "\033[%s;%sm%s\033[0m = \033[%s;%sm%s\033[0m\n" \
        "$NAME_BACKGROUND_COLOR" "$NAME_FONT_COLOR" "$formatted_name" \
        "$VALUE_BACKGROUND_COLOR" "$VALUE_FONT_COLOR" "$formatted_value"
}




