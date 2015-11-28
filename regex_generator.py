#!/usr/bin/env python
# -*- code: utf-8 -*-
from __future__ import print_function

import sys
import re
import random

from flask import current_app


class RegexCrosswordGenerator(object):
    """
    Class for generating the regular expressions for a grid.
    """

    ALLOWED_CHARACTERS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                          "1234567890")

    def __init__(self, width=2, height=2, use_real_words=False,
                 textfile="texts/words.txt"):
        self.reset(width, height, use_real_words=use_real_words,
                   textfile=textfile)

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
    def rows2(self):
        return self._rows2

    @property
    def cols2(self):
        return self._cols2

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    def reset(self, width, height, use_real_words=False,
              textfile="texts/words.txt"):
        """
        Create a new crossword.
        """
        assert width >= 2 and height >= 2

        self._w = width
        self._h = height
        grid = self._generate_grid(
            width, height, use_real_words=use_real_words, textfile=textfile)
        rows = [""] * height
        cols = [""] * width
        rows2 = [""] * height
        cols2 = [""] * width
        for i in xrange(height):
            rows[i] = self._regex_from_string(grid[i])
            rows2[i] = self._regex_from_string(grid[i])
            while rows[i] == rows2[i]:
                rows2[i] = self._regex_from_string(grid[i])
        for i in xrange(width):
            col = "".join(map(lambda x: x[i], grid))
            cols[i] = self._regex_from_string(col)
            cols2[i] = self._regex_from_string(col)
            while cols[i] == cols2[i]:
                cols2[i] = self._regex_from_string(col)
        self._rows = rows
        self._cols = cols
        self._rows2 = rows2
        self._cols2 = cols2
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
                "\n".join(map(lambda x: x.pattern, cols)),
                "Rows2:",
                "\n".join(map(lambda x: x.pattern, rows2)),
                "Cols2:",
                "\n".join(map(lambda x: x.pattern, cols2))
            ]), file=sys.stderr)
            raise AssertionError

    def _generate_grid(self, w, h, use_real_words=False,
                       textfile="texts/words.txt"):
        """
        Generate a grid of random characters.
        This will be one of the possible solutions to the
        crossword.
        """
        grid = []
        if use_real_words:
            with current_app.open_resource(textfile) as f:
                used_words = set()
                text = f.read().split()
                s = ""
                word = random.choice(text).strip().upper()
                while len(s) < w * h:
                    if word.isalnum() and word not in used_words:
                        s += word
                        used_words.add(word)
                    word = random.choice(text).strip().upper()
                for i in xrange(h):
                    grid.append(s[:w])
                    s = s[w:]
        else:
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
            row = solution[i].upper()
            m = self._rows[i].match(row)
            if not m or len(m.group(0)) != self._w:
                print("The pattern {} does not work for row {}"
                      .format(self._rows[i].pattern, row))
                return False
            m = self._rows2[i].match(row)
            if not m or len(m.group(0)) != self._w:
                print("The pattern {} does not work for row {}"
                      .format(self._rows2[i].pattern, row))
                return False

        for i in xrange(len(self._cols)):
            col = reduce(lambda x, y: x + y[i], solution, "").upper()
            m = self._cols[i].match(col)
            if not m or len(m.group(0)) != self._h:
                print("The pattern {} does not work for col {}"
                      .format(self._col[i].pattern, col))
                return False
            m = self._cols2[i].match(col)
            if not m or len(m.group(0)) != self._h:
                print("The pattern {} does not work for col {}"
                      .format(self._col2[i].pattern, col))
                return False

        return True

    def _regex_from_string(self, string):
        """
        Generate the regex for a given string.
        """
        patterns = [
            self._pattern1, self._pattern2, self._pattern3, self._pattern4,
            self._pattern5, self._pattern6, self._pattern7, self._pattern8,
            self._pattern9, self._pattern10, self._pattern11, self._pattern12,
            self._pattern13, self._pattern14, self._pattern15, self._pattern16,
            self._pattern17, self._pattern18
        ]
        end = random.choice("+*")
        return re.compile(random.choice(patterns)(string, end=end))

    def run_many_times(self, n=10000):
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
        if len(string) > 5:
            return self._pattern5(string)

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
        if len(string) > 5:
            return self._pattern5(string)
        c = random.choice(self.ALLOWED_CHARACTERS)  # Add a random character
        return "[" + "".join(sorted(set(string + c))) + "]" + end

    def _pattern3(self, string, length=4, end="+", **kwargs):
        """
        [^ccc...](end)
        """
        if len(string) > 5:
            return self._pattern5(string)
        c = random.choice(self.ALLOWED_CHARACTERS)  # Add a random character
        chars = set(self.ALLOWED_CHARACTERS) - set(string + c)
        chars = random.sample(chars, length)
        return "[^" + "".join(sorted(chars)) + "]" + end

    def _pattern4(self, string, end="*", **kwargs):
        """
        Pat1|Pat2|c(end)
        """
        if len(string) > 5:
            return self._pattern18(string)
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

    def _pattern11(self, string, **kwargs):
        """
        [^ccc...]+.
        """
        cutoff = random.randint(1, len(string) / 2)
        if cutoff < 3:
            end = "+" + "." * cutoff
        else:
            end = "+" + ".{" + str(cutoff) + "}"
        return self._pattern3(string[:len(string) - cutoff], end=end)

    def _pattern12(self, string, **kwargs):
        """
        [^ccc...]+.*(cutoff)cc(cutoff2)
        """
        if len(string) < 3:
            return self._pattern6(string)
        else:
            cutoff1 = len(string) / 2
            cutoff2 = random.randint(cutoff1 + 1, len(string) - 1)
            return (self._pattern3(string[:cutoff1], end=".+") +
                    self._pattern2(string[cutoff2:]))

    def _pattern13(self, string, **kwargs):
        """
        [^ccc...](cutoff)(Pat1|Pat2|Pat3)
        """
        if len(string) < 4:
            return self._pattern1(string)
        else:
            cutoff = random.randint(2, len(string) - 2)
            return (self._pattern3(string[:cutoff]) +
                    "(" + self._pattern1(string[cutoff:]) + ")")

    def _pattern14(self, string, **kwargs):
        """
        (Pat1|Pat2|Pat3)[^ccc...](cutoff)
        """
        if len(string) < 4:
            return self._pattern1(string)
        else:
            cutoff = random.randint(2, len(string) - 2)
            return ("(" + self._pattern1(string[:cutoff]) + ")" +
                    self._pattern3(string[cutoff:]))

    def _pattern15(self, string, end="+", **kwargs):
        """
        (c|Pat1|Pat2)(end)
        """
        duplicates = set(filter(lambda x: string.count(x) > 1, string))
        if duplicates and len(set(string)) > 2:
            c = duplicates.pop()
            chunks = filter(lambda x: bool(x), string.split(c) + [c])
            return "(" + "|".join(chunks) + ")" + end
        else:
            return "(" + self._pattern1(string) + ")"

    def _pattern16(self, string, start="+", end="*", **kwargs):
        """
        [ccc...](start)[ccc...](end)
        [^ccc...](start)[ccc...](end)
        [ccc...](start)[^ccc...](end)
        [^ccc...](start)[^ccc...](end)
        """
        if len(string) < 4:
            return self._pattern5(string)
        else:
            cutoff = random.randint(2, len(string) - 2)
            if random.randint(0, 1):
                first = self._pattern2(string[:cutoff], end=start)
            else:
                first = self._pattern3(string[:cutoff], end=start)
            if random.randint(0, 1):
                last = self._pattern2(string[cutoff:], end=end)
            else:
                last = self._pattern3(string[cutoff:], end=end)
            return first + last

    def _pattern17(self, string, start="+", end="+", **kwargs):
        """
        [ccc...](start)c?[ccc...](end)
        [ccc...](start).?[ccc...](end)
        Pattern 16 with optional char in middle.
        """
        if len(string) < 5:
            return self._pattern5(string)
        elif random.randint(0, 1):
            # Do not use char
            cutoff = random.randint(2, len(string) - 2)
            if random.randint(0, 1):
                first = self._pattern2(string[:cutoff], end=start)
            else:
                first = self._pattern3(string[:cutoff], end=start)
            if random.randint(0, 1):
                last = self._pattern2(string[cutoff:], end=end)
            else:
                last = self._pattern3(string[cutoff:], end=end)
            if random.randint(0, 1):
                c = random.choice(self.ALLOWED_CHARACTERS)
            else:
                c = "."
            return first + c + "?" + last
        else:
            cutoff = random.randint(2, len(string) - 3)
            if random.randint(0, 1):
                c = string[cutoff]
            else:
                c = "."
            if random.randint(0, 1):
                first = self._pattern2(string[:cutoff], end=start)
            else:
                first = self._pattern3(string[:cutoff], end=start)
            if random.randint(0, 1):
                last = self._pattern2(string[cutoff + 1:], end=end)
            else:
                last = self._pattern3(string[cutoff + 1:], end=end)
            return first + c + "?" + last

    def _pattern18(self, string, **kwargs):
        """
        [ccc...]*/+.*/+[ccc...]*/+
        .*/+[ccc...]*/+[ccc...]*/+
        [ccc...]*/+[ccc...]*/+.*/+

        Any combination of size 3 for:
        [ccc...]*/+, [^ccc...]*/+
        .*/+, (Pat1|Pat2|Pat3) (pattern 15)
        """
        if len(string) < 6:
            return self._pattern17(string)
        else:
            chunks = [
                string[:len(string) / 3],
                string[len(string) / 3:len(string) * 2 / 3],
                string[len(string) * 2 / 3:]
            ]
            patterns = ["", "", ""]
            for i in xrange(3):
                end = "+" if random.randint(0, 1) else "*"
                patterns[i] = random.choice([
                    self._pattern2(chunks[i], end=end),
                    self._pattern3(chunks[i], end=end),
                    "." + end,
                    "(" + self._pattern1(chunks[i]) + ")"
                ])
            return "".join(patterns)


def main():
    x = RegexCrosswordGenerator(2, 4)
    x.run_many_times()
    x = RegexCrosswordGenerator(2, 4, use_real_words=True)
    x.run_many_times()
    return 0


if __name__ == "__main__":
    sys.exit(main())
