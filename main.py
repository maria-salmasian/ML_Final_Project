import re
from collections import Counter


# for the keyboard https://www.branah.com/armenian


class ArmenianSpellChecker:
    def __init__(self):
        self.word_probs = Counter()
        self.total_words = 0
        self.keyboard_layout = {
            'ա': 'խսզ', 'բ': 'ւկհն', 'գ': 'ցտֆւ', 'դ': 'րֆկե', 'ե': 'դկհը',
            'զ': 'ցաս', 'է': 'յվստր', 'ը': 'եհճի', 'թ': 'լղծփչպ', 'ժ': 'ռչջ',
            'ի': 'ըճքո', 'լ': 'ոպթղշք', 'խ': 'վձա', 'ծ': 'ղթփ', 'կ': 'ֆդեհբւ',
            'հ': 'կեըճնբ', 'ձ': 'յվխ', 'ղ': 'շլթծ', 'ճ': 'ըիքմնհ', 'մ': 'նճքշ',
            'յ': 'ձվէ', 'ն': 'բհճմ', 'շ': 'մքլղ', 'ո': 'իքլպօ', 'չ': 'ռպթփջժ',
            'պ': 'ոօռչթլ', 'ջ': 'ժչփ', 'ռ': 'օպչժ', 'ս': 'ավէտցզ', 'վ': 'ձյէսախ',
            'տ': 'էրֆգցս', 'ր': 'էտֆդ', 'ց': 'զստգ', 'ւ': 'գֆկբ', 'փ': 'ջչթծ',
            'ք': 'իոլշմճ', 'և': '', 'օ': 'ռպոի', 'ֆ': 'րդկւգտ'
        }


    def calculate_keyboard_distance(self, word1, word2):
        distance = sum(char1 != char2 and char2 not in self.keyboard_layout.get(char1, '') for char1, char2 in zip(word1, word2))
        return distance

    def preprocess_word(self, word):
        return word.lower()


    def train(self, dataset):
        p_dataset = re.sub(r"[՛։—՞՝«»…,]", '', dataset).split()

        # print(p_dataset)

        for word in p_dataset:
            preprocessed_word = self.preprocess_word(word)
            # print(preprocessed_word)
            self.word_probs[preprocessed_word] += 1
            self.total_words += 1

    def get_candidates(self, word, max_edits):
        candidates = set()
        candidates.add(word)

        for _ in range(max_edits):
            new_candidates = set()

            for candidate in candidates:
                new_candidates.update(self.generate_edits(candidate))

            candidates.update(new_candidates)

        return candidates


    def generate_edits(self, word):
        candidates = set()
        for i in range(len(word) - 1):
            char1, char2 = word[i], word[i + 1]
            for char in ArmenianSpellChecker.get_alphabet():
                # Insertion
                candidate = word[:i] + char + char1 + char2 + word[i + 2:]
                candidates.add(candidate)
                # Deletion
                candidate = word[:i] + char2 + word[i + 2:]
                candidates.add(candidate)
                # Substitution
                candidate = word[:i] + char + char2 + word[i + 2:]
                candidates.add(candidate)
                # Transposition
                candidate = word[:i] + char2 + char1 + word[i + 2:]
                candidates.add(candidate)
        # split
        for i in range(1, len(word)):
            prefix = word[:i]
            suffix = word[i:]
            candidates.add(prefix + " " + suffix)
        return candidates


    # def get_correction(self, word, max_edits):
    #     candidates = self.get_candidates(word, max_edits)
    #     best_correction = None
    #     max_prob = 0
    #
    #     for candidate in candidates:
    #         candidate_prob = self.word_probs[candidate]
    #         if candidate_prob > max_prob:
    #             best_correction = candidate
    #             max_prob = candidate_prob
    #
    #     return best_correction

    def get_correction(self, word, max_edits):
        candidates = self.get_candidates(word, max_edits)
        best_correction = None
        max_prob = 0
        min_distance = float('inf')

        for candidate in candidates:
            candidate_prob = self.word_probs[candidate]
            candidate_distance = self.calculate_keyboard_distance(word, candidate)
            # print("candidate ", candidate , " word: ", word ,  " min dist: " , min_distance)

            if candidate_prob > max_prob or (candidate_prob == max_prob and candidate_distance < min_distance):
                best_correction = candidate
                max_prob = candidate_prob
                min_distance = candidate_distance

        return best_correction

    def spell_check(self, word, max_edits):
        preprocessed_word = self.preprocess_word(word)

        if preprocessed_word in self.word_probs:
            return word  # Word is correct

        correction = self.get_correction(preprocessed_word, max_edits)

        return correction

    @staticmethod
    def get_alphabet():
        alphabet = "աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցոչփքևօֆւ"
        return alphabet


# Example usage:
if __name__ == '__main__':
    # Create an instance of the spell checker
    spell_checker = ArmenianSpellChecker()

    # Train the spell checker with your dataset
    dataset = open('karusel.txt').read()

    # print(dataset)
    spell_checker.train(dataset)

    # Test the spell checker
    misspelled_word = "Pրդյ ոք"
    correction = spell_checker.spell_check(misspelled_word, 2)
    print(correction)
