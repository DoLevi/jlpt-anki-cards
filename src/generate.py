import re
import chromedriver_binary
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ROLLOVER = 25


def scrape(browser, link):
    level = link.split('-')[-2]
    print('opening: ' + link)
    browser.get(link)
    print('finding readings')
    readings = browser.find_elements(By.TAG_NAME, 'svg')

    elements = browser.find_elements(By.CLASS_NAME, 'jukugo')

    for idx in range(0, len(elements)):
        print('opening details: ' + str(idx))
        el = browser.find_element(By.CLASS_NAME, 'jukugo')
        el.find_element(By.TAG_NAME, 'a').click()
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, f'//*[contains(@class, "x-hide-small")]')))
        print('processing details: ' + str(idx))
        reading = re.sub('\n\s*<', '<', readings[idx].get_attribute('outerHTML'))
        target_word = el.find_element(By.CLASS_NAME, 'f_kanji').get_attribute('innerText').split('\n')[-1]
        sentence = [s.get_attribute('onclick').split('"')[1] if s.get_attribute('onclick') else s.get_attribute('textContent')
                    for s
                    in browser.find_elements(By.CSS_SELECTOR, '.tatoeba > .noflip')
                    if s and s.is_displayed() and not (s.get_attribute('onclick') and 'English' in s.get_attribute('onclick'))]
        sentence = "".join(sentence)
        browser.save_screenshot(f'debug.png')
        definitions = [vm for vm in el.find_elements(By.CLASS_NAME, 'vm') if vm.is_displayed()]
        if len(definitions) == 2:
            definition = '<div><div>1. ' + definitions[0].get_attribute('innerText').split('1.')[1].strip() + '</div><div>2. ' + definitions[1].get_attribute('innerText').split('2.')[1].strip() + '</div></div>'
        elif len(definitions) == 1:
            definition = definitions[0].get_attribute('textContent')
        else:
            print(f'failed to find definition: {target_word} (found: {len(definitions)})')
        tag = f"(jp)vocab_{level}".lower()

        print('deleting scraped element')
        if idx > 0 and idx % ROLLOVER == 0:
            print('refreshing page')
            browser.refresh()
            readings = browser.find_elements(By.TAG_NAME, 'svg')
            print('removing scraped rows')
            for _ in range(0, idx):
                browser.execute_script('arguments[0].parentNode.removeChild(arguments[0]);', browser.find_element(By.CLASS_NAME, 'jukugorow'))
        else:
            print('removing scraped row')
            browser.execute_script('arguments[0].parentNode.removeChild(arguments[0]);', browser.find_element(By.CLASS_NAME, 'jukugorow'))
        yield '\t'.join(['"' + item.replace('"', '""') + '"' for item in [target_word, sentence, reading, definition, tag]])


if __name__ == '__main__':
    print('setting up webdriver')
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("window-size=1080,1450")
    browser = webdriver.Chrome(options=chrome_options)
    with open('result.tsv', 'w+') as out:
        out.write('#separator:tab\n')
        out.write('#html:true\n')
        out.write('#tags column:5\n')
        with open('./resources/vocab-links.txt', 'r') as f:
            for link in f:
                for line in scrape(browser, link):
                    out.write(line + '\n')

