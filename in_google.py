import gspread
from datetime import datetime
from shapely.geometry import Polygon
key = "1GlB8cq0-vnlpMOhUptJxGdDb2IBEEQC4tbcvfNiEYx4"
def in_google_append(row_g, name):
    global key
    gc = gspread.service_account(filename="credentials_google.json")
    sh = gc.open_by_key(key)
    worksheet = sh.worksheet(name)
    worksheet.resize(100)
    worksheet.insert_row(row_g, index=2)

def get_value(name):
    gc = gspread.service_account(filename="credentials_google.json")
    sh = gc.open_by_key(key)
    worksheet = sh.worksheet(name)
    values_list = worksheet.row_values(2)
    return values_list

def polygion_size_km(data):
    for_poligion = []
    for i in data:
        for_poligion.append((i["lng"],i["lat"]))
    polygon = Polygon(for_poligion)
    return round(polygon.area*7840,2)

def work_and_send(row_g, area_size, name, saved_scooter):
    if len(row_g)==0:
        in_google_append([datetime.today().strftime("%d.%m.%y %H:%M"),1,1,1,1,1,1,1,1,1,1],name)
        return True
    sum_percent = 0
    min_percent = 100
    for i in row_g:
        if i["power"]<min_percent and i["power"]!=0:
            min_percent=i["power"]
        sum_percent+=i["power"]
    len_ts = len(row_g)
    sr_percent = round(sum_percent/len_ts,1)
    old_value = get_value(name)

  #  in_google_append([datetime.today().strftime("%d.%m.%y %H:%M"),
   #                   len(row_g),1,
    ##                 sr_percent,1,
      #                round(len(row_g)/area_size,2),1],
       #              name)



    in_google_append([datetime.today().strftime("%d.%m.%y %H:%M"),
                      len(row_g),str(round((len(row_g)/int(old_value[1])-1)*100))+"%",
                      min_percent,str(round((min_percent/int(old_value[3])-1)*100))+"%",
                      sr_percent,str(round((sr_percent/float(old_value[5].replace(",","."))-1)*100))+"%",
                      round(len(row_g)/area_size,2),str(round((round(len(row_g)/area_size,2)/float(old_value[7].replace(",","."))-1)*100))+"%",
                      saved_scooter, str(round((saved_scooter/int(old_value[9])-1)*100))+"%"],
                     name)