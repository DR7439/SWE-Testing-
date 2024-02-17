import requests
import time
import traceback
import json
import mysql.connector

# Connecting to database
conn = mysql.connector.connect(
    host="dublinbikes.cbiys4e40sjh.eu-west-1.rds.amazonaws.com",
    user="comp30830",
    password="Lochlainn7",
    database="dublinbikes"
)

def grabWeather():
    weather_api_key = "f35e8800b1d73a63d25ce3213748fba7"
    city_id = "2964574"

    response_API = requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={weather_api_key}")
    data = response_API.text
    weather = json.loads(data)
    
    print("Accessing 'main' in weather:", 'main' in weather)

    table_name = "weather_data"
    insert_query = f"""
    INSERT INTO {table_name} (city_id, temperature, humidity, weather_condition)
    VALUES (%s, %s, %s, %s);
    """
    cur = conn.cursor()
    try:
        cur.execute(insert_query, (
            city_id,
            weather['main']['temp'],
            weather['main']['humidity'],
            weather['weather'][0]['main']
        ))

        print(f"Data inserted into table {table_name} successfully.")
        conn.commit()
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close() 
        
grabWeather()
        
# Function to fetch and store bike station data


    
    


