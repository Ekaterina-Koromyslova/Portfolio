#include "patterns_handler.h"

#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "flag_handler.h"
#include "s21_grep.h"

// Компиляция регулярного выражения
int compile_regex(regex_t *regex, const char *pattern, int case_insensitive) {
  int c_flag = REG_EXTENDED;
  const char *effective_pattern =
      (pattern == NULL || strlen(pattern) == 0) ? ".*" : pattern;

  if (case_insensitive) {
    c_flag |= REG_ICASE;
  }

  if (regcomp(regex, effective_pattern, c_flag) != 0) {
    fprintf(stderr, "Ошибка компиляции регулярного выражения: %s\n",
            effective_pattern);
  }

  return 0;
}

// Проверка строки на совпадение с регулярным выражением
int match_line(const char *line, regex_t *regex, Flags *flags) {
  int status = regexec(regex, line, 0, NULL, 0);
  return (flags->flag_v) ? status != 0 : status == 0;
}

void print_matches(const char *line, regex_t *regex) {
  regmatch_t pmatch[1];
  const char *cursor = line;

  // Цикл по всем совпадениям в строке
  while (regexec(regex, cursor, 1, pmatch, 0) == 0) {
    if (pmatch[0].rm_so != -1) {
      // Печать совпавшей подстроки
      printf("%.*s\n", (int)(pmatch[0].rm_eo - pmatch[0].rm_so),
             cursor + pmatch[0].rm_so);
    }
    // Сдвиг курсора после текущего совпадения
    cursor += pmatch[0].rm_eo;
  }
}

int read_patterns_from_file(const char *filename, Patterns *patterns,
                            Flags *flags) {
  FILE *pattern_file = fopen(filename, "r");
  if (pattern_file == NULL) {
    log_error("Не удалось открыть файл с шаблонами", flags);
    return 1;
  }

  char buffer[1024];
  while (fgets(buffer, sizeof(buffer), pattern_file) != NULL) {
    size_t len = strlen(buffer);
    if (len > 0 && buffer[len - 1] == '\n') {
      buffer[len - 1] = '\0';
    }

    if (strlen(buffer) == 0) {
      log_error(
          "Шаблон не может быть пустым. Используется шаблон по умолчанию '.*'",
          flags);
      patterns->patterns[patterns->count] = my_strdup(".*");
    } else {
      patterns->patterns[patterns->count] = my_strdup(buffer);
    }

    if (!patterns->patterns[patterns->count]) {
      log_error("Ошибка выделения памяти", flags);
      fclose(pattern_file);
    }

    patterns->count++;

    if (patterns->count >= 1024) {
      log_error("Превышено максимальное количество шаблонов (1024)", flags);
      fclose(pattern_file);
    }
  }

  if (patterns->count == 0) {
    log_error("Файл с шаблонами пуст", flags);
  }

  fclose(pattern_file);
  return 0;
}

// Готово
int handle_matching_line(FILE *file, char *line, int line_num, Flags *flags,
                         regex_t *regex, const char *filename,
                         int *match_count) {
  if (match_line(line, regex, flags)) {
    (*match_count)++;

    // Обработка флага -l (только имя файла при совпадении)
    if (flags->flag_l) {
      handle_flag_l(filename);
      fclose(file);
    }

    // Если флаг -c не установлен, выводим совпавшую строку
    if (!flags->flag_c) {
      process_matching_line(line, line_num, filename, flags, regex);
    }
  }
  return 0;
}

int compile_all_patterns(Flags *flags, regex_t *regexes) {
  for (int i = 0; i < flags->pattern_list.count; i++) {
    if (compile_regex(&regexes[i], flags->pattern_list.patterns[i],
                      flags->flag_i) != 0) {
      for (int j = 0; j < i; j++) {
        regfree(&regexes[j]);
      }
      log_error("Ошибка компиляции", flags);
    }
  }
  return 0;
}

// готово
int match_with_pattern(const char *line, regex_t *regexes, int pattern_count,
                       Flags *flags) {
  int flag_match_present = 0;

  if (line == NULL || regexes == NULL || flags == NULL) {
    log_error("Неверные аргументы для match_with_pattern", flags);
  }

  for (int i = 0; i < pattern_count; i++) {
    if (match_line(line, &regexes[i], flags)) {
      flag_match_present = 1;
      break;
    }
  }
  return flag_match_present;
}

void free_compiled_patterns(regex_t *regexes, int pattern_count) {
  for (int i = 0; i < pattern_count; i++) {
    regfree(&regexes[i]);
  }
}

void cleanup_patterns(Patterns *patterns) {
  for (int i = 0; i < patterns->count; i++) {
    free(patterns->patterns[i]);
  }
  patterns->count = 0;
}
