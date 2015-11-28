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
        self.reset(width, height)

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

    def reset(self, width, height):
        """
        Create a new crossword.
        """
        assert width >= 2 and height >= 2

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
        try:
            assert self.validate_solution(grid)
        except AssertionError:
            print("\n".join([
                "The solution:",
                "\n".join(grid),
                "does not work for the given rows and cols.",
                "Rows:",
                "\n".join(map(lambda x: x.pattern, rows)),
                "Cols:",
                "\n".join(map(lambda x: x.pattern, cols))
            ]), file=sys.stderr)
            raise AssertionError

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

    def _regex_from_string(self, string):
        """
        Generate the regex for a given string.
        """
        patterns = [
            self._pattern1, self._pattern2, self._pattern3, self._pattern4,
            self._pattern5, self._pattern6, self._pattern7, self._pattern8,
            self._pattern9, self._pattern10
        ]
        end = random.choice("+*")
        return re.compile(random.choice(patterns)(string, end=end))

    def run_many_times(self, n=1000):
        """
        Create many crosswords to make sure the patterns work.
        """
        for i in xrange(n):
            self.reset(self.width, self.height)

    ##########################################
    # PATTERNS GO PAST THIS POINT
    ##########################################

    def _pattern1(self, string, length=3, **kwargs):
        """
        Pat1|Pat2|Pat3
        """
        pos = random.randint(0, length - 1)
        patterns = []
        for i in xrange(length):
            if i == pos:
                patterns.append(string)
            else:
                patterns.append(self._alternate_string(string))
        return "|".join(patterns)

    def _pattern2(self, string, end="+", **kwargs):
        """
        [ccc...](end)
        """
        return "[" + "".join(sorted(set(string))) + "]" + end

    def _pattern3(self, string, length=5, end="+", **kwargs):
        """
        [^ccc...](end)
        """
        chars = set(self.ALLOWED_CHARACTERS) - set(string)
        chars = random.sample(chars, length)
        return "[^" + "".join(sorted(chars)) + "]" + end

    def _pattern4(self, string, end="*", **kwargs):
        """
        Pat1|Pat2|c(end)
        """
        return (self._pattern1(string, 2) + "|" +
                random.choice(self.ALLOWED_CHARACTERS) + end)

    def _pattern5(self, string, start="*", end="*", **kwargs):
        """
        .(start)c1?c2.(end)
        """
        rand_c1 = random.choice(self.ALLOWED_CHARACTERS)
        if len(string) == 2:
            rand_place = random.randint(0, 2)
            if rand_place == 0:
                return ".+" + rand_c1 + "?" + string[1] + ".*"
            elif rand_place == 1:
                return ".*" + string[0] + "?" + string[1] + ".*"
            else:
                return ".*" + rand_c1 + "?" + string[0] + ".+"
        elif len(string) == 3:
            use_optional = random.randint(0, 1)
            if use_optional:
                return random.choice([
                    ".*" + string[0] + "?" + string[1] + ".+",
                    ".+" + string[1] + "?" + string[2] + ".*"
                ])
            else:
                return ".+" + rand_c1 + "?" + string[1] + ".+"
        else:
            use_c1 = random.randint(0, 1)
            start_offset = 1 if start is "+" else 0
            end_offset = len(string) - (2 if end is "+" else 1)
            if use_c1:
                i1 = random.randint(start_offset, end_offset - 1)
                i2 = random.randint(i1, end_offset)
                return ".{}{}?{}.{}".format(start, string[i1], string[i2], end)
            else:
                c2 = string[random.randint(start_offset, end_offset)]
                return ".{}{}?{}.{}".format(start, rand_c1, c2, end)

    def _pattern6(self, string, **kwargs):
        """
        [ccc...]+.
        """
        cutoff = random.randint(1, len(string) / 2)
        if cutoff < 3:
            end = "+" + "." * cutoff
        else:
            end = "+" + ".{" + str(cutoff) + "}"
        return self._pattern2(string[:len(string) - cutoff], end=end)

    def _pattern7(self, string, **kwargs):
        """
        [ccc...]+.*(cutoff)cc(cutoff2)
        """
        if len(string) < 3:
            return self._pattern6(string)
        else:
            cutoff1 = len(string) / 2
            cutoff2 = random.randint(cutoff1 + 1, len(string) - 1)
            return (self._pattern2(string[:cutoff1], end=".+") +
                    self._pattern2(string[cutoff2:]))

    def _pattern8(self, string, **kwargs):
        """
        [ccc...](cutoff)(Pat1|Pat2|Pat3)
        """
        if len(string) < 4:
            return self._pattern1(string)
        else:
            cutoff = random.randint(2, len(string) - 2)
            return (self._pattern2(string[:cutoff]) +
                    "(" + self._pattern1(string[cutoff:]) + ")")

    def _pattern9(self, string, **kwargs):
        """
        (Pat1|Pat2|Pat3)[ccc...](cutoff)
        """
        if len(string) < 4:
            return self._pattern1(string)
        else:
            cutoff = random.randint(2, len(string) - 2)
            return ("(" + self._pattern1(string[:cutoff]) + ")" +
                    self._pattern2(string[cutoff:]))

    def _pattern10(self, string, **kwargs):
        """
        c(.)c(.)ccc\1cc\2
        """
        duplicates = set(filter(lambda x: string.count(x) > 1, string))
        if duplicates:
            # String contains duplicate chars
            pattern = ""
            count = 0
            starting_pos = dict(zip(duplicates, [0] * len(duplicates)))
            for i in xrange(len(string)):
                c = string[i]
                if c in duplicates and not starting_pos[c]:
                    pattern += "(.)"
                    count += 1
                    starting_pos[c] = count
                elif c in duplicates and starting_pos[c]:
                    pattern += "\\" + str(starting_pos[c])
                    if i < len(string) - 1 and string[i + 1].isdigit():
                        pattern += ".*"
                else:
                    pattern += c
            return pattern
        else:
            # String contains all unique characters
            return self._pattern9(string)


def main():
    x = RegexCrosswordGenerator(2, 4)
    x.run_many_times()
    return 0


if __name__ == "__main__":
    sys.exit(main())
