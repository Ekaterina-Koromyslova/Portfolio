-- Session #1
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
UPDATE pizzeria SET rating = rating + 0.1 WHERE id = 1;

-- Session #2
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
UPDATE pizzeria SET rating = rating + 0.1 WHERE id = 2;

-- Session #1
UPDATE pizzeria SET rating = rating + 0.1 WHERE id = 2; -- ждёт блокировки

-- Session #2
UPDATE pizzeria SET rating = rating + 0.1 WHERE id = 1; -- вызывает deadlock

-- Session #1
COMMIT; -- успешно

-- Session #2
COMMIT; -- ROLLBACK
