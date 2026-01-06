BEGIN;

INSERT INTO person_order (id, person_id, menu_id, order_date)
VALUES (
  (SELECT MAX(person_order.id) + 1 FROM person_order),
  (SELECT person.id FROM person WHERE person.name = 'Denis'),
  (SELECT menu.id FROM menu WHERE menu.pizza_name = 'sicilian pizza'),
  DATE '2022-02-24'
);

INSERT INTO person_order (id, person_id, menu_id, order_date)
VALUES (
  (SELECT MAX(person_order.id) + 1 FROM person_order),
  (SELECT person.id FROM person WHERE person.name = 'Irina'),
  (SELECT menu.id FROM menu WHERE menu.pizza_name = 'sicilian pizza'),
  DATE '2022-02-24'
);

COMMIT;