-- Session #1
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT SUM(rating) AS total_rating FROM pizzeria;

-- Session #2
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
INSERT INTO pizzeria (id, name, rating)
VALUES (11, 'Kazan Pizza 2', 4);
COMMIT;

-- Session #1
SELECT SUM(rating) AS total_rating FROM pizzeria; -- остаётся тем же
COMMIT;
SELECT SUM(rating) AS total_rating FROM pizzeria; -- поменяется
