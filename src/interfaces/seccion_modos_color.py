"""Sección de análisis de modos de color."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_PRIMARIO


class SeccionModosColor(SeccionBase):
    """Sección para análisis y conversión de modos de color."""
    
    def __init__(self, ventana_principal):
        super().__init__("MODOS DE COLOR", COLOR_PRIMARIO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de modos de color."""
        self.crear_boton("Extraer Canal Rojo", COLOR_PRIMARIO, lambda: self.extraer_canal("rojo"))
        self.crear_boton("Extraer Canal Verde", COLOR_PRIMARIO, lambda: self.extraer_canal("verde"))
        self.crear_boton("Extraer Canal Azul", COLOR_PRIMARIO, lambda: self.extraer_canal("azul"))
        self.crear_boton("Convertir a HSV", COLOR_PRIMARIO, lambda: self.convertir_modo("hsv"))
        self.crear_boton("Convertir a Escala de Grises", COLOR_PRIMARIO, lambda: self.convertir_modo("gris"))
    
    def extraer_canal(self, canal):
        """Extrae un canal de color específico."""
        nombres = {
            'rojo': 'Canal Rojo',
            'verde': 'Canal Verde',
            'azul': 'Canal Azul'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Extraer: {nombres[canal]}")
        dialogo.agregar_selector_imagen()
        
        info = QLabel(f"Se extraerá el {nombres[canal]} de la imagen seleccionada")
        info.setStyleSheet(f"color: {COLOR_PRIMARIO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            import cv2
            import numpy as np
            
            try:
                if len(imagen.shape) == 2:
                    QMessageBox.warning(dialogo, "Advertencia", 
                                      "La imagen ya es en escala de grises")
                    return
                
                # Extraer canal (imagen en RGB)
                indices = {'rojo': 0, 'verde': 1, 'azul': 2}
                canal_idx = indices[canal]
                
                resultado = imagen[:, :, canal_idx]
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"{nombres[canal]} extraído")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def convertir_modo(self, modo):
        """Convierte la imagen a diferentes modos de color."""
        nombres = {
            'hsv': 'HSV',
            'gris': 'Escala de Grises'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Convertir a: {nombres[modo]}")
        dialogo.agregar_selector_imagen()
        
        info = QLabel(f"Se convertirá la imagen a {nombres[modo]}")
        info.setStyleSheet(f"color: {COLOR_PRIMARIO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            import cv2
            
            try:
                if modo == "hsv":
                    if len(imagen.shape) == 2:
                        QMessageBox.warning(dialogo, "Advertencia", 
                                          "La imagen debe ser a color")
                        return
                    resultado = cv2.cvtColor(imagen, cv2.COLOR_RGB2HSV)
                elif modo == "gris":
                    if len(imagen.shape) == 2:
                        resultado = imagen
                    else:
                        resultado = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"Convertido a {nombres[modo]}")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
