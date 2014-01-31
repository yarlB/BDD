DROP TABLE Femme CASCADE CONSTRAINT
CREATE TABLE Femme (
       id_femme varchar2(20),
       nom varchar2(20),
       prenom varchar2(20),
       date_naissance date,
       nom_naissance varchar2(20),
       nationalite varchar2(20),
       origine_demande varchar2(20),
       PRIMARY KEY (id_femme)
);

DROP TABLE Adresse CASCADE CONSTRAINT
CREATE TABLE Adresse (
       id_adresse varchar2(20),
       adresse varchar2(20),
       complement_adresse varchar2(20),
       code_postal varchar2(20),
       ville varchar2(20),
       telephone varchar2(20),
       pays varchar2(20),
       description_a varchar2(20),
       PRIMARY KEY (id_adresse) 
);

DROP TABLE Demande_Hebergement CASCADE CONSTRAINT
CREATE TABLE Demande_Hebergement (
       id_hebergement varchar2(20),
       id_femme varchar2(20),
       id_adresse varchar2(20),
       date_demande date,
       type_hebergement varchar2(20),
       besoin_logement_adapte varchar2(20),
       date_reponse_positive date,
       PRIMARY KEY (id_femme, id_adresse, id_hebergement),
       FOREIGN KEY id_femme REFERENCES Femme(id_femme),
       FOREIGN KEY id_adresse REFERENCES Adresse(id_adresse)
); 

DROP TABLE Habite CASCADE CONSTRAINT
CREATE TABLE Habite (
       id_femme varchar2(20),
       id_adresse varchar2(20),
       date_emmenagement date,
       date_demenagement date,
       PRIMARY KEY (id_femme, id_adresse, date_emmenagement),
       FOREIGN KEY id_femme REFERENCES Femme(id_femme),
       FOREIGN KEY id_adresse REFERENCES Adresse(id_adresse)
);

DROP TABLE Enfant CASCADE CONSTRAINT
CREATE TABLE Enfant (
       id_enfant varchar2(20),
       id_femme varchar2(20),
       nom varchar2(20),
       prenom varchar2(20),
       sexe boolean, /* VRAI F; FAUX M */
       nationalite varchar2(20),
       scolarise boolean,
       date_naissance date,
       a_charge boolean,
       habite_avec_maman boolean
       PRIMARY KEY (id_enfant),
       FOREIGN KEY id_femme REFERENCES Femme(id_femme)
);

DROP TABLE Contact CASCADE CONSTRAINT
CREATE TABLE Contact (
       id_femme varchar2(20),
       id_contact varchar2(20),
       commentaires text,
       description varchar2(20),
       date_c date,
       PRIMARY KEY (id_femme, id_contact),
       FOREIGN KEY id femme REFERENCES Femme(id_femme)
); 

DROP TABLE Orientation CASCADE CONSTRAINT
CREATE TABLE Orientation (
       id_femme varchar2(20),
       description_o varchar2(20),
       PRIMARY KEY (id_femme, description_o),
       FOREIGN KEY id_femme REFERENCES Femme(id_femme)
);

DROP TABLE Situation_Professionnelle CASCADE CONSTRAINT
CREATE TABLE Situation_Professionnelle (
       id_femme varchar2(20),
       date_sp date,
       description varchar2(20)
       PRIMARY KEY (id_femme, date_sp),
       FOREIGN KEY id_femme REFERENCES Femme(id_femme)
);

DROP TABLE Ressources CASCADE CONSTRAINT
CREATE TABLE Ressources (
       id_femme varchar2(20),
       date_ress date,
       description_r varchar2(20),
       PRIMARY KEY (id_femme, date_ress, description_R),
       FOREIGN KEY id_femme REFERENCES Femme(id_femme) 
); 

DROP TABLE Situation_Maritale CASCADE CONSTRAINT
CREATE TABLE  Situation_Maritale (
       id_femme varchar2(20),
       date_sm date,
       description_sp varchar2(20),
       PRIMARY KEY (id_femme, date_sm),
       FOREIGN KEY id_femme REFERENCES Femme(id_femme)
);

DROP TABLE Telephone_Portable CASCADE CONSTRAINT
CREATE TABLE Telephone_Portable (
       id_femme varchar2(20),
       numero varchar2(10),
       date_tp date,
       PRIMARY KEY (id_femme,numero),
       FOREIGN KEY id_femme REFERENCES Femme(id_femme)
);     


/*prout*/
/*de mammouth*/
