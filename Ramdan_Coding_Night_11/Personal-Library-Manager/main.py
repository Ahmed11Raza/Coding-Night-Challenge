import streamlit as st
import pandas as pd
import json
import os
import datetime
from typing import List, Dict, Optional, Union
import plotly.express as px


class Book:
    def __init__(
        self,
        title: str,
        author: str,
        isbn: str = "",
        genre: str = "",
        publication_year: Optional[int] = None,
        publisher: str = "",
        pages: Optional[int] = None,
        status: str = "Unread",
        date_added: Optional[str] = None,
        rating: Optional[float] = None,
        notes: str = "",
    ):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.publication_year = publication_year
        self.publisher = publisher
        self.pages = pages
        self.status = status  # Unread, Reading, Completed
        self.date_added = date_added or datetime.datetime.now().strftime("%Y-%m-%d")
        self.rating = rating  # 1-5 scale
        self.notes = notes

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "genre": self.genre,
            "publication_year": self.publication_year,
            "publisher": self.publisher,
            "pages": self.pages,
            "status": self.status,
            "date_added": self.date_added,
            "rating": self.rating,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Book":
        return cls(**data)

    def __str__(self) -> str:
        rating_str = f"{self.rating}/5" if self.rating is not None else "Not rated"
        return f"{self.title} by {self.author} ({self.publication_year}) - {self.status} - {rating_str}"


class LibraryManager:
    def __init__(self, data_file: str = "library.json"):
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_library()

    def load_library(self) -> None:
        """Load the library from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as file:
                    books_data = json.load(file)
                    self.books = [Book.from_dict(book) for book in books_data]
                st.success(f"Loaded {len(self.books)} books from {self.data_file}")
            except json.JSONDecodeError:
                st.error(f"Error decoding {self.data_file}. Starting with an empty library.")
        else:
            st.info(f"No library file found at {self.data_file}. Starting with an empty library.")

    def save_library(self) -> None:
        """Save the library to the JSON file."""
        with open(self.data_file, "w") as file:
            json.dump([book.to_dict() for book in self.books], file, indent=2)
        st.success(f"Library saved to {self.data_file}")

    def add_book(self, book: Book) -> None:
        """Add a book to the library."""
        self.books.append(book)
        st.success(f'Added "{book.title}" by {book.author} to the library.')
        self.save_library()

    def remove_book(self, book_title: str) -> bool:
        """Remove a book from the library by title."""
        initial_count = len(self.books)
        self.books = [book for book in self.books if book.title.lower() != book_title.lower()]
        if len(self.books) < initial_count:
            st.success(f'Removed "{book_title}" from the library.')
            self.save_library()
            return True
        else:
            st.error(f'Book "{book_title}" not found in the library.')
            return False

    def get_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by its title."""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def update_book_status(self, title: str, status: str) -> bool:
        """Update the reading status of a book."""
        book = self.get_book_by_title(title)
        if book:
            book.status = status
            st.success(f'Updated "{book.title}" status to {status}.')
            self.save_library()
            return True
        else:
            st.error(f'Book "{title}" not found in the library.')
            return False

    def rate_book(self, title: str, rating: float) -> bool:
        """Add a rating to a book (1-5 scale)."""
        if not 0 <= rating <= 5:
            st.error("Rating must be between 0 and 5.")
            return False

        book = self.get_book_by_title(title)
        if book:
            book.rating = rating if rating > 0 else None
            st.success(f'Rated "{book.title}" as {rating}/5.')
            self.save_library()
            return True
        else:
            st.error(f'Book "{title}" not found in the library.')
            return False

    def add_notes(self, title: str, notes: str) -> bool:
        """Add notes to a book."""
        book = self.get_book_by_title(title)
        if book:
            book.notes = notes
            st.success(f'Added notes to "{book.title}".')
            self.save_library()
            return True
        else:
            st.error(f'Book "{title}" not found in the library.')
            return False

    def search_books(self, query: str) -> List[Book]:
        """Search for books by title, author, or genre."""
        query = query.lower()
        results = []
        for book in self.books:
            if (query in book.title.lower() or
                query in book.author.lower() or
                (book.genre and query in book.genre.lower())):
                results.append(book)
        return results

    def list_books(self, filter_by: Optional[str] = None, value: Optional[str] = None) -> List[Book]:
        """List all books, optionally filtered by a field and value."""
        if not filter_by:
            return self.books
        filtered_books = []
        for book in self.books:
            if hasattr(book, filter_by):
                book_value = getattr(book, filter_by)
                if isinstance(book_value, str) and book_value.lower() == value.lower():
                    filtered_books.append(book)
        return filtered_books

    def get_statistics(self) -> Dict[str, Union[int, Dict[str, int]]]:
        """Get statistics about the library."""
        total_books = len(self.books)
        genres = {}
        statuses = {"Unread": 0, "Reading": 0, "Completed": 0}
        authors = {}
        for book in self.books:
            if book.genre:
                genres[book.genre] = genres.get(book.genre, 0) + 1
            if book.status:
                statuses[book.status] = statuses.get(book.status, 0) + 1
            if book.author:
                authors[book.author] = authors.get(book.author, 0) + 1
        return {
            "total_books": total_books,
            "genres": genres,
            "statuses": statuses,
            "authors": authors
        }

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the library to a pandas DataFrame."""
        return pd.DataFrame([book.to_dict() for book in self.books])


def create_sample_books() -> List[Book]:
    """Create some sample books for testing."""
    return [
        Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            isbn="9780061120084",
            genre="Fiction",
            publication_year=1960,
            publisher="HarperCollins",
            pages=281,
            status="Completed",
            rating=5.0,
            notes="Classic novel about racial injustice in the American South.",
        ),
        Book(
            title="1984",
            author="George Orwell",
            isbn="9780451524935",
            genre="Dystopian",
            publication_year=1949,
            publisher="Signet Classics",
            pages=328,
            status="Reading",
            rating=4.5,
            notes="Orwell's masterpiece about totalitarianism and surveillance.",
        ),
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            isbn="9780743273565",
            genre="Fiction",
            publication_year=1925,
            publisher="Scribner",
            pages=180,
            status="Unread",
            notes="A classic exploration of the American Dream in the Jazz Age.",
        ),
    ]


def view_library():
    st.title("📋 Your Library")
    col1, col2 = st.columns([1, 2])
    with col1:
        filter_option = st.selectbox("Filter by:", ["All", "Status", "Genre", "Author"])
    library = st.session_state.library
    books = library.books
    if filter_option == "Status":
        with col2:
            status_filter = st.selectbox("Select status:", ["All", "Unread", "Reading", "Completed"])
        if status_filter != "All":
            books = [book for book in books if book.status == status_filter]
    elif filter_option == "Genre":
        genres = list(set(book.genre for book in books if book.genre))
        with col2:
            genre_filter = st.selectbox("Select genre:", ["All"] + sorted(genres))
        if genre_filter != "All":
            books = [book for book in books if book.genre == genre_filter]
    elif filter_option == "Author":
        authors = list(set(book.author for book in books if book.author))
        with col2:
            author_filter = st.selectbox("Select author:", ["All"] + sorted(authors))
        if author_filter != "All":
            books = [book for book in books if book.author == author_filter]

    if not books:
        st.info("No books found in your library.")
    else:
        df = pd.DataFrame([book.to_dict() for book in books])
        columns = [col for col in ["title", "author", "genre", "status", "rating", "publication_year",
                                   "publisher", "pages", "date_added", "isbn", "notes"] if col in df.columns]
        df = df[columns]
        column_names = {
            "title": "Title",
            "author": "Author",
            "genre": "Genre",
            "status": "Status",
            "rating": "Rating",
            "publication_year": "Year",
            "publisher": "Publisher",
            "pages": "Pages",
            "date_added": "Date Added",
            "isbn": "ISBN",
            "notes": "Notes"
        }
        df = df.rename(columns={col: column_names[col] for col in columns})
        st.dataframe(df)
        st.write(f"Showing {len(books)} of {len(library.books)} books")


def add_book_form():
    st.title("➕ Add New Book")
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title", help="Required")
            author = st.text_input("Author", help="Required")
            genre = st.text_input("Genre")
            pub_year = st.number_input("Publication Year", min_value=0, max_value=datetime.datetime.now().year, value=2000)
            pages = st.number_input("Number of Pages", min_value=0, value=0)
        with col2:
            isbn = st.text_input("ISBN")
            publisher = st.text_input("Publisher")
            status = st.selectbox("Reading Status", ["Unread", "Reading", "Completed"])
            rating = st.slider("Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.5)
            if rating == 0.0:
                rating = None
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Book")
        if submitted:
            if not title or not author:
                st.error("Book title and author are required.")
            else:
                new_book = Book(
                    title=title,
                    author=author,
                    isbn=isbn,
                    genre=genre,
                    publication_year=pub_year if pub_year > 0 else None,
                    publisher=publisher,
                    pages=pages if pages > 0 else None,
                    status=status,
                    rating=rating,
                    notes=notes
                )
                st.session_state.library.add_book(new_book)
                st.success(f"Added '{title}' by {author} to your library.")


def update_book_form():
    st.title("🔄 Update Book Details")
    library = st.session_state.library
    books = library.books
    if not books:
        st.info("No books in your library to update.")
        return

    book_titles = [book.title for book in books]
    selected_title = st.selectbox("Select a book to update:", book_titles)
    if selected_title:
        book = library.get_book_by_title(selected_title)
        if book:
            with st.form("update_book_form"):
                st.subheader(f"Update '{selected_title}'")
                update_type = st.radio("What would you like to update?", ["Status", "Rating", "Notes", "All Details"])
                if update_type == "Status":
                    new_status = st.selectbox("Select new status", ["Unread", "Reading", "Completed"])
                    submitted = st.form_submit_button("Update Status")
                    if submitted:
                        library.update_book_status(selected_title, new_status)
                elif update_type == "Rating":
                    new_rating = st.slider("Select new rating", 0.0, 5.0, value=book.rating if book.rating is not None else 0.0, step=0.5)
                    submitted = st.form_submit_button("Update Rating")
                    if submitted:
                        library.rate_book(selected_title, new_rating)
                elif update_type == "Notes":
                    new_notes = st.text_area("Enter new notes", value=book.notes)
                    submitted = st.form_submit_button("Update Notes")
                    if submitted:
                        library.add_notes(selected_title, new_notes)
                elif update_type == "All Details":
                    col1, col2 = st.columns(2)
                    with col1:
                        new_title = st.text_input("Title", value=book.title)
                        new_author = st.text_input("Author", value=book.author)
                        new_genre = st.text_input("Genre", value=book.genre)
                        new_pub_year = st.number_input("Publication Year", min_value=0, max_value=datetime.datetime.now().year, value=book.publication_year if book.publication_year else 2000)
                        new_pages = st.number_input("Pages", min_value=0, value=book.pages if book.pages else 0)
                    with col2:
                        new_isbn = st.text_input("ISBN", value=book.isbn)
                        new_publisher = st.text_input("Publisher", value=book.publisher)
                        new_status = st.selectbox("Status", ["Unread", "Reading", "Completed"], index=["Unread", "Reading", "Completed"].index(book.status) if book.status in ["Unread", "Reading", "Completed"] else 0)
                        new_rating = st.slider("Rating", min_value=0.0, max_value=5.0, value=book.rating if book.rating is not None else 0.0, step=0.5)
                    new_notes = st.text_area("Notes", value=book.notes)
                    submitted = st.form_submit_button("Update Book Details")
                    if submitted:
                        book.title = new_title
                        book.author = new_author
                        book.genre = new_genre
                        book.publication_year = new_pub_year if new_pub_year > 0 else None
                        book.pages = new_pages if new_pages > 0 else None
                        book.isbn = new_isbn
                        book.publisher = new_publisher
                        book.status = new_status
                        book.rating = new_rating if new_rating > 0 else None
                        book.notes = new_notes
                        st.success(f'Updated details for "{selected_title}".')
                        library.save_library()


def remove_book_form():
    st.title("❌ Remove Book")
    library = st.session_state.library
    books = library.books
    if not books:
        st.info("No books to remove.")
        return
    book_titles = [book.title for book in books]
    selected_title = st.selectbox("Select a book to remove:", book_titles)
    if selected_title:
        if st.button(f"Remove '{selected_title}'"):
            library.remove_book(selected_title)


def search_books_form():
    st.title("🔍 Search Books")
    library = st.session_state.library
    query = st.text_input("Enter search query (title, author, genre)")
    if st.button("Search"):
        if not query:
            st.error("Please enter a search query.")
        else:
            results = library.search_books(query)
            if results:
                df = pd.DataFrame([book.to_dict() for book in results])
                columns = [col for col in ["title", "author", "genre", "status", "rating", "publication_year",
                                           "publisher", "pages", "date_added", "isbn", "notes"] if col in df.columns]
                df = df[columns]
                column_names = {
                    "title": "Title",
                    "author": "Author",
                    "genre": "Genre",
                    "status": "Status",
                    "rating": "Rating",
                    "publication_year": "Year",
                    "publisher": "Publisher",
                    "pages": "Pages",
                    "date_added": "Date Added",
                    "isbn": "ISBN",
                    "notes": "Notes"
                }
                df = df.rename(columns={col: column_names[col] for col in columns})
                st.dataframe(df)
                st.write(f"Found {len(results)} matching book(s).")
            else:
                st.info("No matching books found.")


def display_statistics():
    st.title("📊 Library Statistics")
    library = st.session_state.library
    stats = library.get_statistics()
    st.write(f"Total Books: {stats['total_books']}")
    
    st.subheader("Status Distribution")
    statuses = stats["statuses"]
    df_status = pd.DataFrame(list(statuses.items()), columns=["Status", "Count"])
    fig_status = px.pie(df_status, names="Status", values="Count", title="Book Status Distribution")
    st.plotly_chart(fig_status)
    
    if stats["genres"]:
        st.subheader("Genre Distribution")
        df_genre = pd.DataFrame(list(stats["genres"].items()), columns=["Genre", "Count"])
        fig_genre = px.bar(df_genre, x="Genre", y="Count", title="Books per Genre")
        st.plotly_chart(fig_genre)
    
    if stats["authors"]:
        st.subheader("Author Distribution (Top 10)")
        df_authors = pd.DataFrame(list(stats["authors"].items()), columns=["Author", "Count"])
        df_authors = df_authors.sort_values(by="Count", ascending=False).head(10)
        fig_authors = px.bar(df_authors, x="Author", y="Count", title="Top 10 Authors by Book Count")
        st.plotly_chart(fig_authors)


def main():
    st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")
    if 'library' not in st.session_state:
        st.session_state.library = LibraryManager()
        # Add sample books if the library is empty
        if not st.session_state.library.books:
            for book in create_sample_books():
                st.session_state.library.add_book(book)
    
    st.sidebar.title("📚 Library Manager")
    nav_selection = st.sidebar.radio("Navigation", 
        ["📋 View Library", "➕ Add Book", "🔄 Update Book", "❌ Remove Book", "🔍 Search", "📊 Statistics"]
    )
    
    if nav_selection == "📋 View Library":
        view_library()
    elif nav_selection == "➕ Add Book":
        add_book_form()
    elif nav_selection == "🔄 Update Book":
        update_book_form()
    elif nav_selection == "❌ Remove Book":
        remove_book_form()
    elif nav_selection == "🔍 Search":
        search_books_form()
    elif nav_selection == "📊 Statistics":
        display_statistics()


if __name__ == "__main__":
    main()
