from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLineEdit, QCheckBox, QLabel, QPushButton)


class CardProdus(QWidget):  # clasa pentru cardul unui produs
    dateSchimbate = pyqtSignal(dict)  # semnal pentru schimbarea datelor
    stergereSolicitata = pyqtSignal(int)  # semnal pentru stergerea unui produs

    def __init__(self, produs, parent=None):  # constructorul clasei
        super().__init__(parent)  # apelarea constructorului clasei parinte
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)  # setarea atributului pentru fundal
        self.produs = produs  # setarea produsului
        self.eInModEditare = False  # setarea modului de editare
        self.configureazaUI()  # configurarea interfetei
        self.actualizeazaFundal()  # actualizarea fundalului

    def configureazaUI(self):  # metoda pentru configurarea interfetei
        self.setFixedHeight(50)  # setarea inaltimii
        self.setStyleSheet(""" 
            background-color: #FAFAFA;
            border: 1px solid #CCC;
            border-radius: 5px;
        """)  # setarea stilului pentru fundal
        mainLayout = QHBoxLayout(self)  # crearea unui layout de tip orizontal
        mainLayout.setContentsMargins(10, 5, 10, 5)  # setarea marginilor
        mainLayout.setSpacing(10)  # setarea spatiului intre elemente

        self.checkCumparat = QCheckBox()  # crearea unui checkbox pentru starea de cumparare
        self.checkCumparat.setChecked(self.produs['cumprat'])  # setarea starii de cumparare
        self.checkCumparat.toggled.connect(self.cumparatToggle)  # conectarea semnalului de schimbare a starii la metoda
        mainLayout.addWidget(self.checkCumparat)  # adaugarea checkbox-ului in layout

        self.textCantitate = QLineEdit(str(self.produs['cantitate']))  # crearea unui camp de editare pentru cantitate
        self.textCantitate.setReadOnly(True)  # setarea campului ca fiind doar pentru citire
        self.textCantitate.setFixedWidth(60)  # setarea latimii campului
        mainLayout.addWidget(self.textCantitate)  # adaugarea campului in layout

        self.textNume = QLineEdit(self.produs['numeProdus'])  # crearea unui camp de editare pentru nume
        self.textNume.setReadOnly(True)  # setarea campului ca fiind doar pentru citire
        mainLayout.addWidget(self.textNume)  # adaugarea campului in layout

        self.textPret = QLineEdit(str(self.produs['pret']))  # crearea unui camp de editare pentru pret
        self.textPret.setReadOnly(True)  # setarea campului ca fiind doar pentru citire
        self.textPret.setFixedWidth(70)  # setarea latimii campului
        mainLayout.addWidget(self.textPret)  # adaugarea campului in layout

        self.textPretTotal = QLabel(self.calculeazaTotal())  # crearea unui label pentru pretul total
        self.textPretTotal.setAlignment(Qt.AlignmentFlag.AlignCenter)  # alinierea textului la centru
        self.textPretTotal.setStyleSheet("color: #007B00; font-weight: bold;")  # setarea stilului pentru text
        self.textPretTotal.setFixedWidth(70)  # setarea latimii label-ului
        mainLayout.addWidget(self.textPretTotal)  # adaugarea label-ului in layout

        self.butonSterge = QPushButton()  # crearea unui buton pentru stergerea produsului
        self.butonSterge.setFixedSize(24, 24)  # setarea dimensiunilor butonului
        self.butonSterge.setText("X")  # setarea textului butonului
        self.butonSterge.setStyleSheet("border: none;")  # setarea stilului pentru buton
        self.butonSterge.clicked.connect(self.stergeProdus)  # conectarea semnalului de apasare a butonului la metoda
        mainLayout.addWidget(self.butonSterge)  # adaugarea butonului in layout

    def mouseDoubleClickEvent(self, event):  # metoda pentru evenimentul de dublu click
        if event.button() == Qt.MouseButton.LeftButton:  # daca butonul apasat este stanga
            self.toggleModEditare()  # apeleaza metoda pentru schimbarea modului de editare
        super().mouseDoubleClickEvent(event)  # apelarea metodei din clasa parinte

    def toggleModEditare(self):  # metoda pentru schimbarea modului de editare
        self.eInModEditare = not self.eInModEditare  # schimbarea modului de editare
        self.textNume.setReadOnly(not self.eInModEditare)  # setarea campului de editare pentru nume
        self.textCantitate.setReadOnly(not self.eInModEditare)  # setarea campului de editare pentru cantitate
        self.textPret.setReadOnly(not self.eInModEditare)  # setarea campului de editare pentru pret
        if not self.eInModEditare:  # daca nu este in modul de editare
            self.salveazaModificari()  # salveaza modificarile
        if self.eInModEditare:  # daca este in modul de editare
            self.setStyleSheet("""
                background-color: #FFF7E6; /* un galben pal */
                border: 1px solid #FFA500;
                border-radius: 5px;
            """)  # setarea stilului pentru fundal
        else:
            self.actualizeazaFundal()  # actualizeaza fundalul

    def salveazaModificari(self):  # metoda pentru salvarea modificarilor
        try:  # incearca sa preia datele
            self.produs['numeProdus'] = self.textNume.text().strip()  # preia numele produsului
            self.produs['cantitate'] = float(self.textCantitate.text())  # preia cantitatea produsului
            self.produs['pret'] = float(self.textPret.text())  # preia pretul produsului
        except ValueError:  # daca apare o eroare
            pass  # ignora eroarea
        self.textPretTotal.setText(self.calculeazaTotal())  # actualizeaza pretul total
        self.dateSchimbate.emit(self.produs)  # emite semnalul pentru schimbarea datelor

    def cumparatToggle(self, checked):  # metoda pentru schimbarea starii de cumparare
        self.produs['cumprat'] = checked  # setarea starii de cumparare
        self.dateSchimbate.emit(self.produs)  # emite semnalul pentru schimbarea datelor
        self.actualizeazaFundal()  # actualizeaza fundalul

    def stergeProdus(self):  # metoda pentru stergerea produsului
        self.stergereSolicitata.emit(self.produs['idProdus'])  # emite semnalul pentru stergerea produsului

    def calculeazaTotal(self) -> str:  # metoda pentru calcularea pretului total
        totalVal = self.produs['cantitate'] * self.produs['pret']  # calculeaza pretul total
        return f"{totalVal:.2f}"  # returneaza valoarea totala formata ca string

    def actualizeazaFundal(self):  # metoda pentru actualizarea fundalului
        if self.produs['cumprat']:  # daca produsul este cumparat
            self.setStyleSheet(""" 
                background-color: #CCE8CC; /* verde deschis */
                border: 1px solid #CCC;
                border-radius: 5px;
            """)  # setarea stilului pentru fundal
        else:  # daca produsul nu este cumparat
            self.setStyleSheet("""
                background-color: #FAFAFA;
                border: 1px solid #CCC;
                border-radius: 5px;
            """)  # setarea stilului pentru fundal
