import csv
import pymysql as MySQLdb

mydb = MySQLdb.connect(host='141.94.37.252',
    user='itzmyweb_manager',
    passwd='4t&6e7Ky5',
    db='manager')
cursor = mydb.cursor()

csv_data = csv.reader(open('employe.csv'), delimiter=';')
for row in csv_data:
    cursor.execute('INSERT INTO employee(firstname, lastname, username, password, email, adresse, city, country) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', row)

#close the connection to the database.
mydb.commit()
cursor.close()
print("Done")