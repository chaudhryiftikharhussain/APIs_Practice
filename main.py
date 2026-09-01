from fastapi import FastAPI, status
from starlette.responses import JSONResponse
from utils import read_employee_names_json_file

app = FastAPI()

@app.get("/return-message")
def read_root():
    return {"message": "Hello World"}


@app.get("/return-message/{number}")
def read_item(number: int):
    return {"message": number}


@app.get("/return-all-employee-names")
def return_all_employees_names():
    print("/return-all-employee-names api is called")
    employee_names = read_employee_names_json_file()
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
