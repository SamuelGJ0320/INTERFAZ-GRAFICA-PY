import os
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
from guicadena_ui import *
import re

class ProcesamientoThread(QThread):
    resultado_procesamiento = pyqtSignal(str, str, int, int)

    def __init__(self, cadena):
        super().__init__()
        self.cadena = cadena

    def run(self):
        contEmojis, contCadena, cadena_modificada = self.analizadorLexicografico(self.cadena)
        self.resultado_procesamiento.emit(self.cadena, cadena_modificada, contEmojis, contCadena)

    def procesarDiccionario(self, dics):
        listaPalabra = []
        for archivo in os.listdir(dics):
            rutaArchivo = os.path.join(dics, archivo)
            if os.path.isfile(rutaArchivo) and archivo.endswith(".txt"):
                with open(rutaArchivo, 'r', encoding="utf-8") as f:
                    palabras = f.read().split()
                    listaPalabra.extend(palabras)
        return listaPalabra

    def analizadorLexicografico(self, cadena):
        contEmojis = 0
        contCadena = 0
        diccionarioBNF = {
            ":)": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/047-feliz-2.png",
            ":(": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/059-triste-2.png",
            ":D": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/005-sonriente.png",
            ";)": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/018-guino.png",
            ":P": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/023-cabeza-alienigena-1.png",
            "xD": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/058-riendo.png",
            ":-)": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/014-sonrisa.png",
            ":-(": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/009-triste.png",
            "(y)": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/045-como.png",
            "(n)": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/046-pulgares-abajo-1.png",
            "<3": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/067-corazon.png",
            "\\m/": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/068-cuernos.png",
            ":-o": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/004-conmocionado.png",
            ":o": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/012-conmocionado-1.png",
            ":-|": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/008-confuso.png",
            ":|": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/013-preocuparse.png",
            ":*": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/069-beso.png",
            ">:(": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/051-enojado-1.png",
            "^^": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/016-estrella.png",
            ":-]": "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/png/056-caca.png",
        }

        dics = "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/dict_rae_txt/dics"
        pattern = re.compile('(?:' + '|'.join(re.escape(k) for k in diccionarioBNF.keys()) + ')', re.IGNORECASE)

        matches = pattern.finditer(cadena)

        cadena_modificada = cadena  # Inicializar con la cadena original

        for match in matches:
            contEmojis += 1
            emoji_key = match.group(0)
            emoji_path = diccionarioBNF[emoji_key]

            # Reemplazar el emoji en la cadena modificada
            cadena_modificada = cadena_modificada[
                     :match.start()] + f'<img src="{emoji_path}" alt="{emoji_key}" height="30" width="30">' + cadena_modificada[
                                                                                                              match.end():]

        diccionario = self.procesarDiccionario(dics)

        # Eliminar emojis de la cadena antes de contar palabras
        cadena_sin_emojis = re.sub('<img.*?>', '', cadena_modificada)
        # Eliminar espacios y contar palabras
        strDics = re.split(r'\s+', cadena_sin_emojis.lower().strip())
        contCadena = sum(1 for word in strDics if word in diccionario and word != '')

        return contEmojis, contCadena, cadena_modificada

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.revisarPalabra)
        self.thread = None

        self.inicializarInterfaz()

    def inicializarInterfaz(self):
        self.cargarImagen()
        self.ui.label_3.setText("")
        self.ui.label_4.setText("Palabras: 0 y emojis: 0")

    def cargarImagen(self):
        logo = QImage(
            "C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/logo_eafit_completo.png")
        sLogo = logo.scaled(120, 100)

        etiquetaImagen = QLabel(self)
        etiquetaImagen.setPixmap(QPixmap.fromImage(sLogo))

        layout = QVBoxLayout(self)
        layout.addWidget(etiquetaImagen, alignment=Qt.AlignTop | Qt.AlignLeft)

    def revisarPalabra(self):
        try:
            palabra = self.ui.textEdit.toPlainText()
            if self.thread is None or not self.thread.isRunning():
                self.thread = ProcesamientoThread(palabra)
                self.thread.resultado_procesamiento.connect(self.actualizarInterfaz)
                self.thread.start()
        except Exception as e:
            print(f"Excepción no manejada: {e}")

    def actualizarInterfaz(self, cadena_original, cadena_modificada, contEmojis, contCadena):
        self.ui.label_3.clear()
        self.ui.label_3.setText(cadena_modificada)
        self.ui.label_4.setText(f"Palabras: {contCadena} y emojis: {contEmojis}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
