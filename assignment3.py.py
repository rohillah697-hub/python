import json
import logging
from pathlib import Path


# ---------------------------------------------------------
#  Task 1: Book Class
# ---------------------------------------------------------
class Book:
    def _init_(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status   # "available" or "issued"

    def _str_(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            status=data.get("status", "available")
        )

    def issue(self):
        if self.status == "issued":
            return False
        self.status = "issued"
        return True

    def return_book(self):
        if self.status == "available":
            return False
        self.status = "available"
        return True

    def is_available(self):
        return self.status == "available"


# ---------------------------------------------------------
#  Task 2 & 3: Inventory Manager + JSON Persistence
# ---------------------------------------------------------
class LibraryInventory:
    def _init_(self, storage_path="books.json"):
        self.books = []
        self.storage_path = Path(storage_path)

        # Load existing data
        self.load_from_file()

    def add_book(self, book):
        # prevent duplicate ISBN
        if self.search_by_isbn(book.isbn):
            raise ValueError("Book with this ISBN already exists.")
        self.books.append(book)
        logging.info(f"Added book: {book}")

    def search_by_title(self, title):
        title = title.lower()
        return [b for b in self.books if title in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return [str(b) for b in self.books]

    def issue_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if not book:
            raise LookupError("Book not found.")
        result = book.issue()
        if result:
            logging.info(f"Issued: {book}")
        return result

    def return_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if not book:
            raise LookupError("Book not found.")
        result = book.return_book()
        if result:
            logging.info(f"Returned: {book}")
        return result

    # ---------------- File Handling ----------------
    def save_to_file(self):
        try:
            with open(self.storage_path, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=2)
            logging.info("Saved inventory to file.")
        except Exception as e:
            logging.error(f"Error saving file: {e}")

    def load_from_file(self):
        if not self.storage_path.exists():
            logging.warning("Books file missing. Starting new inventory.")
            return

        try:
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                self.books = [Book.from_dict(item) for item in data]
            logging.info("Loaded books from file.")
        except Exception as e:
            logging.error(f"Error loading file: {e}")
            self.books = []


# ---------------------------------------------------------
#  Task 4: Menu-driven Command Line Interface
# ---------------------------------------------------------
def main():
    # Logging setup
    logging.basicConfig(
        filename="library.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    inventory = LibraryInventory()

    while True:
        print("\n===== Library Menu =====")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = input("Choose option: ").strip()

        try:
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")
                inventory.add_book(Book(title, author, isbn))
                inventory.save_to_file()
                print("Book added successfully!")

            elif choice == "2":
                isbn = input("Enter ISBN to issue: ")
                if inventory.issue_book(isbn):
                    print("Book issued successfully!")
                else:
                    print("Book already issued or not found.")
                inventory.save_to_file()

            elif choice == "3":
                isbn = input("Enter ISBN to return: ")
                if inventory.return_book(isbn):
                    print("Book returned successfully!")
                else:
                    print("Book already available or not found.")
                inventory.save_to_file()

            elif choice == "4":
                print("\n--- All Books ---")
                for b in inventory.display_all():
                    print(b)

            elif choice == "5":
                mode = input("Search by (t)itle or (i)sbn? ").strip().lower()
                if mode == "t":
                    title = input("Enter title: ")
                    results = inventory.search_by_title(title)
                    print("\n--- Search Results ---")
                    for b in results:
                        print(b)
                    if not results:
                        print("No books found.")
                else:
                    isbn = input("Enter ISBN: ")
                    book = inventory.search_by_isbn(isbn)
                    print(book if book else "Book not found.")

            elif choice == "6":
                inventory.save_to_file()
                print("Goodbye!")
                break

            else:
                print("Invalid option. Try again.")

        except Exception as e:
            print("Error:", e)
            logging.error(f"Error occurred: {e}")


# -------------------- Run Program --------------------
if _name_ == "_main_":
    main()
