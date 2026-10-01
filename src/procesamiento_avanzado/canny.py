"""
Módulo de detección de bordes Canny
"""

import cv2
import numpy as np


class DetectorCanny:
    """Clase para aplicar el detector de bordes Canny."""

    @staticmethod
    def aplicar_canny(
        imagen: np.ndarray,
        umbral_bajo: int = 50,
        umbral_alto: int = 150,
        kernel_blur: int = 5
    ) -> np.ndarray:
        """
        Aplica el detector de bordes Canny.

        Args:
            imagen: Imagen en escala de grises
            umbral_bajo: Umbral inferior
            umbral_alto: Umbral superior
            kernel_blur: Tamaño del kernel gaussiano (impar)

        Returns:
            Imagen binaria de bordes
        """
        # Asegurar escala de grises
        if len(imagen.shape) == 3:
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

        # Suavizado previo
        if kernel_blur > 1:
            imagen = cv2.GaussianBlur(imagen, (kernel_blur, kernel_blur), 0)

        # Canny
        bordes = cv2.Canny(imagen, umbral_bajo, umbral_alto)

        return bordes
