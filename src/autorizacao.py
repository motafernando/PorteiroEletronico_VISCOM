from pathlib import Path
import cv2
import numpy as np

IMG_SIZE = (200, 200)        # largura, altura (px)
THRESHOLD_CONF = 50        # ajuste fino depois do teste

class FaceAuthorizer:
    def __init__(self, folder=None):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.names = []

        # 🔧 garante um diretório válido
        if folder is None:
            folder = Path("data/faces_autorizadas")   # caminho padrão
        else:
            folder = Path(folder)
        # agora `folder` é sempre um Path

        images, labels = [], []
        for idx, img_path in enumerate(folder.glob("*")):
            img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, IMG_SIZE, interpolation=cv2.INTER_AREA)
            img = cv2.equalizeHist(img)          # melhora contraste
            images.append(img)
            labels.append(idx)
            self.names.append(img_path.stem)

        if not images:
            raise RuntimeError(
                f"Nenhuma imagem válida em {folder}. "
                "Adicione fotos de rosto (.jpg/.png)."
            )

        self.recognizer.train(images, np.array(labels))

    def autorizado(self, frame_bgr, xywh):
        x, y, w, h = xywh
        face_gray = cv2.cvtColor(frame_bgr[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
        face_gray = cv2.resize(face_gray, IMG_SIZE, interpolation=cv2.INTER_AREA)
        face_gray = cv2.equalizeHist(face_gray)

        label, conf = self.recognizer.predict(face_gray)
        ok = conf < THRESHOLD_CONF
        nome = self.names[label] if ok else None
        return ok, nome, conf        # devolvo conf p/ debug opcional
