WITH RECURSIVE travel
AS (

SELECT
point1,
point2,
cost,
ARRAY[point1, point2] AS path,
cost AS total_cost
FROM routes 
WHERE point1 = 'a'

UNION ALL

SELECT 
travel.point1 AS visited_point1,
next_route.point2 AS new_visited_point,
next_route.cost,
travel.path || next_route.point2,
travel.total_cost + next_route.cost AS updated_total_cost
FROM travel

JOIN routes AS next_route
ON travel.point2 = next_route.point1
AND NOT next_route.point2 = ANY(travel.path)

)

SELECT
    total_cost 
        + (SELECT cost 
           FROM routes 
           WHERE point1 = travel.point2 AND point2 = 'a') AS total_cost,
    ARRAY_TO_STRING(path || ARRAY['a'], ',') AS tour
FROM travel
WHERE CARDINALITY(travel.path) = 4
ORDER BY total_cost, tour;