import chainlit as cl
import subprocess
import json
import os
from datetime import datetime
from typing import Dict, Any, Tuple

# =======================
# === CONFIGURATION ===
# =======================
MODEL_NAME = "phi3:mini"  # Change to "qwen3:8b", "gemma:2b", etc.
GUIDE_FILE = "guide.json"
PROGRESS_FILE = "progress.json"
VERSION = "4.0"

# =======================
# === FONCTIONS UTILES ===
# =======================
def load_json(filename: str, default: dict) -> dict:
    """Charge un fichier JSON ou retourne une valeur par défaut."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[⚠️] {filename} non trouvé.")
        return default
    except Exception as e:
        print(f"[❌] Impossible de charger {filename}: {e}")
        return default

def save_json(filename: str, data: dict):
    """Sauvegarde un dictionnaire en JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[❌] Impossible de sauvegarder {filename}: {e}")

def run_ollama(prompt: str) -> str:
    """Appelle Ollama et retourne la réponse."""
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"❌ Erreur Ollama : {result.stderr}"
    except Exception as e:
        return f"❌ Échec du modèle : {str(e)}"

# =======================
# === CHARGEMENT DES DONNÉES ===
# =======================
@cl.on_chat_start
async def start():
    guide = load_json(GUIDE_FILE, {"sections": []})
    progress = load_progress()

    welcome = f"""
🚀 **Pi Bot Mentor v{VERSION}**

Bonjour Pioneer !  
Je suis ton assistant IA **100 % local**, sans compte, sans cloud.

📚 Tu suis : **{guide.get('title', 'Guide Inconnu')}**
🎯 Tu es à l'étape : `{progress['currentStep']}`

👉 Tape :
- `guide` → voir tout le parcours
- `où suis-je ?` → ton état actuel
- `terminé` → passer à l'étape suivante
- `aide` → toutes les commandes
"""
    await cl.Message(content=welcome).send()

# =======================
# === GESTION DU PROGRÈS ===
# =======================
def load_progress() -> Dict[str, Any]:
    default = {
        "currentSection": "github-setup",
        "currentStep": "create-account",
        "completed": [],
        "lastUpdated": datetime.now().isoformat()
    }
    return load_json(PROGRESS_FILE, default)

def save_progress(progress: Dict[str, Any]):
    progress["lastUpdated"] = datetime.now().isoformat()
    save_json(PROGRESS_FILE, progress)

def get_next_step(current_step: str) -> Tuple[str, str, str]:
    guide = load_json(GUIDE_FILE, {"sections": []})
    found = False
    for section in guide.get("sections", []):
        for step in section["steps"]:
            if found:
                return step["id"], step.get("desc", ""), step.get("command", "")
            if step["id"] == current_step:
                found = True
    return "", "🎉 Félicitations ! Tu as terminé le guide.", ""

# =======================
# === INTERACTION PRINCIPALE ===
# =======================
@cl.on_message
async def on_message(message: cl.Message):
    content = message.content.strip()
    content_lower = content.lower()

    # Commande : afficher le guide
    if any(k in content_lower for k in ["guide", "parcours", "étapes"]):
        guide = load_json(GUIDE_FILE, {"sections": []})
        progress = load_progress()

        response = "📋 **Guide Interactif - Pi Bot Mentor**\n\n"
        for section in guide.get("sections", []):
            title = section.get("title", "Section")
            response += f"🔹 **{title}**\n"
            for step in section["steps"]:
                status = "✅" if step['id'] in progress["completed"] else "🟡" if step['id'] == progress["currentStep"] else "⚪"
                desc = step.get("desc", "Inconnue")
                response += f"   {status} {desc}\n"
            response += "\n"

        await cl.Message(content=response).send()
        return

    # Commande : où suis-je ?
    elif any(k in content_lower for k in ["où suis-je", "état", "progress", "étape"]):
        progress = load_progress()
        titles = {
            "github-setup": "1. Créer un compte GitHub",
            "vscode-setup": "2. Installer VS Code",
            "react-project": "3. Créer un projet React",
            "pi-connect": "4. Intégrer Pi Connect"
        }
        title = titles.get(progress["currentSection"], "Inconnue")

        completed_count = len(progress["completed"])
        total_steps = sum(len(s.get("steps", [])) for s in load_json(GUIDE_FILE, {}).get("sections", []))
        
        response = f"""
📌 **📍 Tu es ici :**
> Section : **{title}**
> Étape : `{progress['currentStep']}`
> Progression : {completed_count}/{total_steps}

💡 Continue comme ça !
"""
        await cl.Message(content=response).send()
        return

    # Commande : marquer comme terminé
    elif any(k in content_lower for k in ["terminé", "fait", "ok", "suivant", "next"]):
        progress = load_progress()
        current_step = progress["currentStep"]

        if current_step not in progress["completed"]:
            progress["completed"].append(current_step)

        next_id, next_desc, next_command = get_next_step(current_step)

        if next_id:
            progress["currentStep"] = next_id
            action = f"➡️ Prochaine étape : {next_desc}"
            if next_command:
                action += f"\n\n🔧 Commande :\n```bash\n{next_command}\n```"
        else:
            action = "🎉 **Félicitations ! Tu as terminé toutes les étapes.**\n\nTu es prêt à créer ta première app Pi Network."

        save_progress(progress)
        await cl.Message(content=f"✅ Étape '{current_step}' marquée comme terminée.\n\n{action}").send()
        return

    # Commande : aide
    elif "aide" in content_lower or "help" in content_lower:
        help_text = """
🛠️ **Commandes disponibles :**
- `guide` → Voir tout le parcours
- `où suis-je ?` → Ton état actuel
- `terminé` → Passer à l’étape suivante
- `aide` → Ce message

💬 Pose aussi des questions techniques :
> “Comment installer Git ?”
> “Crée un projet React”
> “Vérifie si localhost:5173 fonctionne”

🌐 **Ressources utiles :**
- [GitHub](https://github.com)
- [VS Code](https://code.visualstudio.com)
- [Pi Dev Portal](https://minepi.com/dev)
"""
        await cl.Message(content=help_text).send()
        return

    # Sinon : réponse IA via Ollama
    response = run_ollama(content)
    await cl.Message(author="Pi Bot Mentor", content=response).send()