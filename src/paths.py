from pathlib import Path
ROOT       = Path(__file__).resolve().parent.parent     # …/porteiro_eletronico
FACES_DIR  = ROOT / "data" / "faces_autorizadas"
FACES_DIR.mkdir(parents=True, exist_ok=True)