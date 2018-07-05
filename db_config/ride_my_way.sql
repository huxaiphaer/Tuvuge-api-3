--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

-- Started on 2018-07-05 10:10:29

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12924)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2888 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 2 (class 3079 OID 32864)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 2889 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- TOC entry 242 (class 1255 OID 32858)
-- Name: check_if_user_exixts(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.check_if_user_exixts(un character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$declare
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
$$;


ALTER FUNCTION public.check_if_user_exixts(un character varying) OWNER TO postgres;

--
-- TOC entry 231 (class 1255 OID 32901)
-- Name: create_users(character varying, character varying, text, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.create_users(usn character varying, em character varying, pass text, isd integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$declare
	total integer;

BEGIN
   INSERT INTO all_users (username,email,password_,isDriver,login_status)  VALUES(usn,
																			em,
											PGP_SYM_ENCRYPT(pass,'AES_KEY'),isd,'0');
   RETURN 1;
END;

$$;


ALTER FUNCTION public.create_users(usn character varying, em character varying, pass text, isd integer) OWNER TO postgres;

--
-- TOC entry 257 (class 1255 OID 32838)
-- Name: get_ride_requests(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_ride_requests() RETURNS TABLE(id integer, passengername character varying, time_ timestamp without time zone, name character varying)
    LANGUAGE plpgsql
    AS $$BEGIN
 RETURN QUERY
 
 SELECT * from requests;
 
END; $$;


ALTER FUNCTION public.get_ride_requests() OWNER TO postgres;

--
-- TOC entry 221 (class 1255 OID 32839)
-- Name: getrequests(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.getrequests(id integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$DECLARE
	qty int;
BEGIN
	SELECT COUNT(*) INTO qty
		FROM requests
			WHERE requests.id  = ID;
	RETURN qty;
END;
$$;


ALTER FUNCTION public.getrequests(id integer) OWNER TO postgres;

--
-- TOC entry 254 (class 1255 OID 32862)
-- Name: login_auth(character varying, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.login_auth(usn character varying, pass text) RETURNS integer
    LANGUAGE plpgsql
    AS $$
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

$$;


ALTER FUNCTION public.login_auth(usn character varying, pass text) OWNER TO postgres;

--
-- TOC entry 255 (class 1255 OID 32904)
-- Name: passengers_module(integer, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.passengers_module(lg integer, isd integer) RETURNS text
    LANGUAGE plpgsql
    AS $$

declare
	name integer;
BEGIN
   select username  into name from users where login_status = lg and isDriver=isd;
   RETURN name;
END;

$$;


ALTER FUNCTION public.passengers_module(lg integer, isd integer) OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 205 (class 1259 OID 32907)
-- Name: all_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.all_users (
    id integer NOT NULL,
    username text,
    email text,
    password_ text,
    isdriver text,
    login_status text
);


ALTER TABLE public.all_users OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 32905)
-- Name: all_users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.all_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.all_users_id_seq OWNER TO postgres;

--
-- TOC entry 2890 (class 0 OID 0)
-- Dependencies: 204
-- Name: all_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.all_users_id_seq OWNED BY public.all_users.id;


--
-- TOC entry 201 (class 1259 OID 32847)
-- Name: moiti; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.moiti (
    id integer,
    name character varying(45)
);


ALTER TABLE public.moiti OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 32822)
-- Name: requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.requests (
    id integer NOT NULL,
    passengername text NOT NULL,
    "time" character(50),
    ride_offer_id integer NOT NULL,
    status character(50)
);


ALTER TABLE public.requests OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 32820)
-- Name: requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.requests_id_seq OWNER TO postgres;

--
-- TOC entry 2891 (class 0 OID 0)
-- Dependencies: 199
-- Name: requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.requests_id_seq OWNED BY public.requests.id;


--
-- TOC entry 198 (class 1259 OID 24638)
-- Name: rides; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rides (
    id integer NOT NULL,
    name text NOT NULL,
    details text NOT NULL,
    price money,
    driver text
);


ALTER TABLE public.rides OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 24636)
-- Name: rides_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rides_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rides_id_seq OWNER TO postgres;

--
-- TOC entry 2892 (class 0 OID 0)
-- Dependencies: 197
-- Name: rides_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rides_id_seq OWNED BY public.rides.id;


--
-- TOC entry 203 (class 1259 OID 32852)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(45),
    email character varying(45),
    password_ text,
    isdriver integer,
    login_status text
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 32850)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 2893 (class 0 OID 0)
-- Dependencies: 202
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 2742 (class 2604 OID 32910)
-- Name: all_users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.all_users ALTER COLUMN id SET DEFAULT nextval('public.all_users_id_seq'::regclass);


--
-- TOC entry 2740 (class 2604 OID 32825)
-- Name: requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests ALTER COLUMN id SET DEFAULT nextval('public.requests_id_seq'::regclass);


--
-- TOC entry 2739 (class 2604 OID 24641)
-- Name: rides id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rides ALTER COLUMN id SET DEFAULT nextval('public.rides_id_seq'::regclass);


--
-- TOC entry 2741 (class 2604 OID 32855)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 2880 (class 0 OID 32907)
-- Dependencies: 205
-- Data for Name: all_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.all_users (id, username, email, password_, isdriver, login_status) FROM stdin;
13	jau	j@gmail.com	\\xc30d040703024db0a8515b1cd5027dd23a011d0d31397b0cc8284526f0056c8940c700a21c8103d64d5e6ea1b5ccf41f31dbfa41eb372b5a74aa32bc8d1aaf7c419701236cca3bf6f7697a	0	1
14	yusuf	yusuf@gmail.com	\\xc30d04070302aaa890086cab980477d2390139a8181edded457c16250ae09f767db7e196358b19cd014e34dfd54b22246821c7a4a30f78684e29aabcc3c667a75e3084bf8ccda8c8b837	0	1
\.


--
-- TOC entry 2876 (class 0 OID 32847)
-- Dependencies: 201
-- Data for Name: moiti; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.moiti (id, name) FROM stdin;
\.


--
-- TOC entry 2875 (class 0 OID 32822)
-- Dependencies: 200
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.requests (id, passengername, "time", ride_offer_id, status) FROM stdin;
2	Huza	17:20:38.083813                                   	2	0                                                 
3	Huza	17:41:01.901958                                   	3	0                                                 
4	Huza	15:09:23.587976                                   	5	0                                                 
5	Huza	2018-07-02 15:21:29.244278                        	6	0                                                 
6	Huza	2018-07-04 00:24:17.198130                        	7	0                                                 
7	Huza	2018-07-04 12:14:17.175413                        	24	0                                                 
8	Huza	2018-07-04 14:26:01.212251                        	9	0                                                 
1	Huza	\N	1	0                                                 
\.


--
-- TOC entry 2873 (class 0 OID 24638)
-- Dependencies: 198
-- Data for Name: rides; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rides (id, name, details, price, driver) FROM stdin;
2	easter  offer 	Kampala to Mubende	$40,000.00	Huza
3	katwe  offer 	Kampala to Mubende	$4,000.00	Huza
4	easter  offer 	Kampala to Mubende	$40,000.00	Huza
5	christamas  offer 	Kampala to Mubende	$60,000.00	Huza
6	test  offer 	Kampala to Mubende	$60,000.00	Huza
7	test  offer 	Kampala to Mubende	$60,000.00	Huza
8	 now working  offer 	Kampala to Mubende	$70,000.00	Huza
9	 hello too  offer 	Kampala to Mubende	$70,000.00	Huza
10	 close too  offer 	Kampala to Mubende	$90,000.00	Huza
11	 bwaise too  offer 	Kampala to Mubende	$100,000.00	Huza
12	ramadhan offer	Kampala to Mubende	$100,000.00	Huza
13	ramadhan offer	Kampala to Mubende	$100,000.00	Huza
14	ramadhan offer	Kampala to Mubende	$100,000.00	Huza
15	ramadhan offer	Kampala to Mubende	$100,000.00	Huza
16	x offer	Kampala to Mubende	$100,000.00	Huza
17	x offer	Kampala to Mubende	$100,000.00	Huza
18	x offer	Kampala to Mubende	$100,000.00	Huza
19	x offer	Kampala to Mubende	$100,000.00	Huza
20	x offer	Kampala to Mubende	$100,000.00	Huza
21	x offer	Kampala to Mubende	$100,000.00	Huza
22	x offer	Kampala to Mubende	$100,000.00	Huza
23	x offer	Kampala to Mubende	$100,000.00	Huza
24	op offer	Kampala to Mubende	$100,000.00	Huza
25	katuuso  offer 	Kampala to Mubende	$500.00	Huza
71	Easter offer 2018-07-04 19:46:58.210988	Get an offer of 30% of this	$8,000.00	Huza
72	Easter offer 2018-07-04 19:49:38.789051	Get an offer of 30% of this	$8,000.00	Huza
1	am cool	This offer cuts down 3% of the drive, you want	$2,000.00	Huza
26	mio offer 	Kampala to Mubende	$500.00	Huza
27	trick offer 	Kampala to Mubende	$500.00	Huza
28	great  offer 	Kampala to Mubende	$500.00	Huza
29	Easter offer	Get an offer of 30% of this	$8,000.00	Huza
30			$0.00	Huza
31	Easter offer 2018-07-04 10:37:23.990539	Get an offer of 30% of this	$8,000.00	Huza
32	weekly   offer	ntinda to kibuli	$4,000.00	Huza
33	black friday   offer	ntinda to kibuli	$4,000.00	Huza
34	Easter offer 2018-07-04 14:25:09.957379	Get an offer of 30% of this	$8,000.00	Huza
35	Easter offer 2018-07-04 14:25:15.603318	Get an offer of 30% of this	$8,000.00	Huza
36	red friday   offer	ntinda to kibuli	$4,000.00	Huza
37	Easter offer 2018-07-04 16:14:42.809725	Get an offer of 30% of this	$8,000.00	Huza
38	Easter offer 2018-07-04 16:14:49.367667	Get an offer of 30% of this	$8,000.00	Huza
39	Easter offer 2018-07-04 16:16:49.264066	Get an offer of 30% of this	$8,000.00	Huza
40	Easter offer 2018-07-04 16:48:00.217223	Get an offer of 30% of this	$8,000.00	Huza
41	Easter offer 2018-07-04 16:55:51.163399	Get an offer of 30% of this	$8,000.00	Huza
42	Easter offer 2018-07-04 16:56:19.003762	Get an offer of 30% of this	$8,000.00	Huza
43	Easter offer 2018-07-04 16:57:20.861990	Get an offer of 30% of this	$8,000.00	Huza
44	Easter offer 2018-07-04 17:01:20.202804	Get an offer of 30% of this	$8,000.00	Huza
45	Easter offer 2018-07-04 17:02:04.482387	Get an offer of 30% of this	$8,000.00	Huza
46	Easter offer 2018-07-04 17:04:35.957357	Get an offer of 30% of this	$8,000.00	Huza
47	Easter offer 2018-07-04 17:07:09.165403	Get an offer of 30% of this	$8,000.00	Huza
48	Easter offer 2018-07-04 17:07:44.575163	Get an offer of 30% of this	$8,000.00	Huza
49	Easter offer 2018-07-04 17:12:52.348294	Get an offer of 30% of this	$8,000.00	Huza
50	Easter offer 2018-07-04 17:16:54.481311	Get an offer of 30% of this	$8,000.00	Huza
51	Easter offer 2018-07-04 17:23:13.057091	Get an offer of 30% of this	$8,000.00	Huza
52	Easter offer 2018-07-04 17:24:11.962034	Get an offer of 30% of this	$8,000.00	Huza
53	Easter offer 2018-07-04 17:24:41.705119	Get an offer of 30% of this	$8,000.00	Huza
54	Easter offer 2018-07-04 17:28:07.801337	Get an offer of 30% of this	$8,000.00	Huza
55	Easter offer 2018-07-04 17:31:47.131384	Get an offer of 30% of this	$8,000.00	Huza
56	Easter offer 2018-07-04 17:32:31.252196	Get an offer of 30% of this	$8,000.00	Huza
57	Easter offer 2018-07-04 17:34:22.724273	Get an offer of 30% of this	$8,000.00	Huza
58	Easter offer 2018-07-04 17:35:43.114019	Get an offer of 30% of this	$8,000.00	Huza
59	Easter offer 2018-07-04 17:38:14.266103	Get an offer of 30% of this	$8,000.00	Huza
60	Easter offer 2018-07-04 17:38:52.731184	Get an offer of 30% of this	$8,000.00	Huza
61	Easter offer 2018-07-04 17:41:15.950703	Get an offer of 30% of this	$8,000.00	Huza
62	Easter offer 2018-07-04 17:41:46.858869	Get an offer of 30% of this	$8,000.00	Huza
63	Easter offer 2018-07-04 17:42:38.359486	Get an offer of 30% of this	$8,000.00	Huza
64	Easter offer 2018-07-04 18:10:50.097582	Get an offer of 30% of this	$8,000.00	Huza
65	Easter offer 2018-07-04 18:13:59.723874	Get an offer of 30% of this	$8,000.00	Huza
66	Easter offer 2018-07-04 18:15:48.742822	Get an offer of 30% of this	$8,000.00	Huza
67	Easter offer 2018-07-04 18:16:15.555028	Get an offer of 30% of this	$8,000.00	Huza
68	Easter offer 2018-07-04 18:17:39.303461	Get an offer of 30% of this	$8,000.00	Huza
69	Easter offer 2018-07-04 18:19:01.818615	Get an offer of 30% of this	$8,000.00	Huza
70	Easter offer 2018-07-04 19:46:06.545203	Get an offer of 30% of this	$8,000.00	Huza
73	Easter offer 2018-07-04 20:18:04.337457	Get an offer of 30% of this	$8,000.00	Huza
74	Easter offer 2018-07-04 20:18:17.681404	Get an offer of 30% of this	$8,000.00	Huza
75	Easter offer 2018-07-04 20:23:57.607157	Get an offer of 30% of this	$8,000.00	Huza
76	Easter offer 2018-07-04 20:26:48.403504	Get an offer of 30% of this	$8,000.00	Huza
77	Easter offer 2018-07-04 20:33:10.015148	Get an offer of 30% of this	$8,000.00	Huza
\.


--
-- TOC entry 2878 (class 0 OID 32852)
-- Dependencies: 203
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_, isdriver, login_status) FROM stdin;
1	lutaaya	l@gmail.com	123456789	1	0
2	huzaifah	huza@gmail.com	123456789	1	0
3	idrislutalo	katwe@gmail.com	pbkdf2:sha256:50000$2j5i1gfJ$45a83c19530cc65daec23d11f2956c66667637e526b0b51ca9548e001c6a947d	1	0
4	mzee	rt@gmail.com	\\303\\015\\004\\007\\003\\002\\372\\300\\023\\276F6\\\\l{\\3225\\001O\\236J\\015<-\\205.:\\037\\012;\\236\\361N\\234\\377Z-\\214(H\\243\\252\\220F\\034\\265\\361#\\012`\\326\\235\\323\\361\\275\\206|ofj\\301\\324\\213\\231\\264G\\366Q\\230\\311	1	0
5	kato	k@gmail.com	\\xc30d0407030261a3a332ce5b6aeb79d23a01914236f14fa47aba75e507c5d9e0d18cc5dd678b98be13809e87401750f23f104460d9227f57e04db1bf6a492a3987062342ce0ab1a477a37d	1	1
7	tom	t@gmail.com	\\303\\015\\004\\007\\003\\002\\203\\255\\232\\223\\250\\23538|\\3226\\001<\\376j\\247O\\352\\333\\254\\000\\367\\233!\\200\\234\\335\\207\\006\\227X}?\\365Q\\262<9\\366\\357r\\302\\305\\352\\221\\336\\235\\373\\270\\345o&m\\376\\265\\362\\330#5\\362\\3257\\212f\\245	0	0
9	nabkimil	nabil@gmail.com	\\xc30d04070302e9987ce7f77ca9867cd23a011c6c0bac4d3c8429c6aedaa5ad1daa61133b1a4861d23d513bff6bfddd097201c8f7d9ccd6259d2f7754e8ec8be8258dc3f2a8599cf60889aa	0	0
6	max	nabil@gmail.com	\\xc30d040703022ade566d0f2adfde7ed23a01ace5f819ffb04a407e831e945658f7970b601eaa18daf5103e05a3d87d19118d1deba7760f87563f76c678de9906c02abe49eafcbdcc002f08	0	1
\.


--
-- TOC entry 2894 (class 0 OID 0)
-- Dependencies: 204
-- Name: all_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.all_users_id_seq', 14, true);


--
-- TOC entry 2895 (class 0 OID 0)
-- Dependencies: 199
-- Name: requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.requests_id_seq', 8, true);


--
-- TOC entry 2896 (class 0 OID 0)
-- Dependencies: 197
-- Name: rides_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rides_id_seq', 77, true);


--
-- TOC entry 2897 (class 0 OID 0)
-- Dependencies: 202
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 9, true);


--
-- TOC entry 2750 (class 2606 OID 32915)
-- Name: all_users all_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.all_users
    ADD CONSTRAINT all_users_pkey PRIMARY KEY (id);


--
-- TOC entry 2746 (class 2606 OID 32830)
-- Name: requests requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (id);


--
-- TOC entry 2744 (class 2606 OID 24646)
-- Name: rides rides_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rides
    ADD CONSTRAINT rides_pkey PRIMARY KEY (id);


--
-- TOC entry 2748 (class 2606 OID 32857)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


-- Completed on 2018-07-05 10:10:31

--
-- PostgreSQL database dump complete
--

