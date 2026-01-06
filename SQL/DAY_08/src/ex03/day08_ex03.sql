-- Session #1
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL READ COMMITTED;

BEGIN;
SELECT rating FROM pizzeria WHERE name = 'Pizza Hut';

-- Session #2
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
UPDATE pizzeria SET rating = 3.6 WHERE name = 'Pizza Hut';
COMMIT;

-- Session #1
SELECT rating FROM pizzeria WHERE name = 'Pizza Hut'; -- новое значение
COMMIT;

-- Session #2
SELECT rating FROM pizzeria WHERE name = 'Pizza Hut';