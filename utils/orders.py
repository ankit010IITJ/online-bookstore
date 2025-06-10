import datetime

# def orders(mysql,isbn,quantity,total,pay,userID):
#     cur = mysql.connection.cursor()
#     timestamp = datetime.datetime.now()
#     commitStatus = 0

#     try:
#         mysql.connection.autocommit = False       
#         cur.execute("INSERT into Orders(customerID,bookID,quantity,total,timestamp) values(%s,%s,%s,%s,%s)",(userID,isbn,quantity,total,timestamp))
#         cur.execute("UPDATE Inventory set soldStock = soldStock + %s where bookID = %s",(quantity,isbn))
#         cur.execute("UPDATE Inventory set totalStock = totalStock - %s where bookID = %s",(quantity,isbn))
#         print('Transaction committed')
        
#         try:
#             mysql.connection.autocommit = False
#             cur.execute("INSERT into Payment(customerID,paymentInfo) values (%s,%s)",(userID,pay))
#             print('Payment Added')
#             commitStatus = 1 # payment successful

#         except:
#             print("Transaction rolled back")
#             mysql.connection.rollback()
        
#     except:
#         print("Transaction rolled back")
#         mysql.connection.rollback()
    
#     mysql.connection.commit()
#     cur.close()

#     return commitStatus


def orders(mysql, isbn, quantity, total, pay, userID):
    cur = mysql.connection.cursor()
    timestamp = datetime.datetime.now()
    commitStatus = 0

    try:
        # Start transaction
        mysql.connection.autocommit(False)

        # 1. Insert order
        cur.execute("""
            INSERT INTO Orders(customerID, bookID, quantity, total, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """, (userID, isbn, quantity, total, timestamp))

        # 2. Update Inventory: soldStock
        cur.execute("""
            UPDATE Inventory
            SET soldStock = soldStock + %s
            WHERE bookID = %s
        """, (quantity, isbn))

        # 3. Update Inventory: totalStock
        cur.execute("""
            UPDATE Inventory
            SET totalStock = totalStock - %s
            WHERE bookID = %s
        """, (quantity, isbn))

        # 4. Add payment record
        cur.execute("""
            INSERT INTO Payment(customerID, paymentInfo)
            VALUES (%s, %s)
        """, (userID, pay))

        # If everything is successful, commit
        mysql.connection.commit()
        commitStatus = 1
        print("Transaction committed successfully.")

    except Exception as e:
        # If *anything* goes wrong, rollback everything
        mysql.connection.rollback()
        print("Transaction rolled back due to:", e)

    finally:
        cur.close()
        mysql.connection.autocommit(True)  # reset autocommit back to default

    return commitStatus



# function to display all orders to admin portal
def allorders(mysql,userID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT o.orderID,o.customerID,o.bookID,o.quantity,o.total,o.timestamp,b.title FROM Orders as o, Books as b  WHERE o.bookID = b.bookID ORDER BY orderID")
    Data = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return Data

# def allorders(mysql,userID):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM OrderSummary ORDER BY orderID")
#     Data = list(cur.fetchall())
#     mysql.connection.commit()
#     cur.close()
#     return Data

# function to display customers orders
def myorder(mysql,userID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT o.bookID,o.quantity,o.total,o.timestamp,b.title FROM Orders as o,Books as b WHERE o.bookID = b.bookID AND o.customerID = %s",(userID,))
    Data = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return Data