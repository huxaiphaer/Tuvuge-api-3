CREATE TABLE public.requests
(
    id integer NOT NULL DEFAULT nextval('requests_id_seq'::regclass),
    passengername text COLLATE pg_catalog."default" NOT NULL,
    "time" character(50) COLLATE pg_catalog."default",
    ride_offer_id integer NOT NULL,
    status character(50) COLLATE pg_catalog."default",
    CONSTRAINT requests_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.requests
    OWNER to postgres;