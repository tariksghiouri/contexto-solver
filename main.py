import nltk
nltk.download('wordnet')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import requests
import random
from nlp import get_english_words

def get_feedback(driver, word):
    input_element = driver.find_element(By.CLASS_NAME, "word")
    input_element.clear()
    input_element.send_keys(word)
    input_element.send_keys(Keys.RETURN)
    time.sleep(1)  # Wait for the feedback to be processed

    # Check if the word is recognized
    try:
        error_message = driver.find_element(By.CSS_SELECTOR, "div.message").text
        if "I'm sorry, I don't know this word" in error_message:
            print(f"Word '{word}' is not recognized by the game.")
            return None
    except:
        pass

    feedback_element = driver.find_element(By.CSS_SELECTOR, "#root > div > main > div.message > div > div > div.row > span:nth-child(2)")
    feedback = int(feedback_element.text.strip())
    return feedback

def get_similar_words_online(word, topn=10):
    # Use the Datamuse API to get similar words
    response = requests.get(f"https://api.datamuse.com/words?ml={word}&max={topn}")
    if response.status_code == 200:
        similar_words = [item['word'] for item in response.json()]
        return similar_words
    else:
        return []

def click_hint_button(driver):
    # Click the button to open the hint dropdown
    hint_button = driver.find_element(By.CSS_SELECTOR, "html body div#root div.wrapper.top-ad-padding main div.top-bar div button.btn")
    hint_button.click()
    time.sleep(1)  # Wait for the dropdown to open

    # Click the second element in the dropdown to get a hint
    hint_dropdown = driver.find_element(By.CSS_SELECTOR, "html body div#root div.wrapper.top-ad-padding main div.top-bar div div.dropdown button.menu-item:nth-child(2)")
    hint_dropdown.click()
    time.sleep(1)  # Wait for the hint to be processed

    # Retrieve the hint word
    hint_element = driver.find_element(By.CSS_SELECTOR, "div.message")
    hint_text = hint_element.text.split()[-1]  # Assuming the hint word is the last word in the message
    if hint_text.isalpha():
        print(f"Hint word: {hint_text}")
        return hint_text
    else:
        print(f"Hint '{hint_text}' is not a valid word. Using a random word instead.")
        return random.choice(get_english_words())

def automate_browser(url, input_class):
    # Specify the path to the Firefox binary if it's not in the default location
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Replace with your actual path to Firefox

    # Update the path below if the WebDriver is not in your PATH
    service = Service(executable_path='./driver/geckodriver.exe')  # Use GeckoDriver for Firefox
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # Open the specified URL
        driver.get(url)

        # Wait for the input field to be present on the page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, input_class))
        )

        # Get the initial hint
        hint_word = click_hint_button(driver)

        # Dynamically generate words similar to the hint
        similar_words = get_similar_words_online(hint_word, topn=100)

        if not similar_words:
            similar_words = get_english_words()  # Fallback to the original list if no similar words are found

        random_word = random.choice(similar_words)
        feedback = get_feedback(driver, random_word)

        while feedback != 1:
            if feedback is None:  # Skip unrecognized words
                random_word = random.choice(similar_words)
                feedback = get_feedback(driver, random_word)
                continue

            print(f"Guessed word: {random_word}, Feedback: {feedback}")
            next_word = random.choice(similar_words)
            feedback = get_feedback(driver, next_word)
            random_word = next_word

        print("Game solved! The secret word is:", random_word)

    finally:
        # This line is commented out so that the browser window doesn't close automatically
        # driver.quit()
        pass

if __name__ == "__main__":
    # Replace these values with your specific URL and input class
    website_url = "https://contexto.me/"
    input_class = "word"

    automate_browser(website_url, input_class)
