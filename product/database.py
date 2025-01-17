import sqlite3
import datetime
from sqlite3 import Error
from datetime import datetime


class Database:

    def __init__(self):
        """
        Creates a connection to the database and creates the history table if it doesn't already exist
        :param self:
        :return:
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(r"database.db") #creates the connection to the sqlite3 database file
        except Error as e:
            print(e)

        if self.conn is not None:
            # create histroy table
            self.create_table()
        else:
            print("Error! cannot create the database connection.")


    def create_table(self):
        """ create a table from the create_table_sql statement if it doesn't already exist
        :param self: 
        :return:
        """
        #sql statement
        sql_create_history_table = """ CREATE TABLE IF NOT EXISTS history (  
                                        id integer PRIMARY KEY,
                                        download_speed float NOT NULL,
                                        upload_speed float NOT NULL,
                                        record_datetime text
                                    ); """
        try:
            c = self.conn.cursor()
            c.execute(sql_create_history_table)
        except Error as e:
            print(e)

    def add_record(self, download, upload,cur_datetime):
        """
        Create a new record into the history table
        :param self: 
        :param download: download speed
        :param upload: upload speed
        :return: 
        """
         #gets current day and time
        cur_datetime = cur_datetime.strftime("%b-%d-%Y %H:%M:%S") #formats it into a string

        record = (download, upload, cur_datetime)

        sql = ''' INSERT INTO history(download_speed,upload_speed,record_datetime)
                  VALUES(?,?,?) '''

        cur = self.conn.cursor()
        cur.execute(sql, record)
        self.conn.commit()

    def delete_all_records(self):
        """
        Delete all rows in the history table
        :param self: 
        :return:
        """
        sql = 'DELETE FROM history'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def select_all_record(self):
        """
        Query all rows in the history table
        :param self:
        :return: array of rows of the table
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM history")

        rows = cur.fetchall()
        return rows


