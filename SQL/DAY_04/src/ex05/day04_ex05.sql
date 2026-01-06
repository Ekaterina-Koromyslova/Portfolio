CREATE VIEW v_price_with_discount AS
SELECT
person.name AS name,
menu.pizza_name AS pizza_name,
menu.price AS price,
(menu.price * 0.9)::integer AS discount_price
FROM person_order
JOIN person ON person.id = person_order.person_id
JOIN menu ON menu.id = person_order.menu_id
ORDER BY name, pizza_name;

select *
from v_price_with_discount;