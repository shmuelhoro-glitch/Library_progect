from fastapi import APIRouter,FastAPI
from logs.logger_app import logger
from database.db_connection import db
from routes.book_routes import router as book_routes
from routes.member_routes import router as member_routes
from routes.report_routes import router as report_routes
from contextlib import asynccontextmanager





@asynccontextmanager
async def lifespan(app:FastAPI):
    db.init_db()
    db.init_tables()
    db.get_connection

    print("welcome")
    logger.info("Connection to the database has been established.")

    yield

    db.get_connection.close()
    print("shot down")
    logger.info("Data connection closed, system is shutting down.")
    







app = FastAPI(lifespan=lifespan)



app.include_router(book_routes,prefix="/books",tags=["books"])

app.include_router(member_routes,prefix="/members",tags=["members"])

app.include_router(report_routes,prefix="/reports",tags=["reports"])

    




