import sqlite3
from datetime import datetime

# here database setup 
def setup_database():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()

    # Users Table is here 
    cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL)
                """)
    
    # books table is here
    cur.execute("""
            CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                available INTEGER DEFAULT 1)
            """)
    
    # borrow request table
    cur.execute("""
            CREATE TABLE IF NOT EXISTS borrow_requests(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY(user_id)
                REFERENCES users(id),
                FOREIGN KEY(book_id)
                REFERENCES books(id))
                """)
    
    # Borrow History table 
    cur.execute("""
            CREATE TABLE IF NOT EXISTS
                borrow_history(
                id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrowed_date TEXT NOT NULL,
                returned_date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(book_id) REFERENCES books(id))
                """)
    conn.commit() #executing database instructions
    conn.close() #closing connection of database

    # add Admin User
def add_admin():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE role = 'admin'")
    if not cur.fetchone():
        cur.execute('INSERT INTO users (email,password,role) VALUES (?,?,?)',('admin@library.com','admin123','admin'))
        conn.commit()
        conn.close()

# add admin functions
def admin_menu():
    while True:
        print('\nAdmin Menu:')
        print('1. Add a Book')
        print('2. View Borrow Requests')
        print('3. Approve/Deny a Borrow Request')
        print('4. View User Borrow History')
        print('5. Exit')
        # here we will ask choice of user
        choice = input('Enter your choice: ')
        if choice == '1':
            add_book()
        elif choice == '2':
            view_borrow_requests()
        elif choice == '3':
            approve_deny_requests()
        elif choice == '4':
            view_user_history()
        elif choice == '5':
            break
        else:
            print('Invalid Choice! Please Enter a valid Choice')


# adding book 
def add_book():
    title = input('Enter book title: ')
    author = input('Enter author name: ')
    isbn = input('Enter book ISBN: ')

    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO books (title, author, isbn) VALUES (?,?,?)',(title,author,isbn))
        conn.commit()
        print('Book added successfully!')
    except sqlite3.IntegrityError:
        print('Book with this ISBN already exists.')
    conn.close()

# borrow book request
def view_borrow_requests():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute("""
            SELECT br.id, u.email,
                b.title, br.start_date, br.end_date, br.status
                FROM borrow_requests br JOIN users u ON br.user_id=u.id
                JOIN books b ON br.book_id = b.id
            """)
    request = cur.fetchall()
    conn.close()

    if request:
        for req in request:
            print(f"""Request ID: {req[0]}, User: {req[1]},
                  Book: {req[2]}, Dates: {req[3]} to {req[4]},
                  Status: {req[5]}""")
    else:
        print('No borrow requests found')

    
# Approve and Deny Request 
def approve_deny_requests():
    req_id = input('Enter request ID to approve/deny: ')
    action = input("Enter 'approve' or 'deny': ").lower()
    
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM borrow_requests WHERE id =?',(req_id,))
    req = cur.fetchone()

    if not req:
        print('Request not found')
        conn.close()
        return
    if action == 'approve':
        cur.execute("UPDATE borrow_requests SET status = 'Approved' WHERE id = ?",(req_id,))
        cur.execute("UPDATE books SET available = 0 WHERE id = ?",(req[2],))
        print('Request Approved!')
    elif action == 'deny':
        cur.execute("UPDATE borrow_requests SET status = 'Denied' WHERE id = ?",(req_id,))
        print('Request Denied!')
    else:
        print('Invalid action.')
    
    conn.commit()
    conn.close()

# View user History
def view_user_history():
    user_email = input('Enter user email: ')
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute("""
            SELECT b.title, bh.borrowed_date,
                bh.returned_date FROM borrow_history bh
                JOIN books b ON bh.book_id = b.id
                JOIN users u ON bh.user_id = u.id
                WHERE u.email = ?
                """,(user_email,))
    history = cur.fetchall()
    conn.close()

    if history:
        for record in history:
            print(f"""Book: {record[0]}, Borrowed: {record[1]},
                  Returned: {record[2] or 'Not Returned'}""")
    else:
        print('No borrow history found')
    
# User Functions
def user_menu(user_id):
    while True:
        print("\nUser Menu:")
        print("1. View Available Books")
        print("2. Request a Book")
        print("3. View Borrow History")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            view_available_books()
        elif choice =='2':
            request_book(user_id)
        elif choice == '3':
            view_user_borrow_history(user_id)
        elif choice == '4':
            break
        else:
            print("Invalid Choice! Please try again.")

# Viewing available books
def view_available_books():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute("SELECT id, title, author FROM books WHERE available = 1")
    books = cur.fetchall()
    conn.close()

    if books:
        for book in books:
            print(f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}")
    else:
        print("No books available.")


# book request by given user id 
def request_book(user_id):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    book_id = input('Enter book ID to request: ')
    start_date = input('Enter star date (YYYY-MM-DD): ')
    end_date = input('Enter end date (YYYY-MM-DD): ')

    cur.execute("SELECT available FROM books WHERE id = ?",(book_id,))
    book = cur.fetchone()

    if not book:
        print("Book not found: ")
    elif not book[0]:
        print('Book is not available.')
    else:
        cur.execute("""
            INSERT INTO borrow_requests (user_id, book_id, start_date, end_date)
                    VALUES (?,?,?,?)""",(user_id,book_id,start_date,end_date))
        
    conn.close()  #closing the database connection

def view_user_borrow_history(user_id):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute("""
            SELECT b.title, bh.borrowed_date, bh.returned_date
                FROM borrow_history bh JOIN books b ON bh.book_id = b.id
                WHERE bh.user_id = ?
                """,(user_id))
    history = cur.fetchall()
    conn.close()
    
    if history:
        for record in history:
            print(f"Book: {record[0]},Borrowed: {record[1]},Returned: {record[2] or 'Not Returned'}")
    else:
        print('No Borrow history found')

# Login Functionality here
def login():
    email = input('Enter Email: ')
    password = input('Enter Password: ')

    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute("SELECT id, role FROM users WHERE email = ? AND password = ?",(email,password))
    user = cur.fetchone()
    conn.close()

    if user:
        print(f"Welcome, {email}!")
        if user[1] == 'admin':
            admin_menu()
        else:
            user_menu(user[0])
    else:
        print('Invalid credentials.')

# here our programs will start 
if __name__ == '__main__':
    setup_database()
    add_admin()

    while True:
        print('\nLibrary Management System')
        print('1. Login')
        print('2. Exit')
        choice = input('Enter your choice: ')
        
        if choice == '1':
            login()
        elif choice == '2':
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Please try again')


        