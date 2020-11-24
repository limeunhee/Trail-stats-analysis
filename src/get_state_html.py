# Import libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time

# Specifying the list of states to scrape trails from

states=["alabama", "alaska", "arizona", "arkansas", "california", 
        "colorado", "connecticut", "delaware", "florida", "georgia", 
        "hawaii", "idaho", "illinois", "indiana", "iowa", 
        "kansas", "kentucky", "louisiana", "maine", "maryland", 
        "massachusetts", "michigan", "minnesota", "mississippi", "missouri", 
        "montana", "nebraska", "nevada", "new-hampshire", "new-jersey", 
        "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio",
        "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina",
        "south-dakota", "tennessee", "texas", "utah", "vermont",
        "virginia", "washington", "west-virginia", "wisconsin", "wyoming"]

#states=['hawaii']

def get_html(state):
    """ 
    This function creates state specific url to link to Alltrails.com 
    Aand uses selenium to click "load more" until 500 search results are loaded.
    Then, it returns the source code as a html file

    Args:
        state (str): a state name

    Returns:
        html: html source code for the state search result from Alltrails.com

    """
    # This function creates state specific url to link to Alltrails.com 

    
    if state == 'hawaii':
        url = 'https://www.alltrails.com/hawaii'
    else:
        url='https://www.alltrails.com/us/' + state
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('/Users/eunheelim/Capstone1/chromedriver', options=chrome_options)
    
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    page_num = 0
    while True:
        try:
            driver.find_element_by_css_selector('button.styles-module__button___1nuva ').click()
            time.sleep(1)
            page_num += 1
            if page_num==49: # After clicking "load more" 49 times, stop clicking "load more"
                break
        except:
            break
    
    html = driver.page_source.encode('utf-8')
    
    return html

def save_html(html, state):
    """ 
    This function takes in alltrails result page source code and saves it to an html file

    Args:
        html (str): page source code

    Returns:
        None
    """
    
    soup = BeautifulSoup(html, "lxml")
    filename = '/Users/eunheelim/Capstone1/test_html/'+ state +'.html'
    with open(filename, 'w') as file:
        file.write(str(soup))
    return

def get_htmls_for_all_states(state):
    """ 
    This function takes in state name and returns html file for alltrails result page source code

    Args:
        state (str): a state name

    Returns:
        None
    """

    # This function takes a list of states as an input
    # It returns html files for all states in the state_list
    print(state)

    html = get_html(state)
    save_html(html, state)
        
    return

def main():
    pool = Pool()
    pool.map(get_htmls_for_all_states, states)    
    
if __name__ == '__main__':
    main()