#ifndef PATTERNS_HANDLER_H
#define PATTERNS_HANDLER_H

#include <regex.h>

#include "s21_grep.h"

// Компиляция шаблонов
int compile_all_patterns(Flags *flags, regex_t *regexes);
int compile_regex(regex_t *regex, const char *pattern, int case_insensitive);

// Освобождение ресурсов
void free_compiled_patterns(regex_t *regexes, int pattern_count);
void cleanup_patterns(Patterns *patterns);

// Работа с шаблонами и строками
int match_line(const char *line, regex_t *regex, Flags *flags);
void print_matches(const char *line, regex_t *regex);
int handle_matching_line(FILE *file, char *line, int line_num, Flags *flags,
                         regex_t *regex, const char *filename,
                         int *match_count);
int match_with_pattern(const char *line, regex_t *regexes, int pattern_count,
                       Flags *flags);

// работа с файлом
int read_patterns_from_file(const char *filename, Patterns *patterns,
                            Flags *flags);

#endif
