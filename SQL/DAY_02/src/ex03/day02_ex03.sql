WITH calendar_dates(missing_date) AS (
  SELECT generate_series(DATE '2022-01-01', DATE '2022-01-10', INTERVAL '1 day')::date
),
visits_by_target_persons(visit_date_only) AS (
  SELECT person_visits.visit_date::date
  FROM person_visits
  JOIN (VALUES (1), (2)) AS target_persons(person_id)
    ON target_persons.person_id = person_visits.person_id
  WHERE person_visits.visit_date::date BETWEEN DATE '2022-01-01' AND DATE '2022-01-10'
  GROUP BY person_visits.visit_date::date
)
SELECT calendar_dates.missing_date AS missing_date
FROM visits_by_target_persons
RIGHT JOIN calendar_dates
  ON visits_by_target_persons.visit_date_only = calendar_dates.missing_date
WHERE visits_by_target_persons.visit_date_only IS NULL
ORDER BY missing_date ASC;