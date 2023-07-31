CREATE TABLE IF NOT EXISTS area
(
    area_id integer NOT NULL,
    name text NOT NULL,
    url text NOT NULL,
    PRIMARY KEY (area_id)
);
CREATE TABLE IF NOT EXISTS employer
(
    employer_id integer NOT NULL,
    name text NOT NULL,
    alternate_url text,
    vacancies_url text,
    accredited_it_employer boolean,
    trusted boolean,
    url text,
    PRIMARY KEY (employer_id)
);
CREATE TABLE IF NOT EXISTS vacancy
(
    vacancy_id integer NOT NULL,
    name text NOT NULL,
    alternate_url text,
    created_at text,
    salary integer,
    snippet text,
    apply_alternate_url text,
    area_id integer NOT NULL,
    employer_id integer NOT NULL,
    PRIMARY KEY (vacancy_id),
    CONSTRAINT area_id_key FOREIGN KEY (area_id)
        REFERENCES area (area_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT employer_id_key FOREIGN KEY (employer_id)
        REFERENCES employer (employer_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);
-- Получает список всех компаний и количество вакансий у каждой компании.
SELECT employer.name, COUNT(vacancy.name)
FROM employer JOIN vacancy USING (employer_id)
GROUP BY employer.name
ORDER BY employer.name ASC;
-- Получает список всех вакансий с указанием названия компании, названия
-- вакансии и зарплаты и ссылки на вакансию.
SELECT employer.name, vacancy.name, vacancy.salary, vacancy.alternate_url
FROM employer JOIN vacancy USING (employer_id)
ORDER BY employer.name ASC;
-- Получает среднюю зарплату по вакансиям.
SELECT AVG(salary)
FROM vacancy
WHERE salary <> 0;
-- Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT name, salary, alternate_url FROM vacancy
WHERE salary > (SELECT AVG(salary) FROM vacancy WHERE salary <> 0);
-- Получает список всех вакансий, в названии которых содержатся переданные
-- в метод слова, например “python”.
SELECT name, salary, alternate_url
FROM vacancy
WHERE name ILIKE '%Pattern%';