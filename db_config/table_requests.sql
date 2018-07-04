CREATE TABLE requests
(
    id serial NOT NULL primary key,
    passengername text COLLATE pg_catalog."default" NOT NULL,
    "time" character(50) COLLATE pg_catalog."default",
    ride_offer_id integer NOT NULL,
    status character(50) COLLATE pg_catalog."default"
);