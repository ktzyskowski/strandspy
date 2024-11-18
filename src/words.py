from board import Board, BoardNode
from trie import Trie

Word = list[BoardNode]
"""A word is a list of BoardNode objects."""


def find_all_words(board: Board, trie: Trie) -> list[Word]:
    """Find all the words in a board that match against a word trie.

    :param board: the board.
    :param trie: the trie.
    :return: a list of list of BoardNode objects, representing found words.
    """
    words = []
    # every letter in the board could be the start of a potential word,
    # so we'll initialize our search frontier with all of them
    frontier = [
        [board[row, col]]
        for row in range(board.height)
        for col in range(board.width)
    ]
    while frontier:
        nodes = frontier.pop()  # nodes of word-so-far
        # concat letters in word-so-far to check if trie contains it
        word = "".join(node.letter for node in nodes)
        if trie.contains(word):
            words.append(nodes)
        # otherwise, get last node in word-so-far, and append neighboring letters to it to expand word
        # only add letters if it COULD lead to a word in the trie (i.e. only append known prefixes)
        last_node = nodes[-1]
        for neighbor_node in last_node.neighbors:
            if neighbor_node in nodes:
                continue
            next_word = word + neighbor_node.letter
            if trie.contains(next_word, prefix=True):
                frontier.append(nodes + [neighbor_node])
    return words


def words_overlap(first_word: Word, second_word: Word) -> bool:
    """Check if two words overlap on a board.

    :param first_word: the first word.
    :param second_word: the second word.
    :return: True if they share letters, False otherwise.
    """
    for node in first_word:
        if node in second_word:
            return True
    return False


def words_connect(first_word: Word, second_word: Word) -> bool:
    """Check if the first word connects directly to the second word.

    This is true iff the last letter of the first word is a neighbor of the first letter of the second word.

    :param first_word: the first word.
    :param second_word: the second word.
    :return: True if the words are connected, False otherwise.
    """
    return first_word[-1] in second_word[0].neighbors

# def print_word(word: Word):
#     print(*[node.letter for node in word], sep="")
