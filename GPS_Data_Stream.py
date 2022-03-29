''' 
    Author: Rhema Ike
    Purpose: Continually Stream GPS data from the neo-6m GPS
'''

import serial
import pynmea2

def port_setup(port):
    ser = serial.Serial(port, baudrate=9600, timeout=2)
    return ser

def parseGPSdata(ser):
        keywords = ["$GPRMC","$GPGGA"]
        gps_data = ser.readline()
        gps_data = gps_data.decode("utf-8")

        if len(gps_data) > 5:  # Check to see if the GPS gave any useful data
            if gps_data[0:6] in keywords:   # Check t see if the message code
                gps_msg = pynmea2.parse(gps_data)
                lat = gps_msg.latitude
                lng = gps_msg.longitude
                return (lat,lng)
            else:
                return None
        else:
            return None

if __name__ == "__main__":

    # access serial port
    gps_port = "/dev/serial0"
    ser = port_setup(gps_port)
    # stream = pynmea2.NMEAStreamReader()


    # Print out GPS cordinates
    print("GPS coordinates")
    while True:
        try:
            gps_coords = parseGPSdata(ser)
            if gps_coords is None:
                print("No Data")
            else:
                print(f"latitude: {gps_coords[0]}, longitude: {gps_coords[1]}")

        except serial.SerialException as e:
            print(f"\nERROR: {e}")
            print("... reconnecting to serial\n")
            ser = port_setup()

        except KeyboardInterrupt as e:
            print("--- Program shutting down ---")
            break


