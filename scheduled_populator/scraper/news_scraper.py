from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from scheduled_populator.scraper.utils import start_selenium_container, stop_selenium_container
from scheduled_populator.logging_config import logger


def scrape_cnbc_latest_world_news() -> List:
    """
    Scrapes latest news articles from cnbc.com news website in world region and saves them in a list
    :return: List of scraped news articles
    """
    logger.info("Scraping news articles from cnbc.com news website")

    url = "https://www.cnbc.com/world/?region=world"

    selenium_url = 'http://localhost:4444/wd/hub'

    # Setup selenium webdriver with headless chrome
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless") # Ensure headless mode for non GUI

    driver = webdriver.Remote(
        command_executor=selenium_url,
        options=chrome_options,
    )

    # Load the website
    driver.get(url)

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()

    # Find all headline elements
    headlines = soup.find_all("a", class_="LatestNews-headline")

    logger.info(f"Found {len(headlines)} headlines")

    formatted_headlines = []

    for index, headline in enumerate(headlines):
        formatted_headlines.append(('CNBC', headline.text, headline['href']))

    logger.info(str(formatted_headlines))
    return formatted_headlines


def scrape_ibef_latest_news() -> List:
    """
    Scrapes latest economy news articles from ibef.com news website in world region and saves them in a list
    :return: List of scraped news articles
    """
    logger.info("Scraping news articles from ibef.com news website")
    url = "https://www.ibef.org/indian-economy-news"

    selenium_url = 'http://localhost:4444/wd/hub'

    # Setup selenium webdriver with headless chrome
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless") # Ensure headless mode for non GUI

    driver = webdriver.Remote(
        command_executor=selenium_url,
        options=chrome_options,
    )

    # Load the website
    driver.get(url)

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()

    # Find the news section where the news is listed
    news_items = soup.find_all("p", class_="text-white fw500")

    logger.info(f"Found {len(news_items)} headlines")

    # To remove duplicates
    news_items = list(set(news_items))

    formatted_news = []

    for index, news_item in enumerate(news_items):
        a_tag = news_item.find("a")
        formatted_news.append(('IBEF', news_item.text, a_tag['href']))
    logger.info(str(formatted_news))
    return formatted_news


# @RuntimeError
def scrape_business_standard_news():
    """
    Scrapes latest news articles from business-standard.com news website and saves them in a list
    :return: List of scraped news articles
    """
    logger.info("Scraping news articles from business-standard news website")
    url = "https://www.business-standard.com/"
    selenium_url = 'http://localhost:4444/wd/hub'

    # Setup selenium webdriver with headless chrome
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless") # Ensure headless mode for non GUI

    driver = webdriver.Remote(
        command_executor=selenium_url,
        options=chrome_options,
    )

    # Load the website
    driver.get(url)

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()

    cards = soup.find_all("div", class_="cardlist")

    logger.info(f"Found {len(cards)} headlines")

    formatted_cards = []

    for index, card in enumerate(cards):
        a_tag = card.find("a")
        formatted_cards.append(('BUSINESS-STANDARD', a_tag.text, a_tag['href']))
    logger.info(str(formatted_cards))
    return formatted_cards


def scrape_news_articles() -> List:
    try:
        start_selenium_container()
        scraped_news_list = []
        scraped_news_list.extend(scrape_business_standard_news())
        scraped_news_list.extend(scrape_cnbc_latest_world_news())
        scraped_news_list.extend(scrape_ibef_latest_news())
        stop_selenium_container()
        return scraped_news_list
    except Exception as e:
        logger.error(e)
        return []
    finally:
        stop_selenium_container()

if __name__ == "__main__":
    # scrape_cnbc_latest_world_news()
    # scrape_ibef_latest_news()
    # start_selenium_container()
    # scrape_business_standard_news()
    # stop_selenium_container()
    print(scrape_news_articles())
