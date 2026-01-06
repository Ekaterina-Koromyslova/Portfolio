BEGIN;

CREATE TABLE IF NOT EXISTS person_audit (
    created     timestamptz NOT NULL DEFAULT now(),
    type_event  char(1)     NOT NULL DEFAULT 'I',
    row_id      bigint      NOT NULL,
    name        varchar,
    age         integer,
    gender      varchar,
    address     varchar,
    CONSTRAINT ch_type_event CHECK (type_event IN ('I','U','D'))
);

CREATE OR REPLACE FUNCTION fnc_trg_person_insert_audit()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO person_audit (created, type_event, row_id, name, age, gender, address)
    VALUES (now(), 'I', NEW.id, NEW.name, NEW.age, NEW.gender, NEW.address);

    RETURN NEW; 
END;
$$;

DROP TRIGGER IF EXISTS trg_person_insert_audit ON person;
CREATE TRIGGER trg_person_insert_audit
AFTER INSERT ON person
FOR EACH ROW
EXECUTE FUNCTION fnc_trg_person_insert_audit();

DELETE FROM person WHERE id = 10;

INSERT INTO person(id, name, age, gender, address)
VALUES (10, 'Damir', 22, 'male', 'Irkutsk');

COMMIT;

SELECT * FROM person_audit;