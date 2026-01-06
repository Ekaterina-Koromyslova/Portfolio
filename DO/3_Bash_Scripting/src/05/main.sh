# /bin/bash

source ./lib/help_functions.sh
start_time=$(date +%s.%N)

DIR="$1"
validate_dir "$DIR"

echo "Total number of folders (including all nested ones) = $(get_total_folders "$DIR")"
echo "TOP 5 folders of maximum size arranged in descending order (path and size): = $(get_top_folders "$DIR")"
echo "Total number of files = $(get_total_files "$DIR")"
echo "Configuration files (with the .conf extension) = $(get_conf_files_count "$DIR")"
echo "Text files = $(get_text_files_count "$DIR")"
echo "Executable files = $(get_executable_files_count "$DIR")"
echo "Log files (with the extension .log) = $(get_log_files_count "$DIR")"
echo "Archive files = $(get_archive_files_count "$DIR")"
echo "Symbolic links = $(get_symlinks_count "$DIR")"
echo "TOP 10 files of maximum size arranged in descending order (path, size and type): = $(get_top_files "$DIR")"
echo "TOP 10 executable files of the maximum size arranged in descending order (path, size and MD5 hash): = "
get_top_executable_files "$DIR"

end_time=$(date +%s.%N)
execution_time=$(echo "$end_time - $start_time" | bc)
echo "Script execution time (in seconds) = $execution_time"