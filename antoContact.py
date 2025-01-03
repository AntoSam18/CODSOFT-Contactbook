import sqlite3

def initialize_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
                    name TEXT PRIMARY KEY,
                    phone TEXT NOT NULL,
                    email TEXT,
                    address TEXT)""")
    conn.commit()
    conn.close()

def display_menu():
    print("\nContact Management System")
    print("1. Add Contact")
    print("2. View Contact List")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

def add_contact():
    name = input("Enter Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email Address: ").strip()
    address = input("Enter Address: ").strip()

    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                       (name, phone, email, address))
        conn.commit()
        print(f"Contact for {name} added successfully!")
    except sqlite3.IntegrityError:
        print("Contact with this name already exists!")
    finally:
        conn.close()

def view_contacts():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM contacts")
    results = cursor.fetchall()
    conn.close()

    if not results:
        print("No contacts found.")
        return

    print("\nContact List:")
    print(f"{'Name':<20} {'Phone Number':<15}")
    print("-" * 35)
    for name, phone in results:
        print(f"{name:<20} {phone:<15}")

def search_contact():
    query = input("Enter Name or Phone Number to Search: ").strip()

    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                   (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print("No matching contacts found.")
        return

    print("\nSearch Results:")
    for name, phone, email, address in results:
        print(f"Name: {name}")
        print(f"Phone: {phone}")
        print(f"Email: {email}")
        print(f"Address: {address}\n")

def update_contact():
    name = input("Enter Name of the Contact to Update: ").strip()

    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE LOWER(name) = ?", (name.lower(),))
    contact = cursor.fetchone()

    if not contact:
        print("Contact not found.")
        conn.close()
        return

    print("\nLeave a field blank or type the same to keep current information.")
    phone = input(f"Enter New Phone Number (current: {contact[1]}): ").strip()
    email = input(f"Enter New Email (current: {contact[2]}): ").strip()
    address = input(f"Enter New Address (current: {contact[3]}): ").strip()

    phone = contact[1] if phone == "" or phone == contact[1] else phone
    email = contact[2] if email == "" or email == contact[2] else email
    address = contact[3] if address == "" or address == contact[3] else address

    cursor.execute("UPDATE contacts SET phone = ?, email = ?, address = ? WHERE LOWER(name) = ?",
                   (phone, email, address, name.lower()))
    conn.commit()
    conn.close()
    print(f"Contact for {name} updated successfully!")

def delete_contact():
    name = input("Enter Name of the Contact to Delete: ").strip()

    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE name = ?", (name,))
    contact = cursor.fetchone()

    if not contact:
        print("Contact not found.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete {name}? (yes/no): ").strip().lower()
    if confirm == "yes":
        cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
        conn.commit()
        print(f"Contact for {name} deleted successfully!")
    else:
        print("Deletion cancelled.")

    conn.close()

def main():
    initialize_db()
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Exiting Contact Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
