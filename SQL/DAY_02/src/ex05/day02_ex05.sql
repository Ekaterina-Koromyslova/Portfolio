SELECT
person.name AS name
FROM person
WHERE person.gender = 'female'
AND person.age > 25
ORDER BY name;