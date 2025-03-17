from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def scrape_outlets(area):
    driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
    driver.get("https://subwayisfresh.com.sg/where-to-eat/")
    time.sleep(5)

    try:
        # Search outlet
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Enter your address']"))
        )
        for char in area:
            search_input.send_keys(char)
            time.sleep(0.2)
        driver.switch_to.active_element.send_keys(Keys.ENTER) 
        
        time.sleep(2)

        # Create lists for outlet name, address and phone number
        name = []
        address=[]
        phone = []

        # Scrape outlets information
        outlets = driver.find_elements(By.XPATH,"//li[@class='sl-item']")

        # Process scraped outlets information and add into lists
        for outlet in outlets:
            outinfo = outlet.text.split('\n')
            name.append(outinfo[0])
            address.append(outinfo[1])
            phone.append(outinfo[2])

        driver.quit()

        return name, address, phone

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def geolocation(addresses):
    latitude = []
    longitude = []
    wazelink = []
    googlemapslink = []
    
    # Removing postcode, city and country
    for address in addresses:
        result = address.split('#')[0]

        try:
            print(result)
            geolocator = Nominatim(user_agent="sg_subway_geocoding")
            location = geolocator.geocode(result)
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
            wazelink.append('https://waze.com/ul?ll='+str(location.latitude)+','+str(location.longitude)+'&navigate=yes')
            googlemapslink.append('https://www.google.com/maps/dir//'+str(location.latitude)+','+str(location.longitude))
            time.sleep(20)

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Error: {e}")
            return None
        
    return latitude, longitude, wazelink, googlemapslink


names, addresses, phones= scrape_outlets('jurong')
latitudes, longitudes, wazelinks, googlemapslinks = geolocation(addresses)
