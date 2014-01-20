'''
Copyright 2014 Yarl BAUDIG 

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Personal note : you can share it, correct it (it needs this) ,
modify it (make it better, it can obviously be), erase it, give it a smart and
elegant way to register attributes and FDs, vomit, etc.

Remember, It's a beta (cuz I am), please share BUGS
yarl@sdf.org

'''
#DF is "Dependence Fonctionnelle", I'm a native french and I forgot to write FD then codingly speaking, all fds are written DF, or df, or something..
#[['A','B'],['C','D']] is code for A,B-->C,D


#Gives 2^A
#
#input:
#A : list of attributes
#
#output:
#U : set of frozensets of attributes
def P(A):
    A=frozenset(A)
    if not A:
        return set([frozenset()])
    U=set([A])
    for x in A:
        U = U | P(A-frozenset([x]))
    return U


#Gives X closure
#
#inputs:
#X : list of attributes
#DF list of FD (A FD is a list of 2 lists of attributes)
#
#output:
#X_plus : a set of attributes
def att_closure(X,DF):
    X_plus = set(X)
    change = True
    while change:
        change = False
        for df in DF:
            if set(df[0]) <= X_plus and not set(df[1]) <= X_plus:
                X_plus = X_plus | set(df[1])
                change = True
    return X_plus


#Elementarises dfs (ie {X->YZ} becomes {X->Y, X->Z}
#
#input:
#DF : list of FD
#
#output:
#list of FD elementarised
def elementarise(DF):
    if DF:
        return [[DF[0][0],[Y]] for Y in DF[0][1]]+DF[1:]
    return []
        

#Computes for each df X->Y a minimal X' subset of X such that X''s closure contains Y
#
#inputs:
#ALL_DF : list of FD (because this works by emptying DF, this need to keep ALL the FDs)
#DF : same list as above at first call
#
#output:
#list of FD superfloues-erased
def eraseSuperfloues(ALL_DF,DF):
    if DF:
        df=DF[0]
        puiss=P(df[0])
        for size in range(1,len(df[0])):
            for X in [X for X in puiss if len(X)==size]:
                if set(df[1]) <= set(att_closure(X,ALL_DF)):
                    return [[list(X),df[1]]] + eraseSuperfloues(ALL_DF,DF[1:])
        else:
            return [df] + eraseSuperfloues(ALL_DF,DF[1:])
    return []


#Free your mind and your ass will follow
#
#inputs:
#ALL_DF : same idea as in eraseSuperfloues but this time non-needed FDs ain't keeped
#DF : list of FDs..
#
#output:
#list of DF where redundancies have been eradicated
def eradicateRedundancies(ALL_DF,DF):
    if DF:
        df=DF[0]
        ALL_DF_MINUS_df = ALL_DF[1:]
        if set(df[1]) <= att_closure(df[0], set([(frozenset(dfi[0]),frozenset(dfi[1])) for dfi in ALL_DF_MINUS_df])):
            return eradicateRedundancies(ALL_DF_MINUS_df,DF[1:])
        else:
            return [df] + eradicateRedundancies(ALL_DF_MINUS_df,DF[1:])
    return []


#Given a list of DF, gives the minimal cover.
def CV(DF):
    #elementarisation
    DF=elementarise(DF)
    #Superfloues Attributes erasation
    DF=eraseSuperfloues(DF,DF)
    #Redundancy eradication
    DF=eradicateRedundancies(DF, DF)
    return DF


#Computes all possible keys (and superkeys) for a list of attributes
#
#inputs:
#ATT : list
#DF : list
#
#output:
#set of keys (whose are frozensets)
def ALL_KEYS(ATT,DF):
    ATT=set(ATT)
    superset=P(ATT)
    KEYS=set()
    for A in superset:
        if A not in KEYS:
            A_plus = att_closure(A,DF)
            if A_plus == ATT:
                #Hihihi, be careful, se becomes es
                superESt = P(ATT-A)
                KEYS = KEYS | set([frozenset(A)|frozenset(p) for p in superESt]) # we need to add all superkeys from this one
    return KEYS


#Three next are one. Only one-depth is used ;P
def to_frozenset(L):
    if not L or type(L[0]) == str: # if depth 1
        return frozenset(L)
    return frozenset([to_frozenset(X) for X in L])

def back_to_list(L):
    if not L:
        return []
    x=set(L).pop()
    if type(x) == str: # if depth 1
        return list(L)
    return [back_to_list(X) for X in L]

#remove duplicates from a list (of lists if depth > 1) of str !!!CAN'T BE USE ON A LIST OF TYPINGLY SPEAKING NON EQUIVALENT THINGS!!!
def remove_duplicates(L):
    return back_to_list(to_frozenset(L))


#Returns a minimalest key if can, minimal_key if can't. If minimal_key is null, return the minimal possible key, can be att
def minimalest_key(KEYS,att,minimal_key):
    if minimal_key:
        for ksize in range(1,len(minimal_key)):#can we find a minimalest key?
            for K in [Ki for Ki in KEYS if len(Ki)==ksize]:
                if set(K) <= set(att):
                    return  K
    else:
        for ksize in range(1,len(att)+1):
            for K in [Ki for Ki in KEYS if len(Ki)==ksize]:
                if set(K) <= set(att):
                    return K
    return minimal_key

#Gives 3NF (or Bernstein) normalisation
#
#inputs:
#ATT : list of attributes
#DF list of FDs
#
#output:
#list of [Ri,FDi] where Ri's the i-th relation and FDi's her list of FDs
def THIRD_NF(ATT,DF):
    ATT=remove_duplicates(ATT) # WE DON'T USE remove_duplicates on DF car DF are ordered (ie X-->Y)
    DF = CV(DF) # DF become minimal cover
    KEYS = ALL_KEYS(ATT,DF) #We compute every keys (and superkeys)
    CV_PARTS = {}
    while DF: #FDs grouping
        df = DF[0]
        X=frozenset(df[0])
        Y=set(df[1])
        DF=DF[1:]
        if X in CV_PARTS:
            CV_PARTS[X].append(Y)
        else:
            CV_PARTS[X]=[Y]
    Relations = []
    minimal_key=[]
    for X in CV_PARTS: #Relations creation
        att = list(set([a for a in X]) | reduce(lambda x,y : x|y, CV_PARTS[X],set())) #I'm lazy right now (lary*)
        minimal_key=minimalest_key(KEYS,att,minimal_key)
        dfs = [[list(X),list(Y)] for Y in CV_PARTS[X]] 
        Relations.append([att,dfs])
    if not minimal_key:
        Relations.append([list(minimalest_key(KEYS,ATT,minimal_key)),[]])
    R_COPY=Relations
    Relations=[]
    while R_COPY:
        R=R_COPY[0]
        R_COPY=R_COPY[1:]
        for x in R_COPY+Relations:
            if set(R[0]) <= set(x[0]):
                break
        else:
            Relations.append(R)
    return Relations
    


#Return the first bad fd (for BCNF) found if any xor []
def BAD_DF(R,DF,KEYS):
    for df in DF:
        X=df[0]
        for K in KEYS:
            if K <= set(X):
                break
        else:
            return df
    return []


#Gives BCNF normalisation
#
#inputs:
#ATT : list of attributes
#DF list of FDs
#
#output:
#list of [Ri,FDi] where Ri's the i-th relation and FDi's her list of FDs
def BCNF(ATT,DF):
    ATT=remove_duplicates(ATT) # Fist uniquing things
    bad_relations = [[ATT,DF]]
    good_relations = []
    while bad_relations:
        R_DF = bad_relations[0]
        bad_relations = bad_relations[1:]
        R,DF = R_DF[0],R_DF[1]
        KEYS = ALL_KEYS(R,DF)
        bad_df = BAD_DF(R,DF,KEYS)
        if not bad_df: # If there are no bad fds for the relation, then the relation is BCNF
            good_relations.append(R_DF)
        else:
            att_new_relation = list(set(bad_df[0]) | set(bad_df[1]))
            dfs_new_relation = [df for df in DF if (set(df[0]) | set(df[1])) <= set(att_new_relation)]
            bad_relations.append([att_new_relation, dfs_new_relation])
            att_rest = list(set(R) - (set(bad_df[1]) - set(bad_df[0])))
            dfs_rest = [dfs for dfs in DF if (set(dfs[0]) | set(dfs[1])) <= set(att_rest)] #this is where we can lose fds
            bad_relations.append([att_rest,dfs_rest])
    return good_relations


def print_rels_and_fds(RDF):
    for rdf in RDF:
        print "Relation:"
        for a in rdf[0][:-1]:
            print "%s," % a,
        print rdf[0][-1]
        print "Functionnal dependancies:"
        for df in rdf[1]:
            for x in df[0][:-1]:
                print "%s," % x,
            print df[0][-1],
            print "-->",
            for y in df[1][:-1]:
                print "%s," % y,
            print df[1][-1]
        print ""


#R=["C","T","H","R","S","G"]
#DF=[
#    [
#        ["C"],["T"]
#    ],[
#        ["H","R"],["C"]
#    ],[
#        ["H","T"],["R"]
#    ],[
#        ["C","S"],["G"]
#    ],[
#        ["H","S"],["R"]
#    ]
#]
print """
Hey! That's an example of use:
R=["A","B","C","D","E"]
DF=[
    [
        ["A"],["B"]
    ],[
        ["A"],["C"]
    ],[
        ["C","D"],["E"]
    ],[
        ["B"],["D"]
    ]
]

print_rels_and_fds([[R,DF]])
print ""
print ""

D=BCNF(R,DF)
print "Finally, in BCNF:"
print_rels_and_fds(D)
print ""
print ""

D=THIRD_NF(R,DF)
print "Finally, in 3NF:"
print_rels_and_fds(D)
"""

R=["ID_Femme","ID_Adresse","ID_Hebergement","ID_Enfant","attributs_femme","attributs_enfant","attributs_hebergement","attributs_adresse"]

DF=[
    [["ID_Femme"],["attributs_femme"]],
    [["ID_Enfant"],["attributs_enfant","ID_Femme"]],
    [["ID_Hebergement"],["ID_adresse","attributs_hebergement"]],
    [["ID_adresse"],["attributs_adresse","ID_Hebergement"]]
]

D=BCNF(R,DF)
print "Finally, in BCNF:"
print_rels_and_fds(D)
print ""
print ""

D=THIRD_NF(R,DF)
print "Finally, in 3NF:"
print_rels_and_fds(D)
