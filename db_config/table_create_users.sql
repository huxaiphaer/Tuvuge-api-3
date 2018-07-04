CREATE TABLE public.all_users
(
    id integer NOT NULL DEFAULT nextval('all_users_id_seq'::regclass),
    username text COLLATE pg_catalog."default",
    email text COLLATE pg_catalog."default",
    password_ text COLLATE pg_catalog."default",
    isdriver text COLLATE pg_catalog."default",
    login_status text COLLATE pg_catalog."default",
    CONSTRAINT all_users_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.all_users
    OWNER to postgres;