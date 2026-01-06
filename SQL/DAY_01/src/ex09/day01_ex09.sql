SELECT id, name
FROM pizzeria
WHERE id NOT IN (
    SELECT pizzeria_id
    FROM person_visits
)
ORDER BY id;

SELECT id, name
FROM pizzeria
WHERE NOT EXISTS (
    SELECT 1
    FROM person_visits
    WHERE person_visits.pizzeria_id = pizzeria.id
)