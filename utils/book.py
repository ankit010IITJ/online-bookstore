# add book function
def addBook(mysql, bookID, title, genre, fname, lname, year, price, country, stock, image_url):
    cur = mysql.connection.cursor()
    try:
        # Get or insert Publisher
        cur.execute("SELECT publisherID FROM Publishers WHERE country = %s", (country,))
        publisherID = cur.fetchone()
        if not publisherID:
            cur.execute("INSERT INTO Publishers(country) VALUES (%s)", (country,))
            cur.execute("SELECT publisherID FROM Publishers WHERE country = %s", (country,))
            publisherID = cur.fetchone()

        # Get or insert Author
        cur.execute("SELECT authorID FROM Authors WHERE firstName = %s AND lastName = %s", (fname, lname))
        authorID = cur.fetchone()
        if not authorID:
            cur.execute("INSERT INTO Authors(firstName, lastName) VALUES (%s, %s)", (fname, lname))
            cur.execute("SELECT authorID FROM Authors WHERE firstName = %s AND lastName = %s", (fname, lname))
            authorID = cur.fetchone()

        # Insert into Books
        cur.execute("""
            INSERT INTO Books(bookID, authorID, publisherID, title, genre, publicationYear, price, imageURL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (bookID, authorID[0], publisherID[0], title, genre, year, price, image_url))

        # Insert into Inventory
        cur.execute("INSERT INTO Inventory(bookID, totalStock, soldStock) VALUES (%s, %s, %s)", (bookID, stock, 0))

        result = 1
    except Exception as e:
        print("Error:", e)
        result = 0
    finally:
        mysql.connection.commit()
        cur.close()
    return result


def updateBook(mysql, bookID, title, price, fname, lname, image_url, stock):
    cur = mysql.connection.cursor()
    try:
        # Get author ID
        cur.execute("SELECT authorID FROM Authors WHERE firstName = %s AND lastName = %s", (fname, lname))
        author_row = cur.fetchone()
        if not author_row:
            raise Exception("Author not found")
        authorID = author_row[0]

        # Update Books
        if image_url:
            cur.execute("""
                UPDATE Books SET
                    title = %s,
                    price = %s,
                    imageURL = %s,
                    authorID = %s
                WHERE bookID = %s
            """, (title, price, image_url, authorID, bookID))
        else:
            cur.execute("""
                UPDATE Books SET
                    title = %s,
                    price = %s,
                    authorID = %s
                WHERE bookID = %s
            """, (title, price, authorID, bookID))

        # Update Inventory (stock)
        cur.execute("""
            UPDATE Inventory SET totalStock = %s
            WHERE bookID = %s
        """, (stock, bookID))

        result = 1
    except Exception as e:
        print("Update failed:", e)
        result = 0
    finally:
        mysql.connection.commit()
        cur.close()
    return result



# delete book function
def deleteBook(mysql, bookID):
    cur = mysql.connection.cursor()
    try:
        # Get authorID and publisherID from the book record
        cur.execute("SELECT authorID, publisherID FROM Books WHERE bookID = %s", (bookID,))
        result = cur.fetchone()
        if result is None:
            return 0  # Book doesn't exist

        authorID, publisherID = result

        # Count how many books each is associated with
        cur.execute("SELECT COUNT(*) FROM Books WHERE authorID = %s", (authorID,))
        authorbooks = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM Books WHERE publisherID = %s", (publisherID,))
        publisherbooks = cur.fetchone()[0]

        # Delete from Inventory and Books
        cur.execute("DELETE FROM Inventory WHERE bookID = %s", (bookID,))
        cur.execute("DELETE FROM Books WHERE bookID = %s", (bookID,))

        # Delete author if no more books
        if authorbooks == 1:
            cur.execute("DELETE FROM Authors WHERE authorID = %s", (authorID,))

        # Delete publisher if no more books
        if publisherbooks == 1:
            cur.execute("DELETE FROM Publishers WHERE publisherID = %s", (publisherID,))

        result = 1
    except:
        result = 0

    mysql.connection.commit()
    cur.close()
    return result


# book stock function
def inventory(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,b.title,i.totalStock,i.soldStock FROM Books as b,Inventory as i WHERE b.bookID=i.bookID")
    bookData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return bookData

# book details function
# def bookDetail(mysql, subject):
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT 
#             b.bookID,
#             b.title,
#             b.genre,
#             b.price,
#             b.publicationYear,
#             a.firstName,
#             a.lastName,
#             p.country,
#             i.totalStock,
#             b.imageURL
#         FROM Books AS b
#         JOIN Authors AS a ON b.authorID = a.authorID
#         JOIN Publishers AS p ON b.publisherID = p.publisherID
#         LEFT JOIN Inventory AS i ON b.bookID = i.bookID
#         WHERE b.bookID = %s
#     """, (subject,))
#     bookData = list(cur.fetchone())
#     cur.close()
#     return bookData



def bookDetail(mysql, subject):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BookDetailsView WHERE bookID = %s", (subject,))
    bookData = list(cur.fetchone())
    cur.close()
    return bookData



# cur.execute("SELECT * FROM BookDetailsView WHERE bookID = %s", (bookID,))


# calcuate total cost of books
def totalBookPrice(mysql,bookID,quantity):
    cur = mysql.connection.cursor()
    cur.execute("SELECT bookID,price,title from Books where bookID = %s",(bookID,))
    bookData = list(cur.fetchone())
    mysql.connection.commit()
    cur.close()
    return bookData