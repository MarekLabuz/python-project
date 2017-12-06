CREATE TABLE public.movies
(
    id numeric NOT NULL,
    title text,
    year text,
    rating numeric,
    director text,
    length numeric,
    description text,
    poster_thumb text,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.movies
    OWNER to postgres;



CREATE TABLE public.people
(
    id numeric NOT NULL,
    name text,
    popularity numeric,
    birthday text,
    place_of_birth text,
    gender numeric,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.people
    OWNER to postgres;


CREATE TABLE public.movie_person
(
    movie_id numeric NOT NULL,
    person_id numeric NOT NULL,
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

ALTER TABLE public.movie_person
    OWNER to postgres;


CREATE TABLE public.genres
(
    movie_id numeric NOT NULL,
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

ALTER TABLE public.genres
    OWNER to postgres;