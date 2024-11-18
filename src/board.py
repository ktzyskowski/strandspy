class Board:
    """A grid data structure to represent the Strands letters.

    Implements linked-list style references to facilitate graph search for valid words.
    """

    def __init__(self, letters: str):
        self.width = 6
        self.height = 8
        self._init_nodes(letters)

    def __getitem__(self, position: tuple[int, int]):
        """Get the BoardNode object at the given (row, col) position.

        :param position: a tuple containing the row and column.
        :return: the BoardNode object.
        """
        row, col = position
        index = self._to_index(row, col)
        return self._nodes[index]

    def _init_nodes(self, letters: str):
        """Initialize the nodes of the board.

        :param letters: the letters, flattened into a single string.
        """
        # create each node
        self._nodes = []
        letter_index = 0
        for row in range(self.height):
            for col in range(self.width):
                letter = letters[letter_index]
                self._nodes.append(BoardNode(letter, row, col))
                letter_index += 1
        # link each node together, so their neighbors lists are correct
        for row in range(self.height):
            for col in range(self.width):
                node_to_link = self[row, col]
                for neighbor in self._neighbors(row, col):
                    node_to_link.neighbors.append(neighbor)

    def _neighbors(self, row: int, col: int):
        """Yield the neighbors of a node in the board.

        :param row: the row of the node.
        :param col: the column of the node.
        :return: a generator over the node's neighbors.
        """
        for delta_row in range(-1, 2):
            for delta_col in range(-1, 2):
                if delta_row == 0 and delta_col == 0:
                    continue
                neighbor_row = row + delta_row
                if not (0 <= neighbor_row < self.height):
                    continue
                neighbor_col = col + delta_col
                if not (0 <= neighbor_col < self.width):
                    continue
                yield self[neighbor_row, neighbor_col]

    def _to_index(self, row: int, col: int):
        """Convert (row, col) to list index.

        :param row: the row.
        :param col: the column.
        :return: the list index.
        """
        return row * self.width + col

    def print(self):
        """Pretty print this board."""
        for row in range(self.height):
            for col in range(self.width):
                print(self[row, col].letter, end=" ")
            print(end="\n")

    def is_spangram(self, word) -> bool:
        """Check if the given word is a spangram.

        A spangram is a word that spans the entire board, either horizontally or vertically.
        A word is a spangram if it touches the left and right edges of the board, or the top and bottom edges.

        :param word: list of BoardNode objects.
        :return: whether the word is a spangram.
        """
        top, bottom, left, right = False, False, False, False
        for node in word:
            if node.row == 0:
                top = True
            elif node.row == self.height - 1:
                bottom = True
            if node.col == 0:
                left = True
            elif node.col == self.width - 1:
                right = True
        return (top and bottom) or (left and right)


class BoardNode:
    def __init__(self, letter: str, row: int, col: int):
        self.letter = letter
        self.row = row
        self.col = col
        self.neighbors = []

    def __repr__(self):
        return f"<BoardNode (letter={self.letter}, row={self.row}, col={self.col}, neighbors={list(map(str, self.neighbors))})>"

    def __str__(self):
        return self.letter
