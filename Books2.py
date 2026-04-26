from fastapi import Body, FastAPI,Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date : int

    def __init__(self, id, title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID not needed on Create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    publish_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Author One",
                "description": "A new description of a book",
                "rating": 5,
                "publish_date": 2029
            }
        }
    }


BOOKS = [
    Book(1, "Title One", "Author One", "Description One", 5, 2022),
    Book(2, "Title Two", "Author Two", "Description Two", 4, 2022),
    Book(3, "Title Three", "Author Three", "Description Three", 3, 2021),
    Book(4, "Title Four", "Author Four", "Description Four", 3, 2022),
    Book(5, "Title Five", "Author Five", "Description Five", 4, 2023),
]


@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    print("read_book is called")
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/")
async def read_books_by_rating(rating: int = Query(gt=0, lt=6)):
    return [book for book in BOOKS if book.rating == rating]


@app.get("/books/publish_date/",status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(publish_date: int = Query(gt=1999, lt=2031)):
    return_value = []
    for book in BOOKS:
        if book.publish_date == publish_date:
            return_value.append(book)
    return return_value

@app.post("/create-books",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book(new_book))
    return {"message": "Book created successfully"}


def find_book(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    # print(book)
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    print(f"delete_book is called: {book_id}")
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")