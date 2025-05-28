from fastapi import FastAPI, Body

app = FastAPI()

books = [
    {"title": "The Subtle Art of Not Giving a Fuck", "author": "Mark Manson", "category": "Self Help"},
    {"title": "Adventures in Human Being", "author": "Gavin Francis", "category": "Biology"},
    {"title": "The Dairy of a CEO", "author": "Steven Barlett", "category": "Business"},
    {"title": "The Minimalist Entrepreneur", "author": "Sahil Lavingia", "category": "Business"},
    {"title": "Atomic Habits", "author": "James Clear", "category": "Self Help"},
    {"title": "Good Habits", "author": "James Clear", "category": "Self Help"}
]

@app.get("/books/byauthor/{author}")
async def fetch_all_books_by_author(author: str):
    result = []
    for book in books:
        if book.get("author").casefold() == author.casefold():
            result.append(book)
    
    return result

@app.get("/books/")
async def fetch_author_books(books_by_author: str):
    result = []
    for book in books:
        if book.get("author").casefold() == books_by_author.casefold():
            result.append(book)
    
    return result