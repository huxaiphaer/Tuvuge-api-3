CREATE TABLE public.rides
(
    id serial NOT NULL ,
    name text  NOT NULL,
    details textCOLLATE pg_catalog."default" NOT NULL,
    price money,
    driver text 
  
);