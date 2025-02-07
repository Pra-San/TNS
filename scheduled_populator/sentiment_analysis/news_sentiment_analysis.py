import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scheduled_populator.logging_config import logger


def sentiment_analysis(text):
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
    model = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')

    # Define label mapping from model configuration
    labels = {
        0: 'Positive',
        1: 'Negative',
        2: 'Neutral'
    }

    def predict_sentiment(headline):
        # Tokenize the input text
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)

        # Get model predictions (logits)
        with torch.no_grad():  #Disable Gradient Calculation
            outputs = model(**inputs)
            logits = outputs.logits

        # Get the predicted class
        predicted_class = torch.argmax(logits, dim=-1).item()

        return labels[predicted_class]

    return predict_sentiment(text)


def predict_news_sentiment_list(headlines_df):
    """
    This function predicts the sentiment for each headline in a DataFrame and assigns the result
    to a new column 'headline_sentiment'.

    :param headlines_df: DataFrame with a 'headline' column containing text data.
    """
    logger.info('Using labels 0->Positive, 1->Negative, 2->Neutral')
    # Ensure the 'headline_sentiment' column exists and is initialized
    headlines_df['headline_sentiment'] = ''

    for index, row in headlines_df.iterrows():
        # Predict the sentiment for the current headline
        headline_sentiment = sentiment_analysis(row['headline'])

        # Assign the predicted sentiment in the df to the corresponding row
        headlines_df.at[index, 'headline_sentiment'] = headline_sentiment

    return headlines_df


if __name__ == '__main__':
    print(sentiment_analysis("Stocks rallied and the British pound gained."))
