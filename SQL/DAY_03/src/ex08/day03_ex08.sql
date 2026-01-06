INSERT INTO menu (id, pizzeria_id, pizza_name, price)
VALUES (
  (SELECT MAX(menu.id) + 1 FROM menu),
  (SELECT pizzeria.id FROM pizzeria WHERE pizzeria.name = 'Dominos'),
  'sicilian pizza',
  900
);

SELECT count(*) = 1 AS CHECK
 FROM menu
 WHERE id = 20
   AND pizzeria_id = 2
   AND pizza_name = 'sicilian pizza'
   AND price = 900;