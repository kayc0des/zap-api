# Create a Book Class
import uuid

class Book():
    ''' Book Object '''

    def __init__(self, title: str, author: str, description: str, rating: int):
        ''' Constructor Method Used to Initialize an Instance of the Book Class'''
        self.id = uuid.uuid4()
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

    def to_dict(self):
        return vars(self)
    
Books = [
    Book(title="Adventures in Human Beings", author="Gavin Francis", description="A journey through the human body, told with insight and wonder.", rating=4),
    Book(title="Atomic Habits", author="James Clear", description="An empowering guide to building good habits and breaking bad ones.", rating=5),
    Book(title="Sapiens", author="Yuval Noah Harari", description="An exploration of the history and evolution of humankind.", rating=5),
    Book(title="Educated", author="Tara Westover", description="A memoir of a woman who leaves her survivalist family and earns a PhD.", rating=4),
    Book(title="The Midnight Library", author="Matt Haig", description="A novel about all the lives we could live, and finding meaning in our own.", rating=4),
    Book(title="Thinking, Fast and Slow", author="Daniel Kahneman", description="A deep dive into how our minds work and the biases that shape our decisions.", rating=5),
    Book(title="The Body", author="Bill Bryson", description="A fascinating tour of the human body by a master storyteller.", rating=4),
    Book(title="Becoming", author="Michelle Obama", description="The deeply personal memoir of the former First Lady of the United States.", rating=5),
    Book(title="The Power of Now", author="Eckhart Tolle", description="A spiritual guide to living fully in the present moment.", rating=4),
    Book(title="The Alchemist", author="Paulo Coelho", description="A philosophical tale about following your dreams and listening to your heart.", rating=4)
]