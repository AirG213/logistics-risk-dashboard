import os
import subprocess
import sys
from pathlib import Path

# --------------------------
# 📂 Répertoires
BASE_DIR = Path(__file__).resolve().parent
VENV_DIR = BASE_DIR / "venv"
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"
DATA_SOURCES_NOTEBOOK = BASE_DIR / "data_sources" / "data_pipeline.ipynb"
APP_FILE = BASE_DIR / "dashboard" / "app.py"

step = 1
total = 4

# --------------------------
# [1/4] Créer venv
print(f"[{step}/{total}] 📦 Création du venv...")
if not VENV_DIR.exists():
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    print(f"✅ venv créé : {VENV_DIR}")
else:
    print(f"✅ venv déjà présent : {VENV_DIR}")

# ✅ Définir python_exe et pip_exe **juste après création**
python_exe = VENV_DIR / "Scripts" / "python.exe" if os.name == "nt" else VENV_DIR / "bin" / "python"
pip_exe = VENV_DIR / "Scripts" / "pip.exe" if os.name == "nt" else VENV_DIR / "bin" / "pip"

# --------------------------
# [2/4] Installer requirements
step += 1
print(f"[{step}/{total}] 📦 Installation des requirements...")
subprocess.run([str(pip_exe), "install", "-r", str(REQUIREMENTS_FILE)], check=True)
print("✅ Packages installés.")

# --------------------------
# [3/4] Orchestration DATA SOURCES
step += 1
print(f"[{step}/{total}] 🚀 Orchestration des DATA SOURCES : {DATA_SOURCES_NOTEBOOK}")

process = subprocess.Popen(
    [
        str(python_exe), "-m", "papermill",
        str(DATA_SOURCES_NOTEBOOK),
        str(DATA_SOURCES_NOTEBOOK)
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True
)

for line in process.stdout:
    print(line, end="")

process.wait()

if process.returncode != 0:
    raise subprocess.CalledProcessError(process.returncode, process.args)

print("✅ Données récupérées, extraites et nettoyées.")

# --------------------------
# [4/4] Lancer Streamlit 
step += 1
print(f"[{step}/{total}] 🚀 Lancement de Streamlit : {APP_FILE}")

streamlit_exe = VENV_DIR / "Scripts" / "streamlit.exe" if os.name == "nt" else VENV_DIR / "bin" / "streamlit"

# On lance Streamlit dans le dossier /dashboard
subprocess.run(
    [
        str(streamlit_exe), "run", "app.py"
    ],
    cwd=str(BASE_DIR / "dashboard"),  
    check=True
)

print(f"\n✅✨ Tout le pipeline a été exécuté avec succès !")