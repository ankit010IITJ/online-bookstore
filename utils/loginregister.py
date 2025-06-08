import bcrypt

# function to register customer
# def register(mysql,username,fname,lname,email,password,phone,country,state,pincode,address):        
#     cur = mysql.connection.cursor()
#     try:
#         cur.execute("INSERT INTO Customers(customerID,firstName,lastName,address,pincode,country,phone,state,emailID,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username,fname,lname,address,pincode,country,phone,state,email,password))
#         result = 1 # registration successful
#     except:
#         result =  0 # registration failed
#     mysql.connection.commit()
#     cur.close()
    
#     return result

def register(mysql, username, fname, lname, email, password, phone, country, state, pincode, address):        
    cur = mysql.connection.cursor()
    try:
        # Hash the password before saving
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cur.execute("""
            INSERT INTO Customers(
                customerID, firstName, lastName, address, pincode,
                country, phone, state, emailID, password
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, fname, lname, address, pincode, country, phone, state, email, hashed_password))

        result = 1  # registration successful
    except Exception as e:
        print("Registration failed:", e)
        result = 0  # registration failed
    mysql.connection.commit()
    cur.close()
    
    return result

# function for admin login
def adminLogin(mysql,username,password,account):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from Admins WHERE adminID = %s AND password = %s",(username,password))
    check = cur.fetchall()
    check = list(check)

    if not check:
        result = 0 # login failed
    else:
        result = 1 # login success
    
    mysql.connection.commit()
    cur.close()
    return result

# function for customer login
# def customerLogin(mysql,username,password,account):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * from Customers WHERE customerID = %s AND password = %s",(username,password))
#     check = cur.fetchall()
#     check = list(check)

#     if not check:
#         result = 0 # login failed
#     else:
#         result = 1 # login success

#     mysql.connection.commit()
#     cur.close()
#     return result

def customerLogin(mysql, username, entered_password, account):
    cur = mysql.connection.cursor()
    cur.execute("SELECT password FROM Customers WHERE customerID = %s", (username,))
    row = cur.fetchone()
    cur.close()

    if row is None:
        return 0  # user not found

    stored_hashed_password = row[0].encode('utf-8')

    if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password):
        return 1  # login success
    else:
        return 0  # wrong password
