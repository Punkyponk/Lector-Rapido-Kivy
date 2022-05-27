import json
import pymysql.cursors
#
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from ColorLabel import ColorLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class OpcionesKivy(Screen):
    def __init__(self,**kwargs):
        #Llamar al constructor de la clase base (App)
        super().__init__(**kwargs)
        #Conexión a la Base de Datos
        self.iniciarDB()
        
    def build(self,SM = None):
        self.SM = SM
        self.box_principal = BoxLayout(orientation='vertical',spacing=11)
        #1. Etiqueta
        self.lbl_opc = ColorLabel(text="Ingrese la ruta del libro")
        #2. Caja de texto
        self.txi_ruta = TextInput(text="",multiline=False)
        #3. Botón
        self.btn1 = Button(text="Cargar libro")
        self.btn1.bind(on_press=self.btn1_press)
        #4. Botón
        self.btn2 = Button(text="Abrir lector rapido")
        self.btn2.bind(on_press=self.btn2_press)
        #Agregar
        self.box_principal.add_widget(self.lbl_opc)
        self.box_principal.add_widget(self.txi_ruta)
        self.box_principal.add_widget(self.btn1)
        self.box_principal.add_widget(self.btn2)
        self.add_widget(self.box_principal)
        return self
        
    """ Método para respuesta de eventos que renueva los registros de
        las tablas de la Base de Datos de acuerdo un nuevo libro en
        .txt y modifica el archivo de configuración .json
    """
    def btn1_press(self,obj):
        if self.connection:
            MiCursor = self.connection.cursor()
            #Se eliminan todos los registros anteriores de ambas tablas
            SQL = 'DELETE FROM contador'
            MiCursor.execute(SQL)
            SQL = 'DELETE FROM libro'
            MiCursor.execute(SQL)
            #Se ignora el atributo clave auto-incrementable con "null"
            SQL = """
                INSERT INTO libro
                VALUES (null,%s)
            """
            #Añadir lineas del libro en .txt como registros en "libro"
            with open(self.txi_ruta.text) as libro_txt:
                for linea in libro_txt:
                    #Se ignoran las líneas vacías
                    if (linea != "") or (linea != " "):
                        MiCursor.execute(SQL,linea)
            #Realizar cambios
            self.connection.commit()
            self.lbl_opc.text = "Se ha cargado exitosamente el libro a la BD"
            MiCursor.close()
            #Para el reporte de un nuevo libro, guardar el titulo
            with open("db_lr.json", 'w') as jsonfile:
                self.Conf['NOM_LIBRO'] = self.txi_ruta.text[
                    0:self.txi_ruta.text.find(".txt")
                ]
                json.dump(self.Conf, jsonfile)
        else:
            print("ERROR: No se puedo realizar una conexión a la BD")
            
    """ Método para respuesta de eventos que determina si es posible 
        avanzar a la ventana del "Lector Rápido"
    """
    def btn2_press(self,obj):
        if self.connection:
            MiCursor = self.connection.cursor()
            SQL = 'SELECT * FROM libro'
            MiCursor.execute(SQL)
            #Si la tabla "libro" NO está vacía, se cambia de ventana
            #De otro modo, cambiar el texto de la etiqueta
            resultado = MiCursor.fetchone()
            if resultado:   #Valor diferente de None
                self.SM.current = "Lector Rapido"
            else:   #NoneType
                self.lbl_opc.text = "No se encuentra ningun libro en la BD"
            MiCursor.close()
        else:
            print("ERROR: No se puedo realizar una conexión a la BD")
        
    """ Método que realiza la conexión a la Base de Datos, por medio de
        un Diccionario de Python, inicializado a partir de un archivo de
        configuración .json
    """  
    def iniciarDB(self):
        self.Conf = None
        with open("db_lr.json") as jsonfile:
            self.Conf = json.load(jsonfile)
        self.connection = pymysql.connect(
            host=self.Conf['HOST'], user=self.Conf['DBUSER'],
            password=self.Conf['DBPASS'], database=self.Conf['DBNAME'],
            charset='utf8mb4', port=self.Conf['PORT']
        ) 
    
if __name__ == '__main__':
    pass
