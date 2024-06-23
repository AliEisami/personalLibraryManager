class Book:
    def __init__(self, title, author, year, genre, borrow=None):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.borrow = borrow if borrow else {}

    def set_borrow(self, stud_id, stud_name):
        self.borrow = {'id': stud_id, 'name': stud_name}

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'genre': self.genre,
            'borrow': self.borrow
        }