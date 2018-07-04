CREATE OR REPLACE FUNCTION public.get_ride_requests(
	)
    RETURNS TABLE(id integer, passengername character varying, time_ timestamp without time zone, name character varying) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
BEGIN
 RETURN QUERY
 
 SELECT * from requests;
 
END; 
$BODY$;


