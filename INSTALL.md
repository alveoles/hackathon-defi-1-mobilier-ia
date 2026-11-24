# Installation

Tout tourne **en local**, outils libres. Besoin : ~15 Go libres (modèles) + 3 Go (Python), 16 Go de RAM conseillés.
Les modèles tournent **en séquence** (un seul gros modèle en RAM à la fois) : fermez les applis lourdes.

| Machine | VLM | Remarque |
|---|---|---|
| 16 Go et + | `qwen2.5vl:7b` (défaut) | testé |
| 8 Go | `qwen2.5vl:3b` → `export VLM_MODEL=qwen2.5vl:3b` | moins fiable (rate la traverse), relire les cotes |
| sans GPU | idem | rendu sur CPU ≈ 1-2 min / image (non testé) |

## macOS (Apple Silicon) — testé le 24/11/2026, M1 Pro 16 Go

```bash
xcode-select --install                       # si pas déjà fait
brew install uv ollama
cd hackathon-defi-1-mobilier-ia              # votre repo créé avec « Use this template »
uv venv -p 3.11 .venv && source .venv/bin/activate
uv pip install -r requirements.txt
ollama serve &                               # ou l'app Ollama si elle tourne déjà
scripts/download_models.sh                   # ≈ 9,2 Go ; jour J : MODELS_MIRROR=/Volumes/USB/models scripts/download_models.sh
python check_setup.py                        # chaque brique : diffusion, rembg, ollama, cad (≈30 s)
```

## Linux (NVIDIA) — non testé

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -fsSL https://ollama.com/install.sh | sh          # installe et démarre le service ollama
uv venv -p 3.11 .venv && source .venv/bin/activate
uv pip install torch --index-url https://download.pytorch.org/whl/cu128   # adapter à votre CUDA
uv pip install -r requirements.txt
scripts/download_models.sh
python check_setup.py
```

## Windows 11 (NVIDIA) — non testé

PowerShell :

```powershell
winget install astral-sh.uv Ollama.Ollama Git.Git     # Git fournit Git Bash pour le script de téléchargement
uv venv -p 3.11 .venv; .venv\Scripts\activate
uv pip install torch --index-url https://download.pytorch.org/whl/cu128
uv pip install -r requirements.txt
& "C:\Program Files\Git\bin\bash.exe" scripts/download_models.sh
python check_setup.py
```

Sur la clé USB : `$env:MODELS_MIRROR="E:/models"` avant le script.

## Jour J sans internet

- Modèles : `MODELS_MIRROR=/Volumes/USB/models scripts/download_models.sh` (copie, aucun réseau). Les modèles Ollama sont
  copiés dans `~/.ollama/models` : redémarrer Ollama ensuite.
- Python : `uv pip install --no-index --find-links /Volumes/USB/kit/wheels -r requirements.txt`
  (wheels macOS arm64 / Python 3.11 ; `uv python install 3.11` doit avoir été fait avant).
- Le code force `HF_HUB_OFFLINE=1` : aucun appel réseau à l'exécution.

## Variables d'environnement

| Variable | Défaut | Rôle |
|---|---|---|
| `MODELS_DIR` | `./models` | où le code et le script cherchent/rangent les modèles |
| `MODELS_MIRROR` | — | dossier miroir (clé USB) à copier au lieu de télécharger |
| `VLM_MODEL` | `qwen2.5vl:7b` | modèle Ollama pour les cotes |
| `OLLAMA_HOST` | `127.0.0.1:11434` | serveur Ollama |
| `OLLAMA_MODELS` | `~/.ollama/models` | où le script copie les modèles Ollama du miroir |

## Pièges connus

| Symptôme | Correctif |
|---|---|
| `FAIL ollama` … `Connection refused` | Ollama n'est pas lancé : `ollama serve &` |
| `FAIL ollama` … `HTTP Error 404` (modèle absent) | `ollama pull qwen2.5vl:7b` (ou copie du miroir + redémarrer Ollama) |
| `FAIL diffusion` … `run the library in offline mode` | modèles absents de `$MODELS_DIR` : relancer `scripts/download_models.sh` |
| la machine swappe / gèle | autre appli lourde ouverte ; passer au 3b (`VLM_MODEL=qwen2.5vl:3b`) |

## Optionnel : mesh 3D par IA (TripoSR)

Testé mais **pour visualiser seulement** (formes molles, pas de cotes) ; venv séparé (`transformers==4.35`), 1,7 Go de modèle,
4,9 Go de RAM, 16 s. Recette testée disponible auprès des organisateurs.
