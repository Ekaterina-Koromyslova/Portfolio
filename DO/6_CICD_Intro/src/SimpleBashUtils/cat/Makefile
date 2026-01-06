CC = gcc
CFLAGS = -std=c11 -Wall -Werror -Wextra -pedantic


all: s21_cat

s21_cat: main.c options.c file.c format.c
	$(CC) $(CFLAGS) -o s21_cat main.c options.c file.c format.c

clean:
	rm -f s21_cat

rebuild: clean all
