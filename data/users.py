"""
This module interfaces to our user data.
"""

LEVEL = 'level'
MIN_USER_NAME_LEN = 2


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        - That dictionary must at least include a LEVEL member that has an int
        value.
    """
    users = {
        "Callahan": {
            LEVEL: 0,
        },
        "Reddy": {
            LEVEL: 1,
        },
    }
    return users


def create_user(users, user_name, level):
    """
    Contract:
    - Takes in a user name and level.
    - Adds the user to the users dictionary if valid.
    - Returns the updated users dictionary if the user is added.
    - Raises an error if the user name is a duplicate or invalid.
    """
    if user_name in users:
        raise ValueError(f"Adding duplicate {user_name=}")

    if (
        isinstance(user_name, str)
        and len(user_name) >= MIN_USER_NAME_LEN
        and isinstance(level, int)
    ):
        user = {LEVEL: level}
        users[user_name] = user
        print(user)
        return users
    else:
        raise ValueError(f"Invalid user details: {user_name=}, {level=}")


# Example usage
users = get_users()

try:
    users = create_user(users, "Smith", 2)
    print("User created successfully:", users)
except ValueError as e:
    print("Error:", e)


def delete_user(users, user_name):
    """
    Contract:
    - Takes in a user name.
    - Deletes the user from the users dictionary if found.
    - Returns the deleted user's details if found and deleted.
    - Returns None if the user is not in the dictionary.
    """
    if user_name in users:
        deleted_user = users.pop(user_name)
        print(f"Deleted user: {user_name}")
        return deleted_user
    else:
        print(f"User not found: {user_name}")
        return None


# Example usage
users = get_users()
try:
    users = create_user(users, "Smith", 2)
    print("User created successfully:", users)
except ValueError as e:
    print("Error:", e)

# Deleting a user
deleted_user = delete_user(users, "Smith")
if deleted_user:
    print("Deleted user details:", deleted_user)
else:
    print("User not found.")
