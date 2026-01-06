validate_dir() {
    local dir="$1"

    if [[ -z "$dir" ]]; then
        echo "Error: directory path is not specified."
        echo "Usage: ./script05.sh /path/to/dir/"
        exit 1
    fi

    if [[ "${dir: -1}" != "/" ]]; then
        echo "Error: directory path must end with '/'."
        echo "Example: ./script05.sh /var/log/"
        exit 1
    fi

    if [[ ! -d "$dir" ]]; then
        echo "Error: '$dir' is not a directory or does not exist."
        exit 1
    fi

    if [[ ! -r "$dir" ]]; then
        echo "Error: directory '$dir' cannot be read (permission denied)."
        exit 1
    fi
}

get_total_folders() {
    local dir="$1"
    find "$dir" -type d 2>/dev/null | wc -l
}

get_top_folders() {
    local dir="$1"

    find "$dir" -type d -print0 2>/dev/null \
    | xargs -0 du -s 2>/dev/null \
    | sort -nr \
    | head -5 \
    | awk '{
        size=$1;
        path=$2;

        if (size >= 1024*1024) {
            printf "%d - %s, %.2f GB\n", NR, path, size/1024/1024
        }
        else if (size >= 1024) {
            printf "%d - %s, %.2f MB\n", NR, path, size/1024
        }
        else {
            printf "%d - %s, %d KB\n", NR, path, size
        }
    }'
}

get_total_files() {
    local dir="$1"
    find "$dir" -type f 2>/dev/null | wc -l
}

get_conf_files_count() {
    local dir="$1"
    find "$dir" -type f -name "*.conf" 2>/dev/null | wc -l
}

get_text_files_count() {
    local dir="$1"
    find "$dir" -type f -exec file {} \; 2>/dev/null \
        | grep -i "text" \
        | wc -l
}

get_executable_files_count() {
    local dir="$1"
    find "$dir" -type f -executable 2>/dev/null | wc -l
}

get_log_files_count() {
    local dir="$1"
    find "$dir" -type f -name "*.log" 2>/dev/null | wc -l
}

get_archive_files_count() {
    local dir="$1"
    find "$dir" -type f \( \
        -name "*.zip" -o \
        -name "*.tar" -o \
        -name "*.tar.gz" -o \
        -name "*.tgz" -o \
        -name "*.gz" -o \
        -name "*.bz2" -o \
        -name "*.xz" -o \
        -name "*.7z" -o \
        -name "*.rar" \
    \) 2>/dev/null | wc -l
}

get_symlinks_count() {
    local dir="$1"
    find "$dir" -type l 2>/dev/null | wc -l
}

get_top_files() {
    local dir="$1"
#для мака du -k
    find "$dir" -type f -print0 2>/dev/null \
    | xargs -0 du -b 2>/dev/null \
    | sort -nr \
    | head -10 \
    | awk '{print $1, $2}' \
    | while read -r size path; do
        type=$(file -b "$path")

        if (( size >= 1024*1024*1024 )); then
            hsize=$(printf "%.2f GB" "$(echo "$size/1024/1024/1024" | bc -l)")
        elif (( size >= 1024*1024 )); then
            hsize=$(printf "%.2f MB" "$(echo "$size/1024/1024" | bc -l)")
        elif (( size >= 1024 )); then
            hsize=$(printf "%.2f KB" "$(echo "$size/1024" | bc -l)")
        else
            hsize="${size} B"
        fi

        ((i++))
        echo "$i - $path, $hsize, $type"
    done
}

get_top_executable_files() {
    local dir="$1"
    local i=0

    find "$dir" -type f -executable -print0 2>/dev/null \
    | xargs -0 du -b 2>/dev/null \
    | sort -nr \
    | head -10 \
    | awk '{print $1, $2}' \
    | while read -r size path; do
    hash=$(md5sum "$path" | awk '{print $1}')

        if (( size >= 1024*1024 )); then
            hsize=$(printf "%.2f GB" "$(echo "$size/1024/1024" | bc -l)")
        elif (( size >= 1024 )); then
            hsize=$(printf "%.2f MB" "$(echo "$size/1024" | bc -l)")
        else
            hsize="${size} KB"
        fi

        ((i++))
        echo "$i - $path, $hsize, $hash"
    done
}

