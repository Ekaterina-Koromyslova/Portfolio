#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "patterns_handler.h"
#include "s21_grep.h"

void handle_flag_e(Flags *flags, const char *optarg) {
  if (flags->pattern_list.count >= 1024) {
    fprintf(stderr, "Превышено максимальное количество шаблонов (1024)\n");
  }
  flags->pattern_list.patterns[flags->pattern_list.count] = my_strdup(optarg);
  if (!flags->pattern_list.patterns[flags->pattern_list.count]) {
    log_error("Ошибка выделения памяти", flags);
  }
  flags->pattern_list.count++;
  flags->flag_e = 1;
}

void handle_flag_f(Flags *flags, const char *optarg) {
  flags->flag_f = 1;
  if (read_patterns_from_file(optarg, &flags->pattern_list, flags) != 0) {
    fprintf(stderr, "Ошибка чтения шаблонов из файла: %s\n", optarg);
  }
}

void handle_flag_n(int line_num) { printf("%d:", line_num); }

void handle_flag_o(const char *line, regex_t *regex, int line_num,
                   Flags *flags) {
  // Если активен флаг -h (не выводить имя файла) и это не stdin, то вывести имя
  // файла
  if (!flags->flag_h && flags->multiple_files) {
    printf("%s:", flags->current_filename);
  }

  if (flags->flag_n) {
    handle_flag_n(line_num);
  }
  print_matches(line, regex);
}

void handle_flag_l(const char *filename) { printf("%s\n", filename); }

void handle_flag_c(const char *filename, int match_count, Flags *flags) {
  if (!flags->flag_h && flags->multiple_files) {
    printf("%s:", filename);
  }
  printf("%d\n", match_count);
}

void handle_flag_h(const char *filename, Flags *flags) {
  if (!flags->flag_h && flags->multiple_files) {
    printf("%s:", filename);
  }
}

// Функция для обработки каждого активного флага
void apply_flags_for_line(const char *line, int line_num, const char *filename,
                          Flags *flags, regex_t *regex) {
  if (flags->flag_o) {
    handle_flag_o(line, regex, line_num, flags);
  } else {
    if (!flags->flag_h && flags->multiple_files) {
      printf("%s:", filename);
    }

    if (flags->flag_n) {
      handle_flag_n(line_num);
    }
    printf("%s\n", line);
  }
}

void process_matching_line(const char *line, int line_num, const char *filename,
                           Flags *flags, regex_t *regex) {
  // Убираем символ новой строки из строки line
  size_t len = strlen(line);
  if (len > 0 && line[len - 1] == '\n') {
    ((char *)line)[len - 1] = '\0';
  }

  // Применяем все флаги к текущей строке
  apply_flags_for_line(line, line_num, filename, flags, regex);
}
