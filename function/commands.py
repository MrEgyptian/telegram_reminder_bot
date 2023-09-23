#!/bin/env python
from function import database as db
import nltk
import re
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from telethon.tl import functions, types, custom

time_regex = '([0-9]|1[0-9]|2[0-3])(\:)([0-5][0-9]|[0-5])'


def fix_spelling(sentence):
    """
    Fix spelling mistakes in a sentence.

    Args:
        sentence (str): The input sentence with potential spelling mistakes.

    Returns:
        str: The sentence with corrected spelling.
    """
    spell = SpellChecker()
    u = sentence.lower().split(' ')
    corrected = []
    for i in u:
        corrected += [spell.correction(i)]
    sentence = ' '.join(u)
    return sentence


nltk.data.path=["nltk-data"]

def remove_stopwords(text):
    """
    Remove common stop words from a text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with stop words removed.
    """
    words = nltk.word_tokenize(text)
    # Get the list of English stop words
    stop_words = set(stopwords.words('english'))

    # Remove stop words from the list of words
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)

    return filtered_text


async def handle_message(client, event):
    """
    Handle incoming messages and execute commands.

    Args:
        client: The Telethon client.
        event: The incoming message event.

    Returns:
        None
    """
    message = str(event.message.message)
    if message.startswith('/'):
        command = message.split("\x20")[0].lower().lstrip('/')
        args = message.split("\x20")[1:]
        text = '\x20'.join(message.split("\x20")[1:])
        print(command)
        if command == "start":
            db.add_user(event.chat_id)
            msg = """
            Welcome to the reminder bot, here's some bot using tips:
            /remind **me Piano Course at 18:30** to make a new reminder
            /list to list reminders
            """
            await event.reply(msg)
        if command == "list":
            reminders = db.list_reminders(event.chat_id)
            if len(reminders) != 0:
                buttons = []
                i = 0
                for reminder in reminders:
                    for title, value in reminder.items():
                        buttons.append([
                            custom.Button.inline(f"{title}:{value}"),
                            custom.Button.inline(f"Modify Time", f"mod {i}"),
                            custom.Button.inline(f"Remove", f"rm {i}")
                        ])
                        i += 1
                await event.reply("Here's a list of your reminders", buttons=buttons)
            else:
                await event.reply("Please add a reminder using /remind command")
        if command == "remind":
            if len(args) == 0:
                await event.reply("Tell me the task to remind you")
                await event.reply("For example: at 19:30 I will go shopping")
            else:
                doc = fix_spelling(text)
                doc = remove_stopwords(doc)
                document = '\x20'.join('\x20')
                remind_time = re.findall(time_regex, ''.join(doc))
                if len(remind_time) != 1:
                    await event.reply("I don't know the time")
                    await event.reply("Make sure that time format is like 23:12")
                else:
                    print(remind_time)
                    remind_time = list(remind_time[0])
                    remind_time[0] = remind_time[0] if (len(remind_time[0]) == 2) else f"0{remind_time[0]}"
                    remind_time[2] = remind_time[2] if (len(remind_time[2]) == 2) else f"{remind_time[2]}0"
                    reminder_time = str().join(remind_time)
                    title = doc.replace(reminder_time, '')
                    db.add_reminder(title, event.chat_id, reminder_time)
                    await event.reply(f"reminder {title} is set at {reminder_time}")

