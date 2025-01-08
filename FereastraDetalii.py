from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout, QScrollArea, QMessageBox, QLabel,
                             QPushButton, QHBoxLayout)

from CardProdus import CardProdus
from DialogAdaugareProdus import DialogAdaugaProdus


class FereastraDetalii(QMainWindow):  # cream o clasa FereastraDetalii care mosteneste QMainWindow
    dateModificate = pyqtSignal()  # semnal pentru date modificate

    def __init__(self, stocare, lista, parent=None):  # definim constructorul clasei
        super().__init__(parent)  # apelam constructorul clasei parinte
        self.stocare = stocare  # setam stocarea
        self.lista = lista  # setam lista
        self.setWindowTitle(f"Detalii pentru {self.lista['nume']}")  # setam titlul ferestrei
        self.resize(800, 600)  # setam dimensiunile ferestrei
        mainWidget = QWidget()  # cream un widget principal
        self.setCentralWidget(mainWidget)  # setam widget-ul principal
        mainLayout = QVBoxLayout(mainWidget)  # cream un layout vertical pentru widget-ul principal
        detaliiLayout = QHBoxLayout()  # cream un layout orizontal pentru detalii
        self.textTitlu = QPushButton(f"Lista: {self.lista['nume']}")  # cream un buton pentru titlu
        self.textTitlu.setStyleSheet("font-size: 18px; font-weight: bold;")  # stilizam butonul
        self.textTitlu.setFlat(True)  # setam butonul sa nu aiba efect de apasare
        self.textTitlu.setEnabled(False)  # setam butonul sa fie dezactivat
        detaliiLayout.addWidget(self.textTitlu, alignment=Qt.AlignmentFlag.AlignLeft)  # adaugam butonul in layout

        self.butonAdauga = QPushButton("Adaugă Produs")  # cream un buton pentru adaugare produs
        self.butonAdauga.setFixedHeight(35)  # setam inaltimea butonului
        self.butonAdauga.setStyleSheet("font-size: 14px; font-weight: bold;")  # stilizam butonul
        self.butonAdauga.clicked.connect(
            self.adaugaProdus)  # conectam semnalul de apasare a butonului la metoda adaugaProdus
        detaliiLayout.addWidget(self.butonAdauga, alignment=Qt.AlignmentFlag.AlignLeft)  # adaugam butonul in layout

        self.textTotal = QPushButton("")  # cream un buton pentru afisarea totalului
        self.textTotal.setStyleSheet("font-size: 16px; font-weight: bold; color: #007B00;")  # stilizam butonul
        self.textTotal.setFlat(True)  # setam butonul sa nu aiba efect de apasare
        self.textTotal.setEnabled(False)  # setam butonul sa fie dezactivat
        detaliiLayout.addWidget(self.textTotal,
                                alignment=Qt.AlignmentFlag.AlignRight)  # adaugam butonul in layout principal la dreapta

        mainLayout.addLayout(detaliiLayout)  # adaugam layout-ul de detalii in layout-ul principal

        statisticiLayout = QHBoxLayout()  # cream un layout orizontal pentru statistici

        self.textNumarProduse = QLabel()  # cream un label pentru numarul de produse
        self.textNumarProduse.setStyleSheet("font-size: 12px; font-weight: bold; color: #333;")  # stilizam label-ul
        statisticiLayout.addWidget(self.textNumarProduse)  # adaugam label-ul in layout

        self.textProduseDeCumparat = QLabel()  # cream un label pentru produsele de cumparat
        self.textProduseDeCumparat.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #333;")  # stilizam label-ul
        statisticiLayout.addWidget(self.textProduseDeCumparat)  # adaugam label-ul in layout

        self.textTotalRamas = QLabel()  # cream un label pentru totalul ramas
        self.textTotalRamas.setStyleSheet("font-size: 12px; font-weight: bold; color: #333;")  # stilizam label-ul
        statisticiLayout.addWidget(self.textTotalRamas)  # adaugam label-ul in layout

        mainLayout.addLayout(statisticiLayout)  # adaugam layout-ul de statistici in layout-ul principal

        self.zonaScroll = QScrollArea()  # cream o zona de scroll
        self.zonaScroll.setWidgetResizable(True)  # setam zona de scroll sa fie redimensionabila
        mainLayout.addWidget(self.zonaScroll)  # adaugam zona de scroll in layout-ul principal

        self.gridWidget = QWidget()  # cream un widget pentru grid
        self.gridLayout = QGridLayout(self.gridWidget)  # cream un layout de tip grid pentru widget
        self.gridLayout.setSpacing(5)  # setam spatierea intre elemente
        self.gridLayout.setContentsMargins(10, 10, 10, 10)  # setam marginile layout-ului
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)  # aliniem layout-ul in partea de sus
        self.zonaScroll.setWidget(self.gridWidget)  # setam widget-ul pentru zona de scroll

        self.actualizeazaProduse()  # apelam metoda pentru actualizarea produselor

    def actualizeazaProduse(self):
        while self.gridLayout.count():  # cat timp exista elemente in grid
            item = self.gridLayout.takeAt(0)  # scoatem elementul de pe pozitia 0
            widget = item.widget()  # luam widget-ul
            if widget:  # daca exista widget
                widget.deleteLater()  # il stergem
        produse = self.lista['produse']  # luam produsele din lista
        rand = 0  # initializam randul cu 0
        for produs in produse:  # pentru fiecare produs din lista
            card = CardProdus(produs)  # cream un card pentru produs
            card.dateSchimbate.connect(
                self.schimbareDate)  # conectam semnalul de schimbare date la metoda schimbareDate
            card.stergereSolicitata.connect(
                self.stergeProdus)  # conectam semnalul de stergere solicitata la metoda stergeProdus
            self.gridLayout.addWidget(card, rand, 0)  # adaugam card-ul in grid la randul rand si coloana 0
            rand += 1  # incrementam randul
        self.actualizeazaStatistici()  # apelam metoda pentru actualizarea statisticii

    def actualizeazaStatistici(self):
        produse = self.lista['produse']  # luam produsele din lista
        nrProduse = len(produse)  # numaram produsele
        nrDeCumparat = sum(1 for p in produse if not p['cumprat'])  # numaram produsele de cumparat
        totalAll = sum(p['cantitate'] * p['pret'] for p in produse)  # calculam totalul general
        totalNecumparat = sum(p['cantitate'] * p['pret'] for p in produse if not p['cumprat'])  # calculam totalul ramas
        self.textNumarProduse.setText(f"Nr. produse: {nrProduse}")  # setam textul pentru numarul de produse
        self.textProduseDeCumparat.setText(f"De cumpărat: {nrDeCumparat}")  # setam textul pentru produsele de cumparat
        self.textTotalRamas.setText(f"Rămas: {totalNecumparat:.2f} RON")  # setam textul pentru totalul ramas
        self.textTotal.setText(f"Total General: {totalAll:.2f} RON")  # setam textul pentru totalul general

    def schimbareDate(self, produsModificat):
        self.actualizeazaListaInStocare()  # actualizam lista in stocare
        self.dateModificate.emit()  # emitem semnalul de date modificate
        self.actualizeazaProduse()  # actualizam produsele

    def stergeProdus(self, idProdus):
        confirmare = QMessageBox.question(  # afisam o fereastra de confirmare
            self,  # parintele ferestrei
            "Confirmare Ștergere",  # titlul ferestrei
            "Ești sigur că dorești să ștergi acest produs?",  # mesajul ferestrei
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No  # butoanele ferestrei (Da si Nu)
        )
        if confirmare == QMessageBox.StandardButton.Yes:  # daca s-a apasat butonul Da
            for produs in self.lista['produse']:  # iteram prin produsele din lista
                if produs['idProdus'] == idProdus:  # daca id-ul produsului este cel cautat
                    self.lista['produse'].remove(produs)  # stergem produsul
                    break  # iesim din bucla
            self.actualizeazaListaInStocare()  # actualizam lista in stocare
            self.dateModificate.emit()  # emitem semnalul de date modificate
            self.actualizeazaProduse()  # actualizam produsele

    def actualizeazaListaInStocare(self):  # metoda pentru actualizarea listei in stocare
        for i, lista in enumerate(self.stocare.listeCumparaturi):  # iteram prin listele de cumparaturi
            if lista['idLista'] == self.lista['idLista']:  # daca id-ul listei este cel cautat
                self.stocare.listeCumparaturi[i] = self.lista  # actualizam lista
                break  # iesim din bucla
        self.stocare.salveazaDate()  # salvam datele

    def adaugaProdus(self):  # metoda pentru adaugarea unui produs
        dialog = DialogAdaugaProdus(self)  # cream un dialog pentru adaugarea unui produs
        rezultat = dialog.exec()  # afisam dialogul
        if rezultat == dialog.DialogCode.Accepted:  # daca s-a apasat butonul de acceptare
            nume, cantitate, pret = dialog.getData()  # luam datele din dialog
            if nume:  # daca numele este valid
                if not self.lista['produse']:  # daca lista de produse este goala
                    idProdusNou = 1  # setam id-ul produsului nou la 1
                else:  # altfel
                    idProdusNou = max(p['idProdus'] for p in self.lista[
                        'produse']) + 1  # setam id-ul produsului nou la maximul id-urilor existente + 1
                produsNou = {  # cream un produs nou
                    'idProdus': idProdusNou,  # setam id-ul produsului
                    'numeProdus': nume,  # setam numele produsului
                    'cantitate': cantitate,  # setam cantitatea produsului
                    'pret': pret,  # setam pretul produsului
                    'cumprat': False  # setam starea de cumparare a produsului
                }
                self.lista['produse'].append(produsNou)  # adaugam produsul nou in lista
                self.actualizeazaListaInStocare()  # actualizam lista in stocare
                self.dateModificate.emit()  # emitem semnalul de date modificate
                self.actualizeazaProduse()  # actualizam produsele

    def closeEvent(self, event):  # metoda pentru inchiderea ferestrei
        self.actualizeazaListaInStocare()  # actualizam lista in stocare
        super().closeEvent(event)  # apelam metoda de inchidere a ferestrei parinte
