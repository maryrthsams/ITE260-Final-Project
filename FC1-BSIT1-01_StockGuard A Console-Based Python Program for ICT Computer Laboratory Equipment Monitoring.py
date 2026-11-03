"""
StockGuard: A Console-Based Python Program for ICT Computer Laboratory
Equipment Monitoring
"""

import re



ADMINS = {
    "Fred": "admin123",
    "Maryth": "admin456",
    "Evelyn": "admin789",
}

COMLABS = ["Comlab 1", "Comlab 2", "Comlab 3"]

STATUS_OPTIONS = ["Working", "Under Repair", "Defective"]


CATALOG = {
    "001": "Keyboard",
    "002": "Mouse",
    "003": "Monitor",
    "004": "System Unit",
    "005": "Router / Switch",
    "006": "LAN Cable",
    "007": "Computer Chair",
    "008": "Computer Table",
}



equipment = []




def input_integer(prompt):
    """Digits only (no letters, symbols, signs or decimals)."""
    while True:
        value = input(prompt).strip()
        if value.isascii() and value.isdigit():
            return int(value)
        print("Numbers only. Please enter a whole number (no letters or symbols).")


def input_number(prompt):
    """Digits with an optional decimal part, e.g. 150 or 150.50."""
    while True:
        value = input(prompt).strip()
        if re.fullmatch(r"\d+(\.\d{1,2})?", value):
            return float(value)
        print("Numbers only. Please enter an amount such as 150 or 150.50.")


def choose_from(title, options):
    """Show a numbered list and return the chosen option."""
    print(f"\n{title}")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        choice = input("\nEnter your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Invalid choice. Please try again.")


def print_header(*lines):
    print("=" * 40)
    for line in lines:
        print(line.center(40) if line else "")
    print("=" * 40)


def find_item(prompt):
    """Ask for an Equipment ID and return the matching record.
    The same item (e.g. Keyboard 001) can be in several labs, so if more
    than one record matches, ask which Computer Laboratory is meant."""
    equipment_id = input(prompt).strip()
    if equipment_id.isascii() and equipment_id.isdigit():
        equipment_id = equipment_id.zfill(3)   # "1" -> "001"

    matches = [e for e in equipment if e["id"] == equipment_id]
    if not matches:
        print(f"\nNo equipment found with ID '{equipment_id}'.\n")
        return None
    if len(matches) == 1:
        return matches[0]

    comlab = choose_from(
        f"ID '{equipment_id}' is in several labs. Select Computer Laboratory:",
        [m["comlab"] for m in matches],
    )
    return next(m for m in matches if m["comlab"] == comlab)



def main():
    login_exit()


def login_exit():
    while True:
        print_header("STOCKGUARD", "Digital Stock Monitoring")
        print("\n1. Login")
        print("2. Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            login_user()
        elif choice == "2":
            if confirm_exit():
                print("\nExiting the program. Goodbye!")
                return
        else:
            print("\nInvalid choice. Please try again.\n")


def confirm_exit():
    print_header("STOCKGUARD")
    print("\nAre you sure you want to exit?")
    print("1. Yes")
    print("2. No")
    choice = input("\nEnter your choice: ").strip()
    return choice == "1"


def login_user():
    while True:
        print_header("STOCKGUARD", "Administrator Login")
        username = input("\nUsername: ").strip()
        password = input("Password: ")

        if username in ADMINS and ADMINS[username] == password:
            print(f"\nWelcome, {username}!\n")
            main_menu()
            return

        print("\nInvalid username or password.")
        print("\n1. Try Again")
        print("2. Back to Login Menu")
        while True:
            choice = input("\nEnter your choice: ").strip()
            if choice in ("1", "2"):
                break
            print("Invalid choice. Please try again.")
        if choice == "2":
            print()
            return



def main_menu():
    while True:
        print_header("STOCKGUARD", "Digital Stock Monitoring")
        print("\n             MAIN MENU\n")
        print("1. Add Equipment")
        print("2. View Inventory")
        print("3. Search Equipment")
        print("4. Equipment Status")
        print("5. Logout")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_equipment()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            search_equipment()
        elif choice == "4":
            equipment_status()
        elif choice == "5":
            if confirm_exit():
                print("\nLogging out to login menu.\n")
                return
        else:
            print("\nInvalid choice. Please try again.\n")



def add_equipment():
    print_header("STOCKGUARD")
    print("\n           ADD NEW EQUIPMENT")

    # Equipment can only be picked from the fixed ICT Comlab catalog
    equipment_name = choose_from("Select Equipment:", list(CATALOG.values()))
    # ID is automatic, based on the chosen item
    equipment_id = next(k for k, v in CATALOG.items() if v == equipment_name)

    comlab = choose_from("Select Computer Laboratory:", COMLABS)

    if any(e["id"] == equipment_id and e["comlab"] == comlab for e in equipment):
        print(f"\n{equipment_name} (ID {equipment_id}) is already in {comlab}.\n")
        return

    print(f"\nEquipment Name   : {equipment_name}")
    print(f"Equipment ID     : {equipment_id}  (automatic)")
    print(f"Computer Lab     : {comlab}")
    quantity = input_integer("Quantity         : ")
    price = input_number("Unit Value (PHP) : ")
    total = quantity * price
    print(f"Total Value (PHP): {quantity} x {price:.2f} = {total:,.2f}")

    choice = choose_from("Save this equipment?", ["Save", "Cancel"])

    if choice == "Save":
        equipment.append({
            "id": equipment_id,
            "name": equipment_name,
            "comlab": comlab,
            "quantity": quantity,
            "price": price,
            "status": "Working",
        })

        print(f"\nEquipment '{equipment_name}' (ID {equipment_id}) added to {comlab} successfully.\n")
    else:
        print("\nAdd equipment canceled.\n")




def view_inventory():
    while True:
        print_header("STOCKGUARD")
        print("                          INVENTORY LIST")
        print("-" * 82)
        print(f"{'ID':<6}{'Equipment Name':<18}{'Comlab':<10}{'Qty':<6}{'Unit Value':<12}{'Total Value':<14}{'Status'}")
        print("-" * 82)
        if equipment:
            for item in equipment:
                total = item["quantity"] * item["price"]
                print(
                    f"{item['id']:<6}{item['name']:<18}{item['comlab']:<10}"
                    f"{item['quantity']:<6}{item['price']:<12.2f}{total:<14,.2f}{item['status']}"
                )
        else:
            print("No equipment found.")
        print("-" * 82)
        print("\n1. Back to Menu")
        print("2. View Details")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            return
        elif choice == "2":
            view_equipment_details()
        else:
            print("\nInvalid choice. Please try again.\n")


def view_equipment_details():
    item = find_item("\nEnter Equipment ID to view: ")
    if item:
        total = item["quantity"] * item["price"]
        print(f"\nEquipment ID     : {item['id']}")
        print(f"Equipment Name   : {item['name']}")
        print(f"Computer Lab     : {item['comlab']}")
        print(f"Quantity         : {item['quantity']}")
        print(f"Unit Value (PHP) : {item['price']:.2f}")
        print(f"Total Value (PHP): {item['quantity']} x {item['price']:.2f} = {total:,.2f}")
        print(f"Status           : {item['status']}\n")


def search_equipment():
    while True:
        print_header("STOCKGUARD")
        print("           SEARCH EQUIPMENT\n")
        query = input("Enter Equipment Name or ID: ").strip().lower()

        results = [
            item for item in equipment
            if query in item["id"].lower() or query in item["name"].lower()
        ]

        print("\nResult:")
        print("-" * 58)
        print(f"{'ID':<6}{'Equipment':<18}{'Comlab':<10}{'Qty':<6}{'Status'}")
        print("-" * 58)
        if results:
            for item in results:
                print(
                    f"{item['id']:<6}{item['name']:<18}{item['comlab']:<10}"
                    f"{item['quantity']:<6}{item['status']}"
                )
        else:
            print("NO EQUIPMENT FOUND")
        print("-" * 58)

        print("\n1. Search Again")
        print("2. Back to Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            continue
        elif choice == "2":
            return
        else:
            print("\nInvalid choice. Returning to main menu.\n")
            return





def equipment_status():
    while True:
        print_header("STOCKGUARD")
        print("           EQUIPMENT STATUS")
        print("-" * 58)
        print(f"{'ID':<6}{'Equipment':<18}{'Comlab':<10}{'Status'}")
        print("-" * 58)
        if equipment:
            for item in equipment:
                print(f"{item['id']:<6}{item['name']:<18}{item['comlab']:<10}{item['status']}")
        else:
            print("No equipment found.")
        print("-" * 58)

        print("\nSummary per Computer Lab:")
        for lab in COMLABS:
            lab_items = [e for e in equipment if e["comlab"] == lab]
            counts = ", ".join(
                f"{s}: {sum(1 for e in lab_items if e['status'] == s)}"
                for s in STATUS_OPTIONS
            )
            print(f"  {lab:<9}- {counts}")

        print("\n1. Update Status")
        print("2. Back to Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            update_equipment_status()
        elif choice == "2":
            return
        else:
            print("\nInvalid choice. Please try again.\n")


def update_equipment_status():
    item = find_item("\nEquipment ID     : ")
    if not item:
        return

    print(f"Equipment Name   : {item['name']}")
    print(f"Computer Lab     : {item['comlab']}")
    print(f"Current Status   : {item['status']}")
    new_status = choose_from("Select New Status:", STATUS_OPTIONS)

    print("\n1. Save")
    print("2. Cancel")
    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        item["status"] = new_status
        print(f"\nStatus for '{item['name']}' updated to {new_status}.\n")
    elif choice == "2":
        print("\nUpdate canceled.\n")
    else:
        print("\nInvalid choice. Returning to status menu.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")