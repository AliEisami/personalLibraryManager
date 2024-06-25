from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from book import Book
from library import Library

app = Flask(__name__)
library = Library('library.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books') #not complete!!
def list_books():
    filter_by = request.args.get('filter_by')
    value = request.args.get('value')
    books = library.list_books(filter_by, value)
    return render_template('list_books.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    error = ''
    current_year = datetime.now().year
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        genre = request.form['genre']
        if title != '' and author != '' and year != '' and genre != '':
            try:
                year = int(year)
                if year > current_year:
                    error = f"Year cannot be in the future!!!"
                else:
                    new_book = Book(title, author, year, genre)
                    library.add_book(new_book)
                    return redirect(url_for('list_books'))
            except ValueError:
                error = "Year must be a number!"
        else:
            error = "You have to fill them all"
    return render_template('add_book.html', error=error, current_year=current_year)

@app.route('/edit/<title>', methods=['GET', 'POST'])
def edit_book(title):
    error = ''
    current_year = datetime.now().year
    book = library.get_book(title)
    if request.method == 'POST':
        new_title = request.form['title']
        new_author = request.form['author']
        new_year = request.form['year']
        new_genre = request.form['genre']
        if new_title != '' and new_author != '' and new_year != '' and new_genre != '':
            try:
                year = int(new_year)
                if year > current_year:
                    error = f"Year cannot be in the future!!"
                else:
                    new_book = Book(new_title, new_author, new_year, new_genre)
                    library.edit_book(title, new_book)
                    return redirect(url_for('list_books'))
            except ValueError:
                error = "Year must be a number."
        else:
            error = "You have to fill them all"
    return render_template('edit_book.html', book=book, error=error, current_year=current_year)

@app.route('/borrow/<title>', methods=['GET', 'POST'])
def borrow_book(title):
    book = library.get_book(title)
    if not book:
        return redirect(url_for('list_books'))
    if request.method == 'POST':
        stud_name = request.form['fullname']
        stud_id = request.form['stud_id']
        library.borrow_book(book.title, stud_name, stud_id)
        return redirect(url_for('list_books'))
    return render_template('borrow_book.html', book=book)


@app.route('/return/<title>', methods=['GET', 'POST'])
def return_book(title):
    book = library.get_book(title)
    if not book:
        return redirect(url_for('list_books'))
    if request.method == 'POST':
        stud_name = request.form['fullname']
        stud_id = request.form['stud_id']
        library.return_book(book.title, stud_name, stud_id)
        return redirect(url_for('list_books'))
    return render_template('borrow_book.html', book=book)

@app.route('/delete/<title>', methods=['GET'])
def delete_book(title):
    library.delete_book(title)
    return redirect(url_for('list_books'))

if __name__ == '__main__':
    app.run(debug=True)