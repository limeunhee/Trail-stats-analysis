import requests
from requests import get
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import glob
import os 
from multiprocessing import Pool

def try_except(prompt, lst):
    try:
        a=eval(prompt)
        lst.append(a)
    except:
        lst.append(None)

    return lst


def get_trail_info(state_trail_urls):
    print(state_trail_urls)
    state = state_trail_urls[32:].split('.')[0]
    #filepath = "/Users/eunheelim/Capstone1/urls/washington.txt"
    file1 = open(state_trail_urls, 'r') 
    urls = file1.readlines() 


    #initiate data storage
    #our loop through each container
    names = []
    difficulties = []
    average_ratings=[]
    worst_ratings=[]
    best_ratings=[]
    review_counts=[]
    elevations=[]
    route_types=[]
    short_descriptions=[]
    long_descriptions=[]
    tags_list=[]
    locations=[]
    n_photos=[]
    n_recordings=[]
    n_completed=[]


    # Make for loop into functions /pass in list of URLS as inpur argument
    count = 0
    for trail_url in urls:
        count += 1
        if count % 50 == 0:
            print(f"{state}:{count}")

        #results = requests.get(trail_url[0:-1])
        results = urlopen(trail_url[0:-1])
        soup=BeautifulSoup(results, 'html.parser')


        class_name_10='styles-module__ssrFallback___34ups [object Object] styles-module__flexContainer___1o9fS styles-module__slidingTabs___25XGa'
        div10=soup.find_all('div',{'class':class_name_10})
        
        try:
            stats = [i.text for i in div10[0].find_all('div')]
        
            n_photos.append(int(stats[1][8:-1]))
            n_recordings.append(int(stats[2][12:-1]))
            n_completed.append(int(stats[3][11:-1]))
        except:
            n_photo.append(None)
            n_recordings.append(None)
            n_completed.append(None)


        class_name_3='styles-module__content___1GUwP'
        container=soup.find_all('div', {'class':class_name_3})[0]


        #Get trail name
        try:
            name = container.h1['title']
        except:
            name = None
        names.append(name)

        #Get trail location
        try:
            location = container.a['title']
        except:
            location = None
        locations.append(location)

        #Get trail difficulty
        try:
            difficulty = container.span.text
        except:
            difficulty = None
        difficulties.append(difficulty)

        #Get trail elevation
        try:
            elevation = (
                ((soup.find('section', {'id':'trail-stats'})).find('span',{'class':'elevation-icon'}) \
                .find('span',{'class':'detail-data xlate-none'}) \
                .text[13:].split('f'))[0] \
                .replace(',','')
            )
        except:
            elevation = None
        elevations.append(elevation)

        #Get trail route type
        a = soup.find('section', {'id':'trail-stats'})
        try:
            route_type = a.find_all('span',{'class':'detail-data'})[2].text
        except:
            route_type = None
        route_types.append(route_type)

        #Get trail short description
        try:
            short_description = soup.find('p',{'class':'xlate-google line-clamp-4'}).text
        except:
            short_description = None
        short_descriptions.append(short_description)

        #Get trail long description
        try:
            long_description = soup.find('p',{'class':'styles-module__displayText___17Olo'}).text
        except:
            long_description = None
        long_descriptions.append(long_description)

        #Get trail rating container
        a=(container.find_all('meta'))
        average_rating =(a[0]['content'])
        average_ratings.append(average_rating)

        worst_rating = (a[1]['content'])
        worst_ratings.append(worst_rating)

        best_rating = (a[2]['content'])
        best_ratings.append(best_rating)

        review_count = (a[3]['content'])
        review_counts.append(review_count)

        #Get trail tags
        tags= soup.find('section',{'class':'tag-cloud'}).find_all('span',{'class':'big rounded active'})


        tag_list=[]
        try:
            for item in tags:
                tag_list.append(item.text)
        except:
            pass

        tags_list.append(tag_list)

    #pandas dataframe        
    trails = pd.DataFrame({
    'name': names,
    'difficulty': difficulties,
    'average_rating' :average_ratings,
    'worst_rating': worst_ratings,
    'best_rating':best_ratings,
    'review_count':review_counts,
    'location':locations,
    'elevation':elevations,
    'route_type': route_types,
    'short_description':short_descriptions,
    'long_description':long_descriptions,
    'tag_list' :tags_list,
    'n_photos':n_photos,
    'n_recordings':n_recordings,
    'n_completed':n_completed
    })


    filename='/Users/eunheelim/Capstone1/data5/' + state + '2.csv'

    #add dataframe to csv file named 'filename.csv'
    trails.to_csv(filename)
    
    return
    
    
def main():
    pool = Pool()
    pool.map(get_trail_info, glob.iglob(r'/Users/eunheelim/Capstone1/url2/*.txt'))


if __name__ == "__main__":
    main()