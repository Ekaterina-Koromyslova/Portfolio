SELECT
  menu.pizza_name AS pizza_name,
  menu.price      AS price,
  pizzeria.name   AS pizzeria_name
FROM menu
JOIN pizzeria
  ON pizzeria.id = menu.pizzeria_id
WHERE NOT EXISTS (
  SELECT 1
  FROM person_order
  WHERE person_order.menu_id = menu.id
)
ORDER BY
  pizza_name,
  price,
  pizzeria_name;
