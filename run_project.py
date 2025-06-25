import os
import subprocess
import sys
from pathlib import Path

# --------------------------
# Répertoires
BASE_DIR = Path(__file__).resolve().parent
VENV_DIR = BASE_DIR / ".venv"
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"
DATA_SOURCES_NOTEBOOK = BASE_DIR / "data_sources" / "data_pipeline.ipynb"
APP_FILE = BASE_DIR / "dashboard" / "app.py"

step = 1
total = 5

# --------------------------
# --------------------------
# [1/5] Créer venv
print(f"[{step}/{total}] Création du venv...")

if not VENV_DIR.exists():
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    print(f"venv créé : {VENV_DIR}")
else:
    print(f"venv déjà présent : {VENV_DIR}")

# Définir les exécutables python et pip du venv
python_exe = VENV_DIR / "Scripts" / "python.exe" if os.name == "nt" else VENV_DIR / "bin" / "python"
pip_exe = VENV_DIR / "Scripts" / "pip.exe" if os.name == "nt" else VENV_DIR / "bin" / "pip"

# Ajout du dossier Scripts du venv dans le PATH (utile pour `kaggle`, `papermill`, etc.)
os.environ["PATH"] = str(VENV_DIR / "Scripts") + os.pathsep + os.environ["PATH"]

# Installation du kernel Jupyter (si pas déjà installé)
print("Installation du kernel Jupyter pour le venv...")
subprocess.run([str(pip_exe), "install", "ipykernel"], check=True)

# Enregistrement du kernel Jupyter sous le nom "logistics-env"
subprocess.run([
    str(python_exe), "-m", "ipykernel", "install",
    "--user", "--name=logistics-env"
], check=True)

print("Kernel Jupyter 'logistics-env' enregistré.")

# --------------------------
# [2/5] Installer requirements
step += 1
print(f"[{step}/{total}] Installation des requirements...")
subprocess.run([str(pip_exe), "install", "-r", str(REQUIREMENTS_FILE)], check=True)
print("Packages installés.")

# --------------------------
# [3/5] Orchestration DATA SOURCES
try:
    import papermill as pm
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "papermill"])
    import papermill as pm

step += 1
print(f"[{step}/{total}] Orchestration des DATA SOURCES : {DATA_SOURCES_NOTEBOOK}")

try:
    pm.execute_notebook(
        input_path=str(DATA_SOURCES_NOTEBOOK),
        output_path=str(DATA_SOURCES_NOTEBOOK),
        cwd=str(DATA_SOURCES_NOTEBOOK.parent)
    )
    print("Données récupérées, extraites et nettoyées.")

except Exception as e:
    print(f"Erreur pendant l'orchestration DATA SOURCES : {e}")
    raise

# --------------------------
# [4/5] Vérification des datasets
step += 1
print(f"[{step}/{total}] Vérification des datasets...")

expected_files = [
    "airline_delay_cause_cleaned.csv",
    "amazon_delivery_cleaned.csv",
    "railroad_accident_cleaned.csv",
    "shipping_accidents_cleaned.csv",
    "supply_chain_cleaned.csv",
    "usa_accidents_traffic_cleaned.csv"
]

missing = [f for f in expected_files if not (BASE_DIR / "data" / "cleaned" / f).exists()]

if missing:
    print("❌ Certains datasets sont manquants après l'orchestration :")
    for f in missing:
        print(f" - {f}")
    print("\nLance manuellement `data_pipeline.ipynb` pour corriger ou diagnostiquer.")
    sys.exit(1)
else:
    print("Tous les datasets sont présents.")

# --------------------------
# [4/5] Lancer Streamlit 
step += 1
print(f"[{step}/{total}] Lancement de Streamlit : {APP_FILE}")

streamlit_exe = VENV_DIR / "Scripts" / "streamlit.exe" if os.name == "nt" else VENV_DIR / "bin" / "streamlit"

# On lance Streamlit dans le dossier /dashboard
subprocess.run(
    [
        str(streamlit_exe), "run", "app.py"
    ],
    cwd=str(BASE_DIR / "dashboard"),  
    check=True
)

print(f"\nTout le pipeline a été exécuté avec succès !")