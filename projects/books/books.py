from fastapi import FastAPI

app = FastAPI()

books = [
    {"title": "The Subtle Art of Not Giving a Fuck", "author": "Mark Manson", "category": "Self Help"},
    {"title": "Adventures in Human Being", "author": "Gavin Francis", "category": "Biology"},
    {"title": "The Dairy of a CEO", "author": "Steven Barlett", "category": "Business"},
    {"title": "The Minmalist Entrepreneur", "author": "Sahil Lavingia", "category": "Business"},
    {"title": "Atomic Habits", "author": "James Clear", "category": "Self Help"},
    {"title": "Good Habits", "author": "James Clear", "category": "Self Help"}
]

@app.get("/books")
async def get_all_books():
    return books

@app.get("/books/{index_num}")
async def get_book(index_num):
    return books[int(index_num)]