from fastapi import FastAPI,APIRouter,HTTPException
from routes.book_routes import book
from routes.member_routes import member



router = APIRouter()




@router.get('/summary')
def get_count_of_books():
    summary_dict = {"total_books" : book.count_total_books_in_db()[0],
    "available_books" : book.count_available_books_in_db()[0],
    "currently_borrowed" : book.count_borrowed_books_in_db()[0],
    "active_members" : member.count_active_members_in_db()[0]
    }
    return summary_dict





@router.get('/books-by-genre')
def get_book_by_genre():
    return book.count_by_genre_in_db()



@router.get('/top-member')
def get_most_active_member():
    return member.get_top_member_in_db()




