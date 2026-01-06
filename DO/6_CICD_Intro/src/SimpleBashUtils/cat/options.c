#include "options.h"

#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>

struct option long_options[] = {{"number-nonblank", no_argument, NULL, 'b'},
                                {"number", no_argument, NULL, 'n'},
                                {"squeeze-blank", no_argument, NULL, 's'},
                                {NULL, 0, NULL, 0}};

Options parse_options(int argc, char **argv) {
  Options opts = {0};
  int o = 0;
  while ((o = getopt_long(argc, argv, "benstTE", long_options, NULL)) != -1) {
    switch (o) {
      case 'b':
        opts.number_non_empty = 1;
        opts.number_all = 0;
        break;
      case 'n':
        if (!opts.number_non_empty) opts.number_all = 1;
        break;
      case 's':
        opts.squeeze_empty = 1;
        break;
      case 'e':
        opts.show_dollars = 1;
        opts.show_ctrl_symbols = 1;
        break;
      case 't':
        opts.show_tabs = 1;
        opts.show_ctrl_symbols = 1;
        break;
      case 'T':
        opts.show_tabs = 1;
        break;
      case 'E':
        opts.show_dollars = 1;
        break;
      default:
        opts.error = 1;
        break;
    }
  }
  return opts;
}
