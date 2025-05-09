"""
Captura de rostos para o porteiro eletrônico.
Salva imagens 200×200 px (grayscale) em data/faces_autorizadas/.
"""

import cv2
from pathlib import Path


# --- parâmetros globais --------------------------------------------------------

CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
IMG_SIZE = (200, 200)          # largura, altura
SAVE_DIR = Path("../porteiro_eletronico/data/faces_autorizadas")  # relativo à pasta src/

# --- preparação ----------------------------------------------------------------

nome = input("Nome da pessoa (sem espaços): ").strip().lower()
SAVE_DIR.mkdir(parents=True, exist_ok=True)

detector = cv2.CascadeClassifier(CASCADE)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Webcam não encontrada. Feche apps que usem a câmera e tente de novo.")

print("[i] Pressione C para capturar, ESC para sair.")

contador = 1
try:
    while True:
        ok, frame = cap.read()
        if not ok:
            print("[!] Falha ao ler a câmera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.1, 6, minSize=(80, 80))

        # desenha retângulos
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Cadastro de rostos", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:          # ESC
            break
        elif key == ord("c") and len(faces) == 1:
            (x, y, w, h) = faces[0]
            face = gray[y : y + h, x : x + w]
            face = cv2.resize(face, IMG_SIZE, interpolation=cv2.INTER_AREA)
            face = cv2.equalizeHist(face)

            fname = f"{nome}_{contador}.jpg"
            cv2.imwrite(str(SAVE_DIR / fname), face)
            print(f"[✓] Salvo: {fname}")
            contador += 1
        elif key == ord("c") and len(faces) != 1:
            print("[!] Preciso ver exatamente 1 rosto para capturar.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Cadastro encerrado.")
