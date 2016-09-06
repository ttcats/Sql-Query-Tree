#!/usr/bin/env python

import psycopg2
import psycopg2.extras



def postgre(host,user,passwd,db,port,sql):
  try:
    conn = psycopg2.connect(dbname=db,user=user,password=passwd,host=host,port=port,)
    con = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    #con = conn.cursor()
    con.execute(sql)
    #print con.fetchall()
    return con.fetchall()
    conn.close()
  except Exception, e:
    #print e
    return e


if __name__ == "__main__":
  #sql = "SELECT * FROM company;"
  #sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
  sql = "select * from company;"
  postgre("192.168.1.2","admin","123","omdb",5432,sql)

