"""
Creates a sqlite3 database in memory
"""

import sqlite3
from employee import Employee


connection = sqlite3.connect(':memory:')
cursor = connection.cursor()


cursor.execute(" CREATE TABLE IF NOT EXISTS employees(first text, last text, pay integer)")


def insert_employee(emp):
	with connection:
		cursor.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


def get_emps_by_name(last_name):	
	cursor.execute("SELECT * FROM employees WHERE last=:last", {'last' : last_name})
	fetch = cursor.fetchall()
	fetch_dict = [{'first': row[0], 'last': row[1], 'pay': row[2]} for row in fetch]

	return fetch_dict


def update_pay(emp, pay):
	with connection:
		cursor.execute("UPDATE employees SET pay=:pay WHERE first=:first AND last=:last", { 'pay': pay, 'first': emp.first, 'last': emp.last})		
	connection.commit()


def remove_emp(emp):
	with connection:
		cursor.execute("DELETE FROM employees WHERE first=:first AND last=:last", {'first': emp.first, 'last': emp.last})
	connection.commit()


""" EXAMPLES
hernan = Employee("Hernan", "Llano", 72000)   
natalia = Employee("Natalia", "Velasquez", 25000)
francisco = Employee("Francisco", "Velasquez", 25000)


insert_employee(hernan)
insert_employee(natalia)
insert_employee(francisco)




print (get_emps_by_name("Velasquez"))

update_pay(natalia, 80000)
remove_emp(francisco)

print (get_emps_by_name("Velasquez"))


connection.commit()
connection.close()
"""
