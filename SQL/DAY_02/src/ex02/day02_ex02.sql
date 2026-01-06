SELECT
  COALESCE(person.name, '-')               AS person_name,
  filtered_person_visits.visit_date        AS visit_date,
  COALESCE(pizzeria.name, '-')             AS pizzeria_name
FROM person
FULL JOIN (
  SELECT
    person_visits.visit_date::date AS visit_date,
    person_visits.person_id        AS person_id,
    person_visits.pizzeria_id      AS pizzeria_id
  FROM person_visits
  WHERE person_visits.visit_date::date
        BETWEEN DATE '2022-01-01' AND DATE '2022-01-03'
) AS filtered_person_visits
  ON person.id = filtered_person_visits.person_id
FULL JOIN pizzeria
  ON filtered_person_visits.pizzeria_id = pizzeria.id
ORDER BY person_name, visit_date, pizzeria_name;
