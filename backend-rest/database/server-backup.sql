--
-- PostgreSQL database dump
--

-- Dumped from database version 15.0
-- Dumped by pg_dump version 15.0

-- Started on 2022-11-04 12:29:55

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 842 (class 1247 OID 16686)
-- Name: LogType; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."LogType" AS ENUM (
    'Event',
    'Error'
);


ALTER TYPE public."LogType" OWNER TO postgres;

--
-- TOC entry 845 (class 1247 OID 16692)
-- Name: ObjectType; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."ObjectType" AS ENUM (
    'Can',
    'OtherRobot',
    'OurRobot'
);


ALTER TYPE public."ObjectType" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 214 (class 1259 OID 16699)
-- Name: Logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Logs" (
    "Id" integer NOT NULL,
    "CreatedAt" timestamp without time zone DEFAULT now() NOT NULL,
    "Origin" text,
    "Message" text NOT NULL,
    "Type" public."LogType",
    "StackTrace" text
);


ALTER TABLE public."Logs" OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16705)
-- Name: Logs_Id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Logs_Id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Logs_Id_seq" OWNER TO postgres;

--
-- TOC entry 3357 (class 0 OID 0)
-- Dependencies: 215
-- Name: Logs_Id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Logs_Id_seq" OWNED BY public."Logs"."Id";


--
-- TOC entry 216 (class 1259 OID 16706)
-- Name: Map; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Map" (
    "Id" integer NOT NULL,
    "CreatedAt" timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public."Map" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16710)
-- Name: MapObject; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MapObject" (
    "Id" integer NOT NULL,
    "CreatedAt" timestamp without time zone DEFAULT now() NOT NULL,
    "MapId" integer NOT NULL,
    "ObjectType" public."ObjectType" NOT NULL,
    "LocationX" integer,
    "LocationY" integer,
    "Direction" text
);


ALTER TABLE public."MapObject" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16714)
-- Name: MapObject_Id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MapObject_Id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MapObject_Id_seq" OWNER TO postgres;

--
-- TOC entry 3360 (class 0 OID 0)
-- Dependencies: 218
-- Name: MapObject_Id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MapObject_Id_seq" OWNED BY public."MapObject"."Id";


--
-- TOC entry 219 (class 1259 OID 16715)
-- Name: Map_Id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Map_Id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Map_Id_seq" OWNER TO postgres;

--
-- TOC entry 3361 (class 0 OID 0)
-- Dependencies: 219
-- Name: Map_Id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Map_Id_seq" OWNED BY public."Map"."Id";


--
-- TOC entry 3189 (class 2604 OID 16716)
-- Name: Logs Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Logs" ALTER COLUMN "Id" SET DEFAULT nextval('public."Logs_Id_seq"'::regclass);


--
-- TOC entry 3191 (class 2604 OID 16717)
-- Name: Map Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Map" ALTER COLUMN "Id" SET DEFAULT nextval('public."Map_Id_seq"'::regclass);


--
-- TOC entry 3193 (class 2604 OID 16718)
-- Name: MapObject Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObject" ALTER COLUMN "Id" SET DEFAULT nextval('public."MapObject_Id_seq"'::regclass);


--
-- TOC entry 3344 (class 0 OID 16699)
-- Dependencies: 214
-- Data for Name: Logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Logs" ("Id", "CreatedAt", "Origin", "Message", "Type", "StackTrace") FROM stdin;
1	2022-10-27 14:55:44.350771	app.py	HTTPConnectionPool(host='karr.local', port=5000): Max retries exceeded with url: /right (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000001CDA7B72320>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))	Error	
2	2022-10-28 10:47:17.695846	app.py	HTTPConnectionPool(host='karr.local', port=5000): Max retries exceeded with url: /right (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000019DA17F22F0>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))	Error	
3	2022-11-01 19:57:49.831493	app.py	Logs retrieved from /logs GET	Event	
4	2022-11-01 19:59:07.904438	app.py	Logs retrieved from /logs GET	Event	
5	2022-11-01 20:32:21.870894	app.py	Logs retrieved from /logs GET	Event	
\.


--
-- TOC entry 3346 (class 0 OID 16706)
-- Dependencies: 216
-- Data for Name: Map; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Map" ("Id", "CreatedAt") FROM stdin;
1	2022-10-26 15:03:51.099807
\.


--
-- TOC entry 3347 (class 0 OID 16710)
-- Dependencies: 217
-- Data for Name: MapObject; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."MapObject" ("Id", "CreatedAt", "MapId", "ObjectType", "LocationX", "LocationY", "Direction") FROM stdin;
\.


--
-- TOC entry 3362 (class 0 OID 0)
-- Dependencies: 215
-- Name: Logs_Id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Logs_Id_seq"', 5, true);


--
-- TOC entry 3363 (class 0 OID 0)
-- Dependencies: 218
-- Name: MapObject_Id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."MapObject_Id_seq"', 1, false);


--
-- TOC entry 3364 (class 0 OID 0)
-- Dependencies: 219
-- Name: Map_Id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Map_Id_seq"', 1, true);


--
-- TOC entry 3196 (class 2606 OID 16720)
-- Name: Logs Logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Logs"
    ADD CONSTRAINT "Logs_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3200 (class 2606 OID 16722)
-- Name: MapObject MapObject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObject"
    ADD CONSTRAINT "MapObject_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3198 (class 2606 OID 16724)
-- Name: Map Map_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Map"
    ADD CONSTRAINT "Map_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3201 (class 2606 OID 16725)
-- Name: MapObject MapId; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObject"
    ADD CONSTRAINT "MapId" FOREIGN KEY ("MapId") REFERENCES public."Map"("Id") NOT VALID;


--
-- TOC entry 3355 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO flaskuser WITH GRANT OPTION;


--
-- TOC entry 3356 (class 0 OID 0)
-- Dependencies: 214
-- Name: TABLE "Logs"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public."Logs" TO flaskuser;


--
-- TOC entry 3358 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE "Map"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public."Map" TO flaskuser;


--
-- TOC entry 3359 (class 0 OID 0)
-- Dependencies: 217
-- Name: TABLE "MapObject"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public."MapObject" TO flaskuser;


-- Completed on 2022-11-04 12:29:55

--
-- PostgreSQL database dump complete
--

