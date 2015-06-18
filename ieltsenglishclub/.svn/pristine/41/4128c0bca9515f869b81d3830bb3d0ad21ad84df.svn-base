# -*- coding: utf-8 -*-
import MySQLdb
import sae.const


class SinaBlogDatabase:
    
    def __init__(self):
        self.conn = MySQLdb.connect(host=sae.const.MYSQL_HOST,
                                    port=int(sae.const.MYSQL_PORT),
                                    user=sae.const.MYSQL_USER,
                                    passwd=sae.const.MYSQL_PASS,
                                    db=sae.const.MYSQL_DB,
                                    charset='utf8')
        
    def close(self):
        self.conn.close()

    def execute(self, op, paras=None):
        c = self.conn.cursor()
        if not paras:
            c.execute(op)
        else:
            c.execute(op, paras)
        self.conn.commit()
        return c.fetchall()