#include "format.h"

#include <stdio.h>

void format_char(char c, Options opts) {
  if (c == 9 && opts.show_tabs)
    printf("^I");
  else if (c == 10 && opts.show_dollars)
    printf("$\n");
  else if (c <= 31 && c != 9 && c != 10 && opts.show_ctrl_symbols)
    printf("^%c", c + 64);
  else if (c == 127 && opts.show_ctrl_symbols)
    printf("^?");
  else
    putchar(c);
}
