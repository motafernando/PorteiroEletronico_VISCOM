# src/main.py
import time
import cv2

from camera import Camera
from detector import FaceDetector
from autorizacao import FaceAuthorizer
from door import abrir_porta
import config
from logger import setup as setup_logger

# ────────────────────────────────────────────────
log = setup_logger()          # grava em logs/porteiro.log + console
# ────────────────────────────────────────────────


def main() -> None:
    log.info("=== Porteiro eletrônico iniciado ===")

    cam = Camera()            # VideoCapture(0)
    if not cam.cap.isOpened():
        log.error("Webcam não encontrada (tente src=1 ou libere a câmera). Encerrando.")
        return

    fd   = FaceDetector()
    auth = FaceAuthorizer()

    consecutivos = 0           # frames seguidos reconhecendo
    ultima_acao  = 0.0         # timestamp da última abertura

    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                log.error("Falha ao capturar frame — aguardando 1 s.")
                time.sleep(1)
                continue

            faces = fd.detect(frame)  # lista de (x, y, w, h)
            for (x, y, w, h) in faces:
                ok, nome, conf = auth.autorizado(frame, (x, y, w, h))
                log.debug(f"conf={conf:.1f} • pessoa={nome}")
                label = nome if ok else "Desconhecido"
                cor   = (0, 255, 0) if ok else (0, 0, 255)

                cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 2)
                cv2.putText(frame, label, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 2)

                if ok and (time.time() - ultima_acao > config.DELAY_REARME):
                    consecutivos += 1
                    if consecutivos >= config.THRESHOLD_FRAMES:
                        abrir_porta()
                        log.info(f"Porta aberta para {nome}")
                        ultima_acao  = time.time()
                        consecutivos = 0
                else:
                    consecutivos = 0

            cv2.imshow("Porteiro Eletrônico — ESC para sair", frame)

            # Sai se ESC (27) for pressionado
            if cv2.waitKey(1) & 0xFF == 27:
                log.info("ESC pressionado. Encerrando aplicação.")
                break

    except KeyboardInterrupt:
        log.info("KeyboardInterrupt recebido. Encerrando aplicação.")

    except Exception:
        log.exception("Exceção não tratada:")

    finally:
        cam.release()
        cv2.destroyAllWindows()
        log.info("Recursos liberados. Bye 👋")


if __name__ == "__main__":
    main()
