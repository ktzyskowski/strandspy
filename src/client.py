from playwright.sync_api import sync_playwright

from words import Word


class StrandsClient:
    """A web client that interacts with the NYT games website to play Strands.

    Used to check if words are valid or not.
    """

    def __init__(self, width: int = 6, height: int = 8, headless: bool = True):
        self.width = width
        self.height = height
        self.headless = headless

    def __enter__(self):
        # init browser and navigate to strands page
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.page.goto("https://www.nytimes.com/games/strands")
        self.page.evaluate("document.body.style.zoom=0.3")

        # press play button
        self.page.get_by_test_id("moment-btn-play").click()
        # dismiss help modal
        self.page.get_by_test_id("modal-close").click()

        # get letters
        self.letters = self.page.get_by_test_id("strands-board").text_content().lower()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.close()
        self.playwright.stop()

    def _to_index(self, row: int, col: int):
        """Convert (row, col) to list index.

        :param row: the row.
        :param col: the column.
        :return: the list index.
        """
        return row * self.width + col

    def input_word(self, word: Word) -> bool:
        """Enter a word on the board.

        :param word: the word to enter.
        :return: True if the word inputted is included in the solution set, False otherwise.
        """
        for node in word + [word[-1]]:  # duplicate last letter to simulate double click
            index = self._to_index(node.row, node.col)
            self.page.locator(f"#button-{index}").click()
        # check background color of buttons pressed to see if it was valid
        # (yellow: spangram / blue: theme word)
        locator = self.page.locator(f"#button-{self._to_index(word[0].row, word[0].col)}")
        if style := locator.get_attribute("style"):
            if "--strands-blue" in style:
                return True
            elif "--text-spangram" in style:
                return True
        return False
