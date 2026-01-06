DELETE FROM person_order
WHERE order_date = '2022-02-25';

DELETE FROM menu
WHERE pizza_name = 'greek pizza';

SELECT count(*) = 0 AS CHECK
 FROM person_order
 WHERE order_date = '2022-02-25'
   AND menu_id =
     (SELECT id
     FROM menu
     WHERE pizza_name = 'greek pizza');