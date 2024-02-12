import hashlib
import string
import tkinter as tk
import csv
import random
import os

def hash(text):
    hasher = hashlib.new('sha256')
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()

def usernameExists(username):
    with open("details.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return True
        return False

def pepper(password, salt):
    unhashed = password + salt
    hashed = hash(unhashed)
    return hashed

def salt():
    letterList = string.ascii_letters
    numList = string.digits
    charList = string.punctuation
    rand = 0
    salt = ""
    for i in range(10):
        r = random.randint(1,3)
        if r == 1:
            salt += random.choice(letterList)
        elif r == 2:
            salt+= random.choice(numList)
        else:
            salt += random.choice(charList)
    return salt

def login(username, password):
    with open("details.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                salt = row['salt']
                if row["hash"] == pepper(password, salt):
                    return "Logged in successfully!"
                else:
                    return "Wrong Password."
        return "Username not found."

def signup(username, password):
    with open("details.csv", mode='a', newline='') as file:
        fieldnames = ['username', 'salt', 'hash']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if os.path.getsize("details.csv") == 0:
            writer.writeheader()
        
        salt_value = salt()
        hash_value = pepper(password, salt_value)
        
        writer.writerow({'username': username, 'salt': salt_value, 'hash': hash_value})
        return "Signup successful."

def userHandle(username, password):
    if usernameExists(username):
        return login(username, password)
    else:
        return signup(username, password)

def submit():
    result = userHandle(username_entry.get(), password_entry.get())
    result_label.config(text=result)

# Create details.csv if it doesn't exist
if not os.path.exists("details.csv"):
    with open("details.csv", mode='w', newline='') as file:
        pass  # Just create an empty file

root = tk.Tk()
root.geometry("500x300")

userLabel = tk.Label(root, text="Username: ")
userLabel.place(x=100, y=100)
passLabel = tk.Label(root, text="Password: ")
passLabel.place(x=100, y=150)

# Entry fields for username and password
username_entry = tk.Entry(root)
username_entry.place(x=200, y=100)
password_entry = tk.Entry(root, show="*")
password_entry.place(x=200, y=150)

submitButton = tk.Button(root, text="Submit", command=submit)
submitButton.place(x=250, y=200)

result_label = tk.Label(root, text="")
result_label.place(x=250, y=250)

root.mainloop()
