import sys
from guicadena_ui import *
from PyQt5.QtWidgets import *
from PyQt5.QtgGui import *
from PyQt5.QtCore import *

class Ventana(QWidget):
  def __init__(self, parent=None):
      QtWidgets.QWidget.__init__(self, parent)
      self.ui=Ui_Form()
      self.ui.setupUi(self)
      self.ui.pushButton.clicked.connect(self.lector)

      logo = Qimage("C:/Users/Invitado 1/PycharmProjects/PROYECTO FINAL LENGUAJES DE PROGRAMACION/Guis/emojicshd/emojicshd/logo_eafit_completo.png")
      sLogo = logo.scaled(120, 100)

      etiquetaImagen = QLabel(self)
      etiquetaImagen.setPixmap(QPixmap.fromImage(sLogo))

      layout = QVBoxLayout(self)
      layout.addWidget(etiquetaImagen, alignment=Qt.AlignTop | Qt.AlignLeft)

  def lector(self):
      l = self.ui.textEdit.toPlainText()
      self.ui.label_3.setText(1)

if __name__ == "__main__":
      mi_aplicacion = QApplication(sys.argv)
      mi_app = Ventana()
      mi_app.show()
      sys.exit(mi_aplicacion.exec_())
