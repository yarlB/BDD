R=["ID_Adresse","ID_Femme","ID_Enfant","ID_Contact","ID_Hebergement","Date_SP","Date_Ress","Description_Ress","Date_SM","Numero","Date_Emmenagement","Date_Demenagement","Description_O","TOUT_femme","TOUT_adresse","TOUT_enfant","TOUT_hebergement","TOUT_habite","TOUT_demande_hebergement","TOUT_orientation","TOUT_SP","TOUT_ress","TOUT_SM","TOUT_TP"]

DF=[
    [["ID_Femme"],["TOUT_femme"]],
    [["ID_Enfant"],["ID_Femme","TOUT_enfant"]],
    [["ID_Adresse"],["TOUT_adresse"]],
    [["ID_Hebergement"],["ID_Adresse","TOUT_hebergement"]],
    [["ID_Femme","ID_Adresse","Date_Emmenagement","Date_Demenagement","ID_Enfant"],["TOUT_habite"]],
    [["ID_Femme","ID_Enfant","ID_Hebergement"],["TOUT_demande_hebergement"]],
    [["ID_Femme","Description_O"],["TOUT_orientation"]],
    [["ID_Femme","Date_SP"],["TOUT_SP"]],
    [["ID_Femme","Date_Ress","Description_Ress"],["TOUT_ress"]],
    [["ID_Femme","Date_SM"],["TOUT_SM"]],
    [["ID_Femme","Numero"],["TOUT_TP"]]
]

from normalisation_v2 import *

print_rels_and_fds(BCNF(R,DF))
