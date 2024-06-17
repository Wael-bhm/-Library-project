import datetime

import json
# import collection 
import matplotlib.pyplot as plt
def load_clients():
    try:
        with open("clients.json", "r") as f:
            clients = json.load(f)
    except FileNotFoundError:
        clients = []
    return clients
def load_blacklist():
    try:
        with open("blacklist.json", "r") as f:
            blacklist = json.load(f)
    except FileNotFoundError:
       blacklist= []
    return blacklist

  
def save_clients(clients):    
  with open("clients.json", "w") as f:
    json.dump(clients, f)

def list_clients():
  clients=load_clients()
  print("========== List of clients ==========")
  for client in clients:
    print(f"ID: {client['id']}, Name: {client['name']}, Email: {client['email']}")
    print()      
# Fonction pour ajouter un client
def add_client():
    clients = load_clients()
    client = {}
    client["name"] = input("Enter client name: ")
    client["email"] = input("Enter client email: ")
    is_premium = input("Is the client a premium member? (y/n): ")
    client["is_premium"] = True if is_premium.lower() == 'y' else False
    client["client_type"] = input("Enter client genre(female/male): ")
    client["id"] = 1 if not clients else max(client["id"] for client in clients) + 1
    clients.append(client)
    save_clients(clients)
    print("Client added successfully.")




def delete_client():
  clients=load_clients()
  client_id = int(input("Enter client ID: "))
  for i, client in enumerate(clients):
    if client["id"] == client_id:
      del clients[i]
      print(f"Client with ID {client_id} has been deleted.")
    
      with open("clients.json", "w") as f:
        json.dump(clients, f)
        return
  print(f"Client with ID {client_id} not found.")

# Fonction pour ajouter un client à la liste noire
def add_to_blacklist():
    blacklist=[]
    clients=load_clients()
    client_id = int(input("Enter client ID: "))
    for client in clients:
        if client["id"] == client_id:
            blacklist.append(client_id)
            print(f"Client with ID {client_id} has been added to the blacklist.")
            with open("blacklist.json", "w") as f:
                json.dump(blacklist, f)
            return
    print(f"Client with ID {client_id} not found.")

# Fonction pour modifier un client
def modify_client():
    clients=load_clients()
    client_id = int(input("Enter client ID: "))
    for client in clients:
        if client["id"] == client_id:
            name = input(f"Enter new name for {client['name']}: ")
            email = input(f"Enter new email for {client['email']}: ")
            client_type = input(f"Enter new type for {client['client_type']}: ")
            client["name"] = name
            client["email"] = email
            client["client_type"] = client_type
            print(f"Client with ID {client_id} has been modified.")
            with open("clients.json", "w") as f:
                json.dump(clients, f)
            return
    print(f"Client with ID {client_id} not found.")

def display_blacklist():
    blacklist = load_blacklist()

    if not blacklist:
        print("The blacklist is empty.")
        return

    print("Blacklisted clients:")
    for client_id in blacklist:
        client = next((client for client in load_clients() if client["id"] == client_id), None)
        if client:
            print(f"- {client['name']} (ID: {client_id})")
        else:
            print(f"- Client with ID {client_id} not found.")


####################################
def save_blacklist(blacklist):
    with open("blacklist.json", "w") as f:
        json.dump(blacklist, f)

def blacklist_clients():
    blacklist = load_blacklist()
    clients = load_clients()
    notifications = []

    for client in clients:
        if "borrows" not in client or not client["borrows"]:
            continue

        for borrow in client["borrows"]:
            borrow_date = datetime.datetime.strptime(borrow["borrow_date"], "%Y-%m-%d").date()
            today = datetime.date.today()
#notifications.append
            if (today - borrow_date).days > 15:
                blacklist.append(client["id"])
                print("*" * 80)
                print(f"{client['name']} with id {client['id']} please return book with id {borrow['book_id']} which has exceeded 15 days")
                     
                print("*" * 80)

    save_blacklist(blacklist)

    with open("notifications.txt", "w") as f:
        f.write("\n".join(notifications))

    return notifications



  #################################
def count_clients_by_gender():
    clients = load_clients()
    male_count = 0
    female_count = 0
    for client in clients:
        if client["client_type"] == "male":
            male_count += 1
        elif client["client_type"] == "female":
            female_count += 1
    print(f"Number of male clients: {male_count}")
    print(f"Number of female clients: {female_count}")
