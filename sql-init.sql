DROP TABLE IF EXISTS public.movies CASCADE;
DROP TABLE IF EXISTS public.people CASCADE;
DROP TABLE IF EXISTS public.movie_person;
DROP TABLE IF EXISTS public.genres;

CREATE TABLE public.movies
(
    id integer NOT NULL,
    title text,
    year text,
    rating integer,
    director text,
    length integer,
    description text,
    poster_thumb text,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

--ALTER TABLE public.movies
--    OWNER to postgres;



CREATE TABLE public.people
(
    id integer NOT NULL,
    name text,
    popularity real,
    birthday text,
    place_of_birth text,
    gender integer,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

--ALTER TABLE public.people
--    OWNER to postgres;


CREATE TABLE public.movie_person
(
    movie_id integer NOT NULL,
    person_id integer NOT NULL,
    role_name text,
    CONSTRAINT movie_id FOREIGN KEY (movie_id)
        REFERENCES public.movies (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT person_id FOREIGN KEY (person_id)
        REFERENCES public.people (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
);

--ALTER TABLE public.movie_person
--    OWNER to postgres;


CREATE TABLE public.genres
(
    movie_id integer NOT NULL,
    genre text NOT NULL,
    PRIMARY KEY (movie_id, genre),
    CONSTRAINT movie_id FOREIGN KEY (movie_id)
        REFERENCES public.movies (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
);

--ALTER TABLE public.genres
--    OWNER to postgres;