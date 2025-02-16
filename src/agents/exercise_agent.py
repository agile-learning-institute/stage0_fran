import discord
import logging
from discord import app_commands
from src.services.chain_services import ChainServices
from src.services.workshop_services import WorkshopServices

logger = logging.getLogger(__name__)

def create_exercise_agent(bot):
    """ Registers event handlers and commands for the Fran home channel. """

    @bot.tree.command(name="create_workshop", description="Create a new design-thinking workshop.")
    async def create_workshop(interaction: discord.Interaction):
        """ Slash command to create a new workshop. Opens a modal for input. """
        # Fetch available workshop chains from the service
        chains = ChainServices.get_chains()
        chain_options = [discord.SelectOption(label=chain.name, value=chain._id) for chain in chains]

        # Create a modal form for user input
        class WorkshopModal(discord.ui.Modal, title="Create Workshop"):
            chain = discord.ui.Select(
                placeholder="Select a workshop chain...",
                options=chain_options
            )
            users = discord.ui.TextInput(
                label="Invite users (comma-separated @mentions)",
                placeholder="@user1, @user2",
                required=True
            )

            async def on_submit(self, interaction: discord.Interaction):
                # Extract user inputs
                token = {} # Need a bot token
                breadcrumb = {} # Need a bot breadcrumb
                chain_id = self.chain.values[0]
                user_mentions = self.users.value.split(",")
                guild = interaction.guild
                category = discord.utils.get(guild.categories, name="workshops")  

                # Create a workshop document and Channel
                workshop = WorkshopServices.create_workshop(chain_id, user_mentions, token, breadcrumb)
                channel = WorkshopServices.create_channel(workshop, guild, category)
                await interaction.response.send_message(f"Workshop **{workshop._id}** created in {channel.mention}!", ephemeral=True)

        # Show the modal when the command is executed
        await interaction.response.send_modal(WorkshopModal())

    bot.tree.add_command(create_workshop)

    logger.info("Registered Fran command handlers.")