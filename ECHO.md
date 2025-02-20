# Echo - A Multi-Party Conversational AI Framework

Echo is a Python-based chatbot framework inspired by Flask. Echo enables **multi-party conversational AI** by acting as a bridge between **human group conversations (outer dialog)** and **structured agent interactions (inner dialog).**

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
- **State management for bot and conversations**, ensuring persistence and context awareness.
- **Modular design**, making it easy to add new agents and capabilities.

---

## **📂 Project Structure**
For this initial implementation, Echo is intermingled with the stage0_Fran Flask/Echo project. 
At some point in the future Echo and it's related code will be extracted into an independent package.
```
echo                 # Echo Utility Code
┣ echo.py                    # Core Echo agent framework
┣ discord_bot.py             # Discord client, listens for messages
┣ llm_handler.py             # LLM-driven message interpretation
agents/               # Echo Agent Blueprints
┣ echo_agent.py            # Default built-in Echo agent
┣ bot_agent.py             # Handles bot-related actions
┣ conversation_agent.py    # Handles conversation actions
┣ other_agent.py           # Additional Custom Agents...
routes/               # Flask API Route Blueprints
┣ echo_routes.py           # Default built-in Echo API Endpoints
┣ etc.                     # Additional API endpoints...
services/             # Services to support Agents/Routes with business logic
┣ bot_service.py           # Bot services
┣ conversation_service.py  # Conversation services
┣ other_service.py         # Additional Custom Services...
```

---

## **📌 LLM-Driven Conversational Flow**
The `/agent/action/parameters` syntax is precise but terse. The LLM acts as a **natural language interface** that understands user intent, generates valid agent requests, and reformats structured responses before sharing them with the group.

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

## **🛠️ Installation & Usage**
### **📌 Install Dependencies**
```
pip install -r requirements.txt
```

### **📌 Run the Discord Bot**
```
python discord_bot.py
```

---

## **🔗 Contributing**
Want to contribute? Open an issue or PR on GitHub! 🚀

