# Défi 1 — Prototyper du mobilier avec l'IA

> Hackathon Alvéoles × Epitech — mercredi 2 décembre, TechSud (Saint-Pierre)

## Le défi

À partir d'une **banque de matériaux** et de **contraintes de design et techniques**, utiliser l'IA pour **prototyper des produits mobilier**, via un **workflow open source** déployé en local ou sur serveur.

## Objectif

Construire un outil qui part d'un brief (ex. « une étagère murale en bois local, 80 cm, budget 150 € ») et produit un prototype exploitable par un professionnel du mobilier.

## Livrable attendu

- Un workflow open source qui tourne (local ou serveur)
- Une démo live : brief → proposition de mobilier
- Un README qui explique comment lancer le projet

## Ressources

🚧 En préparation : banque de matériaux, contraintes, exemples de projets, starter code.

## Démarrer en 10 min

1. Cliquer sur **Use this template** pour créer le repo de votre équipe, le cloner.
2. Installer le kit (détails macOS / Windows / Linux et machines 8 Go : [INSTALL.md](INSTALL.md)) :

   ```bash
   brew install uv ollama && ollama serve &                 # macOS ; voir INSTALL.md pour Windows / Linux
   uv venv -p 3.11 .venv && source .venv/bin/activate
   uv pip install -r requirements.txt
   MODELS_MIRROR=/Volumes/USB/models scripts/download_models.sh   # clé USB ; sans la variable = téléchargement (≈ 9 Go)
   python check_setup.py                                     # doit finir par « Kit prêt. »
   ```

3. Travailler en branches + Pull Requests, rien en direct sur `main`.

Le kit installe et vérifie les briques ; **il ne les assemble pas**. Le pipeline, c'est vous.

## Les briques du kit

Toutes testées en local sur un MacBook M1 Pro 16 Go. Libre à vous d'en prendre d'autres : justifiez vos choix.

| Étape | Entrée → sortie | Dans le kit (`models/`) | Mesures | À savoir |
|---|---|---|---|---|
| Rendu photoréaliste | croquis → image | SD 1.5 DreamShaper 8 + ControlNet lineart + LCM-LoRA | 7 s / image en 512², 6,7 Go RAM | ControlNet lineart attend des **traits blancs sur fond noir** ; LCM : 4-8 pas, cfg ≈ 1,5. SDXL testé : la forme dérive, et c'est trop lourd pour 16 Go |
| Fond blanc | image → image détourée | rembg `isnet-general-use` | 1 s | `u2net` laisse du gris entre les pieds |
| Lecture des cotes | croquis / rendu → JSON | `qwen2.5vl:7b` via Ollama (`3b` pour 8 Go) | 4 s à chaud, 20 s à froid | Ollama accepte un schéma JSON (`format`) ; le VLM se trompe : prévoir la correction humaine |
| CAO paramétrique | cotes → STEP / STL | build123d | < 1 s | Pas de Rhino.Compute sur Mac : le `.gh` du Starter Pack sert de référence |
| Découpe CNC | pièces → DXF | build123d `ExportDXF`, ezdxf | < 1 s | contours fermés en mm, un calque par pièce |
| Interface | | Gradio installé (ou autre) | | |

Contraintes machine : un seul gros modèle en RAM à la fois (SD + VLM ne tiennent pas ensemble sur 16 Go) ;
`keep_alive: 0` dans les requêtes Ollama libère la RAM tout de suite.

Exemples : `examples/croquis_chaise.png` (croquis de test) ; `starter-pack/05_Workflow_ComfyUI/` (une chaîne croquis → rendu
qui marche, en ComfyUI, pour comprendre les briques).
