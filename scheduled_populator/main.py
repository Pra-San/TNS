import pandas as pd

from db.sqlite import get_existing_headlines, save_headlines
from logging_config import logger
from scraper.news_scraper import scrape_news_articles
from sector_classification.sector_based_classification import sector_tagging_list
from sentiment_analysis.news_sentiment_analysis import predict_news_sentiment_list


def news_pipeline():
    logger.info("Starting news pipeline")

    """
    Data Collection
    """
    logger.info("Start scraping news articles")
    scraped_news_list = scrape_news_articles()
    logger.info("Start extracting news headlines from database")
    existing_headlines = get_existing_headlines()['headline']
    logger.info(f"Scraped {len(scraped_news_list)} news articles")
    logger.info(f"Obtained {len(existing_headlines)} headlines from database")
    """
    Data Processing
    """
    logger.info("Convert new headlines to dataframe and filter news articles")
    # Convert scraped news list into DataFrame
    scraped_news_df = pd.DataFrame(scraped_news_list, columns=['source', 'headline', 'url'])
    # Filter out already processed news
    scraped_news_df = scraped_news_df[~scraped_news_df['headline'].isin(existing_headlines)]
    logger.info(f"Newly scraped {len(scraped_news_df)} news articles")
    if not scraped_news_df.empty:
        logger.info("Begin inferencing news headlines")

        """
        Financial News Sentiment Analysis (Inference)
        """
        logger.info("Start sentiment analysis")
        inferenced_news_df = predict_news_sentiment_list(scraped_news_df)
        logger.info(str(inferenced_news_df.head()))

        """
        Sector Based Classification Analysis (Inference)
        """
        logger.info("Start sector classification")
        sector_tagged_df = sector_tagging_list(inferenced_news_df)
        logger.info(str(sector_tagged_df.head()))

        """
        Store to database
        """
        save_headlines(sector_tagged_df)
        logger.info("Saved headlines to database")
    else:
        logger.warning("No news articles found after filtering")


if __name__ == '__main__':
    news_pipeline()
