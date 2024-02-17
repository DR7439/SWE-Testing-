import requests
import mysql.connector
import time
import json
import datetime

# Database connection details
conn = mysql.connector.connect(
    host="dublinbikes.cbiys4e40sjh.eu-west-1.rds.amazonaws.com",
    user="comp30830",
    password="Lochlainn7",
    database="dublinbikes"
)

# Function to fetch and store bike station data
def fetch_and_store_bike_data():
    api_key = "e09579eb9d2b15f1a4011ba140bebdd5e4ffee96"
    contract_name = "Dublin"

    response_API = requests.get(f"https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}")
    data = response_API.text
    stations_data = json.loads(data)

    table_name = "availability"
    insert_query = f"""
    INSERT INTO {table_name} (number, last_update, available_bikes, available_bike_stands, status)
    VALUES (%s, %s, %s, %s, %s);
    """
    cur = conn.cursor()
    try:
        for station in stations_data:
            cur.execute(insert_query, (
                station['number'],
                station['last_update'],
                station['available_bikes'],
                station['available_bike_stands'],
                station['status']
            ))
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close()

def grabWeather():
    weather_api_key = "f35e8800b1d73a63d25ce3213748fba7"
    city_id = "Dublin" 

    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={weather_api_key}")
    weather_data = json.loads(response.text)

    table_name = "weather_data"
    insert_query = f"""
    INSERT INTO {table_name} (city_id, temperature, humidity, weather_condition)
    VALUES (%s, %s, %s, %s);
    """
    cur = conn.cursor()
    try:
        cur.execute(insert_query, (
            city_id,
            weather_data['main']['temp'],
            weather_data['main']['humidity'],
            weather_data['weather'][0]['main']
        ))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close()

try:
    while True:
        fetch_and_store_bike_data()
        grabWeather()
        time.sleep(300)  # Delay for 5 minutes before fetching data again
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
