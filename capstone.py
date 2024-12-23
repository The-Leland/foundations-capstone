import sqlite3

import uuid

import csv

import datetime

import bcrypt


connection = sqlite3.connect('competency_database.db')

cursor = connection.cursor()

def initialize_database(connection):
    cursor = connection.cursor()
    
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        user_type TEXT NOT NULL,
                        first_name TEXT NOT NULL,
                        last_name TEXT,
                        city TEXT,
                        state TEXT,
                        email TEXT UNIQUE NOT NULL,
                        occupation TEXT,
                        manager_title TEXT,
                        dat_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')

    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Competencies (
                        competency_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        scale INTEGER,
                        description TEXT,  -- Added missing comma here
                        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')

    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Assessments (
                        assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        competency_id INTEGER,
                        FOREIGN KEY (competency_id) REFERENCES Competencies (competency_id)
                      )''')

   
    cursor.execute('''CREATE TABLE IF NOT EXISTS AssessmentResults (
                        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        assessment_id INTEGER,
                        score REAL,
                        comments TEXT,
                        assessment_date DATE,
                        FOREIGN KEY (user_id) REFERENCES Users (user_id),
                        FOREIGN KEY (assessment_id) REFERENCES Assessments (assessment_id)
                      )''')

   
    competencies = [
        "Computer Anatomy", "Data Types", "Variables", "Functions", "Boolean Logic", "Conditionals", "Loops", 
        "Data Structures", "Lists", "Dictionaries", "Working with Files", "Exception Handling", "Quality Assurance (QA)", 
        "Object-Oriented Programming", "Recursion", "Databases"
    ]
    
    for competency in competencies:
        cursor.execute("INSERT INTO Competencies (name) VALUES (?)", (competency,))
    
    connection.commit()

   
    connection.commit()


initialize_database(connection)



def populate_initial_competencies():
    competencies = [
        ("Computer Anatomy", 1),
        ("Data Types", 1),
        ("Variables", 2),
        ("Functions", 3),
        ("Boolean Logic", 2),
        ("Conditionals", 3),
        ("Loops", 2),
        ("Data Structures", 3),
        ("Lists", 2),
        ("Dictionaries", 3),
        ("Working with Files", 3),
        ("Exception Handling", 2),
        ("Quality Assurance (QA)", 4),
        ("Object-Oriented Programming", 4),
        ("Recursion", 3),
        ("Databases", 3)
    ]
    
    for competency in competencies:
        cursor.execute('''
        INSERT INTO Competencies (name, scale) VALUES (?, ?)
        ''', (competency[0], competency[1]))
    
    connection.commit()
    print("Initial competencies added successfully!")



def generate_unique_id():
    
    return str(uuid.uuid4())




def authenticate_user(username, password, cursor): 
    cursor.execute("SELECT password, user_type FROM Users WHERE username=?", (username,)) 
    result = cursor.fetchone() 
    if result: 
        stored_password, user_type = result 
        if bcrypt.checkpw(password.encode('utf-8'), stored_password): 
            return user_type 
    return None



import bcrypt

def register_user(cursor, connection): 
    while True: 
        user_type = input("Enter user type (manager/user): ").lower() 
        if user_type not in ['manager', 'user']: 
            print("Invalid user type. Please enter 'manager' or 'user'.") 
            continue 
        
        username = input("Enter username: ") 
        password = input("Enter password: ").encode('utf-8') 
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()) 
        
        first_name = input("Enter first name: ") 
        last_name = input("Enter last name: ") 
        city = input("Enter city: ") 
        state = input("Enter state: ") 
        email = input("Enter email: ") 
        occupation = input("Enter occupation: ") 
        
        if user_type == 'manager': 
            manager_title = input("Enter manager title: ") 
            cursor.execute("INSERT INTO Users (username, password, user_type, first_name, last_name, city, state, email, occupation, manager_title) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           (username, hashed_password, user_type, first_name, last_name, city, state, email, occupation, manager_title)) 
        else: 
            cursor.execute("INSERT INTO Users (username, password, user_type, first_name, last_name, city, state, email, occupation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           (username, hashed_password, user_type, first_name, last_name, city, state, email, occupation)) 
            
        connection.commit() 
        print("User registered successfully!") 
        break



def is_first_time_user(username, cursor):
   
    cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username,))
    count = cursor.fetchone()[0]
    
    
    return count == 0




def add_user():
    
    user_type = input("Enter user type (manager/user): ").lower()
    
    if user_type not in ['manager', 'user']:
        print("Invalid user type. Please enter 'manager' or 'user'.")
        return

    username = input("Enter username: ")
    password = input("Enter password: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    email = input("Enter email: ")
    occupation = input("Enter occupation: ")

    manager_title = None
   
    if user_type == 'manager':
        manager_title = input("Enter manager title: ")

    cursor.execute('''INSERT INTO Users (username, password, user_type, first_name, last_name, city, state, email, occupation, manager_title) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (username, password, user_type, first_name, last_name, city, state, email, occupation, manager_title))
    
    connection.commit()
    print("User added successfully!")




COMPETENCY_SCALE = {
    0: "No competency - Needs Training and Direction",
    1: "Basic Competency - Needs Ongoing Support",
    2: "Intermediate Competency - Needs Occasional Support",
    3: "Advanced Competency - Completes Task Independently",
    4: "Expert Competency - Can Effectively pass on this knowledge and can initiate optimizations"
}



def add_assessment_result(user_id, assessment_id):
   
    try:
        score = int(input("Enter score (0-4): "))
    
    except ValueError:
        print("Invalid input. Please enter an integer value between 0 and 4.")
        return
    
    if score not in COMPETENCY_SCALE:
        print("Invalid score. Please enter a value between 0 and 4.")
        return
    
   
    print(f"Competency Scale: {COMPETENCY_SCALE[score]}")

    
    assessment_date = datetime.date.today().isoformat()
    with connection:
        cursor.execute('''INSERT INTO AssessmentResults (user_id, assessment_id, score, assessment_date)
                          VALUES (?, ?, ?, ?)''', 
                       (user_id, assessment_id, score, assessment_date))
    
    print("Assessment result added successfully!")



def delete_assessment_result(assessment_id, user_id):
    
    cursor.execute('SELECT * FROM AssessmentResults WHERE assessment_id = ? AND user_id = ?', (assessment_id, user_id))
    result = cursor.fetchone()

    if result:
        
        with connection:
            cursor.execute('DELETE FROM AssessmentResults WHERE assessment_id = ? AND user_id = ?', (assessment_id, user_id))
        print(f"Assessment result with ID {assessment_id} has been deleted.")
    
    else:
        print(f"Assessment result with ID {assessment_id} does not exist or does not belong to user {user_id}.")



def add_competency():

    name = input("Enter the name of the competency: ")
    scale = int(input("Enter the scale (0-4): "))  
    date_created = datetime.date.today().isoformat()

    cursor.execute('''INSERT INTO Competencies (name, scale, date_created) VALUES (?, ?, ?)''',
                   (name, scale, date_created))
    connection.commit()
    print("Competency added successfully!")




COMPETENCY_SCALE = {
    0: "No competency - Needs Training and Direction",
    1: "Basic Competency - Needs Ongoing Support",
    2: "Intermediate Competency - Needs Occasional Support",
    3: "Advanced Competency - Completes Task Independently",
    4: "Expert Competency - Can Effectively pass on this knowledge and can initiate optimizations"
}

def view_competencies_with_scale(cursor):
    cursor.execute("SELECT competency_id, name, scale FROM Competencies")
    rows = cursor.fetchall()
    
    if rows:
        for row in rows:
            competency_id, name, scale = row
            scale_description = COMPETENCY_SCALE.get(scale, "Unknown scale")
            print(f"ID: {competency_id}, Name: {name}, Scale: {scale} ({scale_description})")
   
    else:
        print("No competencies found.")


def view_user_competency_results(user_id):
    cursor.execute('''SELECT ar.assessment_id, a.name, ar.score
                      FROM AssessmentResults ar
                      JOIN Assessments a ON ar.assessment_id = a.assessment_id
                      WHERE ar.user_id = ?''', (user_id,))
    results = cursor.fetchall()
    
    if results:
        for result in results:
            assessment_name = result[1]
            score = result[2]
            print(f"Assessment: {assessment_name} | Score: {score} ({COMPETENCY_SCALE.get(score, 'Unknown')})")
   
    else:
        print(f"No competency results found for user {user_id}.")



def update_competency_scale(competency_id, new_scale):
    if new_scale not in [0, 1, 2, 3, 4]:
        print("Invalid scale value. Valid values are 0 to 4.")
        return

  
    cursor.execute("SELECT * FROM Competencies WHERE competency_id = ?", (competency_id,))
   
    if not cursor.fetchone():
        print(f"Competency ID {competency_id} does not exist.")
        return

    with connection:
        cursor.execute('''UPDATE Competencies
                          SET scale = ?
                          WHERE competency_id = ?''', (new_scale, competency_id))
    print(f"Competency ID {competency_id} scale updated to {new_scale}.")




def export_users_to_csv(cursor):
    
    file_path = input("Enter the file path to save the CSV (e.g., users.csv): ").strip()

    
    if not file_path:
        print("No file path provided. Cancelling export.")
        return

    
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()

    
    if rows:
        try:
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)

                
                csvwriter.writerow([desc[0] for desc in cursor.description])

                
                csvwriter.writerows(rows)
            print(f"Users exported to {file_path}")
        except Exception as e:
            print(f"An error occurred while exporting to CSV: {e}")
    else:
        print("No data found to export.")




def export_competencies_to_csv(cursor):
    
    file_path = input("Enter the file path to save the CSV (e.g., competencies.csv): ").strip()

   
    if not file_path:
        print("No file path provided. Cancelling export.")
        return

    
    cursor.execute("SELECT * FROM Competencies")
    rows = cursor.fetchall()

    
    if rows:
        try:
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)

                
                csvwriter.writerow([desc[0] for desc in cursor.description])

                
                csvwriter.writerows(rows)
            print(f"Competencies exported to {file_path}")
        except Exception as e:
            print(f"An error occurred while exporting to CSV: {e}")
    else:
        print("No data found to export.")





def remove_competency(competency_id):
    cursor.execute("DELETE FROM Competencies WHERE competency_id=?", (competency_id,))
    cursor.connection.commit()
    print(f"Competency {competency_id} removed successfully.")




def import_assessment_results_from_csv(cursor, connection):
    
    file_path = input("Enter the file path to import assessment results from (e.g., results.csv): ").strip()

    
    if not file_path:
        print("No file path provided. Cancelling import.")
        return

    try:
        
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)  

           
            insert_query = '''INSERT INTO AssessmentResults (user_id, assessment_id, score, assessment_date)
                              VALUES (?, ?, ?, ?)'''

            connection.begin()  

            for row in csvreader:
                if len(row) != len(header):
                    print(f"Skipping invalid row: {row}")
                    continue

                if not validate_assessment_result(row):  
                    continue

                cursor.execute(insert_query, row)  

            connection.commit()  
            print(f"Assessment results imported successfully from {file_path}.")
    
    except Exception as e:
        connection.rollback()  
        print(f"Error importing data: {e}")






def validate_assessment_result(row):
    
    try:
        user_id, assessment_id, score, assessment_date = row
        score = float(score)
        return True
  
    except ValueError:
        return False


def view_data(data_type, filters=None):
    query_map = {
        'users': "SELECT * FROM Users",
        'competencies': "SELECT * FROM Competencies",
        'assessments': "SELECT * FROM Assessments",
        'assessment_results': "SELECT * FROM AssessmentResults",
    }
    
    query = query_map.get(data_type)
    

    if query:
        if filters:
            filter_condition = " AND ".join([f"{key} = ?" for key in filters.keys()])
            query += " WHERE " + filter_condition
            print(f'With filters: {filters}')
            result = cursor.execute(query, tuple(filters.values()))
      
        else:
            result = cursor.execute(query)
            

        rows = result.fetchall()
        print(f'Rows fetched: {len(rows)}')
        if rows:
            for row in rows:
                print(row)

        else:
            print(f'No {data_type} data found.')
        
        input()

    else:
        print("Unknown data type.")


def search_user_by_username(username):
    cursor.execute("SELECT user_id FROM Users WHERE username=?", (username,))
    result = cursor.fetchone()
    
    if result:
        return result[0]  
  
    else:
        print("User not found.")
        return None

def search_competency_by_name(name):
    cursor.execute("SELECT competency_id FROM Competencies WHERE name=?", (name,))
    result = cursor.fetchone()
   
    if result:
        return result[0]  
   
    else:
        print("Competency not found.")
        return None


def search_assessment_by_name(name):
    cursor.execute("SELECT assessment_id FROM Assessments WHERE name=?", (name,))
    result = cursor.fetchone()
   
    if result:
        return result[0] 
   
    else:
        print("Assessment not found.")
        return None


def update_assessment_result(cursor):
    user_id = input("Enter the user ID: ")
    assessment_id = input("Enter the assessment ID: ")
    result_id = search_assessment_result_by_user_and_assessment(user_id, assessment_id)
    
    if result_id:
        new_values = {
            'score': input("Enter new score: "),
            'comments': input("Enter new comments: ")
        }
        edit_data('assessment_result', result_id, new_values)




def search_assessment_result_by_user_and_assessment(user_id, assessment_id):
    cursor.execute("SELECT result_id FROM AssessmentResults WHERE user_id=? AND assessment_id=?", (user_id, assessment_id))
    result = cursor.fetchone()
   
    if result:
        return result[0] 
    
    else:
        print("Assessment result not found.")
        return None





def edit_data(data_type, identifier, new_values):
   
    query_map = {
        'user': """UPDATE Users SET
                      first_name = ?, last_name = ?, email = ?, password = ?, 
                      city = ?, state = ?, occupation = ?
                      WHERE user_id = ?""",
        'competency': """UPDATE Competencies SET
                         name = ?, description = ?
                         WHERE competency_id = ?""",
        'assessment': """UPDATE Assessments SET
                         name = ?, description = ?, competency_id = ?
                         WHERE assessment_id = ?""",
        'assessment_result': """UPDATE AssessmentResults SET
                               score = ?, comments = ?
                               WHERE result_id = ?"""
    }
    
    query = query_map.get(data_type)
    
    if query:
        if data_type == 'user':
            password = new_values['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            new_values['password'] = hashed_password
        
        cursor.execute(query, tuple(new_values.values()) + (identifier,))
        cursor.connection.commit()
        print(f"{data_type.capitalize()} record updated successfully!")
    else:
        print("Unknown data type.")


def update_user_information(cursor):
    username = input("Enter the username of the user to update: ")
    user_id = search_user_by_username(username)
    if user_id:
        new_values = {
            'first_name': input("Enter new first name: "),
            'last_name': input("Enter new last name: "),
            'email': input("Enter new email: "),
            'password': input("Enter new password: "),
            'city': input("Enter new city: "),
            'state': input("Enter new state: "),
            'occupation': input("Enter new occupation: ")
        }
        edit_data('user', user_id, new_values)


def view_your_information(cursor, user_id):
    cursor.execute("SELECT first_name, last_name, email, city, state, occupation FROM Users WHERE user_id = ?", (user_id,))
    user_info = cursor.fetchone()
    
    if user_info:
        print(f"\nYour Information:")
        print(f"First Name: {user_info[0]}")
        print(f"Last Name: {user_info[1]}")
        print(f"Email: {user_info[2]}")
        print(f"City: {user_info[3]}")
        print(f"State: {user_info[4]}")
        print(f"Occupation: {user_info[5]}")
    else:
        print("User not found.")



def view_competency_list(cursor, user_id):
    cursor.execute("SELECT competency_id, competency_name FROM Competencies")
    competencies = cursor.fetchall()
    
    if competencies:
        print("\nCompetency List:")
        for competency in competencies:
            print(f"Competency ID: {competency[0]} - {competency[1]}")
    else:
        print("No competencies found.")



def view_assessment_list(cursor, user_id):
    cursor.execute("SELECT assessment_id, assessment_name FROM Assessments WHERE user_id = ?", (user_id,))
    assessments = cursor.fetchall()
    
    if assessments:
        print("\nAssessment List:")
        for assessment in assessments:
            print(f"Assessment ID: {assessment[0]} - {assessment[1]}")
    else:
        print("No assessments found.")



def view_user_competency_results(cursor, user_id):
    cursor.execute("SELECT competency_id, result FROM CompetencyResults WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()
    
    if results:
        print("\nYour Competency Results:")
        for result in results:
            print(f"Competency ID: {result[0]} - Result: {result[1]}")
    else:
        print("No competency results found.")


def view_your_assessment_results(cursor, user_id):
    cursor.execute("SELECT assessment_id, score FROM AssessmentResults WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()
    
    if results:
        print("\nYour Assessment Results:")
        for result in results:
            print(f"Assessment ID: {result[0]} - Score: {result[1]}")
    else:
        print("No assessment results found.")


def view_scores(cursor):
    # Example query to fetch scores
    query = "SELECT * FROM Scores"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)


def view_user_reports(cursor, user_id):
    # Example query to fetch user reports
    query = "SELECT * FROM Reports WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    for row in results:
        print(row)


def link_assessments_to_competency(cursor):
    competency_id = input("Enter competency ID: ")
    assessment_id = input("Enter assessment ID: ")
    # Example logic to link assessment to competency
    query = "UPDATE Assessments SET competency_id = ? WHERE assessment_id = ?"
    cursor.execute(query, (competency_id, assessment_id))
    print(f"Assessment {assessment_id} linked to competency {competency_id}")


def select_user_and_view_details(cursor, user_id):
    query = "SELECT * FROM Users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        print(result)
    else:
        print("User not found")


def delete_user(cursor, connection, user_id):
    query = "DELETE FROM Users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    connection.commit()
    print(f"User {user_id} deleted")


def edit_competency(cursor, competency_id):
    name = input("Enter new name: ")
    description = input("Enter new description: ")
    query = "UPDATE Competencies SET name = ?, description = ? WHERE competency_id = ?"
    cursor.execute(query, (name, description, competency_id))
    print(f"Competency {competency_id} updated")


def edit_assessment(cursor, assessment_id):
    name = input("Enter new name: ")
    description = input("Enter new description: ")
    query = "UPDATE Assessments SET name = ?, description = ? WHERE assessment_id = ?"
    cursor.execute(query, (name, description, assessment_id))
    print(f"Assessment {assessment_id} updated")


def edit_assessment_result(cursor, assessment_result_id):
    score = input("Enter new score: ")
    comments = input("Enter new comments: ")
    query = "UPDATE AssessmentResults SET score = ?, comments = ? WHERE result_id = ?"
    cursor.execute(query, (score, comments, assessment_result_id))
    print(f"Assessment result {assessment_result_id} updated")


def edit_competency_scale(cursor, competency_id):
    scale = input("Enter new scale: ")
    query = "UPDATE Competencies SET scale = ? WHERE competency_id = ?"
    cursor.execute(query, (scale, competency_id))
    print(f"Competency {competency_id} scale updated")


def authenticate_user(username, password, cursor):
    # Example logic for authenticating user
    query = "SELECT user_type, user_id FROM Users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    if result:
        user_type, user_id = result
        return user_type, user_id
    return None, None


def register_user(cursor, connection):
    username = input("Enter username: ")
    password = input("Enter password: ")
    user_type = input("Enter user type (manager/user): ")
    query = "INSERT INTO Users (username, password, user_type) VALUES (?, ?, ?)"
    cursor.execute(query, (username, password, user_type))
    connection.commit()
    print("User registered successfully")


def manager_menu(cursor, connection):
    while True:
        print("\nManager Menu:")
        print("1. View all users")
        print("2. View all competencies")
        print("3. View all assessments")
        print("4. View scores for competencies and assessments")
        print("5. View reports for competencies and assessments linked to each user")
        print("6. View overall report for competencies and assessments for all users")
        print("7. Add a competency")
        print("8. Remove a competency")
        print("9. Link assessments to a competency")
        print("10. Select a user to view details")
        print("11. Add a user")
        print("12. Delete a user")
        print("13. Edit user information")
        print("14. Edit a competency")
        print("15. Edit an assessment")
        print("16. Edit an assessment result")
        print("17. Edit competency scale")
        print("18. Delete an assessment result")
        print("19. Export users to CSV")
        print("20. Export competencies to CSV")
        print("21. Import assessment results from CSV")
        print("22. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            view_data(cursor, 'users')  
        elif choice == "2":
            view_data(cursor, 'competencies')  
        elif choice == "3":
            view_data(cursor, 'assessments')  
        elif choice == "4":
            view_scores(cursor)  
        elif choice == "5":
            user_id = input('Enter user ID: ').strip()
            if user_id:  
                view_user_reports(cursor, int(user_id))  
        elif choice == "6":
            view_data(cursor, 'overall_reports')  
        elif choice == "7":
            add_competency(cursor)  
        elif choice == "8":
            remove_competency(cursor) 
        elif choice == "9":
            link_assessments_to_competency(cursor)  
        elif choice == "10":
            user_id = input('Enter user ID: ').strip()
            if user_id:  
                select_user_and_view_details(cursor, int(user_id)) 
        elif choice == "11":
            add_user(cursor, connection)  
        elif choice == "12":
            user_id = input('Enter user ID to delete (or press Enter to cancel): ').strip()
            if user_id:  
                delete_user(cursor, connection, int(user_id))  
        elif choice == "13":
            user_id = input('Enter user ID to edit (or press Enter to cancel): ').strip()
            if user_id:  
                new_values = { 
                    'first_name': input("Enter new first name: "), 
                    'last_name': input("Enter new last name: "), 
                    'email': input("Enter new email: "), 
                    'password': input("Enter new password: "), 
                    'city': input("Enter new city: "), 
                    'state': input("Enter new state: "), 
                    'occupation': input("Enter new occupation: ")
                }
                edit_data('user', int(user_id), new_values)  
        elif choice == "14":
            competency_id = input('Enter competency ID to edit (or press Enter to cancel): ').strip()
            if competency_id: 
                edit_competency(cursor, int(competency_id))  
        elif choice == "15":
            assessment_id = input('Enter assessment ID to edit (or press Enter to cancel): ').strip()
            if assessment_id:  
                edit_assessment(cursor, int(assessment_id)) 
        elif choice == "16":
            assessment_result_id = input('Enter assessment result ID to edit (or press Enter to cancel): ').strip()
            if assessment_result_id:  
                edit_assessment_result(cursor, int(assessment_result_id))  
        elif choice == "17":
            competency_id = input('Enter competency ID to edit scale (or press Enter to cancel): ').strip()
            if competency_id:  
                edit_competency_scale(cursor, int(competency_id))  
        elif choice == "18":
            assessment_result_id = input('Enter assessment result ID to delete (or press Enter to cancel): ').strip()
            if assessment_result_id: 
                delete_assessment_result(cursor, int(assessment_result_id)) 
        elif choice == "19":
            export_users_to_csv(cursor)  
        elif choice == "20":
            export_competencies_to_csv(cursor)  
        elif choice == "21":
            import_assessment_results_from_csv(cursor, connection)  
        elif choice == "22":
            print("Goodbye!")  
            break
        else:
            print("Invalid choice. Please try again.")  




def user_menu(cursor, user_id):
    while True:
        print("\nUser Menu:")
        print("1. View your information")
        print("2. Edit your information")
        print("3. View competency list")
        print("4. View assessment list")
        print("5. View your competency results")
        print("6. View your assessment results")
        print("7. Return to previous menu")  

        choice = input("Enter choice (or press Enter to go back): ").strip() 

        if choice == '1':
            view_your_information(cursor, user_id)
        elif choice == '2':
            
            print("Leave fields blank to retain current values.")
            new_values = {
                'first_name': input(f"Enter new first name (current: {get_current_value(cursor, user_id, 'first_name')}): ").strip() or None,
                'last_name': input(f"Enter new last name (current: {get_current_value(cursor, user_id, 'last_name')}): ").strip() or None,
                'email': input(f"Enter new email (current: {get_current_value(cursor, user_id, 'email')}): ").strip() or None,
                'password': input(f"Enter new password (current: {get_current_value(cursor, user_id, 'password')}): ").strip() or None,
                'city': input(f"Enter new city (current: {get_current_value(cursor, user_id, 'city')}): ").strip() or None,
                'state': input(f"Enter new state (current: {get_current_value(cursor, user_id, 'state')}): ").strip() or None,
                'occupation': input(f"Enter new occupation (current: {get_current_value(cursor, user_id, 'occupation')}): ").strip() or None,
            }

            
            new_values = {key: value for key, value in new_values.items() if value is not None}

            if new_values:  
                edit_data('user', user_id, new_values)
            else:
                print("No changes made. Returning to the menu.")
        elif choice == "3":
            view_competency_list(cursor, user_id)
        elif choice == "4":
            view_assessment_list(cursor, user_id)
        elif choice == "5":
            view_user_competency_results(cursor, user_id)
        elif choice == "6":
            view_your_assessment_results(cursor, user_id)
        elif choice == "7" or choice == "":  
            return  
        else:
            print("Invalid choice. Please try again.")


def get_current_value(cursor, user_id, field):
    query = f"SELECT {field} FROM Users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    return result[0] if result else "N/A"




def main_menu(): 
    while True: 
        print("\nWelcome! Please choose an option:") 
        print("1. Log in") 
        print("2. Register") 
        
        choice = input("Enter choice: ") 
        
        if choice == "1": 
            username = input("Enter your username: ") 
            password = input("Enter your password: ") 
            user_type, user_id = authenticate_user(username, password, cursor) 

            if user_type == 'manager':
                manager_menu(cursor, connection)  
            elif user_type == 'user':
                user_menu(cursor, user_id)  
            else:
                print('Invalid username or password. Please try again.')
                continue

        elif choice == "2":
            register_user()  
        else:
            print('Invalid choice. Please try again.')




        
def login_screen():
    while True:
        print("\nWelcome! Please choose an option:")
        
        
        choice = input("Is this your first time logging in? (y/n): ").lower()
        
        if choice == 'y':
            
            print("It seems like this is your first time logging in. Let's register you.")
            register_user()
        
        elif choice == 'n':
            
            print("\nPlease choose an option:")
            print("1. Log in")
            print("2. Exit")
            
            user_choice = input("Enter choice: ")
            
            if user_choice == "1":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                user_type = authenticate_user(username, password, cursor)
                
                if user_type == 'manager':
                    print("Login successful! Welcome, Manager.")
                    manager_menu(cursor, connection)
                elif user_type == 'user':
                    print("Login successful! Welcome, User.")
                    user_menu(cursor, 'user_id')
                else:
                    print("Invalid username or password. Please try again.")
                
            elif user_choice == "2":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def main():
    
    initialize_database(connection)
    
    login_screen()
    
    connection.close()

if __name__ == "__main__":
    main()





