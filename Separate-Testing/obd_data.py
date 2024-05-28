import obd
import time

def get_obd2_rpm():
    response = connection.query(obd.commands.RPM)
    print(f"LE PRINTER: {response}")
    if(response is None):
        print("Response is none")
        return 0
    return response


connection = obd.Async()
if(connection.status() == obd.OBDStatus.CAR_CONNECTED):
    print("Car connected")
    connection.watch(obd.commands.RPM)
    connection.watch(obd.commands.SPEED)
    connection.watch(obd.commands.THROTTLE_POS)
    connection.watch(obd.commands.FUEL_LEVEL)

    connection.start()
    print("Connection started")

    print(f"RPM: {connection.query(obd.commands.RPM)}")
    get_obd2_rpm()
    print(f"SPEED: {connection.query(obd.commands.SPEED)}")
    print(f"THROTTLE_POS: {connection.query(obd.commands.THROTTLE_POS)}")
    print(f"FUEL_LEVEL: {connection.query(obd.commands.FUEL_LEVEL)}")

    time.sleep(120)
    connection.stop()