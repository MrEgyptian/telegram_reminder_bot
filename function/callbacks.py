#!/bin/env python
from function import database as db

async def handle_callback(client, event):
    """
    Handle callback queries.

    Args:
        client: The Telethon client.
        event: The incoming callback event.

    Returns:
        None
    """
    query = event.data.decode().split(" ")
    print(query)
    if query[0] == 'rm':
        db.rm_reminder(query[1], event.chat_id)
        await event.edit(f"Reminder Deleted")
    if query[0] == 'stop':
        db.disable_reminder(query[1], event.chat_id)
        await event.edit(f"Reminder Stopped")
    pass

