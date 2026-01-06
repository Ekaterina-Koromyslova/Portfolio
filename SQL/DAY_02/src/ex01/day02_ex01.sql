SELECT calendar_dates.missing_date::date AS missing_date

FROM (
  SELECT person_visits.visit_date::date AS visit_date_only
  FROM person_visits
  JOIN (VALUES (1), (2)) AS target_persons(person_id)
    ON target_persons.person_id = person_visits.person_id
  WHERE person_visits.visit_date::date BETWEEN DATE '2022-01-01' AND DATE '2022-01-10'
  GROUP BY person_visits.visit_date::date
) AS visits_by_target_persons

RIGHT JOIN generate_series(DATE '2022-01-01', DATE '2022-01-10', INTERVAL '1 day')
       AS calendar_dates(missing_date)
  ON visits_by_target_persons.visit_date_only = calendar_dates.missing_date::date

WHERE visits_by_target_persons.visit_date_only IS NULL
ORDER BY missing_date ASC;
