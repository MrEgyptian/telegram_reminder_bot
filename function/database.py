#!/bin/env python
import json, os, datetime

def read_json(filename):
    """
    Read a JSON file.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        dict: The JSON data as a Python dictionary.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

def update_json(filename, data):
    """
    Update a JSON file with new data.

    Args:
        filename (str): The path to the JSON file.
        data (dict): The data to be written to the file.

    Returns:
        None
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return update_json(filename, data)

def list_users():
    """
    Retrieve a list of users from the database.

    Returns:
        list: A list of user data as dictionaries.
    """
    return read_json('database/users.json')

def list_reminders(user_id):
    """
    Retrieve a list of reminders for a specific user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        list: A list of reminder data as dictionaries.
    """
    return read_json(f'database/{user_id}/reminders.json')

def add_user(user_data):
    """
    Add a new user to the database.

    Args:
        user_data (dict): The user data to be added.

    Returns:
        None
    """
    # Retrieve the current list of users
    users = list_users()
    
    # Append the new user data to the list
    users.append(user_data)
    os.makedirs(f'database/{user_data}', exist_ok=True)
    
    # Update the JSON file with the modified list of users
    update_json('database/users.json', list(set(users)))

def rm_reminder(index, user_id):
    """
    Remove a reminder from a user's list of reminders.

    Args:
        index (int): The index of the reminder to be removed.
        user_id (str): The ID of the user.

    Returns:
        None
    """
    today = datetime.datetime.now().strftime("%d-%m-%y")
    reminders = list_reminders(user_id)
    reminders.pop(int(index))
    try:
        disabled = list_disabled(user_id)
        disabled.remove(index)
    except ValueError:
        pass
    update_json(f'database/{user_id}/{today}.json', disabled)
    update_json(f'database/{user_id}/reminders.json', reminders)

def disable_reminder(index, user_id):
    """
    Disable a reminder for a user.

    Args:
        index (int): The index of the reminder to be disabled.
        user_id (str): The ID of the user.

    Returns:
        None
    """
    today = datetime.datetime.now().strftime("%d-%m-%y")
    reminders = list_disabled(user_id)
    reminders.append(index)
    update_json(f'database/{user_id}/{today}.json', reminders)

def list_disabled(user_id):
    """
    Retrieve a list of disabled reminders for a user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        list: A list of disabled reminder indices.
    """
    today = datetime.datetime.now().strftime("%d-%m-%y")
    return read_json(f'database/{user_id}/{today}.json')

def check_disabled(user_id, index):
    """
    Check if a reminder is disabled for a user.

    Args:
        user_id (str): The ID of the user.
        index (int): The index of the reminder.

    Returns:
        bool: True if the reminder is disabled, False otherwise.
    """
    reminders = list_disabled(user_id)
    return str(index) in reminders

def add_reminder(title, user_id, remind_time):
    """
    Add a new reminder for a user.

    Args:
        title (str): The title of the reminder.
        user_id (str): The ID of the user.
        remind_time (str): The time at which the reminder should trigger.

    Returns:
        None
    """
    # Retrieve the current list of users
    reminders = list_reminders(user_id)
    
    # Append the new reminder data to the list
    reminders.append({
        title: remind_time
    })
    
    # Update the JSON file with the modified list of reminders
    update_json(f'database/{user_id}/reminders.json', reminders)

