diesel::table! {
    news_headlines (id) {
        id -> Integer,
        source -> Text,
        headline -> Text,
        url -> Text,
        headline_sentiment -> Text,
        sector_tags -> Text
    }
}