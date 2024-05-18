def included_in_string(string: str, word_list: list[str]) -> bool:
    """
    Check if any word in the list is in the string.

    Parameters
    ----------
    string (str):
        The string to check
    word_list (List[str]):
        The list of words to check
    Returns:
        bool: True if any word in the list is in the string, False otherwise
    """
    for word in word_list:
        if word in string:
            return True
    return False
