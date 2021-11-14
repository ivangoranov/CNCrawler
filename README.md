# Contract Tender Notice Scraper API
Data collection and delivery API

## Description
### Data delivery
Scrapy spider that collect all of the romanian tender notices for the current day from: http://www.e-licitatie.ro/pub/notices/contract-notices/list/2/1  
spider can be started with django command from project root directory.
### Data Delivery
REST API, that uses collected data from scrapy spider and returns JSON object (or list of
objects) with the fallowing endpoints:
* list - returns a JSON list of all collected tender notices
* search – search by date, returns found tender notices
* &lt;id&gt; - returns a JSON object for tender notice, based on its database

## Getting Started

### Installing

* How/where to download your program
```$ git clone https://github.com/ivangoranov/CNCrawler.git```
or download the project from: https://github.com/ivangoranov/CNCrawler.git
* Any modifications needed to be made to files/folders

### Executing program

* navigate to project directory
```
$ python3 -m venv env
$ source env/bin/activate #
$ pip3 install -r requirements.txt
```

* run django server
```
$ cd cnCrwaler
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```
* run scrapy spider
```
$ cd cnCrwaler
$ python3 manage.py scrape
```

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

