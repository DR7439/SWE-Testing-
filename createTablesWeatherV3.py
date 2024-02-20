import mysql.connector

# Database connection details
conn = mysql.connector.connect(
    host="dublinbikes.cbiys4e40sjh.eu-west-1.rds.amazonaws.com",
    user="comp30830",
    password="Lochlainn7",
    database="dublinbikes"
)

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# SQL statement to create the availability table
create_availability_table_query = """
CREATE TABLE IF NOT EXISTS availability (
    number INTEGER NOT NULL,
    last_update DATETIME NOT NULL,
    available_bikes INTEGER,
    available_bike_stands INTEGER,
    status VARCHAR(128),
    PRIMARY KEY (number, last_update),
    FOREIGN KEY (number) REFERENCES station(number)
);
"""

# SQL statement to create the weather table
create_weather_table_query = """
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT,
    temperature FLOAT,
    humidity INT,
    weather_condition VARCHAR(255),
    capture_time INT,
    INDEX (capture_time)
);
"""

try:
    # Execute the SQL statement to create the tables
    cur.execute(create_availability_table_query)
    cur.execute(create_weather_table_query)

    # Commit the changes to the database
    conn.commit()
except mysql.connector.Error as e:
    print(f"Database error: {e}")
finally:
    # Close the connection when finished
    conn.close()
