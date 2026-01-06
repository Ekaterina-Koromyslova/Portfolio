SELECT
  person_a.name    AS person_name1,
  person_b.name    AS person_name2,
  person_a.address AS common_address
FROM person AS person_a
JOIN person AS person_b
  ON person_a.id > person_b.id
 AND person_a.address = person_b.address
ORDER BY person_name1, person_name2, common_address;
