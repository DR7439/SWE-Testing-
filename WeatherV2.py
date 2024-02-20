import requests
import time
import traceback
import logging
import json
import mysql.connector

logging.basicConfig(filename='weather_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

logging.info("starting connection")

# Connecting to database
conn = mysql.connector.connect(
    host="dublinbikes.cbiys4e40sjh.eu-west-1.rds.amazonaws.com",
    user="comp30830",
    password="Lochlainn7",
    database="dublinbikes"
)

def grabWeather():
    try:
        weather_api_key = "f35e8800b1d73a63d25ce3213748fba7"
        city_id = "2964574"

        response_API = requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={weather_api_key}")
        data = response_API.text
        weather = json.loads(data)

        current_time = datetime.now()

        table_name = "weather_data"
        insert_query = f'''
        INSERT INTO {table_name} (city_id, temperature, humidity, weather_condition, capture_time)
        VALUES (%s, %s, %s, %s, %s);
        '''
        cur = conn.cursor()

        try:
            cur.execute(insert_query, (
                city_id,
                weather['main']['temp'],
                weather['main']['humidity'],
                weather['weather'][0]['main'],
                current_time
            ))

            logging.info(f"Data inserted into table {table_name} successfully.")
            conn.commit()
            
        except mysql.connector.Error as e:
            logging.error(f"Database error: {e}")
        finally:
            cur.close() 

    except Exception as e:
        logging.error("An error occurred in grabWeather: " + str(e))
        traceback.print_exc()

    finally:
        if conn.is_connected():
            conn.close()
            logging.info('Database connection closed.')

print("Data inserted into table")

if __name__ == "__main__":
    grabWeather()
