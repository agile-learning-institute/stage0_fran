# Echo - A Multi-Party Conversational AI Framework

Echo is a Python-based chatbot agent framework inspired by Flask. Since Agent/Action syntax can be terse, Echo uses a **multi-party conversational AI** to act as a bridge between **human group conversations (outer dialog)** and **structured agent interactions (inner dialog).**

## **How Echo Works**
- Echo operates in **two conversational layers:**
  - **Outer Dialog:** The LLM interacts naturally with users in a group chat.
  - **Inner Dialog:** The LLM privately communicates with structured agents to retrieve and execute information.
- The LLM follows a **Retrieval-Augmented Generation (RAG)** approach:
  - **Interprets human intent** from the group chat.
  - **Generates structured agent requests** to gather information or perform actions.
  - **Formats agent responses** into human-readable answers before sending them back to the group.

## **🚀 Features**
- **Agent-based command routing** using `/agent/action/arguments` syntax.
- **LLM-powered conversation interface** that translates natural language into structured commands.
- **Multi-party chat participation**, allowing the LLM to engage with multiple users while retrieving structured responses from agents.
- **Mongo State management** for bot and conversations, ensuring persistence and context awareness.
- **Modular design**, making it easy to add new agents and capabilities.

---

## **📂 Project Structure**
For this initial implementation, Echo is intermingled with the stage0_Fran Flask/Echo project. 
At some point in the future Echo and it's related code will be extracted into an independent package. This is the proposed structure for that package repo.
```text
/src
│── 📁 echo                 # Core Echo Utility Code
│   ├── 📝 echo.py              # Main Echo agent
│   ├── 📝 agent.py             # Base Echo agent functionality
│   ├── 🤖 discord_bot.py       # Discord client handling on_message events
│   ├── 🧠 llm_handler.py       # LLM-driven message generation logic
│   ├── 🔌 ollama_llm_client.py # Ollama driver for LLM processing
│
│── 📁 agents               # Echo Agent Blueprints (Built-in Agents)
│   ├── 🤖 bot_agent.py          # Bot-related actions
│   ├── 💬 conversation_agent.py # Conversation-based actions
│   ├── 🔁 echo_agent.py         # Default Echo agent
│
│── 📁 routes               # Flask API Route Blueprints
│   ├── 🤖 bot_routes.py         # API for bot-related actions
│   ├── 💬 conversation_routes.py # API for conversation-related actions
│   ├── 🔁 echo_routes.py        # API for Echo core functionality
│
│── 📁 services             # Service Layer (Business Logic)
│   ├── 🤖 bot_service.py        # Handles bot-related operations
│   ├── 💬 conversation_service.py # Handles conversation-related operations
```

---

## **📖 Example Conversation**
### **🌍 Outer Dialog (Group Conversation with Humans)**
```
FROM: @Alice
TO: GROUP
MESSAGE: Hey, what's the status of our channels?
```

### **🤖 Inner Dialog (LLM Communicating with Agents)**
```
FROM: FRAN_LLM
TO: AGENTS
MESSAGE: /echo/list/
```

```
FROM: FRAN_AGENT
TO: AGENTS
MESSAGE: Active channels: #general, #bot
```

### **🌍 Outer Dialog (LLM Responds to the Group)**
```
FROM: FRAN_LLM
TO: GROUP
MESSAGE: We are currently active in #general and #bot
```

---

## **🔗 Contributing**
Want to contribute? Open an issue or PR on GitHub! 🚀

