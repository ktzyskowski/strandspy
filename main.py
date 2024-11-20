import time

from src.board import Board
from src.client import StrandsClient
from src.spangrams import find_all_spangrams
from src.trie import Trie
from src.words import Word
from src.words import find_all_words, words_overlap


def solve(headless: bool = True) -> list[Word]:
    solution = []

    trie = Trie.from_file("res/words.txt", min_length=4)
    with StrandsClient(headless=headless) as client:
        board = Board(client.letters)

        # try to fit as many words on the board
        words = find_all_words(board, trie)
        spangrams = find_all_spangrams(board, words)

        while words:
            word = words.pop()
            included = client.input_word(word)
            if included:
                solution.append(word)
                # filter out rest of words to remove overlaps (they wouldn't be valid anyway)
                words = [other_word for other_word in words if not words_overlap(word, other_word)]

        # in case the spangram is 2 words, we need to find it here
        spangrams = [
            spangram for spangram in spangrams if
            all(not words_overlap(word, spangram) for word in solution)
        ]
        while spangrams:
            spangram = spangrams.pop()
            included = client.input_word(spangram)
            if included:
                solution.append(spangram)
                break

        # let the user close on their own
        if not headless:
            input("Press enter to continue...")

    return solution


def print_answer(words: list[Word]):
    for word in words:
        print(f"({word[0].row}, {word[0].col})", "".join(node.letter for node in word))


if __name__ == "__main__":
    start = time.time()

    answer = solve(headless=False)

    end = time.time()
    elapsed_time = end - start
    print(elapsed_time, "seconds")

    print_answer(answer)
