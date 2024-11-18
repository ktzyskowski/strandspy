from board import Board
from words import Word, words_connect, words_overlap


def find_all_spangrams(board: Board, words: list[Word]) -> list[Word]:
    """Find all spangrams.

    :param board: the board.
    :param words: the list of candidate words.
    :return: the spangrams.
    """
    spangrams = []
    # spangrams.extend(find_1word_spangrams(board, words))
    spangrams.extend(find_2word_spangrams(board, words))
    return spangrams


def find_1word_spangrams(board: Board, words: list[Word]) -> list[Word]:
    """Find all one word spangrams.

    :param board: the board.
    :param words: the list of candidate words.
    :return: the spangrams.
    """
    spangrams = []
    for word in words:
        if board.is_spangram(word):
            spangrams.append(word)
    return spangrams


def find_2word_spangrams(board: Board, words: list[Word]) -> list[Word]:
    """Find all two word spangrams.

    A spangram can be two words, so if we have a list of all words, we can create a new list of all "two-words" by
    connecting them. Words can only be connected if they don't overlap and if the second word starts directly adjacent
    to where the first word ends.

    :param board: the board.
    :param words: the list of candidate words.
    :return: the spangrams.
    """
    spangrams = []
    for first_word in words:
        for second_word in words:
            if words_connect(first_word, second_word) and not words_overlap(first_word, second_word):
                combined_word = first_word + second_word
                if board.is_spangram(combined_word):
                    spangrams.append(combined_word)
    return spangrams
