import csv
from sys import set_asyncgen_hooks
from typing import final
rows = []
with open ('data2.csv', 'r') as f:
    csvReader = csv.reader(f)
    for i in csvReader:
        rows.append(i)

headers = rows[0]
planetData = rows[1:]
#print(headers)
headers[0] = "Serial N.O." 
SolarSystemPC = {}
for i in planetData:
    if SolarSystemPC.get(i[11]):
        SolarSystemPC[i[11]] += 1
    else:
        SolarSystemPC[i[11]] = 1

MaxSolarSystem = max(SolarSystemPC, key = SolarSystemPC.get)
#print(MaxSolarSystem)
koi = []
for i in planetData:
    if i[11] == MaxSolarSystem:
        koi.append(i)

#print(len(koi))
#print(koi)

tempPlanetData = list(planetData)
for i in tempPlanetData:
    planetMass = i[3]
    if planetMass.lower() == "unknown":
        planetData.remove(i)
        continue
    else:
        planetMassValue = planetMass.split(" ")[0]
        planetMassRef = planetMass.split(" ")[1]
        if planetMassRef == "Jupiters":
            planetMassValue = float(planetMassValue)*317.8
        i[3] = planetMassValue
    planetRadius = i[7]
    if planetRadius.lower() == 'unknown':
        planetData.remove(i)
        continue
    else:
        planetRadiusValue = planetRadius.split(" ")[0]
        planetRadiusRef = planetRadius.split(' ')[1]
        if planetRadiusRef == 'Jupiters':
            planetRadiusValue = float(planetRadiusValue)*11.2
        i[7] = planetRadiusValue

import plotly.express as px
koiMass = []
koiName = []
for i in koi:
    koiMass.append(i[3])
    koiName.append(i[1])
koiMass.append(1)
koiName.append('Earth')
graph = px.bar(x = koiName, y = koiMass)
#graph.show()

tempPlanetData = list(planetData)
planetMasses = []
planetRadii = []
planetNames = []
planetGravity = []
for i in tempPlanetData:
    if i[1].lower() == "hd 100546 b":
        planetData.remove(i)
for i in planetData:
    planetMasses.append(i[3])
    planetRadii.append(i[7])
    planetNames.append(i[1])
for index,name in enumerate(planetNames):
    gravity = ((float(planetMasses[index])* 5.972e+24)/(float(planetRadii[index])*float(planetRadii[index])*6371000*6371000))*6.674e-11
    planetGravity.append(gravity)

graph2 = px.scatter(x = planetRadii, y = planetMasses, size = planetGravity, hover_data = [planetNames])
#graph2.show()

lowGravPlanets = []
lowGravPlanets2 = []
for index,gravity in enumerate(planetGravity):
    if gravity<10:
        lowGravPlanets.append(planetData[index])
#print(len(lowGravPlanets))

for index, gravity in enumerate(planetGravity):
    if gravity<100:
        lowGravPlanets2.append(planetData[index])
#print(len(lowGravPlanets2))

planetType = []
for i in planetData:
    planetType.append(i[6])
#print(list(set(planetType)))
planetMassLG = []
planetRadiusLG = []
for i in lowGravPlanets2:
    planetMassLG.append(i[3])
    planetRadiusLG.append(i[7])
graph3 = px.scatter(x = planetRadiusLG, y = planetMassLG)
#graph3.show()
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sb
x = []
for index,planetMass in enumerate(planetMassLG):
    templist = [planetRadiusLG[index], planetMass]
    x.append(templist)

wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters = i, init = "k-means++", random_state = 42)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)

plt.figure(figsize = (20,15))
sb.lineplot(range(1,11), wcss, marker = "o", color = 'red')
plt.title("elbowMethod")
plt.xlabel('number of clusters')
plt.ylabel('wcss')
#plt.show()

planetMass = []
planetRadius = []
planetType = []
for i in lowGravPlanets2:
    planetMass.append(i[3])
    planetRadius.append(i[7])
    planetType.append(i[6])
graph4 = px.scatter(x = planetRadius, y = planetMass, color = planetType)
#graph4.show()

suitablePlanets = []
for i in lowGravPlanets2:
    if i[6]=='Super Earth':
        suitablePlanets.append(i)
    if i[6]=='Terrestrial':
        suitablePlanets.append(i)
#print(len(suitablePlanets))
#print(headers)
tempSuitablePlanets = list(suitablePlanets)
for i in tempSuitablePlanets:
    if i[8].lower()== 'unknown':
        suitablePlanets.remove(i)
    if i[9].lower() =='unknown':
        suitablePlanets.remove(i)

for i in suitablePlanets:
    if i[9].split(" ")[1].lower() == 'years':
        i[9] = float(i[9].split(" ")[0])*365
    else:
        i[9] = float(i[9].split(" ")[0])
    i[8] = float(i[8].split(" ")[0])
orbital_radii = []
orbital_periods = []

for i in suitablePlanets:
    orbital_radii.append(i[8])
    orbital_periods.append(i[9])
graph5 = px.scatter(x = orbital_radii, y = orbital_periods)
#graph5.show()

GoldilockPlanets = list(suitablePlanets)
for i in suitablePlanets:
    if i[8] < 0.38 or i[8]>2:
        GoldilockPlanets.remove(i)

#print(len(GoldilockPlanets))
#print(len(suitablePlanets))

planetSpeed = []

for i in suitablePlanets:
    planetDistance = 2*3.14*(i[8]*1.496e+8)
    planetTime = i[9]*86400
    planetSpeed.append(planetDistance/planetTime)
speedSupportPlanets = list(suitablePlanets)
tempSpeedSupportPlanets = list(suitablePlanets)
for index, planetData in enumerate(tempSpeedSupportPlanets):
    if planetSpeed[index]> 200:
        speedSupportPlanets.remove(planetData)
#print(len(speedSupportPlanets))

habitablePlanets = []
for i in speedSupportPlanets:
    if i in GoldilockPlanets:
        habitablePlanets.append(i)
#print(len(habitablePlanets))
finalData = {}
print(planetData)
for index, pd in enumerate(planetData):
    featuresList = []
    #print(pd[1])
    #/(float(pd[7])*float(pd[7])*6371000*6371000)
    #gravity = (float(pd[3])*5.972e+24)
    gravity = gravity * 6.674e-11
    try:
        if gravity<100:
            featuresList.append('gravity')
    except:
        pass
    try:
        if pd[6].lower() == 'terrestrial' or pd[6].lower() == 'super earth':
            featuresList.append('planetType')
    except:
        pass
    try:
        distance = 2*3.14*pd[8]*1.496e+9
        time = pd[9] * 86400
        speed = distance/time
        if speed<200:
            featuresList.append('speed')
    except:
        pass
    try:
        if pd[8]>0.38 or pd[8]<2:
            featuresList.append('goldilock')
    except:
        pass
    finalData[index] = featuresList
#print(finalData)
gravityPlanetCount = 0

for key, value in finalData.items():
    if 'gravity' in value:
        gravityPlanetCount += 1
print("gravityPlanetCount is")
print(gravityPlanetCount)

planetTypeCount = 0
for key,value in finalData.items():
    if 'goldilock' in value:
        planetTypeCount += 1
print(planetTypeCount)