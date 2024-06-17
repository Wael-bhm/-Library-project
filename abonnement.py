from clients import list_clients
from clients import load_clients
import json 
import datetime
import matplotlib.pyplot as plt
from dateutil import *
from dateutil.relativedelta import relativedelta
def load_subscriptions():
    try:
        with open("subscriptions.json", "r") as f:
            subscriptions = json.load(f)
    except FileNotFoundError:
        subscriptions = []
    return subscriptions
  
def save_subscriptions(subscriptions):    
  with open("subscriptions.json", "w") as f:
    json.dump(subscriptions, f)



def list_subscriptions():
  clients = load_clients()
  subscriptions = load_subscriptions()
  
  print("========== List of subscriptions ==========")
  for subscription in subscriptions:
    client_id = subscription["client_id"]
    client = next((client for client in clients if client["id"] == client_id), None)
    if client:
      print(f"Client: {client['name']}, Email: {client['email']}")
    else:
      print("Client not found")
  print()


       

# Fonction pour ajouter un abonnement
def add_subscriptions():
    subscriptions = load_subscriptions()
    clients = load_clients()
    client_id = int(input("Enter client ID: "))
    
    client = next((client for client in clients if client["id"] == client_id), None)

    if not client:
        print("Client not found.")
        return

    subscription = next((subscription for subscription in subscriptions if subscription["client_id"] == client_id), None)

    if subscription:
        print("Client already has an active subscription.")
        renew = input("Do you want to renew the subscription? (y/n)").lower()
        if renew == "y":
            subscription["start_date"] = datetime.date.today().strftime("%Y-%m-%d")
            subscription["end_date"] = (datetime.date.today() + relativedelta(months=1)).strftime("%Y-%m-%d")
            save_subscriptions(subscriptions)
            print("Subscription renewed successfully.")
            return
        else:
            return

    premium = client.get("premium", False)

    subscription_id = 1 if not subscriptions else max(subscription["id"] for subscription in subscriptions) + 1
    subscription = {"id": subscription_id, "client_id": client_id, "start_date": datetime.date.today().strftime("%Y-%m-%d")}

    if premium:
        subscription["end_date"] = (datetime.date.today() + relativedelta(months=2)).strftime("%Y-%m-%d")
        subscription["cost"] = 10
    else:
        subscription["end_date"] = (datetime.date.today() + relativedelta(months=1)).strftime("%Y-%m-%d")
        subscription["cost"] = 5
    
    subscriptions.append(subscription)
    save_subscriptions(subscriptions)
    print("Subscription added successfully.")


# Fonction pour voir statistique de revenus par mois
def accounting():
    subscriptions = load_subscriptions()
    total_fees = 0
    fees_by_month = {}
    
    # Loop through all subscriptions and calculate fees
    for subscription in subscriptions:
        start_date = datetime.datetime.strptime(subscription["start_date"], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(subscription["end_date"], "%Y-%m-%d").date()
        duration = (end_date - start_date).days
        fees = subscription["cost"] * duration / 30  # assuming 30 days per month
        total_fees += fees
        
        # Add fees to dictionary by month
        month_year = start_date.strftime("%m/%Y")
        if month_year not in fees_by_month:
            fees_by_month[month_year] = 0
        fees_by_month[month_year] += fees
    
    # Print total fees
    print(f"Total fees: {total_fees:.2f}D")
    
    # Plot fees by month
    x = list(fees_by_month.keys())
    x.sort(key=lambda d: datetime.datetime.strptime(d, '%m/%Y'))
    y = [fees_by_month[m] for m in x]
    plt.plot(x, y)
    plt.xlabel("Month")
    plt.ylabel("Fees (D)")
    plt.title("Fees by Month")
    plt.show()