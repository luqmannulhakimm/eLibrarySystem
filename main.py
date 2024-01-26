from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elibary_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy database instance
db = SQLAlchemy(app)

# Define a Book model
# Define a Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50))
    author = db.Column(db.String(20))
    publisher = db.Column(db.String(20))
    year_published = db.Column(db.String(20))
    category = db.Column(db.String(20))

    def __repr__(self):
        return f'<Book {self.id}: {self.book_name}>'


with app.app_context():
    db.create_all()

@app.route('/')
def index():

    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page

    books = Book.query.paginate(page=page, per_page=per_page)

    book_categories = ['Fiction', 'Non-Fiction', 'Science Fiction', 
                       'Fantasy', 'Mystery', 'Thriller', 'Romance', 
                       'Historical Fiction', 'Biography', 'Self-Help', 
                       'Business', 'Cookbooks', 'Poetry', 'Art', 'Travel', 
                       'History', 'Philosophy', 'Religion', 'Science', 
                       'Health', 'Fitness', 'Sports', 'Technology', 
                       'Programming', 'Education']
    
    return render_template('index.html', books=books, book_categories=book_categories)

@app.route('/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form['bookName']
        author = request.form['author']
        publisher = request.form['publisher']
        year_published = request.form['yearPublished']
        category = request.form['category']

        print(book_name,author,publisher,year_published,category)
        
        # Create a new Book object
        new_book = Book(book_name=book_name, author=author, publisher=publisher, year_published=year_published, category=category)
        

        # Add the new book record to the database
        db.session.add(new_book)
        db.session.commit()
        
        return redirect(url_for('index'))

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    page = request.args.get('page', 1, type=int)  # Get the current page from the request
    # Find the book by ID
    book = Book.query.get_or_404(book_id)
    try:
        # Delete the book from the database
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('index', page=page))  # Redirect back to the same page
    except:
        return 'Error deleting book'



if __name__ == '__main__':
    app.run(debug=True)