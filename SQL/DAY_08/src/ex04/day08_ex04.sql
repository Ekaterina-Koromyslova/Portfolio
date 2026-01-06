-- Session #1
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
SELECT rating FROM pizzeria WHERE name = 'Pizza Hut';

-- Session #2
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
UPDATE pizzeria SET rating = 3.0 WHERE name = 'Pizza Hut';
COMMIT;

-- Session #1
SELECT rating FROM pizzeria WHERE name = 'Pizza Hut'; -- всё ещё старое значение (3.6)
COMMIT;

SELECT rating FROM pizzeria WHERE name = 'Pizza Hut'; -- новое значение