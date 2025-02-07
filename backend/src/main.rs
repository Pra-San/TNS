use actix_web::{ web, App, HttpResponse, HttpServer, Responder };
use diesel::prelude::*;
use diesel::r2d2::{ self, ConnectionManager };
use dotenv::dotenv;
use std::env;

mod models;
mod schema;


type DbPool = r2d2::Pool<ConnectionManager<SqliteConnection>>;

async fn get_news_headlines(pool: web::Data<DbPool>) -> impl Responder {
    use schema::news_headlines::dsl::*;

    let mut conn = pool.get().expect("Couldn't get db connection from pool");
    let results = news_headlines
        .load::<models::NewsHeadline>(&mut conn)
        .expect("Error loading news headlines");

    HttpResponse::Ok().json(results)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv().ok();

    let database_url = env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    let manager = ConnectionManager::<SqliteConnection>::new(database_url);
    let pool = r2d2::Pool::builder()
        .build(manager)
        .expect("Failed to create pool.");

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(pool.clone()))
            .route("/news_headlines", web::get().to(get_news_headlines))
    })
        .bind("127.0.0.1:8080")?
        .run()
        .await
}