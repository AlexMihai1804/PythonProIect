import sys

from PyQt6.QtWidgets import QApplication

from FereastraPrincipala import FereastraPrincipala
from StocareListe import StocareListe


def main():
    app = QApplication(sys.argv)  # creeaza aplicatia
    stocare = StocareListe()  # creeaza obiectul pentru stocarea listelor
    window = FereastraPrincipala(stocare)  # creeaza fereastra principala
    window.show()  # afiseaza fereastra principala
    sys.exit(app.exec())  # executa aplicatia


if __name__ == "__main__":  # daca fisierul este rulat direct
    main()  # apeleaza functia main
