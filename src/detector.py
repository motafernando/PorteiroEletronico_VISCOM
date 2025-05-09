# src/detector.py
import cv2
from pathlib import Path

class FaceDetector:
    def __init__(self, model_path: str | None = None):
        """
        Inicializa o detector de rostos.

        Args:
            model_path: caminho completo para um arquivo .xml do OpenCV.
                        Se None, usa o cascade padrão 'haarcascade_frontalface_alt2.xml'.
        """
        default_xml = cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
        path = model_path or default_xml

        if not Path(path).exists():
            raise FileNotFoundError(f"Cascade XML não encontrado: {path}")

        self.detector = cv2.CascadeClassifier(path)

    def detect(
        self,
        frame_bgr,
        scaleFactor: float = 1.1,
        minNeighbors: int = 6,
        minSize: tuple[int, int] = (60, 60),
    ):
        """
        Detecta rostos no frame.

        Args:
            frame_bgr: imagem BGR (OpenCV).
            scaleFactor: quanto reduzir a imagem a cada escala.
            minNeighbors: quão “estrito” o agrupamento (maior = menos falsos positivos).
            minSize: tamanho mínimo do rosto em pixels (largura, altura).

        Returns:
            Lista de retângulos (x, y, w, h).
        """
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=scaleFactor,
            minNeighbors=minNeighbors,
            minSize=minSize,
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        return faces
