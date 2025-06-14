# imports
from fastapi import FastAPI, Body
from models import Book, Books
from pydantic import BaseModel, Field

app = FastAPI()

# Introducing Validation with Pydantics
class BookRequest(BaseModel):
    # id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

# APIs
@app.get("/books")
async def get_all_books(): 
    return Books

@app.post("/create_book")
async def create_book(book_request: BookRequest):
    '''
    model.dump() converts a pydantic model/class instance into a plain python dictionary
    ** uses unpacks the dict to be used as kwargs 
    '''
    new_book = Book(**book_request.model_dump())

    # OR
    # add_book = Book(
    #     title=book_request.title,
    #     author=book_request.author,
    #     description=book_request.description,
    #     rating=book_request.rating
    # )

    Books.append(new_book)