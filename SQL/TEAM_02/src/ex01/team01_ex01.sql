--INSERT INTO currency VALUES (100, 'EUR', 0.85, '2022-01-01 13:29');
--INSERT INTO currency VALUES (100, 'EUR', 0.79, '2022-01-08 13:29');

CREATE FUNCTION fnc_nearest_rate(bigint, TIMESTAMP WITHOUT TIME ZONE)
RETURNS numeric AS $$
DECLARE rate numeric;
BEGIN
  SELECT rate_to_usd INTO rate
  FROM Currency WHERE id = $1 AND updated < $2
  ORDER BY updated DESC
  LIMIT 1;

  IF rate IS NULL THEN
    SELECT rate_to_usd INTO rate
    FROM Currency WHERE id = $1 AND updated > $2
    ORDER BY updated
    LIMIT 1;
  END IF;

  RETURN rate;
END;
$$ LANGUAGE plpgsql;

SELECT
  COALESCE(u.name, 'not defined') AS name,
  COALESCE(u.lastname, 'not defined') AS lastname,
  c.name AS currency_name,
  b.money * fnc_nearest_rate(b.currency_id, b.updated) AS currency_in_usd
FROM Balance b
LEFT JOIN "user" u ON b.user_id = u.id
INNER JOIN (
  SELECT DISTINCT
    b_in.currency_id AS id,
    c_in.name AS name
  FROM Balance b_in
  JOIN Currency c_in ON b_in.currency_id = c_in.id
) c ON c.id = b.currency_id
ORDER BY name DESC, lastname, currency_name;
