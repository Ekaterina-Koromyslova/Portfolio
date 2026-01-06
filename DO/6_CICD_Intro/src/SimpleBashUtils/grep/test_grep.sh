#!/bin/bash

MY_GREP="./s21_grep"
ORIGINAL_GREP="grep"

# Очистка файлов логов
rm -f test_results.log
rm -f differences.log

# Функция для выполнения теста
run_test() {
  description=$1
  shift
  command=$@
  
  echo "Running Test: $description" >> test_results.log
  echo "Command: $command" >> test_results.log
  
  eval "$MY_GREP $command" >> my_output.txt 2>&1
  eval "$ORIGINAL_GREP $command" >> original_output.txt 2>&1
  
  if diff -q my_output.txt original_output.txt > /dev/null; then
    echo "Test PASSED" >> test_results.log
  else
    echo "Test FAILED" >> test_results.log
    echo "Differences:" >> test_results.log
    diff -u my_output.txt original_output.txt >> test_results.log
    echo "Differences saved to differences.log"
    diff -u my_output.txt original_output.txt >> differences.log
  fi
  echo "=========================================" >> test_results.log
}

# Тесты для всех флагов
run_test "Тест 1: Флаг -e (поиск строки 'Pattern')" "-e 'Pattern' text.txt"
run_test "Тест 2: Флаг -i (регистронезависимый поиск 'pattern')" "-i 'pattern' text.txt"
run_test "Тест 3: Флаг -v (поиск строк, не содержащих 'Pattern')" "-v 'Pattern' text.txt"
run_test "Тест 4: Флаг -c (подсчёт количества строк с 'Pattern')" "-c 'Pattern' text.txt"
run_test "Тест 5: Флаг -l (показать только имена файлов с совпадениями)" "-l 'Pattern' text.txt text2.txt"
run_test "Тест 6: Флаг -n (вывести номер строки с 'Pattern')" "-n 'Pattern' text.txt"
run_test "Тест 7: Флаг -h (показать совпадения без имени файла)" "-h 'Pattern' text.txt text2.txt"
run_test "Тест 8: Флаг -s (не показывать ошибки для несуществующих файлов)" "-s 'Pattern' non_existent_file.txt"
run_test "Тест 9: Флаг -f (поиск шаблонов из файла test_patterns.txt)" "-f test_patterns.txt text.txt text2.txt"
run_test "Тест 10: Флаг -o (выводить только совпавшую подстроку)" "-o 'Pattern' text.txt"

# Тесты для комбинаций флагов
run_test "Тест 11: Комбинация флагов -i -v" "-i -v 'pattern' text.txt"
run_test "Тест 12: Комбинация флагов -n -c" "-n -c 'Pattern' text.txt"
run_test "Тест 13: Комбинация флагов -i -c" "-i -c 'pattern' text.txt"
run_test "Тест 14: Комбинация флагов -f -c (подсчёт количества строк)" "-f test_patterns.txt -c text.txt text2.txt"
run_test "Тест 15: Комбинация флагов -o -c (подсчёт совпадений и их вывод)" "-o -c 'Pattern' text.txt"
run_test "Тест 16: Комбинация флагов -e -f (шаблоны и шаблоны из файла)" "-e 'line' -f test_patterns.txt text.txt"
run_test "Тест 17: Комбинация флагов -n -o (показать номер строки и совпадение)" "-n -o 'Pattern' text.txt"
run_test "Тест 18: Комбинация флагов -h -n (показать номер строки без имени файла)" "-h -n 'Pattern' text.txt text2.txt"
run_test "Тест 19: Комбинация флагов -v -c (количество строк без совпадений)" "-v -c 'Pattern' text.txt"

# Тесты для ошибок
run_test "Тест 20: Пустой шаблон поиска" "-e '' text.txt"
run_test "Тест 21: Не указаны файлы для поиска" "-e '' Pattern"
run_test "Тест 22: Шаблон из пустого файла" "-f empty_test_patterns.txt text.txt"
run_test "Тест 23: Несуществующий файл" "-e 'Pattern' non_existent_file.txt"
run_test "Тест 24: Превышение максимального количества шаблонов" "-f large_test_patterns.txt text.txt"

echo "Все тесты завершены. Проверьте файл test_results.log"
