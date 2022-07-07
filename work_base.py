import sqlite3
from datetime import datetime
class work_base():
    def __init__(self):
        self.conn = sqlite3.connect("scooter_id.db", check_same_thread=False)  # или :memory: чтобы сохранить в RAM
        self.cursor = self.conn.cursor()

    def write_data(self,table, id, code):
        time_now = datetime.today().strftime("%d.%m.%y %H:%M")
        self.cursor.execute("INSERT INTO " + table + " VALUES (?, ?)", (id, code))
        self.conn.commit()

    def create_table(self, name):
        string = "(id text, code text)"
        cmd = "CREATE TABLE " + name + string
        self.cursor.execute(cmd)
        self.conn.commit()

    def get_data_by_city(self, table):
        self.cursor.execute("SELECT id from "+table)
        data = []
        for i in self.cursor.fetchall(): data.append(i[0])
        return data

    def get_tables(self):

        self.cursor.execute('SELECT name from sqlite_master where type= "table"')
        tables = []
        for i in self.cursor.fetchall(): tables.append(i[0])
        return tables

    def result_to_base(self,name ,result):
        table = name.replace(" ", "_").replace("-","_")
        if not table in self.get_tables(): self.create_table(table)
        data = self.get_data_by_city(table)
        for i in result:
            if not i["id"] in data: self.write_data(table,i["id"],i["code"])
        return len(self.get_data_by_city(table))
