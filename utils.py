import random
from collections import deque, defaultdict


class Buffer(object):

    """
    Uses a deque (double-ended queue) to hold k=2 objects at a time.
    collections.deque has O(1) push and pop operations.
    """

    def __init__(self, k=2):
        self.k = k
        self._deque = deque()

    def push(self, word):
        """
        Adds a word to the deque. If the push would make the deque
        larger than k, then the oldest element is removed.
        Returns True if the buffer is full
        """
        if len(self._deque) == self.k:
            self._deque.popleft()

        self._deque.append(word)
        return len(self._deque) == self.k

    def contents(self):
        """ Returns a k-tuple containing the contents of self._deque. """
        return tuple(word for word in self._deque)


class MarkovDB(object):

    """
    Stores a 2-d dictionary (self.d) which counts how many times
    word pairs have appeared. Probabilities (self.p) are calculated
    after the file is read.
    d = {
        "artificial": {
                "intelligence": 1,
                "tree"        : 1,
                "sweetener"   : 1
            },
        "frosted"   : {
                "flakes" : 1,
            }
        }
    """

    def __init__(self, filename):
        self.d = {}
        self.p = {}

        with open(filename) as f:
            b = Buffer()

            for word in f.read().split():
                word = word.lower().strip()

                # If the buffer is 'full' (there are 2 words), then
                # it contains a tuple we can parse
                full = b.push(word)

                if (full):
                    w1, w2 = b.contents()
                    self.add(w1, w2)

        self._generate_probabilities()

    def add(self, w1, w2):
        """ Adds w1, w2 to the dictionary. w2 follows w1. """
        root = self.d

        if not root.get(w1):
            root[w1] = defaultdict(int)

        root = root[w1]
        root[w2] += 1

    def _generate_probabilities(self):
        """
        Builds self.p with the same structure as self.d, but calculates
        probabilities (part/whole) instead of counting occurrances.
        """
        for word, candidates in self.d.items():
            self.p[word] = {}

            if (candidates):
                whole = sum(candidates.values())

            # Now calculate the probability of each candidate (part/whole)
            for candidate, part in candidates.items():
                self.p[word][candidate] = part / whole

    def query(self, word):
        candidates = self.p.get(word.lower())
        if not candidates:
            print('\nFail to find {} in text (probability=0)'.format(word))
            return

        # Use random sampling to generate the next word
        next_word = self._next(word, candidates)
        print("\nPossible word pair:")
        print("{} {} (probability {})\n".format(
            word, next_word, candidates[next_word]))

        # Now print all possible pairs
        print("All word pairs with probability > 0:")
        for candidate, probability in candidates.items():
            print("{} {} (probability={})".format(
                word, candidate, probability))

    def _next(self, word, candidates, sample_size=100):
        sampling = []
        for candidate, probability in candidates.items():
            for i in range(int(sample_size * probability)):
                sampling.append(candidate)

        return random.choice(sampling)
