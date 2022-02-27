def is_wordle_word(word_str: str):
    if len(word_str) != 5:
        return False

    for char in word_str.strip().lower():
        if char.isdigit() or char in ('-', ",", '.', "'", "/"):
            return False

    return True
