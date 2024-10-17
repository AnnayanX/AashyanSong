from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config

from ..logging import LOGGER


class PragyanMusic(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot... | Logger: @pragyanmusiclogs")
        super().__init__(
            name="PragyanMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            # Get the chat by username
            log_chat = await self.get_chat("@pragyanmusiclogs")
            
            # Send a message to the log channel
            await self.send_message(
                chat_id=log_chat.id,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel. | Logger: @pragyanmusiclogs"
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}. | Logger: @pragyanmusiclogs"
            )
            exit()

        # Ensure the bot is an admin in the log group
        a = await self.get_chat_member(log_chat.id, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel. | Logger: @pragyanmusiclogs"
            )
            exit()

        LOGGER(__name__).info(f"Music Bot Started as {self.name} | Logger: @pragyanmusiclogs")

    async def stop(self):
        await super().stop()
        LOGGER(__name__).info(f"Music Bot Stopped. | Logger: @pragyanmusiclogs")
