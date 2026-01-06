BEGIN;

CREATE OR REPLACE FUNCTION fnc_trg_person_delete_audit()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO person_audit (created, type_event, row_id, name, age, gender, address)
    VALUES (now(), 'D', OLD.id, OLD.name, OLD.age, OLD.gender, OLD.address);

    RETURN OLD;
END;
$$;

DROP TRIGGER IF EXISTS trg_person_delete_audit ON person;
CREATE TRIGGER trg_person_delete_audit
AFTER DELETE ON person
FOR EACH ROW
EXECUTE FUNCTION fnc_trg_person_delete_audit();

DELETE FROM person WHERE id = 10;

COMMIT;

SELECT * FROM person_audit ORDER BY created;
