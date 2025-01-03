import requests
import streamlit as st
from pickle import load
from numpy import array
from pages.utils.models import KNN
from pages.utils.preprocessing import MinMaxScaler
from pages.utils.conn import db_connection
from datetime import date

model = load(open('pages/utils/knn.joblib', 'rb'))
scaler = load(open('pages/utils/minmax_scaler.joblib', 'rb'))
quality_class = {0:'Baik', 1:'Sedang', 2:'Tidak Baik', 3:'Sangat Tidak Baik'}

cursor = db_connection.cursor()
login_status_path = "loginStatus.txt"

with open(login_status_path, "r") as file:
    data_user = file.readline()

if data_user == '':
    st.header("Anda Harus Login Terlebih Dahulu!")
    
else:

    user_id = int(data_user.split(";")[0])
    allowed_interaction = int(data_user.split(";")[1])

    add_selectbox = st.sidebar.selectbox(
        "Fitur",
        ("Fitur 1", "Fitur 2")
    )

    if add_selectbox == 'Fitur 1':

        api_key = '7505104a245774ae2dd85756ed3716dd'

        geo_data = {'Jakarta Utara':(-6.1358859, 106.8419005), 'Jakarta Barat':(-6.1601623,106.6746857), 
                    'Jakarta Timur':(-6.2611416,106.8224464), 'Jakarta Pusat':(-6.1823114,106.7951789), 
                    'Jakarta Selatan':(-6.2841001,106.7195057)}
        data_needed = ['pm10', 'pm2_5', 'so2', 'co', 'o3', 'no2']

        option = st.selectbox(
            "Pilih Daerah di Jakarta",
            (i for i in geo_data.keys()),
            index=None,
            placeholder="pilih daerah"
        )

        if option != None:

            lat, long = geo_data[option]
            url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={api_key}'
            response = requests.get(url)
            data = response.json()

            air_data = data['list'][0]['components']

            air_data_sql = [air_data[i] for i in data_needed]
            today = date.today()
            print(today)
            cursor.execute(f"""
                            SELECT location_id FROM location 
                            WHERE name = '{option}'
                            """)
            location_id = int(cursor.fetchone()[0])
            
            try:
                cursor.execute("""
                                SELECT MAX(input_id) FROM inputs 
                                """)
                input_id = int(cursor.fetchone()[0])
                input_id += 1

            except:
                input_id = 1

            air_data = array([air_data[i] for i in data_needed]).reshape(1, -1)
            air_data_scaled = scaler.transform(air_data)

            air_data_prediction = model.predict(air_data_scaled)
            air_data_prediction = quality_class[air_data_prediction[0]]

            st.write("Hasil Prediksi:", air_data_prediction)

            insert_query = f"""
                            INSERT INTO inputs 
                                (user_id, input_id, location_id, input_date, pm10, pm25, so2, co, o3, no2, kelas) 
                            VALUES ({user_id}, {input_id}, {location_id}, '{today}', {air_data_sql[0]}, {air_data_sql[1]},
                                    {air_data_sql[2]}, {air_data_sql[3]}, {air_data_sql[4]}, {air_data_sql[5]},
                                    '{air_data_prediction}')
                            """
            cursor.execute(insert_query)

            db_connection.commit()

            print("Today's date inserted successfully!")
            print(air_data)
            print(air_data_prediction)

            allowed_interaction -= 1
            with open("loginStatus.txt", "w") as file:
                file.write(f"{user_id};{allowed_interaction}")

    if add_selectbox == 'Fitur 2':

        pm10 = st.text_input("PM10", "")
        pm25 = st.text_input("PM2.5", "")
        so2 = st.text_input("SO2", "")

        co = st.text_input("CO", "")
        o3 = st.text_input("O3", "")
        no2 = st.text_input("NO2", "")

        click = st.button('Klik')

        if click:
            try:

                data_sql = [float(pm10), float(pm25), float(so2),
                                float(co), float(o3), float(no2)]
                today = date.today()

                try:
                    cursor.execute("""
                                    SELECT MAX(input_id) FROM inputs 
                                    """)
                    input_id = int(cursor.fetchone()[0])
                    input_id += 1

                except:
                    input_id = 1

                data = array([[float(pm10), float(pm25), float(so2),
                                float(co), float(o3), float(no2)]])

                data = scaler.transform(data)
                prediction = model.predict(data)
                prediction = quality_class[prediction[0]]

                st.write("Hasil Prediksi:", prediction)

                insert_query = f"""
                                INSERT INTO inputs 
                                    (user_id, input_id, location_id, input_date, pm10, pm25, so2, co, o3, no2, kelas) 
                                VALUES ({user_id}, {input_id}, NULL, '{today}', {data_sql[0]}, {data_sql[1]},
                                        {data_sql[2]}, {data_sql[3]}, {data_sql[4]}, {data_sql[5]},
                                        '{prediction}')
                                """
                cursor.execute(insert_query)

                db_connection.commit()

            except:
                st.write("Dimohon untuk mengisi angka")

            allowed_interaction -= 1
            with open("loginStatus.txt", "w") as file:
                file.write(f"{user_id};{allowed_interaction}")

    if allowed_interaction == 0:    
        with open("loginStatus.txt", "w") as file:
            file.write("")