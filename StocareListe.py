import pandas as pd  # importa biblioteca pandas


class StocareListe:
    def __init__(self):
        self.listeCumparaturi = []  # initializeaza lista de cumparaturi
        self.incarcaDate()  # incarca datele

    def incarcaDate(self):
        try:  # incearca sa incarce lista de cumparaturi
            dfListe = pd.read_csv("Liste.csv")  # incarca lista de cumparaturi din fisierul Liste.csv
        except FileNotFoundError:  # daca fisierul nu exista, initializeaza lista de cumparaturi
            self.listeCumparaturi = []  # initializeaza lista de cumparaturi ca fiind goala
            return  # iese din functie
        try:  # incearca sa incarce produsele
            dfProduse = pd.read_csv("Produse.csv")  # incarca produsele din fisierul Produse.csv
        except FileNotFoundError:  # daca fisierul nu exista, initializeaza lista de cumparaturi
            dfProduse = pd.DataFrame(columns=["idProdus", "idLista", "numeProdus", "cantitate", "pret",
                                              "cumprat"])  # initializeaza un dataframe gol
        for _, rand in dfListe.iterrows():  # pentru fiecare lista, adauga produsele
            lista = {  # creeaza lista
                'idLista': rand['idLista'],  # adauga id-ul listei
                'nume': rand['nume'],  # adauga numele listei
                'produse': []  # adauga produsele listei, initial o lista goala
            }
            dfProdListei = dfProduse[dfProduse['idLista'] == rand['idLista']]  # selecteaza produsele din lista
            for _, randProdus in dfProdListei.iterrows():  # pentru fiecare produs, il adauga in lista
                produs = {  # creeaza produsul
                    'idProdus': randProdus['idProdus'],  # adauga id-ul produsului
                    'numeProdus': randProdus['numeProdus'],  # adauga numele produsului
                    'cantitate': int(randProdus['cantitate']),  # adauga cantitatea produsului
                    'pret': float(randProdus['pret']),  # adauga pretul produsului
                    'cumprat': bool(randProdus['cumprat'])  # adauga starea de cumparare a produsului
                }
                lista['produse'].append(produs)  # adauga produsul in lista
            self.listeCumparaturi.append(lista)  # adauga lista in lista de cumparaturi

    def salveazaDate(self):
        liste = []  # creeaza lista de liste, pentru a salva in fisier
        produse = []  # creeaza lista de produse, pentru a salva in fisier
        for lista in self.listeCumparaturi:  # pentru fiecare lista, adauga produsele
            liste.append({  # adauga lista
                'idLista': lista['idLista'],  # adauga id-ul listei
                'nume': lista['nume']  # adauga numele listei
            })
            for produs in lista['produse']:  # pentru fiecare produs din lista, il adauga
                produse.append({  # adauga produsul
                    'idLista': lista['idLista'],  # adauga id-ul listei
                    'idProdus': produs['idProdus'],  # adauga id-ul produsului
                    'numeProdus': produs['numeProdus'],  # adauga numele produsului
                    'cantitate': produs['cantitate'],  # adauga cantitatea produsului
                    'pret': produs['pret'],  # adauga pretul produsului
                    'cumprat': produs['cumprat']  # adauga starea de cumparare a produsului
                })
        if len(liste) == 0:  # daca nu exista liste, nu salva nimic
            return  # iese din functie
        dfListe = pd.DataFrame(liste)  # creeaza un dataframe cu listele
        dfProduse = pd.DataFrame(produse)  # creeaza un dataframe cu produsele
        dfListe.to_csv("Liste.csv", index=False)  # salveaza listele in fisierul Liste.csv
        dfProduse.to_csv("Produse.csv", index=False)  # salveaza produsele in fisierul Produse.csv
