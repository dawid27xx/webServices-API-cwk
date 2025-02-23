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

    if response.status_code == 201:
        print("Registration successful!")
    else:
        print(f"Error: {response.json()}")

def login(url):
    global BASE_URL, session

    username = input("Enter username: ")
    password = input("Enter password: ")

    data = {"username": username, "password": password}
    response = session.post(f"{BASE_URL}/login/", json=data)

    if response.status_code == 200:
        print("Login successful!")
    else:
        print(f"Error: {response.json()}")

def logout():
    global session
    response = session.post(f"{BASE_URL}/logout/")

    if response.status_code == 200:
        print("Logged out successfully!")
        session = requests.Session() 
    else:
        print(f"Error: {response.json()}")

def list_instances():
    response = session.get(f"{BASE_URL}/list/")
    
    if response.status_code == 200:
        instances = response.json()
        for instance in instances:
            print(
                f"Code: {instance['module__module_code']}, "
                f"Name: {instance['module__module_name']}, "
                f"Year: {instance['year']}, "
                f"Semester: {instance['semester']}, "
                f"Professors: {', '.join([prof['full_name'] for prof in instance['professors']])}"
)

    else:
        print(f"Error: {response.json()}")

def view_ratings():
    response = session.get(f"{BASE_URL}/view/")

    if response.status_code == 200:
        ratings = response.json()
        for rating in ratings:
            print(f"The rating of Professor {rating['full_name']} ({rating['prof_code']}) is {rating['star_rating']}")
    else:
        print(f"Error: {response.json()}")

def average_rating(professor_id, module_code):
    response = session.get(f"{BASE_URL}/average/{professor_id}/{module_code}/")

    if response.status_code == 200:
        data = response.json()
        print(f"The rating of Professor {data['professor']} in module {data['module']} is {data['average_rating']}")
    else:
        print(f"Error: {response.json()}")

def rate(professor_id, module_code, year, semester, rating):
    data = {
        "professor_id": professor_id,
        "module_code": module_code,
        "year": year,
        "semester": semester,
        "rating": int(rating)
    }

    response = session.post(f"{BASE_URL}/rate/", json=data)

    print(f"Raw Response: {response.text}")  # Debugging: Print raw response

    if response.status_code == 200:
        print("Rating submitted successfully!")
    else:
        try:
            print(f"Error: {response.json()}")
        except requests.exceptions.JSONDecodeError:
            print(f"Unexpected response (Not JSON): {response.text}")


def main():
    while True:
        print("\nAvailable commands: register, login <url>, logout, list, view, average <professor_id> <module_code>, rate <professor_id> <module_code> <year> <semester> <rating>, exit")
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
            else:
                rate(args[0], args[1], args[2], args[3], args[4])
        elif cmd == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
