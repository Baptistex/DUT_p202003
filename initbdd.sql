CREATE SCHEMA bcv;

DROP TABLE bcv._personne;
CREATE TABLE bcv._personne (
    id SERIAL,
    nom character varying(20),
    prenom character varying(20),
    mot_de_passe character varying(255),
    mail character varying(40),
    num_tel character varying(20)
);

ALTER TABLE ONLY bcv._personne
ADD CONSTRAINT _personne_pkey PRIMARY KEY (id);

INSERT INTO bcv._personne VALUES (DEFAULT,'Jean','Dupond','aaa','Jean@gmail.com','0123456789');



