import time

import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

#token_laptop = "GxIxdhdibmd-xgl_0uK996cw4ta_9M0INkrjVFqbLILccQIfFUYatmcanJG_7ARcbL0qTifpHO0DJg2-O_ZxBg=="
token_pc = "QV9n46Bpf4I8IUeiwi746ZR2zQwJdDE0FVLNfav3TnNTy2_-TOzO0rVyJxnC2HR4IUTgZuQqQAMLkKJkNV_x2Q=="
org = "Maturaprojekt"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token_pc, org=org)

bucket = "drone_telemetry"

write_api = write_client.write_api(write_options=SYNCHRONOUS)


def write_telemetry(payload):
    temperature = payload["temperature"]
    battery = payload["battery"]
    air_time = payload["flight_time"]
    speed_x = payload["speed_x"]
    speed_y = payload["speed_y"]
    speed_z = payload["speed_z"]
    height = payload["height"]
    barometer = payload["barometer"]

    point1 = (
        Point("temperature")
        .tag("drone", "1")
        .field("temp", int(temperature))
    )
    point2 = (
        Point("air_time")
        .tag("drone", "1")
        .field("air_time", air_time)
    )
    point3 = (
        Point("battery")
        .tag("drone", "1")
        .field("battery", battery)
    )
    point4 = (
        Point("speed_x")
        .tag("drone", "1")
        .field("speed", speed_x)
    )
    point5 = (
        Point("speed_y")
        .tag("drone", "1")
        .field("speed", speed_y)
    )
    point6 = (
        Point("speed_z")
        .tag("drone", "1")
        .field("speed", speed_z)
    )
    point7 = (
        Point("height")
        .tag("drone", "1")
        .field("height", height)
    )
    point8 = (
        Point("barometer")
        .tag("drone", "1")
        .field("barometer", int(barometer))
    )


    write_api.write(bucket=bucket, org="Maturaprojekt", record=point1)
    write_api.write(bucket=bucket, org="Maturaprojekt", record=point2)
    write_api.write(bucket=bucket, org="Maturaprojekt", record=point3)
    write_api.write(bucket=bucket, org="Maturaprojekt", record=point4)
    write_api.write(bucket=bucket, org="Maturaprojekt", record=point5)
    write_api.write(bucket=bucket, org="Maturaprojekt", record=point6)
    write_api.write(bucket=bucket, org="Maturaprojekt", record=point7)
    write_api.write(bucket=bucket, org="Maturaprojekt", record=point8)