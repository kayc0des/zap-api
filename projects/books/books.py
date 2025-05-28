from fastapi import FastAPI

app = FastAPI()

books = [
    {"title": "The Subtle Art of Not Giving a Fuck", "author": "Mark Manson", "category": "Self Help"},
    {"title": "Adventures in Human Being", "author": "Gavin Francis", "category": "Biology"},
    {"title": "The Dairy of a CEO", "author": "Steven Barlett", "category": "Business"},
    {"title": "The Minimalist Entrepreneur", "author": "Sahil Lavingia", "category": "Business"},
    {"title": "Atomic Habits", "author": "James Clear", "category": "Self Help"},
    {"title": "Good Habits", "author": "James Clear", "category": "Self Help"}
]

@app.get("/books")
async def get_all_books():
    return books

@app.get("/books/{book_title}")
async def get_book(book_title: str):
    for book in books:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category: str):
    category_books = []
    for book in books:
        if book.get("category").casefold() == category.casefold():
            category_books.append(book)
    
    return category_books

@app.get("/books/{author}/")
async def read_author_category_by_query(author: str, category: str):
    category_books = []
    for book in books:
        if book.get("author").casefold() == author.casefold() and book.get("category").casefold() == category.casefold():
            category_books.append(book)
    
    return category_books