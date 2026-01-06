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
