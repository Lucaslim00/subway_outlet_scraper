# Subway_Outlet_Scraper
This repository contains code for a webscraper for [Subway Malaysia](https://www.subway.com.my/find-a-subway) which scrapes all the Kuala Lumpur outlets in Malaysia. The code includes Selenium webscraper, PostgreSQL as the database, FastAPI, Streamlit web application and LangChain RAG framework

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
2. Add your database credentials with the following format into .env file, replace 'myuser' and 'mydatabase' with your username and database name
`DATABASE_URL=postgresql://myuser@localhost:5432/mydatabase`

## Selenium
