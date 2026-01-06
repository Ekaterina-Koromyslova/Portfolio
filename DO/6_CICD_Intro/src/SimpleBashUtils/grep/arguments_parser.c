#include <getopt.h>
#include <string.h>

#include "flag_handler.h"
#include "s21_grep.h"

int parse_arguments(int argc, char *argv[], Flags *flags) {
  int opt = 0;
  while ((opt = getopt(argc, argv, "e:ivclnhsf:o")) != -1) {
    switch (opt) {
      case 'e':
        handle_flag_e(flags, optarg);
        break;
      case 'f':
        handle_flag_f(flags, optarg);
        break;
      case 'i':
        flags->flag_i = 1;
        break;
      case 'v':
        flags->flag_v = 1;
        break;
      case 'c':
        flags->flag_c = 1;
        break;
      case 'l':
        flags->flag_l = 1;
        break;
      case 'n':
        flags->flag_n = 1;
        break;
      case 'h':
        flags->flag_h = 1;
        break;
      case 's':
        flags->flag_s = 1;
        break;
      case 'o':
        flags->flag_o = 1;
        break;
      default:
        log_error("Использованы неправильные аргументы", flags);
        break;
    }
  }
  return 0;
}

int check_and_add_default_pattern(int argc, char *argv[], Flags *flags) {
  if ((flags == NULL || argv == NULL) && !flags->flag_s) {
    log_error("Неправильные аргументы", flags);
  }

  if (flags->pattern_list.count == 0) {
    if ((optind >= argc) && !flags->flag_s) {
      log_error("Не указан шаблон", flags);
    } else if ((flags->pattern_list.count >= 1024) && !flags->flag_s) {
      log_error("Ошибка: превышено максимальное количество шаблонов (1024)",
                flags);
    } else {
      flags->pattern_list.patterns[flags->pattern_list.count] =
          my_strdup(argv[optind++]);
      if ((!flags->pattern_list.patterns[flags->pattern_list.count]) &&
          !flags->flag_s) {
        log_error("Ошибка выделения памяти", flags);
      } else {
        flags->pattern_list.count++;
      }
    }
  }
  return 0;
}

int is_multiple_files(int argc, int optind) { return (argc - optind) > 1; }
