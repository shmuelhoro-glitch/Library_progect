from fastapi import APIRouter,HTTPException,FastAPI
from pydantic import BaseModel
from enum import Enum
from database.book_db import BookDB
from routes.member_routes import member



router = APIRouter()

class Real_genre(str,Enum):
     Fiction =  "Fiction" 
     Non_Fiction = "Non-Fiction"
     Science = "Science"
     History = "History"
     Other = "Other"





class Book_base(BaseModel):
    title : str
    author : str
    genre : Real_genre



class Book_up(BaseModel):
    title : str | None = None
    author : str | None = None
    genre : Real_genre | None = None
    is_available : bool | None = None 
    id_member_by_borrowed : bool | None = None




book = BookDB()


@router.post('',status_code=201)
def create_book(new_book:Book_base):
    book.create_book_in_db(new_book.title,new_book.author,new_book.genre)
    return "created successfully"
    



@router.get('')
def get_all_books():
    return book.get_all_books_in_db()


@router.get('/{id:int}')
def get_book_by_id(id:int):
    data = book.get_book_by_id_in_db(id)
    if data:
        return data
    else:
        raise HTTPException(404,"Book not found")


@router.patch('/{id:int}')
def update_book(id,data:Book_up):
    update_data = data.model_dump(exclude_unset=True)
    return book.update_book_in_db(id,update_data)

    



@router.patch('/{id:int}/borrow/{member_id:int}')
def lend_book_to_member(id,member_id):
    if member.get_member_by_id_in_db(member_id)["is_active"] == 0:
        raise HTTPException(400,"Inactive member")
    if book.get_book_by_id_in_db(id)["is_available"] == 0:
        raise HTTPException(400,"The book has already been borrowed.")
    if book.count_active_borrows_by_member_in_db(member_id) >=3:
        raise HTTPException(400,"You already have 3 books.")
    else:
        member.increment_borrows_in_db(member_id)
        return book.set_available_in_db(id,0,member_id)


@router.patch('/{id:int}/return/{member_id:int}')
def return_book_from_member(id:int,member_id:int):
    if book.get_book_by_id_in_db(id)["borrowed_by_member_id"] != member_id:
        raise HTTPException(400,"A book can only be returned by the borrower.")
    return book.set_available_in_db(id,1,member_id)



