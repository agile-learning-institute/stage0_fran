# Echo 

Echo is a chat-bot agent framework, inspired in syntax by Flask, that maps simple chat messages following the ``/{Agent}/{Action}/{arguments}`` syntax onto your code in the same way Flask maps HTTP events onto your code. This framework is used to expose specific actions in a chat conversation, using a syntax that supports usage by intelligent agents that might be involved in a conversation.

Echo chat-bot's have to be "invited" to participate in a conversation. They always answer and participate in direct messages with users, they can be ``@mentioned join`` to join any channel, and ``@mention leave`` to exit the conversation. 

Echo exposes a /echo agent with the following actions
```
/echo/list/{}
/echo/add_channel/{}
/echo/remove_channel/{}
```

Echo uses a bot channels interface with get_channels, add_channel, remove_channel functions to allow external persistence of the channels the bot is participating in. Stage0_utils provides this as BotServices or via the bot_agent. 

Echo uses a conversation interface with add_message function to allow external persistence of bot-conversations. Stage0_utils provides this as ConversationServices or via the conversation_agent.
