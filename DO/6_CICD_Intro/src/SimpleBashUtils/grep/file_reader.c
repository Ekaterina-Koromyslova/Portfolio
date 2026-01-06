#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "flag_handler.h"
#include "patterns_handler.h"
#include "s21_grep.h"

FILE *open_file(const char *filename, Flags *flags) {
  FILE *file = fopen(filename, "r");
  if (!flags || (file == NULL)) return NULL;
  if (!file) {
    if (!flags->flag_s) {
      log_error("Не удалось открыть файл", flags);
    }
  }
  return file;
}

void process_file_lines(FILE *file, regex_t *regexes, int pattern_count,
                        Flags *flags, const char *filename) {
  char line[1024];
  int line_num = 0;
  int match_count = 0;

  while (fgets(line, sizeof(line), file)) {
    line_num++;
    if (match_with_pattern(line, regexes, pattern_count, flags)) {
      match_count++;

      if (flags->flag_l) {
        handle_flag_l(filename);
        return;
      }

      if (!flags->flag_c) {
        process_matching_line(line, line_num, filename, flags, regexes);
      }
    }
  }

  if (flags->flag_c) {
    handle_flag_c(filename, match_count, flags);
  }
}

int read_file(const char *filename, Flags *flags) {
  FILE *file = open_file(filename, flags);
  if (!file) {
    return 1;
  }

  regex_t regexes[flags->pattern_list.count];
  if ((compile_all_patterns(flags, regexes) != 0) && !flags->flag_s) {
    fclose(file);
    log_error("Ошибка компиляции шаблонов", flags);
  }

  process_file_lines(file, regexes, flags->pattern_list.count, flags, filename);
  free_compiled_patterns(regexes, flags->pattern_list.count);

  fclose(file);
  return 0;
}

// Выделено в отдельную функцию чтобы инкапсулировать логику
// обработки нескольких файлов - готово
void process_multiple_files(int argc, char *argv[], Flags *flags) {
  for (int i = optind; i < argc; i++) {
    int result = read_file(argv[i], flags);
    if (result != 0 && !flags->flag_s) {
      fprintf(stderr, "Не удалось открыть файл %s\n", argv[i]);
    }
  }
}

char *my_strdup(const char *str) {
  if (str == NULL) return NULL;
  size_t len = strlen(str) + 1;
  char *copy = malloc(len);
  if (copy != NULL) {
    strcpy(copy, str);
  }
  return copy;
}
