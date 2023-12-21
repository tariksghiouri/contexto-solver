from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from nltk.corpus import wordnet
import nltk

def get_english_words():
    english_words = set()
    for synset in list(wordnet.all_synsets()):
        for lemma in synset.lemmas():
            word = lemma.name().lower()
            # Check if the word has only one word (no spaces) and consists only of alphabetic characters
            if ' ' not in word and word.isalpha():
                english_words.add(word)
    return list(english_words)
    
def automate_browser(url, input_class, words_to_type):
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    try:
        # Open the specified URL
        driver.get(url)

        # Wait for the input field to be present on the page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, input_class))
        )

        # Find the input field by class name using By.CLASS_NAME
        input_element = driver.find_element(By.CLASS_NAME, input_class)

        # Loop through the array of words
        for word in words_to_type:
            # Type the current word into the input field
            input_element.send_keys(word)

            # Simulate pressing Enter
            input_element.send_keys(Keys.RETURN)

            # Wait for a few seconds to see the result (you can adjust this time)
            time.sleep(1)

            # Clear the input field for the next word (optional)
            input_element.clear()

    finally:
        # This line is commented out so that the browser window doesn't close automatically
        # driver.quit()
        pass

if __name__ == "__main__":
    # Replace these values with your specific URL, input class, and array of words
    website_url = "https://contexto.me/"
    input_class = "word"
    words_to_type = get_english_words()

    automate_browser(website_url, input_class, words_to_type)
