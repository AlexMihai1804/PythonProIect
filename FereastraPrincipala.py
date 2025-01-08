from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout, QScrollArea, QPushButton, QLabel,
                             QHBoxLayout)

from CardLista import CardLista
from FereastraDetalii import FereastraDetalii


class FereastraPrincipala(QMainWindow):  # crearea ferestrei principale a aplicatiei
    def __init__(self, stocare, parent=None):  # constructorul clasei
        super().__init__(parent)  # apelarea constructorului clasei parinte
        self.stocare = stocare  # initializarea atributului de tip StocareListe
        self.setWindowTitle("Liste de Cumpărături")  # setarea titlului ferestrei
        self.resize(800, 600)  # setarea dimensiunilor ferestrei
        mainWidget = QWidget()  # crearea unui widget principal
        self.setCentralWidget(mainWidget)  # setarea widget-ului principal al ferestrei
        mainLayout = QVBoxLayout(mainWidget)  # crearea unui layout vertical pentru widget-ul principal
        self.butonNou = QPushButton("Adaugă listă nouă")  # crearea unui buton pentru adaugarea unei liste noi
        self.butonNou.setFixedHeight(40)  # setarea inaltimii butonului
        self.butonNou.setStyleSheet("font-size: 14px; font-weight: bold;")  # setarea stilului butonului
        self.butonNou.clicked.connect(
            self.adaugaListaNoua)  # conectarea semnalului de apasare a butonului la metoda de adaugare a unei liste noi
        mainLayout.addWidget(self.butonNou,
                             alignment=Qt.AlignmentFlag.AlignLeft)  # adaugarea butonului in layout-ul principal

        layoutStatistici = QHBoxLayout()  # crearea unui layout orizontal pentru afisarea statisticilor
        self.textNrListe = QLabel()  # crearea unui label pentru afisarea numarului de liste
        self.textNrProduse = QLabel()  # crearea unui label pentru afisarea numarului de produse
        self.textTotalBani = QLabel()  # crearea unui label pentru afisarea totalului de bani
        self.textNrListe.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #333;")  # setarea stilului label-ului pentru numarul de liste
        self.textNrProduse.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #333;")  # setarea stilului label-ului pentru numarul de produse
        self.textTotalBani.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #007B00;")  # setarea stilului label-ului pentru totalul de bani
        layoutStatistici.addWidget(self.textNrListe)  # adaugarea label-ului pentru numarul de liste in layout
        layoutStatistici.addWidget(self.textNrProduse)  # adaugarea label-ului pentru numarul de produse in layout
        layoutStatistici.addWidget(self.textTotalBani)  # adaugarea label-ului pentru totalul de bani in layout
        mainLayout.addLayout(layoutStatistici)  # adaugarea layout-ului de statistici in layout-ul principal

        self.zonaScroll = QScrollArea()  # crearea unei zone de scroll
        self.zonaScroll.setWidgetResizable(True)  # setarea redimensionarii continutului
        mainLayout.addWidget(self.zonaScroll)  # adaugarea zonei de scroll in layout-ul principal

        self.gridWidget = QWidget()  # crearea unui widget pentru continutul zonei de scroll
        self.gridLayout = QGridLayout(self.gridWidget)  # crearea unui layout de tip grid pentru widget-ul de continut
        self.gridLayout.setSpacing(15)  # setarea spatiului intre elemente
        self.gridLayout.setContentsMargins(20, 20, 20, 20)  # setarea marginilor layout-ului
        self.gridLayout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  # setarea alinierii elementelor
        self.zonaScroll.setWidget(self.gridWidget)  # setarea widget-ului continutului zonei de scroll

        self.incarcaListe()  # incarcarea listelor de cumparaturi

    def incarcaListe(self):  # metoda pentru incarcarea listelor de cumparaturi
        while self.gridLayout.count():  # cat timp exista elemente in layout
            item = self.gridLayout.takeAt(0)  # se ia primul element
            widget = item.widget()  # se preia widget-ul
            if widget:  # daca widget-ul exista
                widget.deleteLater()  # se sterge widget-ul
        liste = self.stocare.listeCumparaturi  # preluarea listelor de cumparaturi
        nrListe = len(liste)  # calcularea numarului de liste
        nrProduseTotal = 0  # initializarea numarului total de produse
        totalBani = 0.0  # initializarea totalului de bani
        cardWidth = 220  # setarea latimii card-ului
        spacing = 15  # setarea spatiului intre card-uri
        availableWidth = self.zonaScroll.viewport().width()  # preluarea latimii disponibile
        if cardWidth + spacing == 0:  # daca latimea card-ului si spatiul intre card-uri sunt 0
            coloane = 1  # se seteaza numarul de coloane la 1
        else:  # altfel
            coloane = max(1, (availableWidth + spacing) // (cardWidth + spacing))  # se calculeaza numarul de coloane
        rand = 0  # initializarea randului
        coloana = 0  # initializarea coloanei
        for lista in liste:  # pentru fiecare lista
            totalLista = 0.0  # initializarea totalului listei
            nrProduseTotal += len(
                lista['produse'])  # adaugarea numarului de produse din lista la numarul total de produse
            for produs in lista['produse']:  # pentru fiecare produs din lista
                totalLista += produs['cantitate'] * produs['pret']  # se adauga valoarea produsului la totalul listei
            totalBani += totalLista  # se adauga totalul listei la totalul de bani
            card = CardLista(lista, totalLista)  # crearea unui card pentru lista
            card.dateSchimbate.connect(
                self.peListaDateSchimbate)  # conectarea semnalului de date schimbate la metoda de prelucrare a listei
            card.dubluClick.connect(
                self.deschideDetalii)  # conectarea semnalului de dublu click la metoda de deschidere a detaliilor
            card.stergereSolicitata.connect(
                self.stergeLista)  # conectarea semnalului de stergere solicitata la metoda de stergere a listei
            self.gridLayout.addWidget(card, rand, coloana)  # adaugarea card-ului in layout
            coloana += 1  # incrementarea coloanei
            if coloana >= coloane:  # daca s-a ajuns la numarul de coloane
                coloana = 0  # se reseteaza coloana
                rand += 1  # se trece la randul urmator
        self.textNrListe.setText(f"Liste: {nrListe}")  # setarea textului pentru numarul de liste
        self.textNrProduse.setText(
            f"Produse total: {nrProduseTotal}")  # setarea textului pentru numarul total de produse
        self.textTotalBani.setText(f"Total bani: {totalBani:.2f} RON")  # setarea textului pentru totalul de bani

    def peListaDateSchimbate(self,
                             listaModificata):  # metoda pentru prelucrarea listei dupa ce aceasta a fost modificata
        for i, lista in enumerate(self.stocare.listeCumparaturi):  # pentru fiecare lista
            if lista['idLista'] == listaModificata[
                'idLista']:  # daca id-ul listei este acelasi cu id-ul listei modificate
                self.stocare.listeCumparaturi[i] = listaModificata  # se inlocuieste lista veche cu lista modificata
                break  # se iese din bucla
        self.stocare.salveazaDate()  # se salveaza datele
        self.incarcaListe()  # se reincarca listele

    def deschideDetalii(self, lista):  # metoda pentru deschiderea detaliilor unei liste
        self.fereastraDetalii = FereastraDetalii(self.stocare, lista, self)  # crearea ferestrei de detalii
        self.fereastraDetalii.dateModificate.connect(
            self.incarcaListe)  # conectarea semnalului de date modificate la metoda de reincarcare a listelor
        self.fereastraDetalii.show()  # afisarea ferestrei

    def adaugaListaNoua(self):  # metoda pentru adaugarea unei liste noi
        from PyQt6.QtWidgets import QInputDialog  # importarea clasei QInputDialog
        titlu, ok = QInputDialog.getText(self, "Listă nouă",
                                         "Nume listă:")  # afisarea unui dialog pentru introducerea numelui listei
        if ok and titlu.strip():  # daca s-a dat OK si numele listei nu este gol
            idNou = 0  # initializarea id-ului listei noi
            for lista in self.stocare.listeCumparaturi:  # pentru fiecare lista
                idNou = max(idNou, lista['idLista'])  # se alege id-ul maxim
            idNou += 1  # se incrementeaza id-ul
            listaNoua = {  # crearea listei noi
                'idLista': idNou,  # setarea id-ului listei
                'nume': titlu.strip(),  # setarea numelui listei
                'produse': []  # initializarea listei de produse
            }
            self.stocare.listeCumparaturi.append(listaNoua)  # adaugarea listei noi in lista de cumparaturi
            self.stocare.salveazaDate()  # salvarea datelor
            self.incarcaListe()  # reincarcarea listelor

    def resizeEvent(self, event: QResizeEvent):  # metoda pentru redimensionarea ferestrei
        super().resizeEvent(event)  # apelarea metodei din clasa parinte
        self.incarcaListe()  # reincarcarea listelor

    def closeEvent(self, event):  # metoda pentru inchiderea ferestrei
        self.stocare.salveazaDate()  # salvarea datelor
        super().closeEvent(event)  # apelarea metodei din clasa parinte

    def stergeLista(self, idLista):  # metoda pentru stergerea unei liste
        for i, lista in enumerate(self.stocare.listeCumparaturi):  # pentru fiecare lista
            if lista['idLista'] == idLista:  # daca id-ul listei este acelasi cu id-ul listei de sters
                self.stocare.listeCumparaturi.pop(i)  # se sterge lista
                break  # se iese din bucla
        self.stocare.salveazaDate()  # se salveaza datele
        self.incarcaListe()  # se reincarca listele
