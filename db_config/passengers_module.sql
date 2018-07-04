CREATE OR REPLACE FUNCTION public.passengers_module(
	lg integer,
	isd integer)
    RETURNS text
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$

declare
	name integer;
BEGIN
   select username  into name from users where login_status = lg and isDriver=isd;
   RETURN name;
END;

$BODY$;


