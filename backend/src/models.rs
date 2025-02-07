use diesel::prelude::*;
use serde::{ Deserialize, Serialize };

#[derive(Queryable, Selectable, Serialize, Deserialize)]
#[diesel(table_name = crate::schema::news_headlines)]
#[diesel(check_for_backend(diesel::sqlite::Sqlite))]
pub struct NewsHeadline {
    pub id: i32,
    pub source: String,
    pub headline: String,
    pub url: String,
    pub headline_sentiment: String,
    pub sector_tags: String
}