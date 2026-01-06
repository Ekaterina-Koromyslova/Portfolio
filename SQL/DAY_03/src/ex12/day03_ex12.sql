INSERT INTO person_order (id, person_id, menu_id, order_date)
SELECT
  generated_number + (SELECT MAX(id) FROM person_order) AS id,
  person.id AS person_id,
  (SELECT id FROM menu WHERE pizza_name = 'greek pizza') AS menu_id,
  DATE '2022-02-25' AS order_date
FROM person
INNER JOIN generate_series(
  1,
  (SELECT COUNT(*) FROM person)
) AS generated_numbers(generated_number)
  ON generated_numbers.generated_number = person.id;

SELECT count(*) = 9 AS CHECK
 FROM person_order
 WHERE order_date = '2022-02-25'
   AND menu_id =
     (SELECT id
     FROM menu
     WHERE pizza_name = 'greek pizza');