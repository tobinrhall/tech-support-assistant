# Tech Support Assistant of Sanctuary 🛠️🔥  
_A Desktop AI-Powered IT Assistant with a Diablo-Themed Mode and GUI Interface_

The **Tech Support Assistant of Sanctuary** is a Python-based application that combines:
- an intelligent IT troubleshooting engine powered by the OpenAI API,  
- a Diablo-inspired “Deckard Cain” mode for fun and flavor,  
- a clean Tkinter GUI for ease of use,  
- a local knowledge-base system for offline facts, and  
- adjustable explanation complexity levels (ELI5, Normal, Advanced).

This project is designed as both a functional support tool **and** a showcase of AI integration, GUI development, and software engineering practices.

---

## ✨ Features

### 🔍 **AI-Powered Troubleshooting**
Uses OpenAI’s GPT-4.1 models to interpret IT issues and return structured, accurate help in a standardized format:

- **Summary**
- **Likely Causes**
- **Recommended Steps**
- **Optional Notes**

Provides consistent, professional troubleshooting advice for real IT problems.

---

### ⚔️ **Diablo Mode (Deckard Cain Mode)**
Switch the AI persona to speak like **Deckard Cain** while still offering accurate, real-world IT recommendations.

Examples:
- “The corrupted runes of your network adapter may be to blame…”
- “Stay awhile and listen, hero — your drivers are shadowed by outdated magic.”

---

### 🧠 **Explanation Difficulty Levels**
Choose how complex the AI’s explanations should be:

- **ELI5** – Beginner-friendly, simple, plain language  
- **Normal** – Standard IT user explanations  
- **Advanced** – Deep technical details for professionals  

---

### 🪟 **Graphical User Interface (GUI)**
A full Tkinter GUI that includes:

- Mode dropdown (Normal / Diablo)  
- Explanation level dropdown  
- Scrollable chat window  
- Input bar + Send button  

Users who aren't comfortable with a terminal can run the GUI with one click.

---

### 📚 **Local Knowledge Base Support**
Drop `.txt` files into the `knowledge_base/` folder, and the assistant will **load them on startup** and use them for contextual help.

Useful for:
- Internal docs  
- SOPs  
- Troubleshooting scripts  
- Checklists  

---

### 🧩 **Modular Architecture**
The application is split into:

- `tech_assistant.py` – core logic, AI prompt building, knowledge base reader  
- `gui_assistant.py` – desktop GUI  
- `knowledge_base/` – local reference files  

Easy to extend and maintain.

---

## 🚀 Getting Started

### **Prerequisites**
- Python 3.10+  
- OpenAI API key with available credit  
- Windows recommended (GUI uses Tkinter)

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/tech-support-assistant.git
cd tech-support-assistant
