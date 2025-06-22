def get_user_words():
    """
    Prompt the user to enter a noun, a verb, and an adjective,
    then return these three words as a tuple.
    """
    noun = input("Please enter a noun: ")
    verb = input("Please enter a verb: ")
    adjective = input("Please enter an adjective: ")
    return noun, verb, adjective

# Example usage
if __name__ == "__main__":
    print("Welcome to the Word Collector!")
    print("I'll help you collect three different types of words.\n")
    
    try:
        noun, verb, adjective = get_user_words()
        print(f"\nGreat! You entered:")
        print(f"Noun: {noun}")
        print(f"Verb: {verb}")
        print(f"Adjective: {adjective}")
        
        # Create a simple sentence with the words
        sentence = f"The {adjective} {noun} likes to {verb}."
        print(f"\nHere's a sentence using your words:")
        print(f"'{sentence}'")
        
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
