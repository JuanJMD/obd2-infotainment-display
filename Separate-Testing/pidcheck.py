import obd

connection = obd.Async()

x = input("Enter a PID: ")

res = obd.commands.has_command(str(x)) # True

if(res):
    print(f"{x} is a valid PID. The Response is: {connection.query(obd.commands[str(x)])}")
else:
    print(f"{x} is not a valid PID")

