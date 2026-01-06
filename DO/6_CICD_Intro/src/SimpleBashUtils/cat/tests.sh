#!/bin/bash


FILES=("empty_file.txt" "text.txt" "ASCII_table.txt")


STD_FLAGS=("-b" "-e" "-n" "-s" "-t")


#GNU_FLAGS=("-number" "-number-nonblank" "-squeeze-blank")


S21_CAT_OUTPUT="s21_cat.output"
CAT_OUTPUT="cat.output"

GREEN="\033[32m"
RED="\033[31m"
RESET="\033[0m"

> "$S21_CAT_OUTPUT"
> "$CAT_OUTPUT"

#тест без аргументов
echo "Тестирование без аргументов..."
./s21_cat < /dev/null >> "$S21_CAT_OUTPUT"
cat < /dev/null >> "$CAT_OUTPUT"

if diff -q "$S21_CAT_OUTPUT" "$CAT_OUTPUT";then
    echo -e "${GREEN}Тест прошел${RESET}"
else
    echo -e "${RED}Тест не прошел${RESET}"
fi


#тест без флагов
echo "Тестирование чтения файлов..."
for file in "${FILES[@]}"; do
    echo "Тестирование файла $file" 
    ./s21_cat "$file" >> "$S21_CAT_OUTPUT"
    cat "$file" >> "$CAT_OUTPUT" 

    if diff -q "$S21_CAT_OUTPUT" "$CAT_OUTPUT";then
        echo -e "${GREEN}Тест прошел${RESET}"
    else
        echo -e "${RED}Тест не прошел${RESET}"
    fi
done 


#тестирование с разными комбинациями файлов и флагов
for file1 in "${FILES[@]}"; do
    for file2 in "${FILES[@]}"; do
        for file3 in "${FILES[@]}"; do
            for std_flag in "${STD_FLAGS[@]}"; do
                #for GNU_flag in "${GNU_FLAGS[@]}"; do
                    cmd_std_flag="./s21_cat $std_flag $file1 $file2 $file3"
                    #cmd_GNU_flag="./s21_cat $GNU_flag $file1 $file2 $file3"

                    cmd_cat_flag="cat $std_flag $file1 $file2 $file3"

                     echo "Идет тестирование $cmd_std_flag"
                    $cmd_std_flag >> "$S21_CAT_OUTPUT"
                    $cmd_cat_flag >> "$CAT_OUTPUT"
                    if diff -q "$S21_CAT_OUTPUT" "$CAT_OUTPUT"; then
                        echo -e "${GREEN}Тест прошел${RESET}"
                    else
                        echo -e "${RED}Тест не прошел${RESET}"
                    fi

                    #echo "Идет тестирование $cmd_GNU_flag"
                    #$cmd_GNU_flag > "$S21_CAT_OUTPUT"
                    #cat -$GNU_flag $file1 $file2 $file3 > "$S21_CAT_OUTPUT"
                    #if diff -q "$S21_CAT_OUTPUT" "$CAT_OUTPUT";then
                        #echo -e "${GREEN}Тест прошел${RESET}"
                    #else
                        #echo -e "${RED}Тест не прошел${RESET}"
                    #fi
                done
            done
        done
    done

rm -f "$S21_CAT_OUTPUT" "$CAT_OUTPUT"
