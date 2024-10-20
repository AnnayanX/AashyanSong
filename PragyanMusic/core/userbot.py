from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="PragyanMusicAssistant",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="PragyanMusic2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="PragyanMusic3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="PragyanMusic4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="PragyanMusic5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")
        assistants_to_start = [
            (self.one, "STRING1"),
            (self.two, "STRING2"),
            (self.three, "STRING3"),
            (self.four, "STRING4"),
            (self.five, "STRING5"),
        ]
        
        for assistant, string in assistants_to_start:
            if getattr(config, string):
                await assistant.start()
                try:
                    await assistant.join_chat("VrindavanNeeko16008")
                except Exception as e:
                    LOGGER(__name__).error(f"Failed to join chat: {e}")
                
                assistants.append(len(assistants) + 1)
                try:
                    # Get the log group by username
                    logger_chat = await assistant.get_chat("@pragyanmusiclogs")
                    await assistant.send_message(
                        chat_id=logger_chat.id,
                        text=f"Assistant {assistant.me.mention} has started!"
                    )
                except (errors.ChannelInvalid, errors.PeerIdInvalid):
                    LOGGER(__name__).error(
                        f"Assistant Account {len(assistants)} has failed to access the log group/channel. Make sure that you have added your assistant to your log group/channel."
                    )
                    exit()
                except Exception as ex:
                    LOGGER(__name__).error(
                        f"Assistant Account {len(assistants)} has failed to access the log group/channel.\n Reason: {type(ex).__name__}."
                    )
                    exit()

                try:
                    a = await assistant.get_chat_member("@pragyanmusiclogs", assistant.id)
                    if a.status != ChatMemberStatus.ADMINISTRATOR:
                        LOGGER(__name__).error(
                            "Please promote your assistant as an admin in your log group/channel."
                        )
                        exit()
                except Exception as ex:
                    LOGGER(__name__).error(
                        f"Failed to get chat member status. Reason: {type(ex).__name__}."
                    )
                    exit()

                assistant.id = assistant.me.id
                assistant.name = assistant.me.mention
                assistant.username = assistant.me.username
                assistantids.append(assistant.id)
                LOGGER(__name__).info(f"Assistant Started as {assistant.name}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except Exception as e:
            LOGGER(__name__).error(f"Error stopping assistants: {e}")
