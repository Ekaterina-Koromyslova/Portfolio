SELECT
    visits.name AS name,
    COALESCE(visits.count_of_visits, 0) +
    COALESCE(orders.count_of_orders, 0) AS
    total_count
FROM
(SELECT
    pizzeria.name AS name,
    COUNT(*) AS count_of_visits
FROM person_visits
JOIN pizzeria ON person_visits.pizzeria_id = pizzeria.id
GROUP BY pizzeria.name
) AS visits
FULL JOIN
(SELECT
    pizzeria.name AS name,
    COUNT(*) AS count_of_orders
FROM person_order
JOIN menu ON person_order.menu_id = menu.id
JOIN pizzeria ON menu.pizzeria_id = pizzeria.id
GROUP BY pizzeria.name
) AS orders
ON visits.name = orders.name
ORDER BY total_count DESC, visits.name ASC;