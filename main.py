import json

from fastapi import FastAPI, status
from starlette.responses import JSONResponse
from utils import read_employee_names_json_file

app = FastAPI()

@app.get("/return-message")
def read_root():
    a = 4 / 0
    return {"message": "Hello World"}


@app.get("/return-message/{number}")
def read_item(number: int):
    return {"message": number}


@app.get("/return-all-employee-names")
def return_all_employees_names():
    print("/return-all-employee-names api is called")
    file_read_ok, employee_names, message = read_employee_names_json_file()
    print("now returning all employee names")
    return employee_names


@app.get("/check-employee/{name}")
def check_employee(name: str):
    print("/check-employee api is called")
    name_exist = False
    file_read_ok, employee_names, message = read_employee_names_json_file()
    if not file_read_ok:
        print("file read not ok")
        if message == "file_not_found_error":
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": "file does not exist",
                    "name_exist": None
                }
            )
        elif message == "file_read_error":
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                content={
                    "message": "file read issue",
                    "name_exist": None
                }
            )
    employee_names = [name.lower() for name in employee_names]
    name = name.lower()
    if name in employee_names:
        print("employee name does exist")
        name_exist = True
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "patient found",
                "name_exist": name_exist
            }
        )
    else:
        print("employee name does not exist")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "patient not found",
                "name_exist": name_exist
            }
        )



@app.get("/search-books/{author_name}")
def search_books_by_name(author_name: str, category: str | None = None):
    try:
        print(f"/search-books api is called with author_name {author_name}, - {category}")

        with open("books_v1.json", "r") as file:
            books = json.load(file)

        author_names_in_db = [b['author_last_name'] for b in books]
        print(author_names_in_db)
        if author_name not in author_names_in_db:
            return JSONResponse(
                status_code=404,
                content={
                    "message": "author does not exist",
                }
            )

        print(author_name)
        print(books)

        author_books = []
        for book in books:
            if book["author_last_name"] == author_name:
                print("book found")
                if category is not None and category == book["category"]:
                    print("category found")
                    author_books.append(book)
                else:
                    author_books.append(book)

        return JSONResponse(
            status_code=200,
            content={
                "message": "books found",
                "author_books": author_books
            }
        )
    except Exception as e:
        print("exception occured")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": f"server error {e}"
            }
        )

