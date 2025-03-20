# Subway_Outlet_Scraper
This repository contains code for a webscraper for [Subway Malaysia](https://www.subway.com.my/find-a-subway) which scrapes all the Kuala Lumpur outlets in Malaysia. The code includes Selenium webscraper, PostgreSQL as the database, FastAPI, Streamlit web application and chatbot LangChain RAG framework

## Installation
**Installation via** **`requirements.txt`**:
```
$ git clone https://github.com/Lucaslim00/subway_outlet_scraper
$ cd subway_outlet_scraper
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```
## Database
1. Set up your postgresql database locally and ensure it is running on port 5432 
2. Add your database credentials with the following format into .env file, replace 'myuser', 'mypassword' and 'mydatabase' with your username, password and database name
```
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydatabase`
```

## Web scraper
1. The web scraper utilises Selenium, so installing Selenium and webdriver is required. ChromeDriver can be downloaded from [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)
2. In order to extract the coordinates of the address scraped, geocoding is implemented. Google Maps geocoding is utilized, can refer to this documentation [Google Maps Geocoding](https://developers.google.com/maps/documentation/geocoding).<br>
**Add Google Maps geocoding api into .env file**
```
GOOGLE_MAPS_API=*********
```
3. **Run**
```
python3 webscraper.py
```

## FastAPI
1. **RUN**
```
uvicorn api:app --reload
```
2. Check if the api is working by accessing [http://127.0.0.1:8000/outlets/]('http://127.0.0.1:8000/outlets/')

## Web Application
1. The chatbot using LangChain RAG Framework requires OpenAi api key, add the OpenAI api key into .env file
```
OPENAI_API_KEY=*********
```
2. **Run**
```
streamlit run webapp.py
```
The web application should be up and running.
