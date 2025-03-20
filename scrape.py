from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from database import engine
import requests
import os
import re

# Load google maps api from .env file
GOOGLE_MAPS_API = os.getenv("GOOGLE_MAPS_API")

def scrape_outlets(area):
    # Initialize webdriver
    driver = webdriver.Chrome()  
    driver.get("https://www.subway.com.my/find-a-subway")
    time.sleep(5)

    try:
        # Search for outlets in Kuala Lumpur area
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Find a Subway']"))
        )
        for char in area:
            search_input.send_keys(char)
            time.sleep(0.2)
        driver.switch_to.active_element.send_keys(Keys.ENTER) 
        
        time.sleep(2)

        # Create empty lists to store scraped data
        name = []
        address=[]
        opening_hours = []
        waze_link = []
        google_maps_link = []

        # Scrape outlets information
        outlet_information = driver.find_elements(By.XPATH,"//div[@class='fp_ll_holder']/div[not (contains(@style, 'display: none'))]/div[@class='location_left']")
        directions = driver.find_elements(By.XPATH,"//div[@class='fp_ll_holder']/div[not (contains(@style, 'display: none'))]/div[@class='location_right']/div[@class='directionButton']/a[@target='_blank']")
        directions_link = [directions.get_attribute('href') for directions in directions]
 
        # Process scraped outlets information and add into lists
        for outlet in outlet_information:
            outinfo = outlet.text.split('\n')
            if len(outinfo) > 1:
                # Exception (1 outlet has no address)
                if 'Monday' in outinfo[1]:
                    name.append(outinfo[0])
                    address.append('Not Available')
                    opening_hours.append(outinfo[1])
                else:
                    name.append(outinfo[0])
                    address.append(outinfo[1])
                    opening_hours.append(" ".join(outinfo[2:]))
            else:
                pass

        for i in range(len(directions_link)):
            if i % 2 == 0:
                google_maps_link.append(directions_link[i])
            else:
                waze_link.append(directions_link[i])
      
        driver.quit()

        return name, address, opening_hours, google_maps_link, waze_link

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def clean_address(address):

    # Regex patterns to remove unnecessary address components
    regex_patterns = [
    r"Lot\s+[A-Za-z0-9&\-(). ]+\s*,?\s*" ,       
    r"\b(G|L|B|F|S|UC|UG|LG)?-\d+[\w\s&-]*,",  
    r"\b(Level|Lvl|Upper|Lower|Ground|First|Second|Third|Fourth|Fifth|Sixth)\s*Floor\b",  
    ]

    for pattern in regex_patterns:
        address = re.sub(pattern, "", address, flags=re.IGNORECASE).strip()

    # Exception (The addresses of these outlets need manual cleaning)
    if address == 'Wangsa Ave, Bandar Wangsa Maju, #9 Jalan Perdana 1,  Wangsa Walk Mall, Kuala Lumpur, 53300':
        address = 'Wangsa Walk Mall'
    elif address == 'Petronas Green Plus Station, Plus Hwy & Sungai Besi Hwy, , QSR 3, Mukim Kajang, Hulu Langat, 43300':
        address = 'PETRONAS - SOLARIS SUNGAI BESI'
    elif address == 'Lvl1, Petronas Svs Station TTDI,Lot29395 & 29396, Pinggir Zaaba, Taman Tun Dr Ismail, Kuala Lumpur, 60000':
        address = 'Petronas Svs Station TTDI, Pinggir Zaaba, Taman Tun Dr Ismail, Kuala Lumpur, 60000'
    elif address =='Ativo Plaza, #1 Jalan PJU 9/1, Damansara Ave, B- Block B, Bandar Sri Damansara, Kuala Lumpur, 52200':
        address = 'Ativo Plaza'
    else:
        pass

    return address
        
def geolocation(addresses):
    latitude = []
    longitude = []

    for address in addresses:

        #Exception (1 outlet has no address)
        if address == 'Not Available':
            latitude.append(0)
            longitude.append(0)
        else:
            # Query google maps api to get latitude and longitude
            cleaned_address = clean_address(address)
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={cleaned_address}&key={GOOGLE_MAPS_API}"
            
            response = requests.get(url).json()

            if response["status"] == "OK":
                location = response["results"][0]["geometry"]["location"]
                latitude.append(location["lat"])
                longitude.append(location["lng"])
            else:
                print(cleaned_address)
                print("Geocoding failed:", response["status"])
                print(response)
            time.sleep(0.5)

    return latitude, longitude

names, addresses, opening_hours, google_maps_link, waze_link = scrape_outlets('kuala lumpur')

latitudes, longitudes = geolocation(addresses)

# Construct dataframe for scraped data
outlet_df = pd.DataFrame({'id': range(1, len(names) + 1), 'name': names, 'address': addresses, 'opening_hours': opening_hours, 'latitude': latitudes, 'longitude': longitudes, 'waze_link': waze_link, 'google_maps_link': google_maps_link})

# Add data into database
outlet_df.to_sql("subway_outlets", engine, if_exists="replace", index=False)


