# newsdiffs3
A project based on [ecprice's newsdiffs](https://github.com/ecprice/newsdiffs).

## Setup
Requires access to a MongoDB server

Copy `config_template.yaml` to `config.yaml`.

Configure access to your database.

Running `scraper.py` scrapes articles from NYTimes, Washington Post, and APNews. I recommend attaching it to a cronjob.

`server.py` serves the web frontend, letting you view articles. Keep this running.

## Usage
![UI](https://github.com/mgitre/newsdiffs3/blob/master/images/ui.png?raw=true)
Navigating to `http://[newsdiffs_location]/article/[article_url]` will show any saved changes for that article. Using the menu on the right, you can select a single saved version to view or select two saved versions to compare. 

## Adding support for a news outlet
Adding a scraper can be done by copying the format from an existing one and replacing matches with ones that apply to your site. All matches are formatted for BeautifulSoup. Please feel free to contribute!

## Built with
* Python
  * Flask
  * BeautifulSoup
* MongoDB
