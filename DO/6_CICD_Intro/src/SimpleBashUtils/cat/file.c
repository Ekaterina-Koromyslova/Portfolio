#include "file.h"

#include <stdio.h>
#include <string.h>

#include "format.h"

#define MAX_LINE_LENGTH 4096

void print_file(const char *filename, Options opts) {
  FILE *file = fopen(filename, "r");
  if (file == NULL) {
    printf("Произошла ошибка при открытии файла");
    return;
  }

  char line[MAX_LINE_LENGTH];
  int line_number = 1;
  int is_blank = 0;

  while (fgets(line, sizeof(line), file)) {
    int is_newline = (line[0] == '\n');

    if (opts.squeeze_empty && is_newline) {
      if (is_blank > 0) continue;
      is_blank++;
    } else
      is_blank = 0;

    if (opts.number_non_empty) {
      if (!is_newline)
        printf("%6d\t", line_number++);
      else if (opts.show_dollars)
        printf("%6s\t", "");
    } else if (opts.number_all) {
      printf("%6d\t", line_number++);
    }

    for (int i = 0; line[i] != '\0'; i++) format_char(line[i], opts);
  }

  fclose(file);
}
