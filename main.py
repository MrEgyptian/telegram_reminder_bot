from function import commands as cmd
from function import database as db
from function import callbacks
import asyncio
import telethon, threading
from telethon import TelegramClient, sync, events

from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetAdminLogRequest
from telethon.tl.functions.channels import GetParticipantsRequest

from telethon.tl.types import ChannelParticipantsRecent
from telethon.tl.types import InputChannel
from telethon.tl.types import ChannelAdminLogEventsFilter
from telethon.tl.types import InputUserSelf
from telethon.tl.types import InputUser
from telethon.tl.custom import Button

import datetime, time

api_id = 23133386
api_hash = 'b3779eef02c32a6a13bdf2574aab9f9d'
#bot_token = '6020661484:AAHkHO4ZYzK_jeZ3HcdAdpKThIA7KnL8UIw'
#client = TelegramClient('meeno', api_id, api_hash)
bot_token = '6575133166:AAEiuptUgnpQ-lk9iR_GBt6sz68ikp6QMrA'
client = TelegramClient('remind_bot', api_id, api_hash)

async def remind_worker(client):
    """
    Worker function to send reminders to users based on their schedule.

    Args:
        client: The Telethon client.

    Returns:
        None
    """
    while True:
        current_time_obj = datetime.datetime.now()
        current_time = current_time_obj.strftime("%H:%M")
        reminders = []
        users = db.list_users()
        for user in users:
            user_reminders = db.list_reminders(user)
            reminders += user_reminders
            i = 0
            for reminder in reminders:
                remind_title, remind_value = list(reminder.items())[0]
                h, m = remind_value.split(":")
                h = int(h)
                m = int(m)
                remind_time_obj = datetime.datetime.combine(
                    datetime.datetime.today(),
                    datetime.time(h, m))
                if (current_time_obj >= remind_time_obj):
                    is_disabled = db.check_disabled(user, i)
                    while (not is_disabled):
                        is_disabled = db.check_disabled(user, i)
                        print(is_disabled)
                        buttons = []
                        buttons.append(Button.inline("Stop Reminder", f"stop {i}"))
                        buttons.append(Button.inline("Delete Reminder", f"rm {i}"))
                        await client.send_message(user, remind_title, buttons=buttons)
                        await asyncio.sleep(600)
                i += 1
        await asyncio.sleep(1)

@client.on(events.CallbackQuery())
async def callback(event):
    await callbacks.handle_callback(client, event)

@client.on(events.NewMessage())
async def readMessages(event):
    await cmd.handle_message(client, event)

try:
    client.start(bot_token=bot_token)
    loop = asyncio.get_event_loop()
    loop.create_task(remind_worker(client))
    #get_contacts()
    # Create a log or print a message in the console indicating that the bot has started.
    client.run_until_disconnected()
finally:
    client.disconnect()
    # Create a log or print a message in the console indicating that the bot has stopped.

