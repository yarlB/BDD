select table_name from user_tables;

DROP TABLE Clients CASCADE CONSTRAINTS;
CREATE TABLE Clients(
       idcl number PRIMARY KEY, 
       nom varchar2(20), 
       pren varchar2(15),
       adr varchar2(30),
       tel varchar2(12)
);

DROP TABLE Livres CASCADE CONSTRAINTS;
CREATE TABLE Livres(
       refl varchar2(10) PRIMARY KEY,
       titre varchar2(20),
       auteur varchar2(20),
       genre varchar2(15),
       note_moy number DEFAULT 0
);

DROP TABLE Achats CASCADE CONSTRAINTS;
CREATE TABLE Achats(
       idcl number REFERENCES Clients(idcl),
       refl varchar2(10) REFERENCES Livres(refl),
       dateachat date CHECK(dateachat BETWEEN to_date('01-jan-2008','DD-MON-YYYY')
       AND to_date('31-dec-2013','DD-MON-YYYY')),
       CONSTRAINT pk_Achat PRIMARY KEY (idcl,refl,dateachat)
);

DROP TABLE Avis CASCADE CONSTRAINTS;
CREATE TABLE Avis(
       idcl number REFERENCES Clients(idcl),
       refl varchar2(10) REFERENCES Livres(refl),
       note number(4,2),
       commentaire varchar2(50),
       CONSTRAINT pk_Avis PRIMARY KEY (idcl,refl)
);

DROP TABLE Parcours CASCADE CONSTRAINTS;
CREATE TABLE Parcours(
       idp varchar2(10),
       intitulep varchar2(15);
       genre varchar2(15),
       date_deb date,
       CONSTRAINT pk_Parcours PRIMARY KEY (idp)
);

DROP TABLE Compo_Parcours CASCADE CONSTRAINTS;
CREATE TABLE Compo_Parcours(
       idp varchar2(10),
       id_evt varchar2(10),
       CONSTRAINT fk_cpp FOREIGN KEY (idp) REFERENCES Parcours(idp),
       CONSTRAINT pk_Compo_Parcours PRIMARY KEY (idp,id_evt)
);

DROP TABLE Inscrip_Parcours CASCADE CONSTRAINTS;
CREATE TABLE Inscrip_Parcours(
       idcl number,
       idp varchar2(10),
       CONSTRAINT fk_ipc FOREIGN KEY (idcl) REFERENCES Clients(idcl),
       CONSTRAINT fk_ipp FOREIGN KEY (idp) REFERENCES Parcours(idp),
       CONSTRAINT pk_Inscrip_Parcours PRIMARY KEY (idcl,idp)
);

DROP TABLE Inscrip_Evt CASCADE CONSTRAINTS;
CREATE TABLE Inscrip_Evt(
       idcl number,
       idp varchar2(10),
       id_evt varchar2(10),
       CONSTRAINT fk_iec FOREIGN KEY (idcl) REFERENCES Clients(idcl),
       CONSTRAINT fk_iep FOREIGN KEY (idp) REFERENCES Parcours(idp),
       CONSTRAINT fk_iecp FOREIGN KEY (id_evt) REFERENCES Compo_Parcours(id_evt),
       CONSTRAINT pk_ie PRIMARY KEY (idcl,idp,id_evt)
);

INSERT INTO Clients VALUES (1,'GIBAUD','Lary','num rue ville','00');
INSERT INTO Livres VALUES ('mouarf','MOUARF','Mr OUAF','horreur');
INSERT INTO Livres VALUES ('mouarf2','MOUARF le retour','Mr OUAF','horreur');
INSERT INTO Achats VALUES (1,'mouarf','01-jan-2008');
INSERT INTO Achats VALUES (1,'mouarf','02-jan-2008');
INSERT INTO Achats VALUES (1,'mouarf','03-jan-2008');
INSERT INTO Achats VALUES (1,'mouarf','04-jan-2008');
INSERT INTO Achats VALUES (1,'mouarf2','01-jan-2008');
INSERT INTO Achats VALUES (1,'mouarf2','02-jan-2008');
INSERT INTO Achats VALUES (1,'mouarf2','03-jan-2008');

SELECT titre, auteur, genre 
FROM Livres NATURAL JOIN (
     SELECT refl FROM Achats 
     GROUP BY refl

     HAVING COUNT(refl) >= 4
);


/* calcul moyenne pour un bouquin passé en param */
DECLARE
    livre_ref Livres.refl%TYPE;
    moy number;
BEGIN
    SELECT AVG(note) INTO moy FROM Avis WHERE refl = livre_ref;
    UPDATE Livres SET note_moy = moy WHERE refl = livre_ref;
END;


DECLARE
    CURSOR C1 IS 
    	   SELECT refl FROM Livres;
BEGIN
    FOR livre_ref in C1 LOOP
    	/* use above bloc */
    END LOOP;
END;


/* Same as a procedure */
CREATE OR REPLACE PROCEDURE calcul_moyenne (livre_ref Livres.refl%TYPE) 
IS
DECLARE
    moy number;
BEGIN
    SELECT AVG(note) INTO moy FROM Avis WHERE refl = livre_ref GROUP BY refl;
    UPDATE Livres SET note_moy = moy WHERE refl = livre_ref;
END;/

CREATE OR REPLACE PROCEDURE calcul_moyennes IS
DECLARE
    CURSOR C1 IS
    	   SELECT refl FROM Livres;
BEGIN 
      FOR r in C1 LOOP
      	  calcul_moyenne(r);
      END LOOP;
END;/



/* Trigger maj moyenne */
CREATE OR REPLACE TRIGGER maj_note_moy
AFTER INSERT OR UPDATE OR DELETE
OF note 
ON Avis
FOR EACH ROW
BEGIN
    calcul_moyenne(:new.refl);
END;/




/* Coherence avis-achat */
CREATE OR REPLACE TRIGGER donne_avis
INSTEAD OF INSERT ON AVIS
FOR EACH ROW
DECLARE
    nb number;
BEGIN
    SELECT COUNT (x) INTO nb FROM Achats WHERE idcl = :new.idcl AND refl = :new.refl;
    IF (nb=0) THEN
       RAISE pas_achete;
    ELSE
	INSERT INTO Avis VALUES(:new.idcl,:new.refl,:new.note,:new.commentaire);
    END IF;
    EXCEPTION
	WHEN pas_achete THEN
	     DBMS_OUTPUT.PUT_LINE('Livre pas achete');
END;/