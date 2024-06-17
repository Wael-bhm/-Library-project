import datetime
#from datetime import date
from datetime import timedelta
import json
from clients import * 
from abonnement import *
def load_books():
    try:
        with open("books.json", "r") as f:
            books = json.load(f)
    except FileNotFoundError:
        books = []
    return books
def save_books(books):
    with open("books.json", "w") as f:
        json.dump(books, f)

def load_books_borrowed():
    try:
        with open("borrows.json", "r") as f:
            borrows = json.load(f)
    except FileNotFoundError:
        borrows = []
    return borrows

def save_books_borrowed(borrows):
    with open("borrows.json", "w") as f:
        json.dump(borrows, f)


def list_books():
    books = load_books()
    for book in books:
        print("Book ID:", book["id"])
        print("Title:", book["title"])
        print("Author:", book["author"])
        print("Published Date:", book["published_date"])
        print("Publisher:", book["publisher"])
        print("Genre:", book["genre"])
        print("")
def add_book():
  books = load_books()
    
    # Create a new empty dictionary to hold information about the new book
  new_book ={}
    
    # Ask the user for the book ID
  #new_book["id"] = int(input("Enter book ID: "))
    
    # Check if the book already exists in the library
  new_book["title"] = input("Enter book title: ")
  new_book["author"] = input("Enter book author: ")
  new_book["publisher"] = input("Enter book publisher: ")
  new_book["isbn"] = input("Enter book ISBN: ")
  for book in books:
    if book["isbn"] == new_book["isbn"]:
      print("Book with ISBN {} already exists in the library.".format(new_book["isbn"]))
      return
    #return 
  new_book["id"] = len(books) + 1
  books.append(new_book)
  save_books(books)
  print("Book added successfully.")
    # Print a message to confirm that the book was added successfull

    
def delete_book():
    books = load_books()
    book_id = int(input("Enter book ID to delete: "))
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            save_books(books)
            print("Book deleted successfully.")
            return
    print("Book not found.")

def modify_book():
    books = load_books()
    book_id = int(input("Enter book ID to modify: "))
    for book in books:
        if book["id"] == book_id:
            print(f"Book ID: {book['id']}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author']}")
            print(f"Published Date: {book['published_date']}")
            print(f"Publisher: {book['publisher']}")
            print(f"Genre: {book['genre']}")
            print("")
            choice = input("Enter the field you want to modify: ")
            if choice.lower() == "id":
                print("ID cannot be modified.")
            elif choice.lower() == "title":
                book["title"] = input("Enter new title: ")
            elif choice.lower() == "author":
                book["author"] = input("Enter new author: ")
            elif choice.lower() == "published date":
                book["published_date"] = input("Enter new published date (YYYY-MM-DD): ")
            elif choice.lower() == "publisher":
                book["publisher"] = input("Enter new publisher name: ")
            elif choice.lower() == "genre":
                book["genre"] = input("Enter new genre: ")
            else:
                print("Invalid choice.")
                return
            save_books(books)
            print("Book modified successfully.")
            return
    print("Book not found.")

def borrow_book():
    clients = load_clients()
    books = load_books()
    blacklist = load_blacklist()
    today = datetime.datetime.today()
    for client in clients:
        borrows = client.get("borrows", [])
        for borrow in borrows:
            if "borrow_date" in borrow:
                borrow_date = datetime.datetime.strptime(borrow["borrow_date"], "%Y-%m-%d")
                if today > borrow_date + timedelta(days=15):
                    client_id = client["id"]
                    if client_id not in blacklist:
                        blacklist.append(client_id)
                      
    save_blacklist(blacklist)
    client_id = int(input("Enter client ID: "))
    client = next((client for client in clients if client["id"] == client_id), None)

    for id in blacklist:
        if id == client_id:
            print("You are banned, you don't have the right to borrow any book.")
            return

    if not client:
        print("Client not found.")
        return

    book_id = int(input("Enter book ID: "))
    book = next((book for book in books if book["id"] == book_id), None)

    if not book:
        print("Book not found.")
        return

    # Check if the client has already borrowed two copies of the same book
    book_copies_borrowed = 0
    for c in clients:
        for borrow in c.get("borrows", []):
            if borrow["book_id"] == book_id:
                book_copies_borrowed += 1
    if book_copies_borrowed >= 2:
        print("No more copies of this book.")
        return

    # Check if the book is already borrowed
    for borrow in client.get("borrows", []):
        if borrow["book_id"] == book_id:
            print("The book is already borrowed.")
            return

    borrows = client.get("borrows", [])
    if len(borrows) >= 3:
        print("This client has reached the maximum number of book borrowings.")
        return

    borrow_date = datetime.date.today().strftime("%Y-%m-%d")
    borrows.append({"book_id": book_id, "borrow_date": borrow_date})
    client["borrows"] = borrows

    print(f"{client['name']} has successfully borrowed '{book['title']}'.")
    print("==========")

    save_books(books)
    save_clients(clients)




def return_book():
    clients = load_clients()
    books = load_books()
    blacklist = load_blacklist()
    

    # Save the updated blacklist
    

    
    
    #book_id = int(input("Enter book ID: "))
    #blacklist_clients()
    book_id_str = input("Enter book ID: ")
    if book_id_str.isdigit():
      book_id = int(book_id_str)
      #blacklist_clients()
    book = next((book for book in books if book["id"] == book_id), None)

    if not book:
        print("Book not found.")
        return

    client_id = int(input("Enter client ID: "))
    client = next((client for client in clients if client["id"] == client_id), None)

    if not client:
        print("Client not found.")
        return

    borrows = client.get("borrows", [])

    borrowed_book = next((borrow for borrow in borrows if borrow["book_id"] == book_id), None)

    if not borrowed_book:
        print("Book is not borrowed by the client.")
        return

    borrows.remove(borrowed_book)

    client["borrows"] = borrows
    if client_id in blacklist:
        blacklist = [id for id in blacklist if id != client_id]
        save_blacklist(blacklist)

    save_clients(clients)
    print("Book returned successfully.")
    save_blacklist(blacklist)
    save_books(books)
    save_books_borrowed(borrows)

import datetime

def notify_and_blacklist():
    clients = load_clients()
    books = load_books()
    borrows = load_books_borrowed()
    blacklist = load_blacklist()
    today = datetime.date.today()
    for borrow in borrows:
        book_id = borrow.get("book_id")
        borrow_date = datetime.datetime.strptime(borrow.get("borrow_date"), "%Y-%m-%d").date()
        days_borrowed = (today - borrow_date).days
        if days_borrowed >= 14:
            client_id = next((client.get("id") for client in clients if client.get("borrows") and any(borrow.get("book_id") == book_id for borrow in client.get("borrows"))), None)
            if client_id:
                client = next((client for client in clients if client.get("id") == client_id), None)
                if client_id not in blacklist:
                    blacklist.append(client_id)
                    print(f"{client.get('name')} has not returned '{next((book.get('title') for book in books if book.get('id') == book_id), None)}' within the borrowing period and has been added to the blacklist.")
                    save_blacklist(blacklist)
                else:
                    print(f"{client.get('name')} has not returned '{next((book.get('title') for book in books if book.get('id') == book_id), None)}' within the borrowing period but is already on the blacklist.")
            else:
                print(f"No client found for book ID {book_id}.")
        elif days_borrowed == 13:
            client_id = next((client.get("id") for client in clients if client.get("borrows") and any(borrow.get("book_id") == book_id for borrow in client.get("borrows"))), None)
            if client_id:
                client = next((client for client in clients if client.get("id") == client_id), None)
                print(f"Reminder: '{next((book.get('title') for book in books if book.get('id') == book_id), None)}' borrowed by {client.get('name')} is due tomorrow.")
            else:
                print(f"No client found for book ID {book_id}.")

def loan_statistics():
    clients = load_clients()
    total_male_loans = 0
    total_female_loans = 0
    for client in clients:
        gender = client["client_type"]
        loans = client.get("borrows", [])
        if gender == "male":
            total_male_loans += len(loans)
        elif gender == "female":
            total_female_loans += len(loans)
    total_loans = total_male_loans + total_female_loans
    male_percentage = total_male_loans / total_loans * 100 if total_loans > 0 else 0
    female_percentage = total_female_loans / total_loans * 100 if total_loans > 0 else 0
    print(f"Out of {total_loans} loans, {male_percentage:.2f}% were borrowed by male clients and {female_percentage:.2f}% were borrowed by female clients.")
