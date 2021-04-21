import json

dataFile = open('tank_game_data.txt', 'r')
lines = dataFile.readlines()
dataFile.close()

csvLines = []
csvLines.append("tankAx,tankAy,tankAr,tankAc,tankBx,tankBy,tankBr,tankBc,r,m,f\n")
for line in lines:
    jsonLine = json.loads(line.strip())
    tankAcanFire = 0
    if jsonLine["tankA"]["can_fire"] == True:
        tankAcanFire = 1
    tankBcanFire = 0
    if jsonLine["tankA"]["can_fire"] == True:
        tankBcanFire = 1

    csvLine = str(jsonLine["tankA"]["x"])+","+str(jsonLine["tankA"]["y"])+","+str(jsonLine["tankA"]["r"])+","+str(tankAcanFire)+","
    csvLine += str(jsonLine["tankB"]["x"])+","+str(jsonLine["tankB"]["y"])+","+str(jsonLine["tankB"]["r"])+","+str(tankBcanFire)+","
    csvLine += str(jsonLine["teamA"]["r"])+","+str(jsonLine["teamA"]["m"])+","+str(jsonLine["teamA"]["f"]) + "\n"
    csvLines.append(csvLine)

csvFile = open('tank_data.csv', 'w')
csvFile.writelines(csvLines)
csvFile.close()
