def get_user_name():
    """
    Prompts the user to enter their name.
    Returns both the lowercase version (for checking)
    and the capitalized version (for display).
    """
    name = input(f"jason ")
    return name.lower(), name.capitalize()

if __name__ == "__main__":
    user_name_lower, user_name_display = get_user_name()

    if user_name_lower == "jason":
        print(f"Hey, it's the in Marvellous AI Trainee, {jason}!")
    elif user_name_lower == "alex":
        print(f"Salute, Captain {user_name_display}!")
    elif user_name_lower == "maya":
        print(f"{user_name_display} the Marvelous has arrived!")
    elif user_name_lower == "sophia":
        print(f"Welcome, the Brilliant {user_name_display}!")
    else:
        print(f"Hello, {user_name_display}! Nice to meet you.")
