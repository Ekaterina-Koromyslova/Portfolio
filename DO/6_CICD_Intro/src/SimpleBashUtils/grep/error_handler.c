#include <stdio.h>
#include <stdlib.h>

#include "s21_grep.h"

void log_error(const char *message, Flags *flags) {
  if (!flags || !message) return;
  if (flags->flag_s) return;
  fprintf(stderr, "Ошибка: %s\n", message);
}
