SELECT object_name
FROM (
    SELECT name        AS object_name, 1 AS src FROM person
    UNION ALL
    SELECT pizza_name  AS object_name, 2 AS src FROM menu
) t
ORDER BY src, object_name ASC;

