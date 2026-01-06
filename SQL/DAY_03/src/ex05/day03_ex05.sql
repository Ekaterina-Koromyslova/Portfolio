SELECT pizzeria.name AS pizzeria_name
FROM pizzeria

WHERE pizzeria.id IN  (
    SELECT person_visits.pizzeria_id
    FROM person_visits
    JOIN person ON person.id = person_visits.person_id
    WHERE person.name = 'Andrey'
)
AND pizzeria.id NOT IN (
    SELECT menu.pizzeria_id
    FROM person_order
    JOIN menu ON menu.id = person_order.menu_id
    JOIN person ON person.id = person_order.person_id
    WHERE person.name = 'Andrey'
        AND menu.pizzeria_id = pizzeria.id
)

ORDER BY pizzeria.name;