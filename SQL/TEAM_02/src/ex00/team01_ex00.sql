WITH vol AS (
  SELECT user_id, type, SUM(money) AS volume
  FROM Balance
  GROUP BY user_id, type
),
last_rate AS (
  SELECT id, rate_to_usd
  FROM (
    SELECT
      id,
      rate_to_usd,
      ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated DESC) AS rn
    FROM Currency
  ) x
  WHERE rn = 1
)
SELECT DISTINCT
  COALESCE(u.name, 'not defined') AS name,
  COALESCE(u.lastname, 'not defined') AS lastname,
  b.type AS type,
  vol.volume AS volume,
  COALESCE(c.name, 'not defined') AS currency_name,
  COALESCE(last_rate.rate_to_usd, 1) AS last_rate_to_usd,
  vol.volume * (COALESCE(last_rate.rate_to_usd, 1)) AS total_volume_in_usd
FROM Balance b
LEFT JOIN "user" u ON u.id = b.user_id
LEFT JOIN vol ON vol.user_id = b.user_id AND vol.type = b.type
LEFT JOIN (
  SELECT DISTINCT
    b_in.currency_id AS id,
    c_in.name AS name
  FROM Balance b_in
  JOIN Currency c_in ON b_in.currency_id = c_in.id
) c ON c.id = b.currency_id
LEFT JOIN last_rate ON last_rate.id = b.currency_id
ORDER BY name DESC, lastname, type;
