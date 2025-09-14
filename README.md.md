# Pi Bot Mentor 💡

🚀 Un assistant IA 100 % local pour guider les Pioneers du Pi Network vers leur première app — étape par étape, sans cloud, sans compte.

> "De Zéro à App Pi" – Un guide interactif intelligent, basé sur Chainlit, Ollama et un système de progression vérifiable.

![Interface du Pi Bot Mentor](https://via.placeholder.com/800x400.png?text=Pi+Bot+Mentor+Interface)  
*Remplace par une capture d’écran réelle plus tard*

---

## 🎯 Vision du Projet

Transformer un simple tutoriel statique en un **copilote interactif intelligent**, capable de :
- ✅ Guider pas à pas dans la création d’un projet (Git, React, Vite)
- 🧠 Répondre aux questions techniques via une IA locale (`phi3:mini`, `qwen3`, etc.)
- 📌 Suivre la progression de l’utilisateur
- 🔍 Valider automatiquement certaines étapes (ex: "Vite+ React s’affiche-t-il ?")
- 🔐 Fonctionner **100 % en local** — sans dépendance à Hugging Face ou autre service centralisé

👉 Inspiré par le document *"Du Guide en Ligne au Copilote de Visioconférence"* :  
> _"Le futur des guides n’est pas dans un PDF, mais dans un agent IA qui interagit avec toi."_

---

## ✅ Fonctionnalités clés

| Fonction | Détail |
|--------|-------|
| 💬 Chatbot IA local | Utilise Ollama + modèle léger (`phi3:mini`) |
| 📚 Guide structuré | Basé sur `guide.json` avec étapes, commandes, validations |
| 📍 Suivi du progrès | Sauvegardé dans `progress.json` |
| 🔧 Commandes copiables | Format ````bash\n<commande>\n```` → bouton "Copier" intégré |
| 🔄 Interaction continue | Le bot comprend le contexte de la conversation |
| 🌐 Open Source | Prêt pour les contributions communautaires |

---

## ⚙️ Installation & Lancement

### 1. Prérequis

- [x] Python 3.9+
- [x] PowerShell / Terminal
- [x] VS Code (recommandé)

### 2. Installe les outils

```bash
# 1. Installe Ollama (https://ollama.com/download)
# 2. Télécharge un modèle IA léger
ollama pull phi3:mini

# 3. Installe Chainlit
pip install chainlit

# 4. Clone le projet
git clone https://github.com/challenge-awake/pi-bot-mentor.git
cd pi-bot-mentor/mentor-chatbot