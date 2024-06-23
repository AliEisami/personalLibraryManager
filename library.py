import json
from book import Book

class Library:
    def __init__(self, file_path):
        self.file_path = file_path
        self.books = self.load_books()

    # function to get all books from file
    def load_books(self):
        try:
            with open(self.file_path, 'r') as file:
                books_data = json.load(file)
                return [Book(**book) for book in books_data]
        except FileNotFoundError:
            return []

    # function to save book to file
    def save_books(self):
        with open(self.file_path, 'w') as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    # function to add book to books array
    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    # function to delete book from books array
    def delete_book(self, title):
        self.books = [book for book in self.books if book.title != title]
        self.save_books()

    # function to get a book
    def get_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    # function to edit an existing book in the books array
    def edit_book(self, old_title, new_book):
        for i, book in enumerate(self.books):
            if book.title == old_title:
                self.books[i] = new_book
                self.save_books()
                return True
        return False

    # function to set the borrowed book
    def borrow_book(self, title, stud_name, stud_id):
        for book in self.books:
            if book.title == title:
                book.set_borrow(stud_id, stud_name)
                self.save_books()
                return True
        return False

    # function to return the borrowed book and set it to not borrowed
    def return_book(self, title, stud_name, stud_id):
        for book in self.books:
            if book.title == title:
                if book.borrow['name'] == stud_name and book.borrow['id'] == stud_id:
                    book.borrow = {}
                    self.save_books()
                    return True
        return False

    # function to return books(not complete)
    def list_books(self, filter_by=None, value=None):
        if filter_by and value:
            if filter_by == 'author':
                return [book for book in self.books if book.author == value]
            elif filter_by == 'genre':
                return [book for book in self.books if book.genre == value]
        return self.books