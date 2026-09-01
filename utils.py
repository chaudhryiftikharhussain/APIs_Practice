import json

def read_employee_names_json_file():
    try:
        with open("employees_names_only1.json", "r") as f:
            try:
                employee_names_list = json.load(f)
            except Exception as e:
                print(str(e))
                return False, [], "file_read_error"
        return True, employee_names_list, "file_read_success"
    except Exception as e:
        print(str(e))
        return False, [], "file_not_found_error"