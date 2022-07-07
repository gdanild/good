import folium, time, config
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from folium import FeatureGroup, LayerControl
class MapWork():
    def __init__(self):
        self.my_map = folium.Map(location=config.start_map_loc, zoom_start=config.start_map_zoom)
        self.marker_whoosh = MarkerCluster().add_to(self.my_map)
        self.feature_whoosh = FeatureGroup(name="Тепловая карта", show=True)
        self.feature_whoosh.add_to(self.my_map)
        LayerControl().add_to(self.my_map)
        self.count_ts = 0

    def print_markers(self, data):
        self.count_ts += len(data)
        for i in data:
            coord = [i["lat"],i["lng"]]
            mark = folium.CircleMarker(radius=9, location=coord, color="#483D8B",fill_opacity=0.94, fill_color="#ff9933")
            mark.add_to(self.marker_whoosh)
    def print_borders(self, border_coord):
        from geojson import MultiPolygon, Feature, FeatureCollection
        data_for_geo_json = []
        for i in border_coord: data_for_geo_json.append((i["lat"], i["lng"]))
        folium.Polygon(data_for_geo_json, fill_color = "yellow" ,  fill_opacity=0.15 , name="test").add_to(self.my_map)

    def print_rectangle(self,coord):
        folium.Rectangle([(coord["upper"]["lat"],coord["upper"]["lng"]),(coord["bottom"]["lat"],coord["bottom"]["lng"])], dash_array='10').add_to(self.my_map)

    def hot_map(self,data):
        hot_map_list = []
        for i in data: hot_map_list.append([i["lat"],i["lng"]])
        HeatMap(hot_map_list, min_opacity=0.1, blur=19, name="Тепловая карта").add_to(self.feature_whoosh)


    def make_map(self, filename):
        title = config.title
        str_for_index = str(time.ctime()) + "<br>" + str(self.count_ts)
        title = title.format(str_for_index)
        self.my_map.get_root().html.add_child(folium.Element(title))
        self.my_map.save(filename)