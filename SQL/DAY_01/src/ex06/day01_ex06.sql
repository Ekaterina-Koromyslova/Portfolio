WITH common AS (
  SELECT order_date AS action_date, person_id
  FROM person_order
  INTERSECT
  SELECT visit_date AS action_date, person_id
  FROM person_visits
)
SELECT
  common.action_date,
  person.name AS person_name
FROM common
JOIN person ON person.id = common.person_id
ORDER BY common.action_date ASC, person_name DESC;