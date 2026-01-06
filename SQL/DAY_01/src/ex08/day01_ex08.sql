
SELECT
  person_order_renamed.order_date,
  person_renamed.name || ' (age:' || person_renamed.age::text || ')' AS customer_info
FROM
  (SELECT person_id, order_date FROM person_order) AS person_order_renamed
NATURAL JOIN
  (SELECT id AS person_id, name, age FROM person) AS person_renamed
ORDER BY person_order_renamed.order_date ASC, customer_info ASC;
