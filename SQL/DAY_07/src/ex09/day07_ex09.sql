SELECT
    person.address AS address,
    ROUND(MAX(person.age) - (MIN(person.age) / MAX(person.age::numeric)), 2) AS formula,
    ROUND(AVG(person.age), 2) AS average,
    CASE
        WHEN (MAX(person.age) - (MIN(person.age) / MAX(person.age))) > AVG(person.age)
        THEN TRUE
        ELSE FALSE
    END AS comparison
FROM person
GROUP BY person.address
ORDER BY person.address;
