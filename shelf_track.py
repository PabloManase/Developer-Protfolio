import sqlite3


# ************************** DATABASE SETUP **************************#

# Function to create a connection
def get_database_connection(db_name="ebookstore.db"):
    """
    Create database connection and return to the SQLite database.
    """
    db = sqlite3.connect(db_name)
    return db


# Function to create book and author tables
def create_tables(db):
    """
    Create the book and author tables if it does not exist.
    """
    # Open a connection to the database
    with get_database_connection() as db:
        cursor = db.cursor()  # create a cursor

        # Create 'author' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
            )
        ''')
        db.commit()

        # Create 'book' table with authorID as foreign key
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book(
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authorID INTEGER NOT NULL,
                qty INTEGER NOT NULL,
                FOREIGN KEY (authorID) REFERENCES author(id)
            )
        ''')
        db.commit()


# Function to populate book and author table
def populate_tables(db):
    """
    Insert initial the initial records into book and author tables.
    """

    # Open a connection to the database
    with get_database_connection():
        cursor = db.cursor()  # create a cursor

        # initail records for book table
        initial_books = [
            (3001, "A Tale of Two Cities", 1290, 30),
            (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
            (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
            (3004, "The Lord of the Rings", 6380, 37),
            (3005, "Alice’s Adventures in Wonderland", 5620, 12)
        ]

        # initial records for author table
        initial_authors = [
            (1290, "Charles Dickens", "England"),
            (8937, "J.K. Rowling", "England"),
            (2356, "C.S. Lewis", "Ireland"),
            (6380, "J.R.R. Tolkien", "South Africa"),
            (5620, "Lewis Carroll", "England"),
        ]

        # Insert all initial records into 'book' table
        cursor.executemany('''
            INSERT OR IGNORE INTO book (id, title, authorID, qty)
            VALUES (?, ?, ?, ?)
        ''', initial_books)

        # Insert all initial records into 'author' table
        cursor.executemany('''
            INSERT OR IGNORE INTO author (id, name, country)
            VALUES (?, ?, ?)
        ''', initial_authors)
        db.commit()


# ************************** VALIDATION FUNCTIONS **************************

# Function to validate the length of the Book Id
def get_valid_integer(prompt, length=4):
    """
    Prompt user for a valid integer with optional length check
    """
    while True:
        try:
            # Prompt the user
            value = input(prompt).strip()
            # Check if user input is the correct
            if not value.isdigit():
                raise ValueError("Input must be a number.")

            # Check if the input has the correct length
            if length and len(value) != length:
                raise ValueError(f"Input must be {length} digits.")

            # Return the input as an integer
            return int(value)
        except ValueError as v:
            print(f"Invalid input: {v}")


# ************************** CORE FUNCTIONALITY **************************

# Function to add a book
def enter_book(db):
    """
    Prompt user to enter details and insert them into book and author tables
    """

    # Open a connection to the database
    with get_database_connection() as db:
        cursor = db.cursor()  # create a cursor

        # prompts user for book records
        id = get_valid_integer("Enter book ID(4 digits): ")
        title = input("Enter book title: ").strip()
        authorID = get_valid_integer("Enter author ID(4 digits): ")
        qty = int(input("Enter quantity: "))

        # Checks if author already exists
        cursor.execute('''
                       SELECT * FROM author WHERE id = ?
        ''', (authorID,))
        if not cursor.fetchone():
            print("Author not found. Please enter author details.")
            name = input("Enter author's name: ").strip()
            country = input("Enter author's country: ").strip()

            # Insert all new records into author table
            cursor.execute('''
                INSERT OR IGNORE INTO author (id, name, country)
                VALUES (?, ?, ?)
            ''', (authorID, name, country))

        # Insert all new records into book table
        cursor.execute('''
            INSERT OR IGNORE INTO book(id, title, authorID, qty)
            VALUES(?, ?, ?, ?)
        ''', (id, title, authorID, qty))
        db.commit()
        print("Book added to book database")


# Function to update a book
def update_book(db):
    """
    Update an existing book or author details
    """

    # Open a connection to the database
    with get_database_connection() as db:
        cursor = db.cursor()  # create a cursor

        # Prompt user for a valid 4-digit book ID
        id = get_valid_integer("Enter 4-digit book ID to update: ")

        #  Fetch the book and author information using INNER JOIN
        cursor.execute('''
            SELECT b.id, b.title, a.name, a.country
            FROM book b
            JOIN author a ON b.authorID = a.id
            WHERE b.id = ?
        ''', (id,))
        record = cursor.fetchone()  # Get the first matching record

        # If no record is found, notify the user and return
        if not record:
            print("Book not found.")
            return
        else:
            # Display current book and author details
            print("\nCurrent details:")
            print(f"Title: {record[1]}")
            print(f"Author: {record[2]}")
            print(f"Country: {record[3]}")

            # Display the available update options
            print("\nUpdate options:")
            print("1. Update quantity (default)")
            print("2. Update title")
            print("3. Update name")
            print("4. Update author country")
            choice = input("Select an option: ").strip()

            # Based on user's choice, perform appropriate update
            if choice == '1':
                # Update quantity in book table
                new_qty = get_valid_integer("Enter new quantity: ")
                cursor.execute('''
                    UPDATE book SET qty = ? WHERE id = ?,
                ''', (new_qty, id))

            elif choice == '2':
                # Update title in book table
                new_title = input("Enter new title: ").strip()
                cursor.execute('''
                    UPDATE book SET title = ? WHERE id = ?,
                ''', (new_title, id))

            elif choice == '3':
                # Update author name in author table
                new_name = input("Enter new name: ").strip()
                cursor.execute('''
                    UPDATE book SET authorID = ? WHERE id = ?,
                 ''', (new_name, record[0]))

            elif choice == '4':
                # Update author's country in author table
                new_country = input("Enter new author country: ").strip()
                cursor.execute('''
                    UPDATE author SET country = ? WHERE id = ?,
                ''', (new_country, record[0]))

            else:
                # If invalid choice is given, print message and exit
                print("Invalid choice.")
                return

            db.commit()
            print("Book updated successfully!")


# =============== Function to delete a book ===============
def delete_book(db):
    """
    Delete a book from the database by the ID.
    """

    # Open a connection to the database
    with get_database_connection() as db:
        cursor = db.cursor()  # create a cursor

        # Prompt the user to enter a 4-digit book ID
        id = get_valid_integer("Enter 4-digit book ID to deete: ")

        # Delete the book with the given ID
        cursor.execute('''
            DELETE FROM book WHERE id = ?
        ''', (id,))

        # Check if any rows were deleted
        if cursor.rowcount == 0:
            print("No book found with that ID.")
        else:
            # If deletion was successful commit the change
            db.commit()
            print("Book deleted successfully.")


# =============== Function to search for a book ===============
def search_book(db):
    """
    Search for a specific book by title or ID.
    """

    # Open a connection to the database
    with get_database_connection() as db:
        cursor = db.cursor()  # create a cursor

        # Prompt user to choose search method
        print("\nSearch options:")
        print("1. Search by ID")
        print("2. Search by title")
        choice = input("Select an option: ").strip()

        # If the user wants to search by book ID
        if choice == '1':
            id = get_valid_integer("Enter book ID: ")  # Validate book ID
            cursor.execute('''
                SELECT * FROM book WHERE id = ?
            '''), (id,)

        # If the user wants to search by title
        elif choice == '2':
            title = input("Enter book title: ").strip()
            cursor.execute('''
                SELECT * FROM book WHERE title LIKE ?
            '''), ('%' + title + '%',)

        # Handle invalid choices
        else:
            print("Invalid choice.")
            return

        # Fetch all matching results from the query
        book_search = cursor.fetchall()
        # If any books were found, print their details
        if book_search:
            print("\nFound books:")
            for book in book_search:
                print(f"ID: {book[0]}, Title: {book[1]}, "
                      f"AuthorID: {book[2]}, Quantity: {book[3]}")
        else:
            print("No matching books found.")


# =============== Function to view all book details ===============
def view_book_details(db):
    """
    Display a list of books with the author's name and country
    """

    with get_database_connection() as db:
        cursor = db.cursor()  # create a cursor

        # Join 'book' and 'author' tables
        cursor.execute('''
            SELECT b.title, a.name, a.country
            FROM book b
            INNER JOIN author a ON b.authorID = a.id
        ''')
        # Fetch matching records from the executed query
        rows = cursor.fetchall()

        # Check if any results were found
        if rows:
            # Loop through results and display
            print("\nDetails")
            for title, name, country in rows:
                print("-" * 50)
                print(f"Title: {title}")
                print(f"Author's Name: {name}")
                print(f"Author's Country: {country}")
                print("-" * 50)
            else:
                print("No books to display.")


# =================== Main Program ===================

# Initialize the database and set up tables
db = get_database_connection()
create_tables(db)
populate_tables(db)

# Main user options
while True:
    print("\nMenu:")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("5. View details of all books")
    print("0. Exit")
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        enter_book(db)
    elif choice == '2':
        update_book(db)
    elif choice == '3':
        delete_book(db)
    elif choice == '4':
        search_book(db)
    elif choice == '5':
        view_book_details(db)
    elif choice == '0':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
