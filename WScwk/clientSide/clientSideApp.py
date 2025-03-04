import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
session = requests.Session() 

def register():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    data = {"username": username, "email": email, "password": password}
    response = requests.post(f"{BASE_URL}/register/", json=data)

    if handle_response(response):
        print("Registration successful!")


def login(url):
    global BASE_URL, session

    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # for testing, commented out
    # BASE_URL = url

    data = {"username": username, "password": password}
    response = session.post(f"{BASE_URL}/login/", json=data)

    if handle_response(response):
        print("Login successful!")


def logout():
    global session
    response = session.post(f"{BASE_URL}/logout/")
    data = handle_response(response)  
    if data:
        print("Logged out successfully!")
        session = requests.Session()

def list_instances():
    response = session.get(f"{BASE_URL}/list/")
    data = handle_response(response)

    if data:
        for instance in data:
            print(
                f"Code: {instance['module__module_code']}, "
                f"Name: {instance['module__module_name']}, "
                f"Year: {instance['year']}, "
                f"Semester: {instance['semester']}, "
                f"Professors: {', '.join([prof['full_name'] for prof in instance['professors']])}"
            )
    else:
        print("No Module Instances.")


def view_ratings():
    response = session.get(f"{BASE_URL}/view/")
    data = handle_response(response)

    if data:
        for rating in data:
            print(f"The rating of Professor {rating['full_name']} ({rating['prof_code']}) is {rating['star_rating']}")


def average_rating(professor_id, module_code):
    response = session.get(f"{BASE_URL}/average/{professor_id}/{module_code}/")
    data = handle_response(response)

    if data:
        print(f"The rating of Professor {data['professor']} in module {data['module']} is {data['average_rating']}")


def rate(professor_id, module_code, year, semester, rating):
    data = {
        "professor_id": professor_id,
        "module_code": module_code,
        "year": year,
        "semester": semester,
        "rating": int(rating)
    }

    response = session.post(f"{BASE_URL}/rate/", json=data)

    if handle_response(response):
        print("Rating submitted successfully!")



def main():
    while True:
        
        # include a 'No connection' options 
        
        print("\nAvailable commands:\n register\n login <url>\n logout\n list\n view\n average <professor_id> <module_code>\n rate <professor_id> <module_code> <year> <semester> <rating>\n exit")
        command = input("Enter command: ").strip().split() 

        if not command:
            print("Please enter a command.")
            continue

        cmd = command[0] 
        args = command[1:] 

        if cmd == "register":
            register()
        elif cmd == "login":
            if len(args) != 1:
                print("Usage: login <url>")
            else:
                login(args[0])
        elif cmd == "logout":
            logout()
        elif cmd == "list":
            list_instances()
        elif cmd == "view":
            view_ratings()
        elif cmd == "average":
            if len(args) != 2:
                print("Usage: average <professor_id> <module_code>")
            else:
                average_rating(args[0], args[1])
        elif cmd == "rate":
            if len(args) != 5:
                print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")
            elif not args[4].isdigit:
                print("Rating must be a number.")
            else:
                rate(args[0], args[1], args[2], args[3], args[4])
        elif cmd == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid command. Try again.")
            
def handle_response(response):
    # if response.status_code == 404: 
    #     print("User must be logged in. Please log in using the login <url> command.")
    #     return None
    
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Unexpected response (Not JSON): {response.text}")
        return None

    if response.status_code in [200, 201]:  
        return data
    else:
        error_message = data.get("error", "An unknown error occurred") 
        print(f"Error: {error_message}")  
        return None



if __name__ == "__main__":
    main()
