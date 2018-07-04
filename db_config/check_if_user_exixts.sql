CREATE OR REPLACE FUNCTION public.check_if_user_exixts(
	un character varying)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$
declare
	total integer;
	declare c_name varchar(45);
BEGIN
  select username into c_name from all_users where username =un; 
  if c_name is null then 
  return 0;
  else 
  return 1;
  
  end if;
   RETURN 0;
END;

$BODY$;
