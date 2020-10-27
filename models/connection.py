
"""Modulo para Conectarse a la base de datos"""

import mysql.connector
from mysql.connector import errorcode

class Connection:

	def Connect(self):
		try:
			connection=mysql.connector.connect(
				user='root',
				host='127.0.0.1',
				password='',
				database='sistema') #Nombre de la base de datos
			return connection
	
		except mysql.connector.Error as err:

			if err.errno==errorcode.ER_ACCESS_DENIED_ERROR:
				print('Error User')

			elif err.errno==errorcode.ER_BAD_DB_ERROR:
				print('Error DB')

			else:
				print('Error unknown')

	def CloseConnection(self,connection):
		connection.close()