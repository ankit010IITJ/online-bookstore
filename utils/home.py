# function to get all books
# def allBooks(mysql):
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT 
#             b.bookID,
#             a.authorID,
#             b.publisherID,
#             b.title,
#             b.genre,
#             b.publicationYear,
#             b.price,
#             b.imageURL,
#             a.firstName,
#             a.lastName
#         FROM Books AS b
#         INNER JOIN Authors AS a ON b.authorID = a.authorID
#         ORDER BY bookID
#     """)
#     booksData = cur.fetchall()
#     booksData = list(booksData)
#     mysql.connection.commit()
#     cur.close()
#     return booksData


def allBooks(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BookListView ORDER BY bookID")
    booksData = cur.fetchall()
    booksData = list(booksData)
    mysql.connection.commit()
    cur.close()
    return booksData


def bookDetail(mysql, bookID):
    cur = mysql.connection.cursor()

    # 1. Fetch Book and Author details
    cur.execute("""
        SELECT 
            b.bookID, 
            b.title, 
            b.genre, 
            b.price, 
            b.publicationYear, 
            a.firstName, 
            a.lastName,
            p.country AS publicationCountry
        FROM Books AS b
        JOIN Authors AS a ON b.authorID = a.authorID
        JOIN Publishers AS p ON b.publisherID = p.publisherID
        WHERE b.bookID = %s
    """, (bookID,))
    bookData = cur.fetchone()
    return bookData


# function to get all genre
def allGenre(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT genre from Books")
    genreData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return genreData