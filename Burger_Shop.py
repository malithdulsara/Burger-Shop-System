import os
import sys
import time
from datetime import datetime
import maskpass
from colorama import Fore,Style,init

init(autoreset=True)

order_ids = []
customer_ids = []
customer_names = []
quantities = []
order_statuses = []
order_times = []
 

BURGER_PRICE = 500.0

PREPARING = 0 
DELIVERED = 1
CANCEL = 2 

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_all_data():
    with open("orders.txt", "w") as f:
        for i in range(len(order_ids)):
            f.write(f"{order_ids[i]},{customer_ids[i]},{customer_names[i]},{quantities[i]},{order_statuses[i]},{order_times[i]}\n")

def load_data():
    order_ids.clear()
    customer_ids.clear()
    customer_names.clear()
    quantities.clear()
    order_statuses.clear()
    order_times.clear()

    if os.path.exists("orders.txt"):
        with open("orders.txt", "r") as f:
            for line in f:
                try:
                    parts = line.strip().split(",")
                    if len(parts) == 6:
                        order_ids.append(parts[0])
                        customer_ids.append(parts[1])
                        customer_names.append(parts[2])
                        quantities.append(int(parts[3]))
                        order_statuses.append(int(parts[4]))
                        order_times.append(parts[5])
                except (ValueError,IndexError):
                    continue

def generate_order_id():
   
    if not order_ids:
        return "B0001"
    last_id = order_ids[-1]
    last_num = int(last_id[1:])
    new_num = last_num + 1
    return f"B{new_num:04d}"

def place_order():
    while True:
        clear_console()
        print(f"{Fore.CYAN}" + "-" * 45)
        print(f"{Fore.CYAN}\t    PLACE ORDER")
        print(f"{Fore.CYAN}" + "-" * 45)

        order_id = generate_order_id()
        print(f"{Fore.WHITE}ORDER ID - {Fore.YELLOW}{order_id}")
        print(f"{Fore.CYAN}" + "=" * 15)
        
        while True:
            cust_id = input(f"\n{Fore.WHITE}Enter Customer ID (phone no.): ").strip()

            temp_id = cust_id.replace(" ","")
            if len(temp_id) == 10 and temp_id.startswith("0") and temp_id.isdigit():
                break
            print(f"{Fore.RED}Invalid Phone Number! It should be 10 digits starting with 0.") 
        
        name = ""
        if temp_id in customer_ids:
            idx = customer_ids.index(temp_id)
            name = customer_names[idx]
            print(f"{Fore.WHITE}Customer Name : {Fore.YELLOW}{name}")
        else:
            while True:
                name = input("Customer Name : ")
                if name.isalpha() and len(name) >=3: 
                    break
                else:
                    print(f"{Fore.RED}Invalid Name! Name should have at least 3 letters and no numbers/symbols.")
            
        while True:
            try:
                qty = int(input(f"{Fore.WHITE}Enter Burger Quantity - "))
                if qty > 0:
                    break
                print("Quantity must be greater than 0!")
            except ValueError:
                print(f"{Fore.RED}Invalid input! Please enter a number for quantity.")
        
        total = qty * BURGER_PRICE
        print(f"{Fore.WHITE}Total value - {Fore.GREEN}{total:.2f}")
        
        while True:
            confirm = input(f"\n{Fore.WHITE}Are you confirm order (Y/N) - ").lower()
            if confirm == 'y':
                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                
                order_ids.append(order_id)
                customer_ids.append(temp_id)
                customer_names.append(name)
                quantities.append(qty)
                order_statuses.append(PREPARING)
                order_times.append(current_time)
                
                save_all_data()
                print(f"\n{Fore.GREEN}Order placed at: {current_time}")
                print(f"{Fore.GREEN}Your order is entered to the system successfully...") 
                break 
            elif confirm == 'n':
                print(f"\n{Fore.RED}Order Cancelled.")
                break
            else:
                print(f"{Fore.RED}Invalid input! Please enter 'Y' to confirm or 'N' to discard.")
            
        if input(f"\n{Fore.WHITE}Do you want to place another order (Y/N): ").lower() != 'y':
            break

def search_best_customer():
    clear_console()
    now = datetime.now()
    current_month_year = now.strftime("%Y-%m")
    print(f"{Fore.CYAN}" + "-" * 45)
    print(f"{Fore.CYAN}\tBEST CUSTOMERS - {Fore.YELLOW}{now.strftime('%B %Y').upper()}")
    print(f"{Fore.CYAN}" + "-" * 45)
    
    unique_customers = []
    for cid in customer_ids:
        if cid not in unique_customers:
            unique_customers.append(cid)
            
    customer_totals = []
    for cid in unique_customers:
        total = 0
        name = ""
        for i in range(len(customer_ids)):
            if customer_ids[i] == cid and order_statuses[i] == DELIVERED and order_times[i].startswith(current_month_year):
                total += quantities[i] * BURGER_PRICE
                name = customer_names[i]
        if total > 0:
            customer_totals.append([cid, name, total])
    if not customer_totals:
        print(f"\n{Fore.RED}\tNo Delivered Orders Found Yet!")
        print(f"{Fore.WHITE}\tComplete an order to see best customers.")
    else:  
        customer_totals.sort(key=lambda x: x[2], reverse=True)
    
        print(f"{Fore.WHITE}{'CustomerID':<15} {'Name':<15} {'Total':>10}")
        print(f"{Fore.CYAN}"+"-" * 45)
        for cust in customer_totals:
            print(f"{Fore.WHITE}{cust[0]:<15} {cust[1]:<15} {cust[2]:>10.2f}")
    print(f"{Fore.CYAN}"+"-" * 45)   
    input(f"\n{Fore.WHITE}Do you want to go back to main menu? (Y/N)> ")

def search_order():
    while True:
        clear_console()
        print(f"{Fore.CYAN}" + "-" * 45)
        print(f"{Fore.CYAN}\t    SEARCH ORDER DETAILS")
        print(f"{Fore.CYAN}" + "-" * 45)
        
        oid = input(f"\n{Fore.WHITE}Enter order Id - ").strip()
        if oid in order_ids:
            idx = order_ids.index(oid)
            status_list = ["Preparing", "Delivered", "Cancel"]
            current_status = status_list[order_statuses[idx]]

            print(f"{Fore.CYAN}" + "-"* 45)
            print(f"{Fore.WHITE} ORDER ID    : {order_ids[idx]}")
            print(f"{Fore.WHITE} DATE & TIME : {order_times[idx]}") 
            print(f"{Fore.CYAN}" + "-"* 45)
            print(f"{Fore.WHITE} Customer ID : {customer_ids[idx]}")
            print(f"{Fore.WHITE} Name        : {customer_names[idx]}")
            print(f"{Fore.CYAN}" + "-"* 45)
            print(f"{Fore.WHITE} Quantity    : {quantities[idx]}")
            print(f"{Fore.WHITE} Unit Price  : {BURGER_PRICE:>10.2f}")
            
            total_value = quantities[idx] * BURGER_PRICE
            print(f"{Fore.WHITE} Total Value : {total_value:>10.2f}")
            print(f"{Fore.CYAN}" + "-"* 45)
            print(f"{Fore.WHITE} Order Status: {current_status}")
            print(f"{Fore.CYAN}" + "-"* 45)
        else:
            print(f"{Fore.RED}Invalid Order ID.") 
            
        if input(F"\n{Fore.WHITE}Do you want to search another order details (Y/N): ").lower() != 'y': break

def search_customer():
    while True:
        clear_console()
        print(f"{Fore.CYAN}" + "-" * 45)
        print(f"{Fore.CYAN}\t    SEARCH CUSTOMER DETAILS")
        print(f"{Fore.CYAN}" + "-" * 45)
        cid = input(f"\n{Fore.WHITE}Enter customer Id (Phone No) - ").strip() 
        
        if cid in customer_ids:
            print(f"\n{Fore.WHITE}CustomerID - {cid}")
            print(f"{Fore.WHITE}Name       - {customer_names[customer_ids.index(cid)]}")
            print(f"\n{Fore.CYAN}Customer Order Details")
            print(f"{Fore.CYAN}{'Order_ID':<12} {'Qty':<5} {'Total_Value':>10}")
            print(f"{Fore.WHITE}"+"-" * 30)
            for i in range(len(order_ids)):
                if customer_ids[i] == cid:
                    print(f"{Fore.WHITE}{order_ids[i]:<12} {quantities[i]:<5} {quantities[i]*BURGER_PRICE:>10.2f}")
        else:
            print(f"{Fore.RED}This customer ID is not added yet....") 
            
        if input(f"\n{Fore.WHITE}Do you want to search another customer details (Y/N): ").lower() != 'y': break

def view_orders():
    while True:
        clear_console()
        print(f"{Fore.CYAN}" + "-" * 45)
        print(f"{Fore.CYAN}\t    VIEW ORDER LIST")
        print(f"{Fore.CYAN}" + "-" * 45)
        
        print(f" {Fore.YELLOW}[1]{Fore.WHITE} Delivered Orders")
        print(f" {Fore.YELLOW}[2]{Fore.WHITE} Preparing Orders")
        print(f" {Fore.YELLOW}[3]{Fore.WHITE} Cancel Orders")

        opt = input(f"\n{Fore.GREEN}Enter option > {Fore.WHITE}")
        
        status_view = {"1": DELIVERED, "2": PREPARING, "3": CANCEL}.get(opt, -1)
        if status_view == -1: break
        
        clear_console()
        print(f"{Fore.CYAN}{'OrderID':<10} {'CustomerID':<15} {'Name':<12} {'Qty':<5} {'Total':>10}")
        print("-" * 60)
        for i in range(len(order_ids)):
            if order_statuses[i] == status_view:
                print(f"{Fore.WHITE}{order_ids[i]:<10} {customer_ids[i]:<15} {customer_names[i]:<12} {quantities[i]:<5} {quantities[i]*BURGER_PRICE:>10.2f}")
        if input(f"\n{Fore.WHITE}Go to home page (Y/N): ").lower() == 'y': break

def update_order_details():
    while True:
        clear_console()
        print(f"{Fore.CYAN}" + "-" * 45)
        print(f"{Fore.CYAN}\t    UPDATE ORDER DETAILS")
        print(f"{Fore.CYAN}" + "-" * 45)
        oid = input(f"\n{Fore.WHITE}Enter order Id - ") 
        
        if oid not in order_ids:
            print(f"{Fore.RED}Invalid Order ID.")
            if input(f"{Fore.WHITE}Try again? (Y/N): ").lower() != 'y': break
            continue
            
        idx = order_ids.index(oid)
        if order_statuses[idx] == DELIVERED: print(f"{Fore.RED}Already Delivered! Cannot update.") 
        elif order_statuses[idx] == CANCEL: print(f"{Fore.RED}Already Cancelled! Cannot update.")
        else:
            print(f"\n{Fore.WHITE}Name: {Fore.YELLOW}{customer_names[idx]}{Fore.WHITE} | Qty: {Fore.YELLOW}{quantities[idx]}")
            print(f"{Fore.WHITE}Status: {Fore.CYAN}{['Preparing', 'Delivered', 'Cancel'][order_statuses[idx]]}")
            print("-" * 25)
            print(f"{Fore.YELLOW}(01){Fore.WHITE} Update Quantity")
            print(f"{Fore.YELLOW}(02){Fore.WHITE} Update Status") 
            
            opt = input(f"\n{Fore.GREEN}Option - {Fore.WHITE}")

            if opt == '1' or opt == '01':
                while True:
                    try:
                        new_qty = int(input(f"{Fore.WHITE}Enter New Quantity: "))
                        if new_qty > 0:
                            quantities[idx] = new_qty
                            new_total = new_qty * BURGER_PRICE
                            print(f"{Fore.GREEN}Quantity Updated! New Total Value: {new_total:.2f}")
                            break
                        print(f"{Fore.RED}Quantity must be greater than 0!")
                    except ValueError:
                        print(f"{Fore.RED}Invalid input! Please enter a number.")
            
            elif opt == '2' or opt == '02':
                print(f"\n{Fore.CYAN}New Status: {Fore.YELLOW}(0)Preparing (1)Delivered (2)Cancel")
                while True:
                    try:
                        new_status = int(input(f"{Fore.WHITE}Enter Status Number > "))
                        if new_status in [0, 1, 2]:
                            order_statuses[idx] = new_status
                            status_name = ['Preparing', 'Delivered', 'Cancel'][new_status]
                            print(f"{Fore.GREEN}Status Updated to: {status_name}")
                            break
                        print(f"{Fore.RED}Invalid! Please enter 0, 1 or 2.")
                    except ValueError:
                        print(f"{Fore.RED}Invalid input!")
            save_all_data()
        if input(f"\n{Fore.WHITE}Do you want to update another order? (Y/N): ").lower() != 'y': break

def home_page():
    load_data()
    while True:
        clear_console()
        print(f"{Fore.CYAN}" + "-" * 40)
        print(f"{Fore.CYAN}\t       BURGER SHOP")
        print(f"{Fore.CYAN}" + "-" * 40)
        print(f" {Fore.YELLOW}[1]{Fore.WHITE} Place Order\t\t {Fore.YELLOW}[2]{Fore.WHITE} Search Best Customer")
        print(f" {Fore.YELLOW}[3]{Fore.WHITE} Search Order\t\t {Fore.YELLOW}[4]{Fore.WHITE} Search Customer")
        print(f" {Fore.YELLOW}[5]{Fore.WHITE} View Orders\t\t {Fore.YELLOW}[6]{Fore.WHITE} Update Order Details")
        print(f" {Fore.YELLOW}[7]{Fore.WHITE} Exit")

        option = input(f"\n{Fore.GREEN}Enter option > {Fore.WHITE}")

        if option.isdigit():    
            if option == '1': place_order()
            elif option == '2': search_best_customer()
            elif option == '3': search_order()
            elif option == '4': search_customer()
            elif option == '5': view_orders()
            elif option == '6': update_order_details()
            elif option == '7': 
                print(f"\n{Fore.CYAN}\tYou left the program...\n") 
                time.sleep(1)
                sys.exit()
            else:
                input(f"\n{Fore.RED}Invalid Option! Press Enter to try again...")
        else:
            input(f"\n{Fore.RED}Invalid Input! Please enter only numbers (1-7). Press Enter...")

def login_system():
    correct_password = "admin" 
    
    while True:
        clear_console()
        print(f"{Fore.CYAN}" + "-" * 40)
        print(f"{Fore.CYAN}\t   BURGER SHOP LOGIN")
        print(f"{Fore.CYAN}" + "-" * 40)
        
        entered_password = maskpass.askpass(prompt="\n Enter System Password: ")
        
        if entered_password == correct_password:
            print(f"\n{Fore.GREEN} Login Successful! Access Granted.")
            import time
            time.sleep(1)
            break
        else:
            print(f"\n{Fore.RED} Incorrect Password! Please try again.")
            input(f"\n{Fore.WHITE} Press Enter to continue...")

if __name__ == "__main__":
    login_system()
    home_page()