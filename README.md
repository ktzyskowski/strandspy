# strands.py

This repository contains source code for my solution to solving the NYT Strands game, using tries and some smart brute
force.

### Install

```shell
pip install playwright
playwright install
```

### Usage

See `main.py` for usage

You can run the solver on today's puzzle using:

```shell
python main.py
```

### Known Issues

- If a spangram is two words, and one of the words is less than 4 characters but the spangram is 4 or more characters,
  it is not found. This needs to be fixed in the logic for loading words into the trie, and how the spangrams are
  constructed prior to search
