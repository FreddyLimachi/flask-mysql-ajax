
from connection import *


class Data(Connection):

    def RegistrarCliente(self, name, ip, direc, phone, amount, megas, date):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL add_client ('{}','{}','{}','{}','{}','{}','{}')".format(
            name, ip, direc, phone, amount, megas, date))
        cnx.commit()
        self.CloseConnection(cnx)

    def ConsultarCliente(self):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL consult_client ('{}')".format('all'))
        Lista = Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista

    def ActualizarCliente(self, N, AN, IP, Direc, Telef, Monto, Megas, FI):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL edit_client ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
            N, AN, IP, Direc, Telef, Monto, Megas, FI))
        cnx.commit()
        self.CloseConnection(cnx)

    def ActualizarEstado(self, N, Estado):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL edit_status ('{}','{}')".format(N, Estado))
        cnx.commit()
        self.CloseConnection(cnx)

    def RegistrarPagoMes(self, Age, ID):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL add_payment ('{}','{}')".format(Age, ID))
        cnx.commit()
        self.CloseConnection(cnx)

    def ActualizarPagoMes(self, ID, Age, Mes, Pago, Fecha):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL edit_payment ('{}','{}','{}','{}','{}')".format(
            ID, Age, Mes, Pago, Fecha))
        cnx.commit()
        self.CloseConnection(cnx)

    def RegistrarHistorial(self, Accion, Fecha, Monto, ID):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL add_history ('{}','{}','{}','{}')".format(
            Accion, Fecha, Monto, ID))
        cnx.commit()
        self.CloseConnection(cnx)

    def ActualizarHistorial(self, N, Accion, Fecha, Monto):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL edit_history ('{}','{}','{}','{}')".format(
            N, Accion, Fecha, Monto))
        cnx.commit()
        self.CloseConnection(cnx)

    def ActualizarFIH(self, ID, Accion, Fecha):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL edit_fih ('{}','{}','{}')".format(ID, Accion, Fecha))
        cnx.commit()
        self.CloseConnection(cnx)

    def ConsultarHistorial(self, ID):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL consult_history ('{}')".format(ID))
        Lista = Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista

    def CargarHistorial(self, N):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL upload_history ('{}')".format(N))
        Lista = Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista

    def EliminarHistorial(self, N):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL delete_history ('{}')".format(N))
        cnx.commit()
        self.CloseConnection(cnx)

    def EliminarPagoMes(self, ID):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL delete_payment ('{}')".format(ID))
        cnx.commit()
        self.CloseConnection(cnx)

    def CargarPagoMes(self, ID, Age, Mes):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL upload_payment ('{}','{}','{}')".format(ID, Age, Mes))
        Lista = Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista

    def Upload_xname(self, name):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL upload_xname ('{}')".format(name))
        Lista = Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista

    def EliminarCliente(self, N):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL delete_client ('{}')".format(N))
        cnx.commit()
        self.CloseConnection(cnx)

    def CargarCliente(self, N):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL upload_client ('{}')".format(N))
        Lista = Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista

    # Obtener el numero de clientes registrados en la base de datos
    def RelacionarCliente(self):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL rel_client ()")
        Lista = Cursor.fetchall()
        Arreglo = []
        for dato in Lista:
            Arreglo = dato[0]
        self.CloseConnection(cnx)
        return Arreglo
