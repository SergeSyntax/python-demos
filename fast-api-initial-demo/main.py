from typing import Optional
from datetime import date
from fastapi import FastAPI, Body, HTTPException, Path, Query
from pydantic import BaseModel, Field, field_validator
from starlette import status

class Book:
    id: int
    title: str
    author: str
    category: str
    description: str
    rating: int
    published: date

    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        category: str,
        description: str,
        rating: int,
        published: date,
    ):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.description = description
        self.rating = rating
        self.published = published


class BookRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    category: Optional[str] = None
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published: date  # Add published field

    @field_validator('published')
    def name_must_contain_space(cls, v):
        if not 1900 <= v.year <= 2024:
            raise ValueError('Published year must be between 1900 and 2024')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "tegegw",
                "description": "A new description of a book",
                "rating": 5,
                "published": "2023-05-01",  # Use a date string
            }
        }


BOOKS = [
    Book(
        1,
        "Title One",
        "Author One",
        "science",
        "A science book",
        4,
        date.fromtimestamp(1679616000.0),
    ),
    Book(
        2,
        "Title Two",
        "Author Two",
        "science",
        "Another science book",
        5,
        date.fromtimestamp(1679616000.0),
    ),
    Book(
        3,
        "Title Three",
        "Author Three",
        "history",
        "A history book",
        3,
        date.fromtimestamp(1679616000.0),
    ),
    Book(
        4,
        "Title Four",
        "Author Four",
        "math",
        "A math book",
        4,
        date.fromtimestamp(1679616000.0),
    ),
    Book(
        5,
        "Title Five",
        "Author Five",
        "math",
        "Another math book",
        5,
        date.fromtimestamp(1679616000.0),
    ),
    Book(
        6,
        "Title Six",
        "Author Two",
        "math",
        "Yet another math book",
        4,
        date.fromtimestamp(1679616000.0),
    ),
]


app = FastAPI()


def generate_book_id():
    return 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1


@app.get("/books", status_code=status.HTTP_200_OK)
async def fetch_books(book_rating: int = Query(gt=0, lt=6)):
    return [book for book in BOOKS if book.rating == book_rating] if book_rating else BOOKS

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(
        id=generate_book_id(),
        **book_request.model_dump(),
    )
    BOOKS.append(new_book)

    return new_book


def get_book_index(book_id: int):
    return next(
        (index for (index, book) in enumerate(BOOKS) if book["id"] == book_id), None
    )


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int = Path(gt=0)):
    book_index = get_book_index(book_id)
    return BOOKS[book_index]


@app.put("/books/{book_id}")
def update_book(book_id: int, bookRequest: BookRequest):
    book_index = get_book_index(book_id)
    if book_index is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in bookRequest.items():
        if key in BOOKS[book_index]:
            BOOKS[book_index][key] = value
            print(BOOKS[book_index][key])

    return BOOKS[book_index]


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=2)):
    book_index = get_book_index(book_id)

    if book_index is None:
        raise HTTPException(status_code=404, detail="book not found")

    BOOKS.pop(book_index)


@app.get("/books/search")
async def function_search_book(q: str, author: str):
    print(author)
    filtered_books = list(
        filter(
            lambda book: book["title"].casefold() == q.casefold()
            or book["author"].casefold() == author.casefold(),
            BOOKS,
        )
    )

    print(BOOKS[0])

    return filtered_books
