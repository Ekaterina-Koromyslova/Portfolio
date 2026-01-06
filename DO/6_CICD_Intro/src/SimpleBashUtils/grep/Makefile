CC = gcc
CFLAGS = -std=c11 -Wall -Werror -Wextra -pedantic


all: s21_grep

s21_grep: s21_grep_main.c patterns_handler.c file_reader.c arguments_parser.c flag_handler.c error_handler.c
	$(CC) $(CFLAGS) -o s21_grep s21_grep_main.c patterns_handler.c file_reader.c arguments_parser.c flag_handler.c error_handler.c

clean:
	rm -f s21_grep

rebuild: clean all