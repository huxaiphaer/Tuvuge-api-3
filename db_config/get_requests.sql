CREATE OR REPLACE FUNCTION public.getrequests(
	id integer)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$
DECLARE
	qty int;
BEGIN
	SELECT COUNT(*) INTO qty
		FROM requests
			WHERE requests.id  = ID;
	RETURN qty;
END;

$BODY$;

ALTER FUNCTION public.getrequests(integer)
    OWNER TO postgres;

