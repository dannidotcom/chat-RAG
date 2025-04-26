# chat-RAG
Ce projet a pour but d'implémenter un Chatbot en se basant sur l'architecture RAG.
# 🚀 Chatbot RAG avec Chainlit

Un chatbot intelligent utilisant l'architecture **RAG** (Retrieval-Augmented Generation) et une interface interactive avec **Chainlit**.


## 📋 Fonctionnalités
- 🔍 Recherche sémantique dans des documents
- 💬 Conversations fluides avec gestion du contexte
- 🧠 Génération de réponses par LLM (OpenAI)
- 🗃️ Stockage des embeddings dans PostgreSQL + pgvector

## ⚙️ Prérequis
- Python 3.10+
- PostgreSQL 15+ avec extension pgvector
- Clé API OpenAI

## 🛠️ Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/dannidotcom/chat-RAG.git
cd chatbot-rag

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer l'environnement
cp .env.example .env
# Editer le fichier .env avec vos credentials
