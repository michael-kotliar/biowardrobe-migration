#! /usr/bin/env python3
import MySQLdb
import logging
from sqlparse import split
from contextlib import closing
from biowardrobe_migration.utils.files import norm_path, open_file


logger = logging.getLogger(__name__)


class Connect:

    def __init__(self, config_file):
        self.config = [line for line in open_file(config_file) if not line.startswith("#")]

    def get_conn(self):
        conn_config = {
            "host": self.config[0],
            "user": self.config[1],
            "passwd": self.config[2],
            "db": self.config[3],
            "port": int(self.config[4]),
            "cursorclass": MySQLdb.cursors.DictCursor
        }
        conn = MySQLdb.connect(**conn_config)
        return conn

    def execute(self, sql, option=None):
        with closing(self.get_conn()) as connection:
            with closing(connection.cursor()) as cursor:
                for sql_segment in split(sql):
                    if sql_segment:
                        cursor.execute(sql_segment)
                        connection.commit()
                if option == 1:
                    return cursor.fetchone()
                elif option == 2:
                    return cursor.fetchall()
                else:
                    return None

    def fetchone(self, sql):
        return self.execute(sql,1)

    def fetchall(self, sql):
        return self.execute(sql,2)

    def get_settings_raw(self):
        return {row['key']: row['value'] for row in self.fetchall("SELECT * FROM settings")}

    def get_settings_data(self):
        settings = self.get_settings_raw()
        settings_data = {
            "home":     norm_path(settings['wardrobe']),
            "raw_data": norm_path("/".join((settings['wardrobe'], settings['preliminary']))),
            "anl_data": norm_path("/".join((settings['wardrobe'], settings['advanced']))),
            "indices":  norm_path("/".join((settings['wardrobe'], settings['indices']))),
            "upload":   norm_path("/".join((settings['wardrobe'], settings['upload']))),
            "bin":      norm_path("/".join((settings['wardrobe'], settings['bin']))),
            "temp":     norm_path("/".join((settings['wardrobe'], settings['temp']))),
            "experimentsdb": settings['experimentsdb'],
            "airflowdb":     settings['airflowdb'],
            "threads":       settings['maxthreads']
        }
        return settings_data

    def apply_patch(self, filename):
        logger.debug(f"Apply SQL patch: {filename}")
        with open(filename) as patch_stream:
            self.execute(patch_stream.read())