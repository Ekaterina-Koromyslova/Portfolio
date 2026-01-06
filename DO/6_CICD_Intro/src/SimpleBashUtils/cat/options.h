#ifndef OPTIONS_H
#define OPTIONS_H

#include <getopt.h>

typedef struct {
  int number_all;
  int number_non_empty;
  int squeeze_empty;
  int show_ctrl_symbols;
  int show_dollars;
  int show_tabs;
  int error;
} Options;

extern struct option long_options[];

Options parse_options(int argc, char **argv);

#endif  // OPTIONS_H
