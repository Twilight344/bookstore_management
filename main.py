import mysql.connector as p
import getpass
conn = p.connect(
    host="localhost",
    user="root",
    passwd="" #Enter your pass
)
if conn.is_connected():
    print("Bookstore Management")
    cursor = conn.cursor()

    cursor.execute("create database if not exists bookstore")
    cursor.execute("use bookstore")
    cursor.execute("create table if not exists sign(username varchar(20),password varchar(20))")
    while True:
        print("1: Signup\n"
              "2: Login")
        ch = int(input("SIGNUP/LOGIN(1,2):"))
        if ch == 1:
            usr = input("Enter your username: ")
            passw = getpass.getpass("Enter Password:")
            cursor.execute(f"insert into sign values('{usr}','{passw}')")
            conn.commit()
        elif ch == 2:
            usr = input("Enter username: ")
            cursor.execute(f"select username from sign where username = '{usr}'")
            sec = cursor.fetchone()
            conn.commit()
            if sec is not None:
                print("you have a valid username :)")
                passw = getpass.getpass("Enter Password:")
                cursor.execute(f"select password from sign where password ='{passw}'")
                pp = cursor.fetchone()
                if pp is not None:
                    print("LOGIN SUCCESSFULL ")
                    cursor.execute(
                        "create table if not exists Available_Books(BookName varchar(30) primary key,Genre varchar(20),Quantity int(3),Author varchar(20),Publication varchar(30),Price int(4))")
                    cursor.execute(
                        "create table if not exists Sell_rec(CustomerName varchar(20),PhoneNumber char(10) unique key, BookName varchar(30),Quantity int(100),Price int(4),foreign key (BookName) references Available_Books(BookName))")
                    conn.commit()
                    while (True):
                        print("1: add books/update\n"
                              "2: Delete books\n"
                              "3: search books\n"
                              "4: sell record\n"
                              "5: available books\n"
                              "6: total income after the latest rest\n"
                              "7: exit\n")
                        l = int(input("Enter your choice:"))
                        if l == 1:
                            choice = int(input("1: Add Books\n"
                                           "2: Update Books\n"
                                               "-->"))
                            if choice == 1:
                                print("kindly fill all the information :) ")
                                book_name = input("enter the book name: ")
                                gen = input("Enter boook genre: ")
                                quan = int(input("Enter the number of books: "))
                                author = input("Enter book author: ")
                                publication = input("Enter the publication of the book: ")
                                price = int(input("Enter the price of the book: " ))
                                cursor.execute(f"insert into Available_Books values('{book_name}','{gen}',{quan},'{author}','{publication}',{price})")
                                conn.commit()

                            elif choice == 2:
                                book_name_update = input("Enter the book to update:")
                                cursor.execute(f"select quantity from Available_Books where BookName = '{book_name_update}'")
                                x = cursor.fetchone()
                                for j in x:
                                    if j is not None:
                                        sa = int(input(f"Enter the quantity of books to be added for {book_name_update}: "))
                                        oo = j + sa
                                        cursor.execute(f"update Available_Books set Quantity = {oo} where BookName = '{book_name_update}'")
                                        conn.commit()
                            else:
                                continue
                        elif l == 2:
                            print("You may delete a book using the name of the book ")
                            book_to_be_removed = input("Enter book name to be deleted: ")
                            cursor.execute(f"select BookName from Available_Books where BookName = '{book_to_be_removed}'")
                            vb = cursor.fetchone()
                            conn.commit()
                            if vb is not None:
                                cursor.execute(f" DELETE FROM Available_Books where BookName = '{book_to_be_removed}'")
                                conn.commit()
                                print("record was deleted!")
                            elif vb is None:
                                print("record not found! please check for typos")
                        elif l == 3:
                            print("You may search books using book name!")
                            book_to_search = input("enter the book name you want to search for: ")
                            cursor.execute(f"select BookName from Available_Books where BookName = '{book_to_search}' ")
                            cvb = cursor.fetchone()
                            conn.commit()
                            if cvb is not None:
                                cursor.execute(f"select * from Available_Books where BookName = '{book_to_search}'")
                                ccv=cursor.fetchone()
                                print(ccv)
                            else:
                                print("book not found! check for typos!")
                        elif l == 4:
                            print("you may sell records using book name")
                            cus_name = input("Enter name of customer: ")
                            ph_no = int(input("Enter phone number of customer: "))
                            book_to_be_sold = input("Enter book name to sell: ")
                            qua = int(input("enter the quantity of the books you want to buy: "))
                            cursor.execute(f"select BookName from Available_Books where BookName = '{book_to_be_sold}'")
                            vbb = cursor.fetchone()
                            conn.commit()
                            if vbb is not None:
                                cursor.execute(f"select price from Available_Books where BookName = '{book_to_be_sold}'")
                                pll = cursor.fetchone()
                                for lol in pll:
                                    int(lol)
                                    total_price = lol * qua  #total price
                                    cursor.execute(f"insert into Sell_rec values('{cus_name}',{ph_no},'{book_to_be_sold}',{qua},{total_price})")
                                    #this is to subtract the value of books sold  from Available_Books
                                    cursor.execute(f"select quantity from Available_Books where BookName = '{book_to_be_sold}'")
                                    bnn = cursor.fetchone()
                                    for ind in bnn:
                                        fa = int(ind)
                                        final_quantity = int(ind - qua)
                                        cursor.execute(f"update Available_Books set Quantity = {final_quantity} where BookName = '{book_to_be_sold}'")
                                        conn.commit()
                                print("Done!")
                            else:
                                print("BOOK OUT OF STOCK!")
                        elif l == 5:
                            cursor.execute("select * from Available_Books")
                            data = cursor.fetchall()
                            for n in data:
                                print(n)
                        elif l == 6:
                            cursor.execute("select sum(price) as total_earning from Sell_rec")
                            for xd in cursor:
                                print(f"The total earning made is {list(xd)}")
                                cursor.execute("select BookName,price from sell_rec")
                                selrec = cursor.fetchall()
                                a = [selrec]
                                for iii in a:
                                    print("The earnings made by all the books separately",iii,end="\n")
                        elif l == 7:
                            print(f"Hope to have you again {usr}")
                            break
                    break
                else:
                    print("wrong password")
                    break
            else:
                print("wrong username")
                break
