# Workflow ComfyUI : croquis → rendu bois

`sketch2cnc_croquis_vers_rendu.json` : une chaîne croquis → rendu qui marche, à ouvrir pour comprendre les briques
(ControlNet, LoRA, sampler) avant de les réimplémenter, les remplacer ou les dépasser.

```
Croquis → Inverser → ControlNet lineart ┐
DreamShaper 8 → LCM-LoRA → ModelSamplingDiscrete(lcm) → KSampler (lcm / sgm_uniform, 6 pas, cfg 1.5, 512²) → Save
```

Testé le 24/11/2026 (ComfyUI 0.46, M1 Pro 16 Go) : chargé dans l'interface et exécuté tel quel, **14 s** à froid.

## Lancer

```bash
scripts/download_models.sh --comfy              # depuis la racine du repo (ou MODELS_MIRROR=... pour la clé USB)
git clone --depth 1 https://github.com/comfyanonymous/ComfyUI tools/ComfyUI
cd tools/ComfyUI && uv venv -p 3.11 .venv && uv pip install -p .venv -r requirements.txt
printf 'sketch2cnc:\n  base_path: ../../models/comfy\n  checkpoints: checkpoints\n  controlnet: controlnet\n  loras: loras\n' > extra_model_paths.yaml
.venv/bin/python main.py                        # http://127.0.0.1:8188
```

Puis glisser-déposer le JSON dans la fenêtre, charger un croquis dans le nœud **Croquis** (ex. `examples/croquis_chaise.png`)
et cliquer **Run**. Changer le bois / le style dans le nœud **Prompt**.

## Limites (à améliorer par les équipes)

- Le croquis est seulement inversé : un croquis gris ou une photo de papier donne des traits flous.
  Nettoyer le trait avant (OpenCV, préprocesseur ComfyUI…) change beaucoup le résultat.
- Pas de détourage, pas de vue lifestyle, une seule variante.
