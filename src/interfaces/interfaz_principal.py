"""
Interfaz principal del sistema de procesamiento de imágenes.
Diseño con panel lateral izquierdo y 3 paneles de imagen (Imagen 1, Imagen 2, Resultado).
"""

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QSizePolicy
)
from PySide6.QtGui import QPixmap, QImage, QAction
from PySide6.QtCore import Qt


from config import *

# Importar secciones modulares organizadas
from src.interfaces.seccion_archivo import SeccionArchivo
from src.interfaces.seccion_utilidades import SeccionUtilidades
from src.interfaces.seccion_aritmeticas import SeccionAritmeticas
from src.interfaces.seccion_logicas import SeccionLogicas
from src.interfaces.seccion_ajuste_brillo import SeccionAjusteBrillo
from src.interfaces.seccion_segmentacion import SeccionSegmentacion
from src.interfaces.seccion_morfologia import SeccionMorfologia
from src.interfaces.seccion_filtros import SeccionFiltros
from src.interfaces.seccion_ruido import SeccionRuido
from src.interfaces.seccion_fourier import SeccionFourier
from src.interfaces.seccion_modos_color import SeccionModosColor
from src.interfaces.seccion_componentes_conexas import SeccionComponentesConexas
from src.interfaces.histograma_widget import PanelImagenConHistograma
from src.interfaces.seccion_canny import SeccionCanny



class VentanaPrincipal(QMainWindow):
    """Ventana principal de la aplicación con panel lateral y 3 áreas de imagen."""
    
    def __init__(self):
        super().__init__()
        # Variables de estado
        self.imagen_actual = None  # Imagen 1 (principal)
        self.imagen_original_backup = None  # Backup de Imagen 1
        self.imagen_segunda = None  # Imagen 2
        self.imagen_segunda_backup = None  # Backup de Imagen 2
        self.imagen_resultado = None  # Resultado de operaciones
        
        # Historiales para deshacer/rehacer
        self.historial_img1 = []
        self.historial_rehacer_img1 = []
        self.historial_img2 = []
        self.historial_rehacer_img2 = []
        self.imagen_activa = 1  # 1 o 2 (por default Imagen 1)

        self.init_ui()
    
    def init_ui(self):
        """Inicializar la interfaz gráfica con panel lateral izquierdo y 3 imágenes."""

        self.setWindowTitle("Procesamiento de Imágenes - PDI Completo")
        self.setGeometry(50, 50, 1600, 900)
        self.setMinimumSize(1200, 700)
        self.setStyleSheet(f"background-color: {COLOR_FONDO};")

        self.seccion_archivo = SeccionArchivo(self)
        self.seccion_utilidades = SeccionUtilidades(self)
        self.seccion_aritmeticas = SeccionAritmeticas(self)
        self.seccion_logicas = SeccionLogicas(self)
        self.seccion_ajuste_brillo = SeccionAjusteBrillo(self)
        self.seccion_segmentacion = SeccionSegmentacion(self)
        self.seccion_morfologia = SeccionMorfologia(self)
        self.seccion_filtros = SeccionFiltros(self)
        self.seccion_ruido = SeccionRuido(self)
        self.seccion_fourier = SeccionFourier(self)
        self.seccion_modos_color = SeccionModosColor(self)
        self.seccion_componentes = SeccionComponentesConexas(self)
        self.seccion_canny = SeccionCanny(self)


        # Menú superior
        self.crear_menu_superior()

        # Toolbar
        toolbar = self.addToolBar("Herramientas")
        toolbar.setMovable(False)

        btn_cargar = QAction("📂", self)
        btn_cargar.setToolTip("Cargar Imagen 1")
        btn_cargar.triggered.connect(self.seccion_archivo.cargar_imagen_1)
        toolbar.addAction(btn_cargar)

        btn_guardar = QAction("💾", self)
        btn_guardar.setToolTip("Guardar Resultado")
        btn_guardar.triggered.connect(self.seccion_archivo.guardar_resultado)
        toolbar.addAction(btn_guardar)

        toolbar.addSeparator()

        # Botón Deshacer
        self.btn_deshacer = QAction("↶", self)
        self.btn_deshacer.setToolTip("Deshacer (Ctrl+Z)")
        self.btn_deshacer.setShortcut("Ctrl+Z")
        self.btn_deshacer.triggered.connect(self.deshacer)
        self.btn_deshacer.setEnabled(False)
        toolbar.addAction(self.btn_deshacer)

        # Botón Rehacer
        self.btn_rehacer = QAction("↷", self)
        self.btn_rehacer.setToolTip("Rehacer (Ctrl+Y)")
        self.btn_rehacer.setShortcut("Ctrl+Y")
        self.btn_rehacer.triggered.connect(self.rehacer)
        self.btn_rehacer.setEnabled(False)
        toolbar.addAction(self.btn_rehacer)

        # Widget central y layout principal (HORIZONTAL)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setStretch(0, 0)  # Panel lateral no se estira
        main_layout.setStretch(1, 1)  # Área principal se estira
        
       
        
        # AREA PRINCIPAL (DERECHA) - 3 PANELES DE IMAGEN
        area_principal = QWidget()
        area_layout = QVBoxLayout(area_principal)
        area_layout.setSpacing(0)
        area_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area para las imágenes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background: {COLOR_FONDO};
                border: none;
            }}
            QScrollBar:vertical, QScrollBar:horizontal {{
                background: {COLOR_OSCURO};
                width: 14px;
                height: 14px;
                border-radius: 7px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLOR_PRIMARIO}, stop:1 {COLOR_ACENTO});
                border-radius: 7px;
                min-height: 30px;
                min-width: 30px;
            }}
            QScrollBar::handle:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLOR_ACENTO}, stop:1 {COLOR_EXITO});
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                height: 0px;
                width: 0px;
            }}
        """)
        
        area_imagenes = QWidget()
        imagenes_layout = QHBoxLayout(area_imagenes)
        imagenes_layout.setSpacing(15)
        imagenes_layout.setContentsMargins(15, 15, 15, 15)
        area_imagenes.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Panel 1: Imagen Principal (Imagen 1) con histograma
        self.panel_img1 = PanelImagenConHistograma("IMAGEN 1", COLOR_PRIMARIO)
        self.panel_img1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.panel_img1.setMinimumWidth(300)
        self.panel_img1.hide()  # Oculto inicialmente
        imagenes_layout.addWidget(self.panel_img1, 1)
        
        # Panel 2: Segunda Imagen (Imagen 2) con histograma
        self.panel_img2 = PanelImagenConHistograma("IMAGEN 2", COLOR_SECUNDARIO)
        self.panel_img2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.panel_img2.setMinimumWidth(300)
        self.panel_img2.hide()  # Oculto inicialmente
        imagenes_layout.addWidget(self.panel_img2, 1)
        
        # Panel 3: Resultado con histograma
        self.panel_resultado = PanelImagenConHistograma("RESULTADO", COLOR_EXITO)
        self.panel_resultado.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.panel_resultado.setMinimumWidth(300)
        self.panel_resultado.hide()  # Oculto inicialmente
        imagenes_layout.addWidget(self.panel_resultado, 1)
        
        scroll_area.setWidget(area_imagenes)
        area_layout.addWidget(scroll_area)
        
        main_layout.addWidget(area_principal)
        
        # Barra de estado
        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_CARD}, stop:1 {COLOR_OSCURO});
                color: {COLOR_TEXT_PRIMARY};
                border-top: 2px solid {COLOR_PRIMARIO};
                font-size: 10px;
                font-weight: bold;
                padding: 5px;
            }}
        """)
        self.statusBar().showMessage("Listo para procesar imagenes")
        
        # Actualizar estado de botones
        self.actualizar_botones_historial()
    
    def crear_menu_superior(self):
        menubar = self.menuBar()

        # ARCHIVO
        menu_archivo = menubar.addMenu("Archivo")
        menu_archivo.addAction(
            QAction("Cargar Imagen 1", self,
                    triggered=self.seccion_archivo.cargar_imagen_1)
        )
        menu_archivo.addAction(
            QAction("Cargar Imagen 2", self,
                    triggered=self.seccion_archivo.cargar_imagen_2)
        )
        menu_archivo.addAction(
            QAction("Guardar Resultado", self,
                    triggered=self.seccion_archivo.guardar_resultado)
        )

        # EDITAR (nuevo menú para deshacer/rehacer)
        menu_editar = menubar.addMenu("Editar")
        
        act_deshacer = QAction("Deshacer", self)
        act_deshacer.setShortcut("Ctrl+Z")
        act_deshacer.triggered.connect(self.deshacer)
        menu_editar.addAction(act_deshacer)
        
        act_rehacer = QAction("Rehacer", self)
        act_rehacer.setShortcut("Ctrl+Y")
        act_rehacer.triggered.connect(self.rehacer)
        menu_editar.addAction(act_rehacer)

        # UTILIDADES
        menu_utilidades = menubar.addMenu("Utilidades")
        menu_utilidades.addAction(
            QAction("Convertir a Color", self,
                    triggered=self.seccion_utilidades.convertir_a_color)
        )
        menu_utilidades.addAction(
            QAction("Convertir a Grises", self,
                    triggered=self.seccion_utilidades.convertir_a_grises)
        )
        menu_utilidades.addAction(
            QAction("Convertir a Binaria", self,
                    triggered=self.seccion_utilidades.convertir_a_binaria)
        )

        # OPERACIONES ARITMÉTICAS
        menu_arit = menubar.addMenu("Operaciones Aritméticas")
        menu_arit.addAction(
            QAction("Suma Escalar", self,
                    triggered=lambda: self.seccion_aritmeticas.aplicar_operacion("suma"))
        )
        menu_arit.addAction(
            QAction("Resta Escalar", self,
                    triggered=lambda: self.seccion_aritmeticas.aplicar_operacion("resta"))
        )
        menu_arit.addAction(
            QAction("Multiplicación Escalar", self,
                    triggered=lambda: self.seccion_aritmeticas.aplicar_operacion("multiplicacion"))
        )
        menu_arit.addAction(
            QAction("División Escalar", self,
                    triggered=lambda: self.seccion_aritmeticas.aplicar_operacion("division"))
        )

        # OPERACIONES LÓGICAS
        menu_logicas = menubar.addMenu("Operaciones Lógicas")
        for op in ["and", "or", "xor", "not"]:
            menu_logicas.addAction(
                QAction(op.upper(), self,
                        triggered=lambda checked=False, o=op: self.seccion_logicas.aplicar_operacion(o))
            )

        # AJUSTE DE BRILLO
        menu_brillo = menubar.addMenu("Ajuste de Brillo")
        for metodo, nombre in [
            ("gamma", "Corrección Gamma"),
            ("clahe", "CLAHE"),
            ("uniforme", "Ecualización Uniforme"),
            ("exponencial", "Ecualización Exponencial"),
            ("rayleigh", "Ecualización Rayleigh")
        ]:
            menu_brillo.addAction(
                QAction(nombre, self,
                        triggered=lambda checked=False, m=metodo: self.seccion_ajuste_brillo.aplicar_brillo(m))
            )

        # SEGMENTACIÓN
        menu_segmentacion = menubar.addMenu("Segmentación")

        segmentaciones = [
            ("otsu", "Otsu"),
            ("kapur", "Kapur"),
            ("media", "Media"),
            ("kmeans", "K-Means")
        ]

        for metodo, nombre in segmentaciones:
            menu_segmentacion.addAction(
                QAction(
                    nombre,
                    self,
                    triggered=lambda checked=False, m=metodo:
                        self.seccion_segmentacion.aplicar_segmentacion(m)
                )
            )


        # FILTROS
        menu_filtros = menubar.addMenu("Filtros Espaciales")
        for tipo, nombre in [
            ("promediador", "Promediador"),
            ("mediana", "Mediana"),
            ("gaussiano", "Gaussiano"),
            ("bilateral", "Bilateral"),
            ("minimo", "Mínimo"),
            ("maximo", "Máximo")
        ]:
            menu_filtros.addAction(
                QAction(f"Filtro {nombre}", self,
                        triggered=lambda checked=False, t=tipo: self.seccion_filtros.aplicar_filtro(t))
            )

        # CANNY
        menu_canny = menubar.addMenu("Fronteras")

        menu_canny.addAction(
            QAction(
                "Detector Canny",
                self,
                triggered=self.seccion_canny.aplicar_canny
            )
        )

        # MORFOLOGÍA

        menu_morfologia = menubar.addMenu("Morfología Matemática")
        for op, nombre in [
                            ("erosion", "Erosión"),
                            ("dilatacion", "Dilatación"),
                            ("apertura", "Apertura"),
                            ("cierre", "Cierre"),
                            ("gradiente", "Gradiente Morfológico"),
                            ("tophat", "Top-Hat"),
                            ("blackhat", "Black-Hat")
                        ]:


            menu_morfologia.addAction(
                QAction(nombre, self,
                        triggered=lambda checked=False, o=op: self.seccion_morfologia.aplicar_morfologia(o))
            )

        # RUIDO
        menu_ruido = menubar.addMenu("Ruido")
        for tipo, nombre in [
            ("sal_pimienta", "Sal y Pimienta"),
            ("gaussiano", "Gaussiano"),
            ("uniforme", "Uniforme")
        ]:
            menu_ruido.addAction(
                QAction(nombre, self,
                       triggered=lambda checked=False, t=tipo: self.seccion_ruido.aplicar_ruido(t))
            )

        # FOURIER / DCT
        menu_fourier = menubar.addMenu("Frecuencia")
        menu_fourier.addAction(
            QAction("FFT 2D", self,
                    triggered=lambda checked=False: self.seccion_fourier.aplicar_fourier("fft")

        ))
        menu_fourier.addAction(
            QAction("Filtro Pasa Bajas", self,
                    triggered=lambda checked=False: self.seccion_fourier.aplicar_fourier("lowpass"))
        )
        menu_fourier.addAction(
            QAction("Filtro Pasa Altas", self,
                    triggered=lambda checked=False: self.seccion_fourier.aplicar_fourier("highpass"))
        )
        menu_fourier.addAction(
            QAction("DCT Compresión", self,
                    triggered=self.seccion_fourier.aplicar_dct_dialogo)
        )

       
        # MODOS DE COLOR
        menu_color = menubar.addMenu("Modos de Color")

        menu_color.addAction(
            QAction("Extraer Canal Rojo", self,
                    triggered=lambda checked=False: self.seccion_modos_color.extraer_canal("rojo"))
        )

        menu_color.addAction(
            QAction("Extraer Canal Verde", self,
                    triggered=lambda checked=False: self.seccion_modos_color.extraer_canal("verde"))
        )

        menu_color.addAction(
            QAction("Extraer Canal Azul", self,
                    triggered=lambda checked=False: self.seccion_modos_color.extraer_canal("azul"))
        )

        menu_color.addSeparator()

        menu_color.addAction(
            QAction("Convertir a HSV", self,
                    triggered=lambda checked=False: self.seccion_modos_color.convertir_modo("hsv"))
        )

        menu_color.addAction(
            QAction("Convertir a Escala de Grises", self,
                    triggered=lambda checked=False: self.seccion_modos_color.convertir_modo("gris"))
        )


        # IMAGEN ACTIVA
        menu_activa = menubar.addMenu("Imagen Activa")

        act_img1 = QAction("Trabajar sobre Imagen 1", self)
        act_img1.triggered.connect(lambda: self.set_imagen_activa(1))
        menu_activa.addAction(act_img1)

        act_img2 = QAction("Trabajar sobre Imagen 2", self)
        act_img2.triggered.connect(lambda: self.set_imagen_activa(2))
        menu_activa.addAction(act_img2)

        menu_activa.addSeparator()

        act_swap = QAction("Intercambiar Imagen 1 ↔ Imagen 2", self)
        act_swap.triggered.connect(self.intercambiar_imagenes)
        menu_activa.addAction(act_swap)

        # COMPONENTES CONEXAS
        menu_conexas = menubar.addMenu("Componentes Conexas")
        menu_conexas.addAction(
            QAction("Etiquetar Componentes", self,
                    triggered=self.seccion_componentes.contar_componentes)
        )
    
    def set_imagen_activa(self, idx: int):
        """Define qué imagen se considera 'activa' para operaciones de una sola imagen."""
        self.imagen_activa = 1 if idx == 1 else 2
        self.statusBar().showMessage(f"Imagen activa: {self.imagen_activa}")
        self.actualizar_botones_historial()

    def _ejecutar_en_imagen_activa(self, func):
        """
        Ejecuta una operación que normalmente trabaja sobre 'imagen_actual' (Imagen 1),
        pero si la imagen activa es la 2, hace un swap temporal para reutilizar la lógica sin modificar secciones.
        """
        if self.imagen_activa == 1:
            return func()

        # Swap temporal: Imagen 2 -> Imagen 1
        img1, bak1 = self.imagen_actual, self.imagen_original_backup
        img2, bak2 = self.imagen_segunda, self.imagen_segunda_backup

        self.imagen_actual, self.imagen_original_backup = img2, bak2
        try:
            res = func()
        finally:
            # Guardar lo que haya quedado en imagen_actual como imagen_segunda
            self.imagen_segunda = self.imagen_actual
            self.imagen_segunda_backup = self.imagen_original_backup

            # Restaurar Imagen 1
            self.imagen_actual, self.imagen_original_backup = img1, bak1

            # Refrescar paneles si hay imágenes
            self.mostrar_imagen_1()
            self.mostrar_imagen_2()

        return res

    def intercambiar_imagenes(self):
        """Intercambia Imagen 1 e Imagen 2."""
        self.imagen_actual, self.imagen_segunda = self.imagen_segunda, self.imagen_actual
        self.imagen_original_backup, self.imagen_segunda_backup = self.imagen_segunda_backup, self.imagen_original_backup
        
        # Intercambiar también los historiales
        self.historial_img1, self.historial_img2 = self.historial_img2, self.historial_img1
        self.historial_rehacer_img1, self.historial_rehacer_img2 = self.historial_rehacer_img2, self.historial_rehacer_img1
        
        self.mostrar_imagen_1()
        self.mostrar_imagen_2()
        self.actualizar_botones_historial()
        self.statusBar().showMessage("Imagen 1 e Imagen 2 intercambiadas")


    def _crear_separador(self):
        """Crea un separador horizontal."""
        separador = QWidget()
        separador.setFixedHeight(2)
        separador.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLOR_PRIMARIO}, stop:0.5 {COLOR_ACENTO}, stop:1 {COLOR_PRIMARIO});
            border-radius: 1px;
        """)
        return separador
    
    def guardar_en_historial(self):
        """Guarda el estado actual de la imagen activa en el historial."""
        if self.imagen_activa == 1 and self.imagen_actual is not None:
            self.historial_img1.append(self.imagen_actual.copy())
            if len(self.historial_img1) > 20:
                self.historial_img1.pop(0)
            self.historial_rehacer_img1.clear()
        elif self.imagen_activa == 2 and self.imagen_segunda is not None:
            self.historial_img2.append(self.imagen_segunda.copy())
            if len(self.historial_img2) > 20:
                self.historial_img2.pop(0)
            self.historial_rehacer_img2.clear()
        
        self.actualizar_botones_historial()
    
    def deshacer(self):
        """Deshace la última operación en la imagen activa."""
        if self.imagen_activa == 1:
            if len(self.historial_img1) > 0:
                # Guardar estado actual en rehacer
                if self.imagen_actual is not None:
                    self.historial_rehacer_img1.append(self.imagen_actual.copy())
                
                # Restaurar estado anterior
                self.imagen_actual = self.historial_img1.pop()
                self.mostrar_imagen_1()
                self.statusBar().showMessage("Deshacer aplicado en Imagen 1")
            else:
                self.statusBar().showMessage("No hay operaciones para deshacer en Imagen 1")
        
        elif self.imagen_activa == 2:
            if len(self.historial_img2) > 0:
                # Guardar estado actual en rehacer
                if self.imagen_segunda is not None:
                    self.historial_rehacer_img2.append(self.imagen_segunda.copy())
                
                # Restaurar estado anterior
                self.imagen_segunda = self.historial_img2.pop()
                self.mostrar_imagen_2()
                self.statusBar().showMessage("Deshacer aplicado en Imagen 2")
            else:
                self.statusBar().showMessage("No hay operaciones para deshacer en Imagen 2")
        
        self.actualizar_botones_historial()
    
    def rehacer(self):
        """Rehace la última operación deshecha en la imagen activa."""
        if self.imagen_activa == 1:
            if len(self.historial_rehacer_img1) > 0:
                # Guardar estado actual en historial
                if self.imagen_actual is not None:
                    self.historial_img1.append(self.imagen_actual.copy())
                
                # Restaurar estado rehecho
                self.imagen_actual = self.historial_rehacer_img1.pop()
                self.mostrar_imagen_1()
                self.statusBar().showMessage("Rehacer aplicado en Imagen 1")
            else:
                self.statusBar().showMessage("No hay operaciones para rehacer en Imagen 1")
        
        elif self.imagen_activa == 2:
            if len(self.historial_rehacer_img2) > 0:
                # Guardar estado actual en historial
                if self.imagen_segunda is not None:
                    self.historial_img2.append(self.imagen_segunda.copy())
                
                # Restaurar estado rehecho
                self.imagen_segunda = self.historial_rehacer_img2.pop()
                self.mostrar_imagen_2()
                self.statusBar().showMessage("Rehacer aplicado en Imagen 2")
            else:
                self.statusBar().showMessage("No hay operaciones para rehacer en Imagen 2")
        
        self.actualizar_botones_historial()
    
    def actualizar_botones_historial(self):
        """Actualiza el estado habilitado/deshabilitado de los botones de historial."""
        if self.imagen_activa == 1:
            self.btn_deshacer.setEnabled(len(self.historial_img1) > 0)
            self.btn_rehacer.setEnabled(len(self.historial_rehacer_img1) > 0)
        elif self.imagen_activa == 2:
            self.btn_deshacer.setEnabled(len(self.historial_img2) > 0)
            self.btn_rehacer.setEnabled(len(self.historial_rehacer_img2) > 0)
    
    def mostrar_imagen_1(self):
        """Muestra la imagen 1 en su panel con histograma."""
        if self.imagen_actual is not None:
            self.panel_img1.show()
            self.panel_img1.mostrar_imagen(self.imagen_actual)
    
    def mostrar_imagen_2(self):
        """Muestra la imagen 2 en su panel con histograma."""
        if self.imagen_segunda is not None:
            self.panel_img2.show()
            self.panel_img2.mostrar_imagen(self.imagen_segunda)
    
    def mostrar_resultado(self):
        """Muestra el resultado en su panel con histograma."""
        if self.imagen_resultado is not None:
            self.panel_resultado.show()
            self.panel_resultado.mostrar_imagen(self.imagen_resultado)


def main():
    """Función principal."""
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":  
    main()