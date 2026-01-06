#ifndef FLAG_HANDLER_H
#define FLAG_HANDLER_H

#include "patterns_handler.h"
#include "s21_grep.h"

// Обработка сложных флагов -e и -f
void handle_flag_e(Flags *flags, const char *optarg);
void handle_flag_f(Flags *flags, const char *optarg);

// Обработка флагов, связанных с выводом данных
void handle_flag_l(const char *filename);
void handle_flag_n(int line_num);
void handle_flag_c(const char *filename, int match_count, Flags *flags);
void handle_flag_h(const char *filename, Flags *flags);
void handle_flag_o(const char *line, regex_t *regex, int line_num,
                   Flags *flags);

// функции затрагивающие строки
void process_matching_line(const char *line, int line_num, const char *filename,
                           Flags *flags, regex_t *regex);

int is_multiple_files(int argc, int optind);
void apply_flags_for_line(const char *line, int line_num, const char *filename,
                          Flags *flags, regex_t *regex);

#endif
