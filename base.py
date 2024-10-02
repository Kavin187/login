import streamlit as st
import psycopg2

# Database connection details
hostname = '127.0.0.1'
database = 'postgres'
db_username = 'postgres'
pwd = 'postgres'
portid = 5432

# Function to insert user data into the database
def insert_user(username, password):
    conn = None
    cursor = None
    try:
        # Establish connection
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=db_username,
            password=pwd,
            port=portid
        )
        cursor = conn.cursor()

        # Create table if not exists
        create_table_script = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
        '''
        cursor.execute(create_table_script)
        conn.commit()

        # Insert user into table
        insert_user_script = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        cursor.execute(insert_user_script, (username, password))
        conn.commit()

        st.success("User information stored successfully!")

    except Exception as error:
        st.error(f"Error: {error}")

    finally:
        # Ensure cursor and connection are properly closed
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Streamlit UI for login page
def login_page():
    st.title("User Login Page")

    # Form for username and password
    with st.form("login_form"):
        username = st.text_input("Enter your username:")
        password = st.text_input("Enter your password:", type="password")
        submit_button = st.form_submit_button("Submit")

    # When user submits, store the data
    if submit_button:
        if username and password:
            insert_user(username, password)
        else:
            st.warning("Please fill in both the username and password.")

if __name__ == '__main__':
    login_page()
