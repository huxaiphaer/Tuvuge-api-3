CREATE OR REPLACE FUNCTION public.login_auth(
	usn character varying,
	pass text)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$

declare
	total integer;
declare c_usn varchar(200);
BEGIN
   SELECT PGP_SYM_DECRYPT(password_::bytea, 'AES_KEY') as password  into c_usn  from all_users where username = usn;
   
   if c_usn != pass  then
   return 0;
   else 
   UPDATE all_users SET login_status = '1' WHERE username = usn;
   return 1;
   

   end if ;
   return 0;
END;

$BODY$;


