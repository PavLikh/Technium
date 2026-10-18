from sqlite3 import connect

# 1
try:
    conn = connect("library.db")
    cursor = conn.cursor()
    print("Connect to SQLite successful")

except Exception as e:
        print('Connection failure:', e)

# 2
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER DEFAULT NULL
    );
    """
)

# 3.1
def insert_book(book) -> None:
    title = str(book[0])
    author = str(book[1])
    year = int(book[2])
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    print(f"Book: {title} added successful")

# 3.2
def get_books() -> list:
    return cursor.execute(
        "SELECT * FROM books;"
    ).fetchall()

# 3.3
def update_book(book) -> None:
    if 'id' in book and isinstance(book['id'], int) and not isinstance(book['id'], bool):
        id = book["id"]
        fields = []
        values = []
    else:
        print('Invalid or missing id')
        return

    if 'title' in book:
        fields.append("title = ?")
        values.append(str(book['title']))

    if 'author' in book:
        fields.append("author = ?")
        values.append(str(book['author']))

    if 'year' in book:
        fields.append("year = ?")
        values.append(str(book['year']))

    fields = ", ".join(fields)
    values.append(id)

    try:
        cursor.execute("UPDATE books SET " + fields + ' WHERE id = ?', values)
        conn.commit()
        rows_updated = cursor.rowcount
        print(f"Rows updated: {rows_updated}")
    except Exception as e:
        conn.rollback()
        print(f"Error update: {e}")

# bonus
def delete_book(id: int) -> None:
    if isinstance(id, int) and not isinstance(id, bool):
        cursor.execute("SELECT 1 FROM books WHERE id = ?", (id,))
        if cursor.fetchone() is None:
            print(f"Row with id = {id} not found")
    else:
        print('Invalid or missing id')
        return

    try:
        cursor.execute("DELETE FROM books WHERE id = ?", (id,))
        conn.commit()
        rows_updated = cursor.rowcount
        print(f"Rows deleted: {rows_updated}")
    except Exception as e:
        conn.rollback()
        print(f"Error delete: {e}")


book1 = ['War and peace','L. N. Tolstoi', 2001]
book2 = ('The Iliad', 'Homer', 2004)
book3 = ('Hamlet', 'Shakespeare', 1995)
book4 = ('The Haunted Hotel', 'Collins Wilkie', 2022)

updateBookWrongId = {'id': 100, 'year': 2024}
updateBook4 = {'id': 4, 'title': 'The Haunted Hotel: A Mystery of Modern Venice', 'year': 2023}

print(get_books())
insert_book(book1)
insert_book(book2)
insert_book(book3)
insert_book(book4)
print(get_books())
update_book(updateBookWrongId)
update_book(updateBook4)
print(get_books())
delete_book(10)
delete_book('asd')
delete_book(1)
print(get_books())

cursor.close()
conn.close()