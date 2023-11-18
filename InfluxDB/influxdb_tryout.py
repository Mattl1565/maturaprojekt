from influxdb import InfluxDBClient

# Set up InfluxDB connection
host = 'localhost'  # Change this to your InfluxDB server host
port = 8086  # Change this to your InfluxDB server port
database = 'maturaprojekt'  # Change this to your desired database name
username = 'admin'  # Change this to your InfluxDB username
password = 'admin'  # Change this to your InfluxDB password

client = InfluxDBClient(host, port, username, password, database)

# Define a sample data point
measurement = 'temperature'
tags = {'location': 'room1'}
fields = {'value': 25.5}
json_body = [
    {
        'measurement': measurement,
        'tags': tags,
        'fields': fields
    }
]

# Write data to InfluxDB
client.write_points(json_body)

# Query data from InfluxDB
result = client.query('SELECT * FROM "{}"'.format(measurement))
print("Query Result:")
print(result.raw)

# Close the InfluxDB connection
client.close()
