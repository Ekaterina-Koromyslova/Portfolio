COMMENT ON TABLE person_discounts IS
    'Таблица, в которой хранится персональная скидка для каждого клиента в каждой пиццерии. Используется для системы лояльности.';

COMMENT ON COLUMN person_discounts.id IS
    'Уникальный идентификатор записи о скидке (первичный ключ).';

COMMENT ON COLUMN person_discounts.person_id IS
    'Внешний ключ на клиента, которому назначена скидка.';

COMMENT ON COLUMN person_discounts.pizzeria_id IS
    'Внешний ключ на пиццерию, в которой действует скидка.';

COMMENT ON COLUMN person_discounts.discount IS
    'Значение скидки в процентах (от 0 до 100).';

SELECT count(*) = 5 AS check
FROM pg_description
WHERE objoid = 'person_discounts'::regclass;
