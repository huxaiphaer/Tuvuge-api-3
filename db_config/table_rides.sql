CREATE TABLE public.rides
(
    id integer NOT NULL DEFAULT nextval('rides_id_seq'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    details text COLLATE pg_catalog."default" NOT NULL,
    price money,
    driver text COLLATE pg_catalog."default",
    CONSTRAINT rides_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.rides
    OWNER to postgres;