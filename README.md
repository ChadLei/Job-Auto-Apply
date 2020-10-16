# Software Dev Job Auto Apply & Scraper

A script to scrape company job sites hosted on Greenhouse for job listings and automatically apply to each job using pre-populated data.

## Inspiration
Job hunting is rough. Having to answer the same generic questions 1000 times is even rougher. You can't automate every site, but one was good enough for me!
Thank you to https://github.com/harshibar for making this easier.

## Installation
1. Install [ChromeDriver] `pip install ChromeDriverManager`
2. Install [Selenium]: `pip install selenium`
3. Install [BeautifulSoup]: `pip install beautifulsoup4`

## Usage
#### To scrape jobs:
1. Put in your companies of interest (their greenhouse url) in `scraper_and_scraped_urls/job_websites_to_scrap.txt`. It comes by default with 100+ companies in the file.
2. Run `python webScraper.py`. URLs found will be saved to `scraped_jobs.txt`.

#### To auto apply:
1. Put in your information in `form_input_basic_info.py`.
2. Run `python main.py`
3. Sometimes you might encounter applications that ask for information that isn't included in this script, so you'll have to manually fill those out.
4. You also may encounter captcha. Currently looking for a solution for this (VERY OPEN TO SUGGESTIONS AND HELP!). I'm thinking of implementing a anti-captcha solver service.


## Thanks

* [Selenium](https://selenium-python.readthedocs.io/) - A tool designed for QA testing, but that actually works great for making these types of bots
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/doc) - A tool to scrape HTML/XML content (that saved be *big time* with this project)
* [Harshi harshibar](https://github.com/harshibar/common-intern) - The base of where I started for this project.
