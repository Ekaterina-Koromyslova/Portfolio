CREATE TABLE cities (
    city VARCHAR
);

CREATE TABLE routes (
    point1 VARCHAR,
    point2 VARCHAR,
    cost INT
);

INSERT INTO cities (city)
VALUES
('a'),
('b'),
('c'),
('d');

INSERT INTO routes (point1, point2, cost)
VALUES
('a', 'b', 10),
('a', 'c', 15),
('a', 'd', 20),
('b', 'a', 10),
('b', 'c', 35),
('b', 'd', 25),
('c', 'a', 15),
('c', 'b', 35),
('c', 'd', 30),
('d', 'a', 20),
('d', 'b', 25),
('d', 'c', 30);


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
WHERE CARDINALITY(path) = 4
  AND (
      total_cost 
        + (SELECT cost 
           FROM routes 
           WHERE point1 = travel.point2 AND point2 = 'a')
    ) = (
      SELECT MIN(
          total_cost 
            + (SELECT cost 
               FROM routes 
               WHERE point1 = t.point2 AND point2 = 'a')
        )
      FROM travel AS t
      WHERE CARDINALITY(t.path) = 4
    )
ORDER BY total_cost, tour;