#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>

#include "flag_handler.h"
#include "s21_grep.h"

int main(int argc, char *argv[]) {
  Flags flags_struct = {0};
  Flags *flags = &flags_struct;

  parse_arguments(argc, argv, flags);
  check_and_add_default_pattern(argc, argv, flags);
  flags->multiple_files = is_multiple_files(argc, optind);
  void finalize_program(Flags * flags);
  process_multiple_files(argc, argv, flags);
  cleanup_patterns(&flags->pattern_list);

  return 0;
}
