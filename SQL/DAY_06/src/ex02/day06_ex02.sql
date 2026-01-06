SELECT
    person.name AS name,
    menu.pizza_name AS pizza_name,
    menu.price AS price,
    ROUND(menu.price * (1 - COALESCE(pd.discount, 0) / 100), 2)
    AS discount_price,
    pizzeria.name AS pizzeria_name
FROM person_order
JOIN menu ON person_order.menu_id = menu.id
JOIN pizzeria ON menu.pizzeria_id = pizzeria.id
JOIN person ON person_order.person_id = person.id
LEFT JOIN person_discounts AS pd
    ON person_order.person_id = pd.person_id
    AND menu.pizzeria_id = pd.pizzeria_id
ORDER BY person.name, menu.pizza_name;