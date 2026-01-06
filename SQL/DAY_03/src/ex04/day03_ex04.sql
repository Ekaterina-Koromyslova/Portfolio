SELECT pizzeria.name AS pizzeria_name
FROM pizzeria
WHERE EXISTS (
  SELECT 1
  FROM person_order
  INNER JOIN person ON person.id = person_order.person_id
  INNER JOIN menu   ON menu.id   = person_order.menu_id
  WHERE menu.pizzeria_id = pizzeria.id
    AND person.gender = 'female'
)
AND NOT EXISTS (
  SELECT 1
  FROM person_order
  INNER JOIN person ON person.id = person_order.person_id
  INNER JOIN menu   ON menu.id   = person_order.menu_id
  WHERE menu.pizzeria_id = pizzeria.id
    AND person.gender = 'male'
)

UNION

SELECT pizzeria.name AS pizzeria_name
FROM pizzeria
WHERE EXISTS (
  SELECT 1
  FROM person_order
  INNER JOIN person ON person.id = person_order.person_id
  INNER JOIN menu   ON menu.id   = person_order.menu_id
  WHERE menu.pizzeria_id = pizzeria.id
    AND person.gender = 'male'
)
AND NOT EXISTS (
  SELECT 1
  FROM person_order
  INNER JOIN person ON person.id = person_order.person_id
  INNER JOIN menu   ON menu.id   = person_order.menu_id
  WHERE menu.pizzeria_id = pizzeria.id
    AND person.gender = 'female'
)
ORDER BY pizzeria_name;
