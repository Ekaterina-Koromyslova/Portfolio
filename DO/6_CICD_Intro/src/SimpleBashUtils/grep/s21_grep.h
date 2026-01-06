#ifndef S21_GREP_H
#define S21_GREP_H

#include <regex.h>
#include <stdio.h>

#define EXIT_FAILURE 1
#define EXIT_SUCCESS 0

typedef struct {
  char *patterns[1024];
  int count;
} Patterns;

typedef struct {
  int flag_e;
  int flag_i;
  int flag_v;
  int flag_c;
  int flag_l;
  int flag_n;
  int flag_h;
  int flag_s;
  int flag_f;
  int flag_o;
  int wrong_flag;
  int multiple_files;
  int error_status;
  Patterns pattern_list;
  char *file_with_patterns;
  char *current_filename;
} Flags;

int parse_arguments(int argc, char *argv[], Flags *flags);
int check_and_add_default_pattern(int argc, char *argv[], Flags *flags);

// file_reader.c
FILE *open_file(const char *filename, Flags *flags);
void process_file_lines(FILE *file, regex_t *regexes, int pattern_count,
                        Flags *flags, const char *filename);
int read_file(const char *filename, Flags *flags);
void process_multiple_files(int argc, char *argv[], Flags *flags);
char *my_strdup(const char *str);

// error_handler.c
void log_error(const char *message, Flags *flags);
void finalize_program(Flags *flags);

#endif
