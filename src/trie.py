class Trie:
    """Trie, or prefix tree.

    Implemented using nodes of dictionaries. Case-sensitive.
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        """Inserts a word into the trie.

        :param word: the word.
        :return: None.
        """
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.is_leaf = True

    def contains(self, word: str, prefix: bool = False):
        """Checks if a word is in the trie.

        :param word: the word.
        :param prefix: whether to check for prefixes only.
        :return: boolean indicating if word is in the trie.
        """
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return current_node.is_leaf or prefix

    @staticmethod
    def from_file(path: str, min_length: int = 4):
        """Create a new trie from a file containing words separated by newline.

        :param path: path to the file.
        :param min_length: minimum length for a word to be inserted into the trie.
        :return: the newly created trie.
        """
        trie = Trie()
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                word = line.strip()
                if len(word) >= min_length:
                    trie.insert(word)
        return trie


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_leaf = False
