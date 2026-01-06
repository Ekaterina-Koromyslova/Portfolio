CREATE TABLE person_discounts(
    id bigint PRIMARY KEY,
    person_id bigint CONSTRAINT fk_person_discounts_person_id
    REFERENCES person(id),
    pizzeria_id bigint CONSTRAINT fr_person_discounts_pizzeria_id
    REFERENCES pizzeria(id),
    discount numeric
);

SELECT count(*) = 1 AS check
FROM pg_tables
WHERE tablename = 'person_discounts';