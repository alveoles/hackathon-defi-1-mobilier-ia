#!/usr/bin/env bash
# Télécharge les modèles du starter dans $MODELS_DIR (défaut ./models), depuis Hugging Face OU depuis un miroir local.
#
#   scripts/download_models.sh                    # internet : diffusers + rembg + qwen2.5vl:7b     (≈ 9,2 Go)
#   scripts/download_models.sh --comfy            # + fichiers uniques pour ComfyUI                (+ 3,0 Go)
#   scripts/download_models.sh --3b               # + qwen2.5vl:3b, secours machines 8 Go           (+ 3,2 Go)
#   MODELS_MIRROR=/Volumes/USB/models scripts/download_models.sh   # jour J, clé USB : copie, aucun réseau
#
# Tailles (fichiers réellement chargés) :
#   hf/dreamshaper-8 (fp16)                 2,13 Go   Lykon/dreamshaper-8
#   hf/control_v11p_sd15_lineart (fp16)     0,72 Go   lllyasviel/control_v11p_sd15_lineart
#   hf/lcm-lora-sdv1-5                      0,13 Go   latent-consistency/lcm-lora-sdv1-5
#   rembg/.../isnet-general-use.onnx        0,18 Go   github.com/danielgatis/rembg
#   comfy/ (checkpoint + controlnet + lora) 2,99 Go   option --comfy
#   ollama qwen2.5vl:7b                     6,0 Go    (dans $OLLAMA_MODELS, défaut ~/.ollama/models)
#   ollama qwen2.5vl:3b                     3,2 Go    option --3b
#   => clé USB complète (tout ce qui précède) : ≈ 15,4 Go  (+ 1,2 Go de wheels Python pour une install hors ligne)
#
# Préparer la clé (sur une machine qui a tout téléchargé avec --comfy --3b) :
#   cp -R models /Volumes/USB/models && cp -R ~/.ollama/models /Volumes/USB/models/ollama
set -euo pipefail

MODELS_DIR=${MODELS_DIR:-models}
OLLAMA_DIR=${OLLAMA_MODELS:-$HOME/.ollama/models}
COMFY=0; Q3B=0
for a in "$@"; do
  case $a in
    --comfy) COMFY=1 ;;
    --3b) Q3B=1 ;;
    *) echo "option inconnue : $a" >&2; exit 2 ;;
  esac
done
mkdir -p "$MODELS_DIR"

if [ -n "${MODELS_MIRROR:-}" ]; then
  [ -d "$MODELS_MIRROR/hf" ] || { echo "miroir invalide : $MODELS_MIRROR/hf introuvable" >&2; exit 1; }
  echo "copie depuis le miroir $MODELS_MIRROR -> $MODELS_DIR"
  for d in hf rembg comfy; do
    [ -d "$MODELS_MIRROR/$d" ] && cp -R "$MODELS_MIRROR/$d" "$MODELS_DIR/"
  done
  if [ -d "$MODELS_MIRROR/ollama" ]; then
    echo "copie des modèles Ollama -> $OLLAMA_DIR (redémarrer ollama ensuite)"
    mkdir -p "$OLLAMA_DIR" && cp -R "$MODELS_MIRROR/ollama/." "$OLLAMA_DIR/"
  fi
else
  HF=$(command -v hf || echo .venv/bin/hf)   # fourni par huggingface-hub (requirements.txt)
  dl() { "$HF" download "$@"; }
  dl Lykon/dreamshaper-8 --local-dir "$MODELS_DIR/hf/dreamshaper-8" model_index.json \
    scheduler/scheduler_config.json feature_extractor/preprocessor_config.json \
    tokenizer/merges.txt tokenizer/special_tokens_map.json tokenizer/tokenizer_config.json tokenizer/vocab.json \
    text_encoder/config.json text_encoder/model.fp16.safetensors \
    unet/config.json unet/diffusion_pytorch_model.fp16.safetensors \
    vae/config.json vae/diffusion_pytorch_model.fp16.safetensors
  dl lllyasviel/control_v11p_sd15_lineart --local-dir "$MODELS_DIR/hf/control_v11p_sd15_lineart" \
    config.json diffusion_pytorch_model.fp16.safetensors
  dl latent-consistency/lcm-lora-sdv1-5 --local-dir "$MODELS_DIR/hf/lcm-lora-sdv1-5" pytorch_lora_weights.safetensors
  ONNX="$MODELS_DIR/rembg/models/isnet-general-use/isnet-general-use.onnx"
  [ -s "$ONNX" ] || { mkdir -p "$(dirname "$ONNX")" && curl -fL -o "$ONNX" \
    https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx; }
  if [ $COMFY = 1 ]; then
    dl Lykon/DreamShaper DreamShaper_8_pruned.safetensors --local-dir "$MODELS_DIR/comfy/checkpoints"
    dl comfyanonymous/ControlNet-v1-1_fp16_safetensors control_v11p_sd15_lineart_fp16.safetensors \
      --local-dir "$MODELS_DIR/comfy/controlnet"
    mkdir -p "$MODELS_DIR/comfy/loras"   # même LoRA que la version diffusers : copie, pas de 2e téléchargement
    cp "$MODELS_DIR/hf/lcm-lora-sdv1-5/pytorch_lora_weights.safetensors" "$MODELS_DIR/comfy/loras/lcm-lora-sdv1-5.safetensors"
  fi
  ollama pull qwen2.5vl:7b
  if [ $Q3B = 1 ]; then ollama pull qwen2.5vl:3b; fi
fi

du -sh "$MODELS_DIR"/* 2>/dev/null || true
echo "OK. Vérifier : python check_setup.py"
