from books1 import *
from clients import *
from abonnement import * 
#from book import modify_book
def main_menu():
  while True:
    print("")
    print("                            ")
    print("  Library Management System ")
    print("                            ")
    print("")
    print("                                ")
    print(" _____Enter your choice_____ ")
    print("                                ")
    print("1. Officer area")
    print("2. Client area ")
    print("3. Exit")

    user_type = input("Enter choice (1/2/3): ")
    if user_type == "1":
      password = input("Enter password: ")
      if password == "officer123":   ### check if the password is correct
        while True:
            print(" Officer  Menu ")
            print("                      ")
            print("Select option:")
            print("1. Clients  Management")
            print("2. Subscriptions Management")
            print("3. Books Management")
            print("4. see statistics")
            print("5. Exit")

            admin_choice = input("Enter choice (1/2/3/4): ")
            if admin_choice == "1":
              print(" Clients ")
              print("                  ")
              print("1. List clients")
              print("2. Add client")
              print("3. delete client")
              print("4. modify client")
              print("5. Add to blacklist")
              print("6. display blacklist")
            
              print("8. statistics clients")
              print("9. exit")
              sub_choice = int(input("Enter your choice: "))
              if sub_choice == 1:
                list_clients()
              elif sub_choice == 2:
                add_client()
              elif sub_choice == 3:
                delete_client()
              elif sub_choice == 4:
                modify_client() 
              elif sub_choice == 5:
                add_to_blacklist()
              elif sub_choice == 6:
                display_blacklist()
              elif sub_choice == 8:
                count_clients_by_gender()    
             
              elif sub_choice == 9:
                  continue  
              else:
                print("Invalid choice.")
                continue
                
                # code to display clients
                
            elif admin_choice == "2":
              print(" Subscriptions ")
              print("                   ")
              print("1. List subscriptions")
              print("2. Add subscription")
              print("3. Back")

              sub_choice = int(input("Enter your choice: "))
              if sub_choice == 1:
                list_subscriptions()
              elif sub_choice == 2:
                add_subscriptions()
              elif sub_choice ==3:
                 continue
              else:
               print("Invalid choice.")
               continue
                # code to display subscriptions
                
            elif admin_choice == "3":
               print(" Books   ")
               print("                ")
         
                   
               print("1. List books")
               print("2. Add book")
          
               print("4. remove book")
               print("5. modify  book")
               print("6. assuidite des clients")
               print("3. Back")

               sub_choice = int(input("Enter your choice: "))
               if sub_choice == 1:
                 list_books()
               elif sub_choice == 2:
                 add_book()
               elif sub_choice == 4:
                 delete_book()
               elif sub_choice == 5:
                 modify_book()
               elif sub_choice == 6:
                 loan_statistics()  #fonction qui calcule % des livres borrowed par hommes et femmmes 
               elif sub_choice == 3:
                 continue
               else:
                 print("Invalid choice.")
                # code to display books
               
            elif admin_choice == "4":
              accounting()
              

              
                # code to display books
                
            elif admin_choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
                continue
      else:
        print("Incorrect password. Access denied.")
    elif user_type == "2":
        while True:
            print(" Client area ")
            print("                  ")
            print("Select option:")
            print("1. Borrow a book")
            print("2. Return a book")
            print("3. see Notifications")
            print("4. Exit")

            client_choice = input("Enter choice (1/2/3): ")
            if client_choice == "1":
              borrow_book()
            elif client_choice == "2":
              return_book()   
                
            elif client_choice == "3":
              blacklist_clients()
            elif client_choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
    
    elif user_type == "3":
        break
    
    else:
        print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main_menu()
