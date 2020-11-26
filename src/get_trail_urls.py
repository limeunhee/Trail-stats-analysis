import glob
from bs4 import BeautifulSoup
from multiprocessing import Pool
import numpy as np
import pandas as pd

# def try_except(prompt, lst):
#     """ 
#     This function tries out prompt, and appends the result to lst

#     Args:
#         prompt (str): an expression to evaulate
#         lst (List[Object]): a list where output to prompt is appened to

#     Returns:
#         lst

#     """

#     try:
#         a = eval(prompt)
#         lst.append(a)
#     except:
#         lst.append(None)

#     return lst


# Defining class names
trail_card_class = "styles-module__containerDescriptive___3aZqQ styles-module__trailCard___2oHiP"
trail_info_class = "styles-module__info___1Mbn6"
info_values_class = "xlate-none"


def get_trail_urls(state_html):
    """ 
    This function takes in a filepath for a state html and 
    i) saves a file with urls of trails in that state from Alltrails.com 
    ii) saves a csv file containing duration and distance of trails from the state 

    Args:
        state_html (str): a filepath for a file that contains html of trails search result for a state
    Returns:
        None
    """

    # Extract state name from the html filename
    state = state_html[37:].split(".")[0]
    print(state)

    soup = BeautifulSoup(open(state_html), "html.parser")

    each_urls = []
    durations = []
    distances = []

    trail_cards = soup.find_all("div", {"class": trail_card_class})

    for card in trail_cards:

        # Get list of url to .txt file
        each_url = "https://www.alltrails.com" + (card.a["href"])
        each_url = each_url.replace("?ref=result-card", "")
        each_urls.append(each_url)

        # Save list of url to .txt file
        filename = "/Users/eunheelim/Capstone1/url2/" + state + ".txt"
        np.savetxt(filename, each_urls, fmt="%s", delimiter=",")

        trail_info = card.find_all("div", {"class": trail_info_class})

        # Get list of durations for each of 500 trail
        try:
            duration = trail_info[1].find_all("span", {"class": info_values_class})[1].text[5:]
        except:
            duration = None
        durations.append(duration)

        # Get list of distances for each of 500 trail
        try:
            distance = trail_info[1].find_all("span", {"class": info_values_class})[0].text[8:]
        except:
            distance = None
        distances.append(distance)

        filename = "/Users/eunheelim/Capstone1/data4/" + state + ".csv"
        pd.DataFrame({"durations": durations, "distances": distances}).to_csv(filename)
        
    return


def main():
    pool = Pool()
    pool.map(get_trail_urls, glob.iglob(r"/Users/eunheelim/Capstone1/tes2_html/*.html"))


if __name__ == "__main__":
    main()
