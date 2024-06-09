from nltk.corpus import wordnet

def get_english_words():
    english_words = set()
    for synset in list(wordnet.all_synsets()):
        for lemma in synset.lemmas():
            word = lemma.name().lower()
            # Check if the word has only one word (no spaces) and consists only of alphabetic characters
            if ' ' not in word and word.isalpha():
                english_words.add(word)
    return list(english_words)

word_list = get_english_words()
print(word_list)
