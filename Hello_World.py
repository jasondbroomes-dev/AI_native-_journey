# This script asks the user for their name and then prints a greeting.

def get_user_name():
  """
  Prompts the user to enter their name and returns the input.
  """
  name = input("Please enter your name: ")
  return name

if __name__ == "__main__":
  user_name = get_user_name()
  print(f"Hello, {user_name}! Nice to meet you.")
