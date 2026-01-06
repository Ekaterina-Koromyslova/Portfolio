#include <stdio.h>
#include <unistd.h>

#include "file.h"

int main(int argc, char *argv[]) {
  int exit_code = 0;

  Options options = parse_options(argc, argv);

  if (options.error) {
    fprintf(stderr, "Программа была завершена, неправильный аргумент\n");
    exit_code = 1;
  } else {
    for (int i = optind; i < argc; i++) {
      print_file(argv[i], options);
    }
  }
  return exit_code;
}
