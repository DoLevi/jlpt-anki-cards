import re
import chromedriver_binary
import urllib.parse
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep


def scrape_reading(browser, kanji, reading):
    has_kanji = bool(kanji)
    query = urllib.parse.quote_plus(kanji if has_kanji else reading)
    url = f'https://takoboto.jp/?q={query}'
    browser.get(url)
    print('waiting for page load of ' + url)
    WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, f'//*[text()="English"]')))
    print('scraping reading html')
    try:
        reading = browser.find_element(By.XPATH, '//div[text()="Readings"]/following-sibling::div/*[contains(@class, WordJapDiv)]/div/span')
        try:
            browser.execute_script('arguments[0].parentNode.removeChild(arguments[0]);', reading.find_element(By.CSS_SELECTOR, 'span:last-child'))
        except:
            browser.execute_script('arguments[0].parentNode.removeChild(arguments[0]);', reading.find_element(By.CSS_SELECTOR, 'span:last-child'))
    except:
        reading = browser.find_element(By.XPATH, '//*[contains(@class, WordJapDiv)]/div/span')
    return reading.get_attribute('outerHTML')


def scrape_row(row):
    [kanji_raw, reading_raw, meaning_raw, frequency_raw] = row.find_elements(By.TAG_NAME, 'td')
    kanji = kanji_raw.get_attribute('textContent')
    reading = reading_raw.get_attribute('textContent')
    meanings = meaning_raw.get_attribute('textContent').split('] ')
    if len(meanings) > 1:
        meanings = '<div><div>' + '</div><div>'.join([f'{idx}. {m.split(" [")[0]}' for (idx, m) in enumerate(meanings[1:])]) + '</div></div>'
    else:
        meanings = meanings[0]
    frequency = frequency_raw.get_attribute('textContent')
    frequency = 999999 if 'N/A' in frequency else int(frequency)
    return [kanji, reading, meanings, frequency]


def scrape_page(browser, link, level):
    print('opening: ' + link)
    browser.get(link)
    sleep(5)
    result = []
    for (idx, row) in enumerate(browser.find_elements(By.CSS_SELECTOR, 'tbody > tr')):
        print(f'scraping row {idx}')
        result.append(scrape_row(row))
    return result


if __name__ == '__main__':
    print('setting up webdriver')
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("window-size=1700,1200")
    browser = webdriver.Chrome(options=chrome_options)
    with open('result.tsv', 'w+') as out:
        out.write('#separator:tab\n')
        out.write('#html:true\n')
        out.write('#tags column:4\n')
        with open('./resources/vocab-links.txt', 'r') as f:
            for link in f:
                level = link.split('/')[-1].strip()
                tag = f"(jp)vocab_{level}".lower()
                lines = sorted(scrape_page(browser, link.strip(), level), key=lambda line: line[3])
                for line in lines:
                    out.write((line[0] if line[0] else line[1]) + '\t"' + scrape_reading(browser, line[0], line[1]).replace('"', '""') + '"\t' + line[2] + '\t' + tag + '\n')

