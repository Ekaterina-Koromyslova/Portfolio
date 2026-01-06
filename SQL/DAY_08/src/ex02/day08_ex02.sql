-- Session #1
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT rating FROM pizzeria WHERE name = 'Pizza Hut';
UPDATE pizzeria SET rating = 4 WHERE name = 'Pizza Hut';

-- Session #2
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT rating FROM pizzeria WHERE name = 'Pizza Hut';
UPDATE pizzeria SET rating = 3.6 WHERE name = 'Pizza Hut';  -- зависает

-- Session #1
COMMIT;

-- Session #2
COMMIT;  -- выдаст ошибку

-- Session #1
-- проверка
SELECT rating FROM pizzeria WHERE name = 'Pizza Hut';

-- Session #2
-- проверка
SELECT rating FROM pizzeria WHERE name = 'Pizza Hut';