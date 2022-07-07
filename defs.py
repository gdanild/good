from pathlib import Path
from yandex_geocoder import Client
import json, copy, time

def append_to_list(old_list, time_list):
    id_old_list = []
    for i in old_list: id_old_list.append(i["id"])
    for i in time_list:
        if  not (i["id"] in id_old_list):
            old_list.append({
                "lat":i["state"]["position"]["point"]["lat"],
                "lng":i["state"]["position"]["point"]["lng"],
                "power":i["battery"]["power"],
                "id":i["id"],
                "code":i["code"]
            })
            id_old_list.append(i["id"])
    return old_list

def coord_city(data_coord):
    min_lng = 1000
    min_lat = 1000
    max_lng = -1000
    max_lat = -1000

    for i in data_coord:
        min_lng = min(min_lng, i["lng"])
        max_lng = max(max_lng, i["lng"])
        min_lat = min(min_lat, i["lat"])
        max_lat = max(max_lat, i["lat"])
    result = {
        "upper":{
            "lat":round(max_lat+0.02,6),
            "lng":round(min_lng-0.02,6)
        },
        "bottom":{
            "lat":round(min_lat-0.02,6),
            "lng":round(max_lng+0.02,6)
        }
    }
    return result

def get_coord_centr_city(city):
    client = Client("d2a4cbcf-1301-4287-a084-84b12ed71dd0")  # поиск яндекса
    credentials_file = Path('save_coord.json')
    with credentials_file.open('r') as cred_file: citys_by_file = dict(json.load(cred_file))
    if not (city in citys_by_file.keys()):
        coordinates_y = client.coordinates("город " + city)
        region_coord = {
            "lat": float(coordinates_y[1]),
            "lng": float(coordinates_y[0])
        }
        citys_by_file.update({city: region_coord})
        with open('save_coord.json', 'w') as cred_file: cred_file.write(json.dumps(citys_by_file))
    region_coord = citys_by_file[city]
    return region_coord

def get_data_of_scooters(city ,coord_all, work_requests):
    sum_bad_r, sum_good_r, ideal_xy,result_dt = 0, 0, 0.05,[]
    region_coord = get_coord_centr_city(city)
    raznos_y = round(coord_all["upper"]["lat"] - coord_all["bottom"]["lat"], 6)
    count_uch_y = int((raznos_y / ideal_xy) + 1)
    work_coord = copy.deepcopy(coord_all)
    work_coord["bottom"]["lat"] = coord_all["upper"]["lat"] - ideal_xy
    work_coord["bottom"]["lng"] = coord_all["upper"]["lng"] + ideal_xy
    region_data = work_requests.regions(region_coord["lat"], region_coord["lng"])

    for k in range(count_uch_y):
        bad_requets, good_requests = 0, 0
        while work_coord["bottom"]["lng"] < coord_all["bottom"]["lng"] + ideal_xy:
            while True:
                for i in range(5):
                    try:
                        result = work_requests.get_scooters(work_coord, region_id=region_data["id"])["devices"]
                        print("good requests")
                        break
                    except Exception as ex:
                        print(ex)
                        time.sleep(15)
                        
                if len(result) < 300:
                    good_requests += 1
                    work_coord["upper"]["lng"] = round(work_coord["bottom"]["lng"], 6) - 0.0001
                    work_coord["bottom"]["lng"] = round(work_coord["upper"]["lng"] + ideal_xy, 6) - 0.0001
                    break
                else:
                    bad_requets += 1
                    work_coord["bottom"]["lng"] -= (work_coord["bottom"]["lng"] - work_coord["upper"]["lng"]) / 2
                    work_coord["bottom"]["lng"] = round(work_coord["bottom"]["lng"], 6)
            result_dt = append_to_list(result_dt, result)
        sum_good_r += good_requests
        sum_bad_r += bad_requets
        work_coord["upper"]["lat"] -= ideal_xy + 0.0001
        work_coord["bottom"]["lat"] -= ideal_xy + 0.0001
        work_coord["upper"]["lng"] = coord_all["upper"]["lng"]
        work_coord["bottom"]["lng"] = coord_all["upper"]["lng"] + ideal_xy
    return result_dt
