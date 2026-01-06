BEGIN;

CREATE OR REPLACE FUNCTION func_minimum(arr double precision[])
RETURNS double precision
LANGUAGE SQL
AS $$
    SELECT MIN(x)
    FROM unnest(arr) AS x;
$$;

COMMIT;

SELECT func_minimum(VARIADIC arr => ARRAY[10.0, -1.0, 5.0, 4.4]);