from transformers import pipeline
from scheduled_populator.logging_config import logger


def sector_tagging(text):
    sector_labels = ["AutoComponents", "Agriculture and Allied Industries", "Aviation", "Automobiles", "E-Commerce",
                     "Chemicals", "Banking", "Insurance", "Healthcare", "Financial Services", "IT & BPM",
                     "Pharmaceuticals", "Real Estate", "Power"]

    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    result = classifier(text, candidate_labels=sector_labels)
    return result


def sector_tagging_list(headlines_df):
    MIN_LABEL_COUNT = 2
    CUMULATIVE_THRESHOLD = 0.5

    logger.info(f"Using {MIN_LABEL_COUNT} as minimum label count")
    logger.info(f"Using {CUMULATIVE_THRESHOLD} as Cumulative Threshold")

    # Ensure the 'headline_sentiment' column exists and is initialized
    headlines_df['sector_tags'] = [[] for _ in range(len(headlines_df))]

    for index, row in headlines_df.iterrows():
        # Predict the sentiment for the current headline
        sector_result = sector_tagging(row['headline'])

        # Extract the labels and scores
        labels = sector_result['labels']
        scores = sector_result['scores']

        # Get the top MIN_LABEL_COUNT
        top_labels = labels[:MIN_LABEL_COUNT]

        # Initialise list to hold the selected labels
        sector_tags = top_labels.copy()

        cumulative_score = sum(scores[:MIN_LABEL_COUNT])

        for label, score in zip(labels[MIN_LABEL_COUNT:], scores[MIN_LABEL_COUNT:]):
            if cumulative_score < CUMULATIVE_THRESHOLD:
                sector_tags.append(label)
                cumulative_score += score
            else:
                break

        # Assign the predicted sentiment in the df to the corresponding row
        headlines_df.at[index, 'sector_tags'] = sector_tags

    return headlines_df
