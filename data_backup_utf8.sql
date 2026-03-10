--
-- PostgreSQL database dump
--

\restrict t20FzA7AA0ioqU99vDhX7SuzMaieuwGHcgBMWDAzlP3cPhsB86T3jhkLcJFMKIK

-- Dumped from database version 17.9
-- Dumped by pg_dump version 17.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: utilisateurs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.utilisateurs (id, email, mot_de_passe, role, email_verifie, tel_verifie, kyc_valide, compte_actif, token_email, token_email_expiry, code_sms, code_sms_expiry, tentatives_sms, created_at, updated_at, last_login) FROM stdin;
3	jeanhuguesekongo9@yahoo.com	$2b$12$RI1S43CD7yyoH24Pbtjf/OgjaiphyhCWTnmUEzH3XmZ2fna9OhOi6	membre	t	t	t	t	\N	\N	\N	\N	0	2026-03-10 06:25:22.721792	2026-03-10 06:30:04.241275	\N
2	jeanhuguesekongo9@gmail.com	$2b$12$p7M1k7arUQwgHe1VPHaly.8qIUIEu0Knt0Z6P1RLSzOJNkHIsugrC	membre	t	t	t	t	\N	\N	\N	\N	0	2026-03-10 05:28:19.118365	2026-03-10 09:54:23.439492	2026-03-10 09:54:23.438266
1	admin@tontinesecure.com	$2b$12$aLXYNfQvjKEvljhaVt0sieTG7ZNj9xNQwUkM9HcVMpaLuFwzPKkze	admin	t	t	t	t	\N	\N	\N	\N	0	2026-03-10 05:04:15.609801	2026-03-10 10:43:09.121896	2026-03-10 10:43:09.12109
4	elysekongo17@gmail.com	$2b$12$etOlDiOUTqWZog0ulL48OueawNJ5GYtNUHy7VvhZxzdvOFitap9Fy	membre	t	t	t	t	\N	\N	\N	\N	0	2026-03-10 10:38:21.576008	2026-03-10 10:44:04.332275	\N
5	gracesylvia792@gmail.com	$2b$12$shsyB/X3iiI0nBIhAEoO5.fvGYlyilMfDM./RYGA4fitp//LjUV8e	membre	t	t	f	t	\N	\N	\N	\N	0	2026-03-10 12:16:02.940995	2026-03-10 12:22:51.395812	\N
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_logs (id, user_id, action, detail, ip_address, user_agent, created_at) FROM stdin;
1	1	deconnexion	\N	127.0.0.1	\N	2026-03-10 05:27:55.395314
2	2	inscription	Email: jeanhuguesekongo9@gmail.com	127.0.0.1	\N	2026-03-10 05:28:19.125271
3	2	kyc_soumis	\N	127.0.0.1	\N	2026-03-10 05:29:31.15325
4	1	kyc_approuve	User: 2	127.0.0.1	\N	2026-03-10 05:30:29.389152
5	2	rejoindre_tontine	Tontine: TB64965BD	127.0.0.1	\N	2026-03-10 05:45:00.723807
6	2	deconnexion	\N	127.0.0.1	\N	2026-03-10 06:24:35.179612
7	3	inscription	Email: jeanhuguesekongo9@yahoo.com	127.0.0.1	\N	2026-03-10 06:25:22.747663
8	3	kyc_soumis	\N	127.0.0.1	\N	2026-03-10 06:28:34.677816
9	1	kyc_approuve	User: 3	127.0.0.1	\N	2026-03-10 06:30:04.300059
10	2	connexion	\N	127.0.0.1	\N	2026-03-10 06:37:28.403966
11	2	deconnexion	\N	127.0.0.1	\N	2026-03-10 06:37:53.583616
12	2	connexion	\N	127.0.0.1	\N	2026-03-10 06:37:58.550109
13	2	connexion	\N	127.0.0.1	\N	2026-03-10 09:54:23.448599
14	4	inscription	Email: elysekongo17@gmail.com	127.0.0.1	\N	2026-03-10 10:38:21.597388
15	4	kyc_soumis	\N	127.0.0.1	\N	2026-03-10 10:42:27.175075
16	1	connexion	\N	127.0.0.1	\N	2026-03-10 10:43:09.127379
17	1	kyc_approuve	User: 4	127.0.0.1	\N	2026-03-10 10:44:04.347354
18	4	rejoindre_tontine	Tontine: TB64965BD	127.0.0.1	\N	2026-03-10 10:45:30.131312
19	5	inscription	Email: gracesylvia792@gmail.com	127.0.0.1	\N	2026-03-10 12:16:03.005594
\.


--
-- Data for Name: tontines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tontines (id, code, nom, montant_panier, nombre_membres, min_membres, max_membres, statut, date_debut, jour_collecte, description, createur_id, created_at) FROM stdin;
1	TB64965BD	TONTINE STANDARD	50000	2	5	10	recrutement	\N	10		1	2026-03-10 05:31:26.756945
\.


--
-- Data for Name: contrats; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contrats (id, reference, user_id, tontine_id, fichier_pdf, hash_contrat, signe, signe_le, ip_signature, created_at) FROM stdin;
\.


--
-- Data for Name: kyc; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kyc (id, user_id, doc_identite, type_doc, doc_identite2, bulletin_salaire, statut, note_admin, verifie_par, verifie_le, created_at, updated_at) FROM stdin;
1	2	identites\\549e876aeb84ba936176489e2444d8ad.pdf	passeport	identites\\1a94e05bb782c72929af31490323bbc7.pdf	bulletins\\95a1f008150c2ab15c7cab3fe251072d.pdf	approuve	\N	1	2026-03-10 05:30:29.334479	2026-03-10 05:29:31.142794	2026-03-10 05:30:29.34328
2	3	identites\\f704a72c29713e05e7d88aec5157a0ec.pdf	passeport	identites\\dfd7a6d3f5aefaa822959c754ca17044.pdf	bulletins\\d0fa018d0f7e68caa398fd3cb3fa89ee.pdf	approuve	\N	1	2026-03-10 06:30:04.151856	2026-03-10 06:28:34.651794	2026-03-10 06:30:04.184097
3	4	identites\\3299ae88658e459679df575b28158b96.pdf	cni	identites\\7c9d6ac1d95e94524f6a7b46d45c064c.pdf	bulletins\\fe745718398056455a82fae4fbdcc37f.pdf	approuve	\N	1	2026-03-10 10:44:04.239411	2026-03-10 10:42:27.16177	2026-03-10 10:44:04.241906
\.


--
-- Data for Name: membres_tontines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.membres_tontines (id, user_id, tontine_id, ordre_collecte, a_recu, statut, date_adhesion, contrat_signe, contrat_signe_le) FROM stdin;
1	2	1	\N	f	actif	2026-03-10 05:45:00.688871	f	\N
2	4	1	\N	f	actif	2026-03-10 10:45:30.11914	f	\N
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, user_id, titre, message, type_notif, lue, lien, created_at) FROM stdin;
1	2	Dossier approuve	Votre dossier KYC a ete approuve. Vous pouvez rejoindre une tontine !	success	f	/tontines/	2026-03-10 05:30:29.368893
2	2	Adhesion confirmee	Vous avez rejoint la tontine TONTINE STANDARD.	success	f	/tontines/mes-tontines	2026-03-10 05:45:00.622479
3	3	Dossier approuve	Votre dossier KYC a ete approuve. Vous pouvez rejoindre une tontine !	success	f	/tontines/	2026-03-10 06:30:04.256842
4	4	Dossier approuve	Votre dossier KYC a ete approuve. Vous pouvez rejoindre une tontine !	success	f	/tontines/	2026-03-10 10:44:04.336082
5	4	Adhesion confirmee	Vous avez rejoint la tontine TONTINE STANDARD.	success	f	/tontines/mes-tontines	2026-03-10 10:45:30.111784
\.


--
-- Data for Name: paiements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paiements (id, reference, user_id, tontine_id, montant, type_paiement, mois_reference, statut, date_echeance, date_paiement, created_at) FROM stdin;
\.


--
-- Data for Name: profils; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profils (id, user_id, nom, prenom, date_naissance, telephone, ville, pays, adresse, profession, employeur, revenu_mensuel, photo_profil, rib, banque, created_at) FROM stdin;
1	1	Admin	TontineSecure	1990-01-01	+00000000000	Paris	France	\N	Administrateur	\N	\N	\N	\N	\N	2026-03-10 05:04:15.619277
2	2	SEKONGO	KLOGNON Jean Hugue	2006-05-26	+221785385310	DAKAR	S├®n├®gal	\N	FINANCIER	Hg Capital SA	2500000	photos\\997373ce2a98b8933c5cc6bc057c0bce.jpeg	\N	\N	2026-03-10 05:29:00.98868
3	3	SEKONGO	Kephas	2005-05-10	+2250584022323	Senegal	C├┤te dÔÇÖivoire	\N			\N	photos\\543bc6f2259c24d88fb2434730702ca7.jpg	\N	\N	2026-03-10 06:27:29.779396
4	4	Sekongo	Tinloh Elys├®e	2003-08-25	+33503354921	Abidjan	Cote d'Ivoire	\N	ETUDIAN		100000	photos\\52a3b77aac80894c36e79384b55a0b65.jpg	\N	\N	2026-03-10 10:40:22.354819
5	5	Sylvia	Gr├óce	2005-05-22	0505846347	Abidjan	C├┤te d'Ivoire	\N			\N	\N	\N	\N	2026-03-10 12:22:51.420562
\.


--
-- Name: audit_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.audit_logs_id_seq', 19, true);


--
-- Name: contrats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contrats_id_seq', 1, false);


--
-- Name: kyc_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kyc_id_seq', 3, true);


--
-- Name: membres_tontines_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.membres_tontines_id_seq', 2, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notifications_id_seq', 5, true);


--
-- Name: paiements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.paiements_id_seq', 1, false);


--
-- Name: profils_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.profils_id_seq', 5, true);


--
-- Name: tontines_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tontines_id_seq', 1, true);


--
-- Name: utilisateurs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.utilisateurs_id_seq', 5, true);


--
-- PostgreSQL database dump complete
--

\unrestrict t20FzA7AA0ioqU99vDhX7SuzMaieuwGHcgBMWDAzlP3cPhsB86T3jhkLcJFMKIK

