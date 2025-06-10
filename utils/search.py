# # def searchTitle(mysql,query):
# def searchTitle(mysql, query):
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT b.bookID, a.authorID, b.publisherID, b.title, b.genre,
#                b.publicationYear, b.price, a.firstName, a.lastName, b.imageURL
#         FROM Books AS b, Authors AS a
#         WHERE b.title LIKE %s AND b.authorID = a.authorID
#     """, ('%' + query + '%',))
#     booksData = list(cur.fetchall())
#     cur.close()
#     return booksData


# def searchTitle(mysql, query):
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT b.bookID, a.authorID, b.publisherID, b.title, b.genre,
#                b.publicationYear, b.price, a.firstName, a.lastName, b.imageURL
#         FROM Books AS b, Authors AS a
#         WHERE b.title LIKE %s AND b.authorID = a.authorID
#     """, ('%' + query + '%',))
#     booksData = list(cur.fetchall())
#     cur.close()
#     return booksData



# # def searchGenre(mysql,query):
# def searchGenre(mysql, query):
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT b.bookID, a.authorID, b.publisherID, b.title, b.genre,
#                b.publicationYear, b.price, a.firstName, a.lastName, b.imageURL
#         FROM Books AS b, Authors AS a
#         WHERE b.genre LIKE %s AND b.authorID = a.authorID
#     """, ('%' + query + '%',))
#     booksData = list(cur.fetchall())
#     cur.close()
#     return booksData



# # def searchAuthor(mysql,query):
# def searchAuthor(mysql, query):
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT b.bookID, a.authorID, b.publisherID, b.title, b.genre,
#                b.publicationYear, b.price, a.firstName, a.lastName, b.imageURL
#         FROM Books AS b, Authors AS a
#         WHERE a.firstName LIKE %s AND b.authorID = a.authorID
#     """, ('%' + query + '%',))
#     list1Data = list(cur.fetchall())

#     cur.execute("""
#         SELECT b.bookID, a.authorID, b.publisherID, b.title, b.genre,
#                b.publicationYear, b.price, a.firstName, a.lastName, b.imageURL
#         FROM Books AS b, Authors AS a
#         WHERE a.lastName LIKE %s AND b.authorID = a.authorID
#     """, ('%' + query + '%',))
#     list2Data = list(cur.fetchall())

#     booksData = list({tuple(row) for row in list1Data + list2Data})
#     cur.close()
#     return booksData








def searchTitle(mysql, query):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.bookID, a.authorID, b.publisherID, b.title, b.genre,
               b.publicationYear, b.price, a.firstName, a.lastName, b.imageURL
        FROM Books AS b
        JOIN Authors AS a ON b.authorID = a.authorID
        WHERE b.title LIKE %s
    """, ('%' + query + '%',))
    booksData = list(cur.fetchall())
    cur.close()
    return booksData


def searchGenre(mysql, query):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.bookID, a.authorID, b.publisherID, b.title, b.genre,
               b.publicationYear, b.price, a.firstName, a.lastName, b.imageURL
        FROM Books AS b
        JOIN Authors AS a ON b.authorID = a.authorID
        WHERE b.genre LIKE %s
    """, ('%' + query + '%',))
    booksData = list(cur.fetchall())
    cur.close()
    return booksData


def searchAuthor(mysql, query):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.bookID, a.authorID, b.publisherID, b.title, b.genre,
               b.publicationYear, b.price, a.firstName, a.lastName, b.imageURL
        FROM Books AS b
        JOIN Authors AS a ON b.authorID = a.authorID
        WHERE a.firstName LIKE %s
    """, ('%' + query + '%',))
    list1Data = list(cur.fetchall())

    cur.execute("""
        SELECT b.bookID, a.authorID, b.publisherID, b.title, b.genre,
               b.publicationYear, b.price, a.firstName, a.lastName, b.imageURL
        FROM Books AS b
        JOIN Authors AS a ON b.authorID = a.authorID
        WHERE a.lastName LIKE %s
    """, ('%' + query + '%',))
    list2Data = list(cur.fetchall())

    booksData = list({tuple(row) for row in list1Data + list2Data})
    cur.close()
    return booksData
