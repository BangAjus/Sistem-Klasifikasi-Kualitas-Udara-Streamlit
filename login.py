import streamlit as st
from pages.utils.conn import db_connection

cursor = db_connection.cursor()

account = {'username':['user'],
           'password':['root']}

add_selectbox = st.sidebar.selectbox(
    "Login & Register",
    ('Login', 'Register')
)

if add_selectbox == 'Login':

    user = st.text_input("username", "")
    pasw = st.text_input("password", "")

    click = st.button('Klik')

    if click:
        
        cursor.execute(f"""
                        SELECT * FROM pengguna WHERE 
                            user_name = '{user}' 
                        AND          
                            password = '{pasw}'                  
                        """)
        data = cursor.fetchone()

        if data == []:
            st.write("Akun tidak ditemukan!")

        else:
            st.write("Berhasil login! Silahkan di-refresh.")

            with open("loginStatus.txt", "w") as file:
                file.write(f"{data[0]};30")

if add_selectbox == 'Register':

    user = st.text_input("username", "")
    pasw = st.text_input("password", "")

    click = st.button('Klik')

    if click:

        cursor.execute(f"""
                        SELECT * FROM pengguna WHERE 
                            user_name = '{user}' 
                        AND          
                            password = '{pasw}'                  
                       """)
        data = cursor.fetchall()

        if data == []:

            cursor.execute(f"""
                            SELECT MAX(user_id) FROM pengguna
                            """)
            last_user_id = cursor.fetchone()[0]
            
            cursor.execute(f"""
                            INSERT INTO pengguna (user_id, user_name, password)
                            VALUES ({last_user_id+1}, '{user}', '{pasw}')               
                            """)
            db_connection.commit()

            st.write("Akun berhasil dibuat!")

        else:
            st.write("Akun sudah ada!")