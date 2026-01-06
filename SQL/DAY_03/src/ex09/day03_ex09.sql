BEGIN;

INSERT INTO person_visits (id, person_id, pizzeria_id, visit_date)
VALUES (
  (SELECT MAX(person_visits.id) + 1 FROM person_visits),
  (SELECT person.id FROM person WHERE person.name = 'Denis'),
  (SELECT pizzeria.id FROM pizzeria WHERE pizzeria.name = 'Dominos'),
  DATE '2022-02-24'
);

INSERT INTO person_visits (id, person_id, pizzeria_id, visit_date)
VALUES (
  (SELECT MAX(person_visits.id) + 1 FROM person_visits),
  (SELECT person.id FROM person WHERE person.name = 'Irina'),
  (SELECT pizzeria.id FROM pizzeria WHERE pizzeria.name = 'Dominos'),
  DATE '2022-02-24'
);

COMMIT;