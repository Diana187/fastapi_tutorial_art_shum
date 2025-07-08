from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel


app = FastAPI()


books = [
    {
        "id": 1,
        "title": "Alice in wonderland",
        "author": "Lewis Carroll",
    },
    {
        "id": 2,
        "title": "The Adventures of Huckleberry Finn",
        "author": "Mark Twain",
    },
]


@app.get(
    "/books",
    tags=["Books"],
    summary="Get all books",
)
def read_books():
    return books


@app.get("/books/{book_id}", tags=["Books"], summary="Get the book")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


class NewBook(BaseModel):
    # fastAPI сам валидирует эти данные
    title: str
    author: str


@app.post("/books", tags=["Create book"])
def create_book(new_book: NewBook):
    books.append(
        {
            "id": len(books) + 1,
            "title": new_book.title,
            "author": new_book.author,
        }
    )
    # fastAPI сам преобразует словарь в Json
    return {"success": True, "message": "Book was added successfully"}
