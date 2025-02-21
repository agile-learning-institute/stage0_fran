class EchoAgent(Agent):
    def __init__(self, bot):
        super().__init__('echo')
        self.bot = bot

    @Agent.action('list')
    async def list_channels(self, arguments, channel, message):
        """Lists the active channels."""
        return f"Active channels: {', '.join(map(str, self.bot.active_channels))}" if self.bot.active_channels else "No active channels."

    @Agent.action('add_channel')
    async def add_channel(self, arguments, channel, message):
        """Adds the bot to a channel."""
        self.bot.active_channels.add(channel.id)
        return f"Joined channel: {channel.name}"

    @Agent.action('remove_channel')
    async def remove_channel(self, arguments, channel, message):
        """Removes the bot from a channel."""
        self.bot.active_channels.discard(channel.id)
        return f"Left channel: {channel.name}"    