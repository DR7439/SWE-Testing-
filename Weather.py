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
    weather_api_key = "e09579eb9d2b15f1a4011ba140bebdd5e4ffee96"
    city_id = "Dublin"
    
    response_API = requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={weather_api_key}")
    data = response_API.text
    weather = json.loads(data)

    print(weather)  # Print the full response
    print(type(weather))  # Confirm that 'weather' is a dictionary

    # Add this line to debug the specific access
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
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close() 
        
grabWeather()
        
# Function to fetch and store bike station data


    
    


