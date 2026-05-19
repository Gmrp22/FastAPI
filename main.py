from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import json
from error import myCustomError
app = FastAPI()

# Business errors: el cliente hizo algo mal (404, 400, etc.)
@app.exception_handler(myCustomError)
def my_custom_error_handler(request, exception):
    return JSONResponse(
        status_code=exception.status_code,
        content={"error": exception.message}
    )

# Server errors: algo inesperado crasheó (BD lenta, librería, bug, etc.)
@app.exception_handler(Exception)
def global_exception_handler(request, exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Error inesperado en el servidor"}
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/books")
def get_books(genre: str = 'all'):
    try:
        with open("books.json", "r") as file:
            books_db = json.load(file)
            if genre == 'all':
                return books_db
            return [book for book in books_db if book.get("genre") == genre]
    except FileNotFoundError:
        raise myCustomError("File not found", 500)
    except Exception as e:
        raise myCustomError(str(e), 500)


@app.get("/books/{id}")
def get_book(id: int):
    try:
        with open("books.json", "r") as file:
            books_db = json.load(file)
    except FileNotFoundError:
        raise myCustomError("File not found", 500)
    except Exception as e:
        raise myCustomError(str(e), 500)

    for book in books_db:
        if book.get("id") == id:
            return book

    raise myCustomError("Book not found", 404)


@app.get('/books/author/{book_author}')
def read_author_category_by_query(book_author: str, category: str = 'all'):
    try:
        with open("books.json", "r") as file:
            books_db = json.load(file)
    except FileNotFoundError:
        raise myCustomError("File not found", 500)
    except Exception as e:
        raise myCustomError(str(e), 500)

    if category == 'all':
        ##guarda book de book en books caudno
        return [book for book in books_db if book.get("author") == book_author]
    return [book for book in books_db if book.get("author") == book_author and book.get("genre") == category]


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    try:
        with open("books.json", "r") as file:
            books_db = json.load(file)
    except FileNotFoundError:
        raise myCustomError("File not found", 500)
    except Exception as e:
        raise myCustomError(str(e), 500)

    books_db.append(new_book)
    with open("books.json", "w") as file:
        json.dump(books_db, file, indent=4)
    return new_book