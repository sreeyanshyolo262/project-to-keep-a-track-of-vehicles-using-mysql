import mysql.connector
import csv
db=mysql.connector.connect(host="localhost",user="root",password="1234",auth_plugin='mysql_native_password')
p=db.cursor()
p.execute("CREATE DATABASE vehicles")
p.execute("USE vehicles")
p.execute("CREATE TABLE vehicle_inventory(NO int,Make varchar(30),Model varchar(30),Year int,Color varchar(30),Mileage int)")
print("VEHICLE INVENTORY")
def addVehicle():
    try:
        num1=int(input("Enter record number"))
        make1=input('Enter vehicle make: ')
        model1=input('Enter vehicle model: ')
        year1 = int(input('Enter vehicle year: '))
        color1 = input('Enter vehicle color: ')
        mileage1 = int(input('Enter vehicle mileage: '))
        val=(num1,make1,model1,year1,color1,mileage1)
        sql = "INSERT INTO vehicle_inventory (NO,Make,Model,Year,Color,Mileage) VALUES (%s, %s,%s,%s,%s,%s)"
        p.execute(sql,val)
        db.commit()
        print()
        print("This vehicle has been added")
        print()
        return True
    except ValueError:
        print('Please try entering vehicle information again using only whole numbers for mileage and year')
        return False
def viewinventory():
    p.execute("SELECT * FROM vehicle_inventory")
    print("NO.", "Make", "Model", "Year", "Color", "Mileage",sep='\t')
    result = p.fetchall()
    for row in result:
        for x in row:
            print(x,end='\t')
        print()
    print()
        
def updateinventory():
    vehicle_id = int(input("Enter the ID of the vehicle: "))
    make = input("Enter the new make (Press enter to keep old value): ")
    model = input("Enter the new model (Press enter to keep old value): ")
    year_input = input("Enter the new year (Press enter to keep old value): ")
    color = input("Enter the new color (Press enter to keep old value): ")
    mileage_input=input("Enter the new mileage (Press enter to keep old value): ")

    query = "SELECT Make, Model, Year, Color,Mileage FROM vehicle_inventory WHERE NO = %s"
    p.execute(query, (vehicle_id,))
    old_vehicle = p.fetchone()

    if make == "":
        make = old_vehicle[0]
    if model == "":
        model = old_vehicle[1]
    if year_input == "":
        year = old_vehicle[2]
    else:
        year = int(year_input)
    if color == "":
        color = old_vehicle[3]
    if  mileage_input=="":
         mileage=old_vehicle[4]
    else:
        mileage=int(mileage_input)

    query = "UPDATE vehicle_inventory SET Make=%s, Model=%s, Year=%s, Color=%s, Mileage=%s WHERE NO=%s"
    values = (make, model, year, color, mileage, vehicle_id)
    p.execute(query, values)
    db.commit()
    print("Vehicle updated successfully.")
    
    
def exportinventory():
    writer = csv.writer(open("out.csv", 'w'))
    p.execute("SELECT * FROM vehicle_inventory")
    result = p.fetchall()
    for row in result:
        writer.writerow(row)
        
while True:

    print('#1 Add Vehicle to Inventory')
    print('#2 Delete Vehicle from Inventory')
    print('#3 View Current Inventory')
    print('#4 Update Vehicle in Inventory')
    print('#5 Export Current Inventory')
    print('#6 Quit')
    userInput=input('Please choose from one of the above options: ') 
    if userInput=="1": 
        #add a vehicle
        addVehicle()
    elif userInput=='2':
        #delete a vehicle
        viewinventory()
        item = int(input('Please enter the number associated with the vehicle to be removed: '))
        item1=(item,)
        query="DELETE FROM vehicle_inventory WHERE NO= %s"
        p.execute(query,item1)
        db.commit()
        print('This vehicle has been removed')
    elif userInput == '3':
        viewinventory()
    elif userInput == '4':
        #edit vehicle 
        viewinventory()
        updateinventory()
        
        print('This vehicle has been updated')
    elif userInput == '5':
        exportinventory()
        print('The vehicle inventory has been exported to a file')
    elif userInput == '6':
        #exit the loop
        print('Goodbye')
        break
    else:
        #invalid user input
        print('This is an invalid input. Please try again.')
