def get_user_words():
    """
    Prompt the user to enter a noun, a verb, and an adjective,
    then return these three words as a tuple.
    """
    noun = input("Please enter a noun: ")
    verb = input("Please enter a verb: ")
    adjective = input("Please enter an adjective: ")
    return noun, verb, adjective
