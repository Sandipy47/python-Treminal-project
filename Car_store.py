import mysql.connector
import getpass
from mysql.connector import Error  # To handle errors during the database connection.

class CarCollectionStore:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.Name = 'Tanvi-Car-Collection'
        self.store_Name = ''
        self.store_Password = ''
        self.connect_to_database()

    def connect_to_database(self):
        """Generates a connection to the MySQL database."""
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                database="Car_store",
                password="Urmila@47",
                auth_plugin="mysql_native_password"
            )
            self.cursor = self.db.cursor()
            print("Connected to the database successfully.")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.db = None
            self.cursor = None

    def create_tables(self):
        """Creates the necessary tables in the database."""
        if self.db is None or self.cursor is None:
            print("Database connection is not established.")
            return

        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    Name VARCHAR(20) NOT NULL,
                    Last_Name VARCHAR(20) NOT NULL,
                    Password VARCHAR(20) NOT NULL,
                    Email VARCHAR(80) NOT NULL UNIQUE
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS cars (
                    Car_Id INT NOT NULL PRIMARY KEY,
                    Car_Model_Year INT NOT NULL,
                    Car_Name VARCHAR(50) NOT NULL,
                    Car_Type VARCHAR(10) NOT NULL,
                    Car_Condition VARCHAR(10) NOT NULL
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Booked_Car (
                    Car_Id INT NOT NULL,            
                    Car_Model INT NOT NULL,
                    Car_Name VARCHAR(50) NOT NULL,
                    Car_Type VARCHAR(10) NOT NULL,
                    Car_Condition VARCHAR(10) NOT NULL
                )
            ''')
            self.db.commit()
            print("Tables created successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")

    def Add_car(self, Car_Id, Car_Model_Year, Car_Name, Car_Type, Car_Condition):
        """Adds a single new car to the inventory."""
        if self.db is None or self.cursor is None:
            print("Database connection is not established.")
            return

        try:
            self.cursor.execute('''
                INSERT INTO cars (Car_Id, Car_Model_Year, Car_Name, Car_Type, Car_Condition)
                VALUES (%s, %s, %s, %s, %s)
            ''', (Car_Id, Car_Model_Year, Car_Name, Car_Type, Car_Condition))
            self.db.commit()
            print("✅ Car added successfully.")
        except Error as e:
            print(f"❌ Error adding car: {e}")

    def Register(self):
        """Registers a new user."""
        if self.db is None or self.cursor is None:
            print("Database connection is not established.")
            return

        print('\n--- 📝 USER REGISTRATION ---')
        name = input('Enter your Name: ')
        last_name = input('Enter your Last Name: ')
        password = getpass.getpass('Enter your Password: ')
        email = input('Enter your Email: ')

        try:
            self.cursor.execute('''
                INSERT INTO users (Name, Last_Name, Password, Email)
                VALUES (%s, %s, %s, %s)
            ''', (name, last_name, password, email))
            self.db.commit()
            print("✅ Registration successful.")
        except Error as e:
            print(f"❌ Error during user registration: {e}")

    def Owner_Login(self):
        """Allows the owner to log in."""
        print('---------🧑‍💻 ADMIN LOGIN ---------')
        self.store_Name = input('Enter your Name: ')
        if self.store_Name == "Sandip@47":
            self.store_Password = getpass.getpass("Enter your password: ")
            if self.store_Password == "Urmila@47":
                print("✅ Login successful. Welcome to the Car Collection Store!")
                while True:
                    print("\n1. Add Car")
                    print("2. View Cars")
                    print("3. View Users")
                    print("4. Exit")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        car_Id = input("Enter Car ID: ")
                        car_model_year = input("Enter Car Model Year: ")
                        car_name = input("Enter Car Name: ")
                        car_type = input("Enter Car Type (P/D): ")
                        car_condition = input("Enter Car Condition (New/Used): ")
                        self.Add_car(car_Id, car_model_year, car_name, car_type, car_condition)
                    elif choice == '2':
                        self.View_Cars()
                    elif choice == '3':
                        print("Displaying all registered users:")
                        self.View_Users()
                    elif choice == '4':
                        print("Exiting the admin panel.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("❌ Incorrect password. Please try again.")
        else:
            print("❌ Incorrect username. Please try again.")

    def User_Login(self):
        """Allows a user to log in."""
        if self.db is None or self.cursor is None:
            print("Database connection is not established.")
            return

        print('---------👤 USER LOGIN ---------')
        email = input('Enter your Email: ')
        password = getpass.getpass('Enter your Password: ')

        try:
            self.cursor.execute('''
                SELECT * FROM users WHERE Email = %s AND Password = %s
            ''', (email, password))
            user = self.cursor.fetchone()
            if user:
                self.name = user[0]
                self.last_name = user[1]
                self.email = user[2]
                print(f'✅ Welcome {self.name} {self.last_name}!')
                while True:
                    print("\n1. View Cars")
                    print("2. Book Car")
                    print("3. Exit")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        self.View_Cars()
                    elif choice == '2':
                        self.Book_Car()
                    elif choice == '3':
                        print("Exiting user panel.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("❌ Invalid email or password.")
        except Error as e:
            print(f"❌ Error during user login: {e}")

    def Book_Car(self):
        """Books a car for a user."""
        if self.db is None or self.cursor is None:
            print("Database connection is not established.")
            return

        user_email = input("Enter your email: ")
        car_id = input("Enter the Car ID you want to book: ")

        try:
            self.cursor.execute('''
                INSERT INTO Booked_Car (Car_Id, Car_Model, Car_Name, Car_Type, Car_Condition)
                SELECT Car_Id, Car_Model_Year, Car_Name, Car_Type, Car_Condition
                FROM cars WHERE Car_Id = %s
            ''', (car_id,))
            self.db.commit()
            print("✅ Car booked successfully.")
        except Error as e:
            print(f"❌ Error booking car: {e}")

    def View_Users(self):
        """Displays all registered users."""
        if self.db is None or self.cursor is None:
            print("Database connection is not established.")
            return

        try:
            self.cursor.execute('SELECT * FROM users')
            users = self.cursor.fetchall()
            if not users:
                print("⚠️ No users found.")
            else:
                print("📜 Registered Users:")
                for user in users:
                    print(user)
        except Error as e:
            print(f"❌ Error retrieving user data: {e}")

    def View_Cars(self):
        """Displays all available cars."""
        if self.db is None or self.cursor is None:
            print("Database connection is not established.")
            return

        try:
            self.cursor.execute('SELECT * FROM cars')
            cars = self.cursor.fetchall()
            if not cars:
                print("⚠️ No cars found.")
            else:
                print("🚗 Available Cars:")
                for car in cars:
                    print(car)
        except Error as e:
            print(f"❌ Error retrieving car data: {e}")

    def Home(self):
        """Displays the home menu."""
        while True:
            print(f"\n🏪 Welcome to the {self.Name} Store!")
            print("1. Owner Login")
            print("2. User Login")
            print("3. Register")
            print("4. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.Owner_Login()
            elif choice == '2':
                self.User_Login()
            elif choice == '3':
                self.Register()
            elif choice == '4':
                print("👋 Exiting the application.")
                break
            else:
                print("❌ Invalid choice. Please try again.")


# Initialize and run the app
Store = CarCollectionStore()
Store.create_tables()
Store.Home()
