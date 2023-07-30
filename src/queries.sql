CREATE TABLE IF NOT EXISTS area
(
    id integer NOT NULL,
    name text NOT NULL,
    url text NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS employer
(
    id integer NOT NULL,
    name text NOT NULL,
    alternate_url text,
    vacancies_url text,
    accredited_it_employer boolean,
    trusted boolean,
    url text,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS vacancy
(
    id integer NOT NULL,
    name text NOT NULL,
    alternate_url text,
    created_at text,
    salary integer,
    snippet text,
    apply_alternate_url text,
    area_id integer NOT NULL,
    employer_id integer NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT area_id_key FOREIGN KEY (area_id)
        REFERENCES area (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT employer_id_key FOREIGN KEY (employer_id)
        REFERENCES employer (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);