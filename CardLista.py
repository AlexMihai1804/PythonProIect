from PyQt6.QtCore import pyqtSignal, Qt, QEvent
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton)


class CardLista(QWidget):
    dateSchimbate = pyqtSignal(dict)  # semnal pentru schimbarea datelor
    dubluClick = pyqtSignal(object)  # semnal pentru dublu click
    stergereSolicitata = pyqtSignal(int)  # semnal pentru stergerea unei liste

    def __init__(self, lista, total, parent=None):  # constructorul clasei
        super().__init__(parent)  # apelarea constructorului clasei parinte
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)  # setarea atributului pentru fundal
        self.lista = lista  # setarea listei
        self.total = total  # setarea totalului
        self.eInModEditare = False  # setarea modului de editare
        self.configureazaUI()  # configurarea interfetei
        self.actualizeazaCampuri()  # actualizarea campurilor
        self.textNume.installEventFilter(self)  # instalarea filtrului de evenimente

    def configureazaUI(self):  # metoda pentru configurarea interfetei
        self.setFixedSize(250, 240)  # setarea dimensiunilor
        self.setStyleSheet("""
            background-color: #F0F4FF;
            border: 1px solid #CCC;
            border-radius: 8px;
        """)  # setarea stilului pentru fundal
        layoutMain = QVBoxLayout(self)  # crearea unui layout de tip vertical
        layoutMain.setContentsMargins(10, 10, 10, 10)  # setarea marginilor
        layoutMain.setSpacing(10)  # setarea spatiului intre elemente

        headerLayout = QHBoxLayout()  # crearea unui layout de tip orizontal
        headerLayout.setSpacing(5)  # setarea spatiului intre elemente
        self.textNume = QLineEdit()  # crearea unui camp de editare pentru nume
        self.textNume.setReadOnly(True)  # setarea campului ca fiind doar pentru citire
        self.textNume.setStyleSheet("font-weight: bold; font-size: 18px;")  # setarea stilului pentru text
        headerLayout.addWidget(self.textNume, stretch=1)  # adaugarea campului in layout

        self.textSterge = QPushButton("X")  # crearea unui buton pentru stergerea listei
        self.textSterge.setFixedSize(30, 30)  # setarea dimensiunilor butonului
        self.textSterge.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: red; border: none;")  # setarea stilului pentru buton
        self.textSterge.clicked.connect(self.stergeLista)  # conectarea semnalului de apasare a butonului la metoda
        headerLayout.addWidget(self.textSterge, alignment=Qt.AlignmentFlag.AlignRight)  # adaugarea butonului in layout

        layoutMain.addLayout(headerLayout)  # adaugarea layout-ului in layout-ul principal

        self.textProduse = QLabel()  # crearea unui label pentru numarul de produse
        self.textProduse.setStyleSheet("font-size: 16px; color: #333;")  # setarea stilului pentru text
        layoutMain.addWidget(self.textProduse, alignment=Qt.AlignmentFlag.AlignCenter)  # adaugarea label-ului in layout

        self.textDeCumparat = QLabel()  # crearea unui label pentru numarul de produse de cumparat
        self.textDeCumparat.setStyleSheet("font-size: 16px; color: #333;")  # setarea stilului pentru text
        layoutMain.addWidget(self.textDeCumparat,
                             alignment=Qt.AlignmentFlag.AlignCenter)  # adaugarea label-ului in layout

        self.textTotal = QLabel()  # crearea unui label pentru totalul listei
        self.textTotal.setStyleSheet("font-size: 16px; color: #007B00;")  # setarea stilului pentru text
        layoutMain.addWidget(self.textTotal, alignment=Qt.AlignmentFlag.AlignCenter)  # adaugarea label-ului in layout

        self.textRamas = QLabel()  # crearea unui label pentru totalul ramas de cumparat
        self.textRamas.setStyleSheet("font-size: 16px; color: #007B00;")  # setarea stilului pentru text
        layoutMain.addWidget(self.textRamas, alignment=Qt.AlignmentFlag.AlignCenter)  # adaugarea label-ului in layout

        layoutMain.addStretch()  # adaugarea unui spatiu intre elemente

    def actualizeazaCampuri(self):  # metoda pentru actualizarea campurilor
        self.textNume.setText(self.lista['nume'])  # setarea textului campului de editare pentru nume
        nrProduse = len(self.lista['produse'])  # preluarea numarului de produse
        nrNecumparate = sum(
            1 for p in self.lista['produse'] if not p['cumprat'])  # preluarea numarului de produse de cumparat
        total = 0.0  # initializarea totalului
        totalNecumparat = 0.0  # initializarea totalului de cumparat
        for produs in self.lista['produse']:  # pentru fiecare produs
            val = produs['cantitate'] * produs['pret']  # calcularea valorii
            total += val  # adaugarea valorii la total
            if not produs['cumprat']:  # daca produsul nu este cumparat
                totalNecumparat += val  # adaugarea valorii la totalul de cumparat
        self.total = total  # setarea totalului
        self.textProduse.setText(f"Produse: {nrProduse}")  # setarea textului label-ului pentru numarul de produse
        self.textDeCumparat.setText(
            f"De cumpărat: {nrNecumparate}")  # setarea textului label-ului pentru numarul de produse de cumparat
        self.textTotal.setText(f"Total: {total:.2f} RON")  # setarea textului label-ului pentru total
        self.textRamas.setText(
            f"Rămas: {totalNecumparat:.2f} RON")  # setarea textului label-ului pentru totalul de cumparat

    def stergeLista(self):  # metoda pentru stergerea listei
        idLista = self.lista['idLista']  # preluarea id-ului listei
        self.stergereSolicitata.emit(idLista)  # emiterea semnalului pentru stergerea listei

    def eventFilter(self, obj, event):  # metoda pentru filtrarea evenimentelor
        if obj == self.textNume:  # daca obiectul este campul de editare pentru nume
            if event.type() == QEvent.Type.MouseButtonDblClick:  # daca evenimentul este de dublu click
                self.toggleModEditare()  # apeleaza metoda pentru schimbarea modului de editare
                return True  # returneaza True
        return super().eventFilter(obj, event)  # apelarea metodei din clasa parinte

    def toggleModEditare(self):  # metoda pentru schimbarea modului de editare
        self.eInModEditare = not self.eInModEditare  # schimbarea modului de editare
        self.textNume.setReadOnly(not self.eInModEditare)  # setarea campului de editare pentru nume
        if self.eInModEditare:  # daca este in modul de editare
            self.setStyleSheet("""
                background-color: #FFF7E6;
                border: 1px solid #FFA500;
                border-radius: 8px;
            """)  # setarea stilului pentru fundal
        else:  # daca nu este in modul de editare
            self.lista['nume'] = self.textNume.text().strip()  # preluarea numelui listei
            self.dateSchimbate.emit(self.lista)  # emiterea semnalului pentru schimbarea datelor
            self.setStyleSheet(""" 
                background-color: #F0F4FF;
                border: 1px solid #CCC;
                border-radius: 8px;
            """)  # setarea stilului pentru fundal

    def mouseDoubleClickEvent(self, event: QMouseEvent):  # metoda pentru evenimentul de dublu click
        self.dubluClick.emit(self.lista)  # emiterea semnalului pentru dublu click
        super().mouseDoubleClickEvent(event)  # apelarea metodei din clasa parinte
