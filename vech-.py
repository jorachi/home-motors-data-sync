import requests
import json
from bs4 import BeautifulSoup
import csv


title = ["vehicle_id","title","description","url","make","model","year","mileage.value","mileage.unit","image[0].url","image[0].tag[0]","transmission","fuel_type","body_style","drivetrain","vin","condition","price","address","exterior_color","sale_price","availability","state_of_vehicle","latitude","longitude"]

with open("vehicle.csv", 'w', newline='', encoding="utf8") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(title)


p_id  = 0
while p_id < 8:
    response = requests.get("https://www.home-motors.com/VehicleSearchResults?limit=24&offset={}".format(str(p_id * 24)))
    soup = BeautifulSoup(response.text, 'lxml')
    all_des = soup.find_all('span', {'class': 'trim'})
    all_tags = soup.find_all('a', {'class': 'primary'})
    all_tags.pop()
    for id, tag in enumerate(all_tags):
        app = []

        description = all_des[id].text

        url = tag.get('href')
        response1 = requests.get(url)
        # soup1 = BeautifulSoup(response1.content)
        # table = soup1.select_one("table.schedule.has-team-logos")
        content = response1.text
        addr_id = content.find('"address":')
        a_txt = content[addr_id + 10:]
        addr_id_2 = a_txt.find("},")
        address = a_txt[:addr_id_2+1]
        address = address.replace("\r\n", "")
        start = content.find("ContextManager")
        f_txt = content[start+20:]
        second = f_txt.find(";")
        s_txt = f_txt[:second-1]
        results = json.loads(s_txt)
        data = results["vehicle"]
        app.append(data["stockNumber"])
        app.append(description)
        app.append(data["category"] + " " +  data["year"] + " " + data["make"] + " " + data["model"])
        app.append(url)
        app.append(data["make"])
        app.append(data["model"])
        app.append(data["year"])
        app.append("ZERO")
        app.append("MI")
        app.append(data["photoUrl"])
        app.append(" ")
        app.append(data["transmission"])
        app.append("GASOLINE")
        app.append("TRUCK")
        app.append("4x2")
        app.append(data["vin"])
        app.append("EXCELLENT")
        app.append(data["price"])
        app.append(address)
        app.append(data["interior"])
        app.append(data["internetPrice"])
        app.append("AVAILABLE")
        app.append(data["category"])
        app.append(results["latitude"])
        app.append(results["longitude"])
        with open("vehicle.csv", 'a', newline='', encoding="utf8") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(app)
    p_id = p_id + 1