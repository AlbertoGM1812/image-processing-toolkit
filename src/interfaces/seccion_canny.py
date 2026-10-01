"""
Sección de detección de bordes Canny
"""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_PRIMARIO
import cv2


class SeccionCanny(SeccionBase):
    """Sección para aplicar el detector de bordes Canny."""

    def __init__(self, ventana_principal):
        super().__init__("CANNY", COLOR_PRIMARIO, ventana_principal)

    def crear_botones(self):
        self.crear_boton(
            "Detector Canny",
            COLOR_PRIMARIO,
            self.aplicar_canny
        )

    def aplicar_canny(self):
        dialogo = DialogoBase(self.ventana_principal, "Detector de Bordes Canny")
        dialogo.agregar_selector_imagen()

        umbral_bajo = dialogo.agregar_spin(
            "Umbral Bajo:", 0, 255, 50, 5
        )
        umbral_alto = dialogo.agregar_spin(
            "Umbral Alto:", 0, 255, 150, 5
        )
        kernel_blur = dialogo.agregar_spin(
            "Kernel Gaussiano:", 1, 15, 5, 2
        )

        info = QLabel(
            "Canny detecta bordes a partir de gradientes y umbralización con histéresis."
        )
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)

        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return

            from src.procesamiento_avanzado.canny import DetectorCanny

            try:
                resultado = DetectorCanny.aplicar_canny(
                    imagen,
                    umbral_bajo.value(),
                    umbral_alto.value(),
                    kernel_blur.value()
                )

                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(
                    "Detector Canny aplicado"
                )
                dialogo.accept()

            except Exception as e:
                QMessageBox.critical(dialogo, "Error", str(e))

        dialogo.agregar_botones(aplicar)
        dialogo.exec()
