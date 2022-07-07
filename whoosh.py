from requests_main import user_work
from gen_maps import MapWork
import config, time, copy,in_google
from datetime import datetime
from defs import *
from work_base import work_base



print("start")
work_map = MapWork()
work_requests = user_work()
work_base = work_base()
time_all_old = time.time()


def go():
    work_map = MapWork()
    all_result_for_google = []

    for i in config.citys_name:
        area_size, result_dt,all_city_borders,ideal_xy = 0, [], [], 0.05
        region_coord = get_coord_centr_city(i)
        region_zones_test = work_requests.get_zones(region_coord["lat"],region_coord["lng"])
        if not region_zones_test:
            all_result_for_google.append(0)
            continue

        for j in region_zones_test["region"]["areas"]:
            if j["type"]=="PERMITTED":
                borders = j["borders"]["coordinates"]
                work_map.print_borders(borders)
                area_size+=in_google.polygion_size_km(borders)
                all_city_borders+=borders

        coord_all = coord_city(all_city_borders)
        work_map.print_rectangle(coord_all)
        try:
            result_dt = get_data_of_scooters(city=i,coord_all=coord_all,work_requests=work_requests)
            print("good city")
        except Exception as ex:
            print(ex)
            print("ebani========================================================================================------------------------------")
            result_dt = []
        saved_scooter = work_base.result_to_base(i,result_dt)

        all_result_for_google.append(len(result_dt))
        in_google.work_and_send(result_dt, area_size, i, saved_scooter)
        time.sleep(5)

        work_map.print_markers(data=result_dt)
        work_map.hot_map(data=result_dt)

    work_map.make_map("index.html")
    all_result_for_google = [datetime.today().strftime("%d.%m.%y %H:%M")]+all_result_for_google
    in_google.in_google_append(all_result_for_google,"len ts(all)")
    print(time.time()-time_all_old)


go()

while True:
    time_now = datetime.today()
    date = int(time_now.strftime("%H"))
  #  if date == 2: go()
    go()
    time.sleep(3600)