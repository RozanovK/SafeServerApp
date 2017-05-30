import random
import time
import interfaces
import difflib


class Password(object):


    def __init__(self, minLength=8, maxLength=12, groupMax=6,
                 maxSimilarity=0.6, seed=None,
                 minLowerLetter=None, minUpperLetter=None, minDigits=None,
                 minSpecials=None, minOthers=None,
                 minUniqueCharacters=None, minUniqueLetters=None):
        self.minLength = minLength
        self.maxLength = maxLength
        self.groupMax = groupMax
        self.maxSimilarity = maxSimilarity
        self.random = random.Random(seed or time.time())
        self.minLowerLetter = minLowerLetter
        self.minUpperLetter = minUpperLetter
        self.minDigits = minDigits
        self.minSpecials = minSpecials
        self.minOthers = minOthers
        self.minUniqueCharacters = minUniqueCharacters
        self.minUniqueLetters = minUniqueLetters

    def _checkSimilarity(self, new, ref):
        similarity = difflib.SequenceMatcher(None, new, ref).ratio()
        if similarity > self.maxSimilarity:
            raise interfaces.TooSimilarPassword(
                similarity=similarity, maxSimilarity=self.maxSimilarity)

    def verify(self, new, ref=None):
        if not new:
            raise interfaces.NoPassword()
        if len(new) < self.minLength:
            raise interfaces.TooShortPassword(minLength=self.minLength)
        if len(new) > self.maxLength:
            raise interfaces.TooLongPassword(maxLength=self.maxLength)
        if ref is not None:
            self._checkSimilarity(new, ref)
        num_lower_letters = 0
        num_upper_letters = 0
        num_digits = 0
        num_specials = 0
        num_others = 0
        uniqueChars = set()
        uniqueLetters = set()
        for char in new:
            uniqueChars.add(char.lower())
            if char in self.LOWERLETTERS:
                num_lower_letters += 1
                uniqueLetters.add(char.lower())
            elif char in self.UPPERLETTERS:
                num_upper_letters += 1
                uniqueLetters.add(char.lower())
            elif char in self.DIGITS:
                num_digits += 1
            elif char in self.SPECIALS:
                num_specials += 1
            else:
                num_others += 1
        if (num_lower_letters > self.groupMax or
            num_upper_letters > self.groupMax or
            num_digits > self.groupMax or
            num_specials > self.groupMax or
            num_others > self.groupMax):
            raise interfaces.TooManyGroupCharacters(
                groupMax=self.groupMax)

        if (self.minLowerLetter is not None
            and num_lower_letters < self.minLowerLetter):
            raise interfaces.TooFewGroupCharactersLowerLetter(
                        minLowerLetter=self.minLowerLetter)

        if (self.minUpperLetter is not None
            and num_upper_letters < self.minUpperLetter):
            raise interfaces.TooFewGroupCharactersUpperLetter(
                        minUpperLetter=self.minUpperLetter)

        if (self.minDigits is not None
            and num_digits < self.minDigits):
            raise interfaces.TooFewGroupCharactersDigits(
                        minDigits=self.minDigits)

        if (self.minSpecials is not None
            and num_specials < self.minSpecials):
            raise interfaces.TooFewGroupCharactersSpecials(
                        minSpecials=self.minSpecials)

        if (self.minOthers is not None
            and num_others < self.minOthers):
            raise interfaces.TooFewGroupCharactersOthers(
                        minOthers=self.minOthers)

        if (self.minUniqueCharacters is not None
            and len(uniqueChars) < self.minUniqueCharacters):
            raise interfaces.TooFewUniqueCharacters(
                        minUniqueCharacters=self.minUniqueCharacters)

        if (self.minUniqueLetters is not None
            and len(uniqueLetters) < self.minUniqueLetters):
            raise interfaces.TooFewUniqueLetters(
                        minUniqueLetters=self.minUniqueLetters)

        return
