from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# template:
# #separator:tab
# #html:true
# #tags column:8
# Po    Detektiv Parzival Po    p+o     red     1s      Hintern         (jp)vocab_n5
# # tgt sentence                reading pitch   acc p   definition  scr tag


def scrape(browser, link):
    level = link.split('-')[-2]
    print('opening: ' + link)
    browser.get(link)
    peaks = browser.find_elements(By.CSS_SELECTOR, '.pitch-char:last-child')
    definitions = browser.find_elements(By.CLASS_NAME, 'vm')
    pitches = browser.find_elements()
    result = []
    for (idx, el) in enumerate(browser.find_elements(By.CLASS_NAME, 'furigana')):
        print('expanding details: ' + idx)
        el.click()
        close = WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, 'x-hide-small')))
        # reading
        furigana = el.get_attribute('textContent')
        # target word
        f_kanji = el.find_element(By.XPATH, 'following-sibling::*').get_attribute('textContent')
        # sentence
        sentence = [s.onclick.toString().split('"')[1]
                    for s
                    in browser.find_elements(By.CSS_SELECTOR('.tatoeba > .noflip'))
                    if s and  s.isDisplayed()]
        # pek
        peak = peaks[idx].textContent
        # definition
        definition = definitions[idx * 2].innerText.split('\n')[1] + '\n' + definitions[idx * 2 + 1].innerText.split('\n')[1]
        # tag
        tag = f"(jp)vocab_{level}".lower()

        close.click()
        arrays.append((f_kanji, sentence, furigana, PITCH, peak, definition, None, tag))

    furigana = [el.get_attribute('textContent') for el in browser.find_elements(By.CLASS_NAME, 'furigana')]
    f_kanji = [el.get_attribute('textContent') for el in browser.find_elements(By.CLASS_NAME, 'f_kanji')]
    


if __name__ == '__main__':
    browser = webdriver.Firefox()
    with open('./resources/vocab-links.txt', 'r') as f:
        for link in f:
            scrape(browser, link)

