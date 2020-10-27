
from .connection import Connection

class Data(Connection):

    # --Sección de usuario y contraseña
    
    def ValidarContra(self,password): #Validar contraseña actual para el cambio de contraseña nueva
        cnx=self.Connect()
        Cursor=cnx.cursor()
        Cursor.execute("SELECT * FROM login WHERE user='admin' AND password = %(password)s",
             {'password': password})
        for i in Cursor:
            self.CloseConnection(cnx)
            return True
        self.CloseConnection(cnx)
        return False
    
    def ActualizarContra(self,password): #Cambiar contraseña de usuario
        cnx=self.Connect()
        Cursor=cnx.cursor()
        Cursor.execute("UPDATE login SET password='{}' WHERE user='admin'".format(password))
        cnx.commit()
        self.CloseConnection(cnx)
    
    def ConsultarLogin(self,user,password): #Consultar Usuario y contraseña de la base de datos
        cnx=self.Connect()
        Cursor=cnx.cursor()
        Cursor.execute("SELECT * FROM login WHERE user= %(user)s AND password= %(password)s", 
            {'password': password,'user': user})
        for i in Cursor:
            self.CloseConnection(cnx)
            return True
        self.CloseConnection(cnx)
        return False


    #---SECCIÓN CLIENTE

    def RegistrarCliente(self, name, ip, direc, phone, amount, megas, date):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL add_client ('{}','{}','{}','{}','{}','{}','{}')".format(
            name, ip, direc, phone, amount, megas, date))
        cnx.commit()
        self.CloseConnection(cnx)

    def ConsultarCliente(self, view, order):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL consult_client ('{}','{}')".format(view,order))
        Lista = Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista
    
    def CargarCliente(self, id): #Obtener el cliente determinado
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL upload_client ('{}')".format(id))
        Lista = Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista

    def ActualizarCliente(self, id, AN, IP, Direc, Telef, Monto, Megas, FI):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL edit_client ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
            id, AN, IP, Direc, Telef, Monto, Megas, FI))
        cnx.commit()
        self.CloseConnection(cnx)
    
    def BuscarCliente(self,view,name):
        cnx=self.Connect()
        Cursor=cnx.cursor()
        Cursor.execute("CALL search_client ('{}','{}%')".format(view,name))
        Lista=Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista
    
    def EliminarCliente(self, id):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL delete_client ('{}')".format(id))
        cnx.commit()
        self.CloseConnection(cnx)
    
    def ActualizarEstado(self, id, status, date): #Actualizar estado del cliete ('activo','inactivo')
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL edit_status ('{}','{}','{}')".format(id, status, date))
        cnx.commit()
        self.CloseConnection(cnx)
    
    def UltimoCliente(self): #Obtener el ultimo cliente registrado
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL last_client ()")
        Lista = Cursor.fetchall()
        for dato in Lista:
            client_id = dato[0]
        self.CloseConnection(cnx)
        return client_id

    #----SECCIÓN HISTORIAL

    def RegistrarHistorial(self, description, date, payment, id):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL add_history ('{}','{}','{}','{}')".format(
            description, date, payment, id))
        cnx.commit()
        self.CloseConnection(cnx)
    
    def ConsultarHistorial(self, id):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL consult_history ('{}')".format(id))
        Lista = Cursor.fetchall()
        self.CloseConnection(cnx)
        return Lista
    
    def ActualizarHistorial(self, id, description, date, payment):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL edit_history ('{}','{}','{}','{}')".format(
            id, description, date, payment))
        cnx.commit()
        self.CloseConnection(cnx)
    
    def EliminarHistorial(self, id):
        cnx = self.Connect()
        Cursor = cnx.cursor()
        Cursor.execute("CALL delete_history ('{}')".format(id))
        cnx.commit()
        self.CloseConnection(cnx)
