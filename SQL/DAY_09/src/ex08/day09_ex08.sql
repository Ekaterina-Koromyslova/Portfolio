BEGIN;

CREATE OR REPLACE FUNCTION fnc_fibonacci(pstop integer DEFAULT 10)
RETURNS TABLE(fib integer)
LANGUAGE plpgsql
AS $$
DECLARE
    a integer := 0;
    b integer := 1;
BEGIN
    WHILE a < pstop LOOP
        fib := a;
        RETURN NEXT;
        SELECT b, a + b INTO a, b;
    END LOOP;
END;
$$;

COMMIT;


SELECT * FROM fnc_fibonacci(20);
