# Porteiro Eletrônico – Visão Computacional (Python)

Projeto didático para reconhecer rostos autorizados pela webcam e ― se aprovado ―
chamar a função `abrir_porta()` (printa “🚪 Porta aberta!”).  
Nenhum hardware real é acionado.

---

## 1. Estrutura de Pastas

porteiro_eletronico/
│
├─ README.md
├─ requirements.txt
│
├─ data/
│ └─ faces_autorizadas/ ← fotos 200 × 200 px, grayscale
│
└─ src/
├─ init.py
├─ autorizacao.py ← LBPH + treinamento dinâmico
├─ cadastro.py ← captura rostos pela webcam
├─ camera.py ← wrapper do VideoCapture
├─ config.py ← THRESHOLDs ajustáveis
├─ detector.py ← Haar Cascade
├─ door.py ← print “🚪 Porta aberta!”
├─ logger.py ← arquivo + console
├─ main.py ← loop principal
└─ paths.py ← ROOT / FACES_DIR (caminho único)

yaml
Copiar
Editar

---

## 2. Pré-requisitos

* **Python ≥ 3.11 (64 bits)**
* Build Tools MSVC + CMake (somente se quiser compilar dlib — não usado agora)
* Bibliotecas listadas em `requirements.txt` (somente `opencv-contrib-python` + `numpy`)

---

## 3. Fluxo de uso
3.1 Cadastrar rostos

python src/cadastro.py
#  ↳ digite o nome (sem espaços)
#  ↳ pressione C para capturar cada foto
#  ↳ pressione ESC para sair
As imagens (200×200 px, grayscale) são salvas em
data/faces_autorizadas/<nome>_<n>.jpg.

Dica: capture 3-5 fotos por pessoa, com expressões e ângulos leves diferentes.

4.2 Iniciar o porteiro

python src/main.py
Quadrado verde + nome + confiança < THRESHOLD_CONF → conta como “match”.

Após THRESHOLD_FRAMES matches consecutivos a porta “abre”.

Pressione ESC (ou Ctrl+C no terminal) para encerrar.

5. Configurações rápidas (src/config.py)
Parâmetro	Descrição	Padrão
THRESHOLD_FRAMES	Nº de frames seguidos reconhecendo antes de abrir	8
DELAY_REARME	Tempo mínimo (s) entre duas aberturas	60

Ajuste de precisão no src/autorizacao.py:


THRESHOLD_CONF = 65   # distância LBPH; baixe se liberar demais, suba se recusar

6. Logs
Todos os eventos são gravados em logs/porteiro.log.

Ajuste o nível de detalhe em logger.py (level=logging.DEBUG).

7. Solução de Problemas
Sintoma	Possível causa / correção
RuntimeError: Nenhuma imagem válida …	Pasta data/faces_autorizadas vazia ou caminho errado. Rode cadastro.py ou mova as fotos.
conf sempre > 100	Fotos de cadastro muito diferentes (iluminação, enquadramento). Recadastre com o mesmo cenário da webcam.
Falsos-positivos	Diminua THRESHOLD_CONF (ex.: 55) ou aumente THRESHOLD_FRAMES.
Webcam não abre	Use Camera(src=1) se houver mais de uma ou feche apps que usam a câmera.