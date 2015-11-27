#!/usr/bin/env python
# -*- code: utf-8 -*-
from __future__ import print_function

import sys
import re
import random


class RegexCrosswordGenerator(object):
    """
    Class for generating the regular expressions for a grid.
    """

    ALLOWED_CHARACTERS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                          "1234567890")

    def __init__(self, width=2, height=2):
        self._w = width
        self._h = height
        grid = self._generate_grid(width, height)
        rows = [""] * height
        cols = [""] * width
        for i in xrange(height):
            rows[i] = self._regex_from_string(grid[i])
        for i in xrange(width):
            cols[i] = self._regex_from_string(
                "".join(map(lambda x: x[i], grid)))
        self._rows = rows
        self._cols = cols
        self._grid = grid

        # Just make sure the regex generated from the grid
        # works with the grid itself.
        assert self.validate_solution(grid)

    @property
    def possible_solution(self):
        return self._grid

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    def _generate_grid(self, w, h):
        """
        Generate a grid of random characters.
        This will be one of the possible solutions to the
        crossword.
        """
        grid = []
        for i in xrange(h):
            grid.append("".join(random.sample(self.ALLOWED_CHARACTERS, w)))
        return grid

    def _alternate_string(self, string):
        """
        Generate a random string that is different
        and the same length as the given string.
        """
        length = len(string)
        diff_str = "".join(random.sample(self.ALLOWED_CHARACTERS, length))
        while diff_str == string:
            diff_str = "".join(random.sample(self.ALLOWED_CHARACTERS, length))
        return diff_str

    def _pattern1(self, string, count=3):
        """
        Pat1|Pat2|Pat3
        """
        pos = random.randint(0, count - 1)
        patterns = []
        for i in xrange(count):
            if i == pos:
                patterns.append(string)
            else:
                patterns.append(self._alternate_string(string))
        return "|".join(patterns)

    def _regex_from_string(self, string):
        """
        Generate the regex for a given string.
        """
        return re.compile(self._pattern1(string))

    def validate_solution(self, solution):
        """
        Check that a solution works for the rows and cols.
        """
        for i in xrange(len(self._rows)):
            m = self._rows[i].match(solution[i].upper())
            if not m or len(m.group(0)) != self._w:
                return False

        for i in xrange(len(self._cols)):
            m = self._cols[i].match(
                reduce(lambda x, y: x + y[i], solution, "").upper())
            if not m or len(m.group(0)) != self._h:
                return False

        return True


def main():
    x = RegexCrosswordGenerator(4, 7)
    print("Rows:", map(lambda x: x.pattern, x.rows))
    print("Cols:", map(lambda x: x.pattern, x.cols))
    print("Possible solution:")
    print("\n".join(x.possible_solution))
    return 0


if __name__ == "__main__":
    sys.exit(main())
