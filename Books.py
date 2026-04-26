from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]
# {"title": "Title Seven", "author": "Author Two", "category": "Math"}

@app.get("/api-endpoint")
async def fast_api():
    return {"message": "Hello, World!"}

@app.get("/books")
async def get_books():
    return {"books": BOOKS}

@app.get("/books/{book_title}")
async def get_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return {"book": book}
    return {"error": "Book not found"}

@app.get("/books/")
async def get_books_by_query(category: str):
    books_in_category = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_in_category.append(book)
    return {"books": books_in_category}

@app.get("/books/byother/")
def get_books_by_other_author(author_name: str):
    books_by_author = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books_by_author.append(book)
    return {"books": books_by_author}

@app.get("/books/{book_author}/")
async def get_books_by_author(book_author: str,category: str):
    books_by_author = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold() and book.get('author').casefold() == book_author.casefold():
            books_by_author.append(book)
    return {"books": books_by_author}

@app.post("/books/create_books")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

@app.put("/books/update_books")
async def update_book(updated_book = Body()):
    for i, book in enumerate(BOOKS):
        if book.get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}
    return {"error": "Book not found"}

@app.delete("/books/delete_books/{book_title}")
async def delete_book(book_title: str):
    for i, book in enumerate(BOOKS):
        if book.get('title').casefold() == book_title.casefold():
            deleted_book = BOOKS.pop(i)
            return {"message": "Book deleted successfully", "book": deleted_book}
    return {"error": "Book not found"}
