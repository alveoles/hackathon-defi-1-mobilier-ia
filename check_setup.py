"""Vérifie que chaque brique du kit tourne sur cette machine. Ne résout pas le défi : à vous de les assembler.
python check_setup.py   (≈1 min ; env : MODELS_DIR=./models, OLLAMA_HOST=127.0.0.1:11434, VLM_MODEL=qwen2.5vl:7b)
"""
import gc, json, os, sys, tempfile, time, traceback, urllib.request
from pathlib import Path

M = Path(os.environ.get("MODELS_DIR", "models")).resolve()
os.environ.setdefault("REMBG_HOME", str(M / "rembg"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")
tmp = Path(tempfile.mkdtemp())


def diffusion():  # charge SD 1.5 + ControlNet + LCM-LoRA, génère une petite image (sans croquis)
    import torch
    from diffusers import ControlNetModel, StableDiffusionPipeline
    dev = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
    dt = torch.float32 if dev == "cpu" else torch.float16
    ControlNetModel.from_pretrained(M / "hf/control_v11p_sd15_lineart", torch_dtype=dt, variant="fp16")
    pipe = StableDiffusionPipeline.from_pretrained(M / "hf/dreamshaper-8", torch_dtype=dt, variant="fp16",
                                                   safety_checker=None).to(dev)
    pipe.load_lora_weights(M / "hf/lcm-lora-sdv1-5", weight_name="pytorch_lora_weights.safetensors")
    pipe("a wooden chair", num_inference_steps=2, height=256, width=256).images[0].save(tmp / "sd.png")
    return f"{dev}, image -> {tmp / 'sd.png'}"


def rembg():
    from rembg import new_session
    new_session("isnet-general-use")
    return "isnet-general-use chargé"


def ollama():
    host = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434")
    host = host if host.startswith("http") else f"http://{host}"
    model = os.environ.get("VLM_MODEL", "qwen2.5vl:7b")
    body = {"model": model, "prompt": "Say OK", "stream": False, "keep_alive": 0, "options": {"num_predict": 5}}
    r = json.load(urllib.request.urlopen(urllib.request.Request(f"{host}/api/generate", json.dumps(body).encode()),
                                         timeout=300))
    return f"{model} répond : {r['response'].strip()!r}"


def cad():
    import ezdxf
    from build123d import Box, ExportDXF, Rectangle, export_step
    export_step(Box(400, 400, 18), tmp / "test.step")
    dxf = ExportDXF()
    dxf.add_shape(Rectangle(400, 400))
    dxf.write(tmp / "test.dxf")
    return f"STEP + DXF ({len(ezdxf.readfile(tmp / 'test.dxf').modelspace())} entités)"


failed = 0
for check in (diffusion, rembg, ollama, cad):  # en séquence : un seul gros modèle en RAM à la fois
    t = time.time()
    try:
        msg = check()
        print(f"OK   {check.__name__:9s} {time.time() - t:5.1f} s  {msg}")
    except Exception:
        failed += 1
        print(f"FAIL {check.__name__}\n{traceback.format_exc(limit=1)}")
    gc.collect()
print("Kit prêt." if not failed else f"{failed} brique(s) en échec : voir INSTALL.md « Pièges connus ».")
sys.exit(failed)
