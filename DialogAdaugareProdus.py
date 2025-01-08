from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDoubleSpinBox, QHBoxLayout, QPushButton
)


class DialogAdaugaProdus(QDialog):  # crearea unui dialog pentru adaugarea unui produs
    def __init__(self, parent=None):  # constructorul clasei
        super().__init__(parent)  # apelarea constructorului clasei parinte
        self.setWindowTitle("Adaugă Produs")  # setarea titlului ferestrei
        self.configureazaUI()  # apelarea metodei pentru configurarea interfetei

    def configureazaUI(self):  # metoda pentru configurarea interfetei
        formLayout = QFormLayout(self)  # crearea unui layout de tip formular
        self.txtNume = QLineEdit()  # crearea unui camp de editare pentru nume
        self.spinCantitate = QDoubleSpinBox()  # crearea unui camp de editare pentru cantitate
        self.spinCantitate.setRange(0.1, 9999)  # setarea unui interval pentru valoarea campului
        self.spinCantitate.setSingleStep(0.1)  # setarea pasului de incrementare
        self.spinCantitate.setDecimals(2)  # setarea numarului de zecimale
        self.spinPret = QDoubleSpinBox()  # crearea unui camp de editare pentru pret
        self.spinPret.setRange(0.1, 9999)  # setarea unui interval pentru valoarea campului
        self.spinPret.setSingleStep(0.1)  # setarea pasului de incrementare
        self.spinPret.setDecimals(2)  # setarea numarului de zecimale
        formLayout.addRow("Nume produs:", self.txtNume)  # adaugarea campului de editare pentru nume in formular
        formLayout.addRow("Cantitate:",
                          self.spinCantitate)  # adaugarea campului de editare pentru cantitate in formular
        formLayout.addRow("Preț:", self.spinPret)  # adaugarea campului de editare pentru pret in formular
        layoutButoane = QHBoxLayout()  # crearea unui layout de tip orizontal
        butonOK = QPushButton("OK")  # crearea unui buton pentru confirmare
        butonAnuleaza = QPushButton("Anulează")  # crearea unui buton pentru anulare
        butonOK.clicked.connect(self.accept)  # conectarea semnalului de apasare a butonului la metoda accept
        butonAnuleaza.clicked.connect(self.reject)  # conectarea semnalului de apasare a butonului la metoda reject
        layoutButoane.addWidget(butonOK)  # adaugarea butonului de confirmare in layout
        layoutButoane.addWidget(butonAnuleaza)  # adaugarea butonului de anulare in layout
        formLayout.addRow(layoutButoane)  # adaugarea layout-ului de butoane in formular
        self.setLayout(formLayout)  # setarea layout-ului formularului

    def getData(self):  # metoda pentru preluarea datelor introduse de utilizator
        return (  # returnarea datelor introduse de utiliz
            self.txtNume.text().strip(),  # preluarea textului introdus in campul de editare pentru nume
            float(self.spinCantitate.value()),  # preluarea valorii introduse in campul de editare pentru cantitate
            float(self.spinPret.value())  # preluarea valorii introduse in campul de editare pentru pret
        )
