CREATE OR REPLACE FUNCTION create_users(
	usn character varying,
	em character varying,
	pass text,
	isd integer)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$
declare
	total integer;

BEGIN
   INSERT INTO all_users (username,email,password_,isDriver,login_status)  VALUES(usn,
																			em,
											PGP_SYM_ENCRYPT(pass,'AES_KEY'),isd,'0');
   RETURN 1;
END;

$BODY$;



