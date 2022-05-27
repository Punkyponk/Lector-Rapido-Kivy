import json
import pymysql.cursors
import datetime
from reportlab.pdfgen import canvas
#
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from ColorLabel import ColorLabel
from kivy.uix.boxlayout import BoxLayout

class LectorRapidoKivy(Screen):
    def __init__(self,**kwargs):
        #Llamar al constructor de la clase base (App)
        super().__init__(**kwargs)
        #Conexión a la Base de Datos
        self.iniciarDB()
        #Número total de "páginas"
        self.total_pags()
        #Contadores de pulsación para botones
        self.cont_regresar = 0
        self.cont_continuar = 0
        #Contador de "página"
        self.cont_pagina = 1
    
    def build(self,SM = None):
        self.SM = SM
        self.box_principal = BoxLayout(orientation='vertical',spacing=11)
        #Modificar "cont_pagina"
        MiCursor = self.connection.cursor()
            #El registro más actual
        SQL = """
            SELECT * FROM contador
            WHERE id_contador = (
                SELECT MAX(id_contador) FROM contador
            )
        """
        MiCursor.execute(SQL)
        resultado = MiCursor.fetchone()
        if resultado:   #Diferente de None 
            self.cont_pagina = int(resultado[1])
        else:   #NoneType
            self.cont_pagina = 1
        MiCursor.close()
        #1. Etiqueta
        self.lbl_lector = ColorLabel(text = "")
        if self.leer_linea() != None:
            self.lbl_lector.text = self.leer_linea()
            #Mods
        self.lbl_lector.background_color = [1,165/255,0,0.875]
        self.lbl_lector.size_hint =(1,3.25)   #Tamaño en el layout (en 100%)
        self.lbl_lector.text_size = (360,None)   #Pixeles delimitadores
        self.lbl_lector.font_size = 25   #Tamaño de letra
        self.lbl_lector.color = (1,1,1)   #Color de letra
        self.lbl_lector.bold = True
        self.lbl_lector.italic = True
        #2. Grid
        self.box_accion = BoxLayout(orientation='horizontal',spacing=10)
            #Widgets
        self.btn_left = Button(text='Regresar')
        self.btn_center = Button(text='Actualizar Reporte')
        self.btn_right = Button(text='Continuar')
            #Mods
        self.btn_left.background_color = [238/255,250/255,0,0.95]
        self.btn_left.font_size = 28
        self.btn_left.bold = True
        self.btn_left.italic = True
        self.btn_center.background_color = [238/255,250/255,0,0.95]
        self.btn_center.font_size = 28
        self.btn_center.bold = True
        self.btn_center.italic = True
        self.btn_right.background_color = [238/255,250/255,0,0.95]
        self.btn_right.font_size = 28
        self.btn_right.bold = True
        self.btn_right.italic = True
                #Eventos/Métodos
        self.status_btn()
        self.btn_left.bind(on_press=self.btn_left_press)
        self.btn_center.bind(on_press=self.btn_center_press)
        self.btn_right.bind(on_press=self.btn_right_press)
        #Agregar
        self.box_principal.add_widget(self.lbl_lector)
        self.box_accion.add_widget(self.btn_left)
        self.box_accion.add_widget(self.btn_center)
        self.box_accion.add_widget(self.btn_right)
        self.box_principal.add_widget(self.box_accion)
        self.add_widget(self.box_principal)
        return self
    
    """ Método que lee un registro específico (linea) de la tabla
        "libro", de acuerdo con el atributo "cont_pagina"
        -->Devuelve una cadena (str)
    """
    def leer_linea(self):
        resultado = ""
        if self.connection:
            MiCursor = self.connection.cursor()
            SQL = """
                SELECT linea FROM libro
                WHERE num_linea = %s
            """
            MiCursor.execute(SQL,self.cont_pagina)
            #De lista a cadena con [] y str()
            resultado = MiCursor.fetchone()
            if resultado != None:
                resultado = str(resultado[0])
            MiCursor.close()
        else:
            print("ERROR: No se puedo realizar una conexión a la BD")
        return resultado
    
    """ Método que determina si alguno de los botones de "Regresar" o
        "Continuar" debe ser desactivado
    """
    def status_btn(self):
        self.btn_left.disabled = False
        self.btn_right.disabled = False
        #Primera página
        if self.cont_pagina == 1:
            self.btn_left.disabled = True
        #Última página
        elif self.cont_pagina == self.total_paginas:
            self.btn_right.disabled = True
    
    """ Método para respuesta de eventos que modifica la etiqueta con
        lineas obtenidas de la tabla "libro" de la Base de Datos,
        disminuye el contador "cont_pagina" y aumenta el "cont_regresar"
    """
    def btn_left_press(self,obj):
        self.cont_regresar += 1 
        self.cont_pagina -= 1
        #Modificar texto a mostrar
        if self.leer_linea() != None:
            self.lbl_lector.text = self.leer_linea()
        self.status_btn()
    
    """ Método para respuesta de eventos que añade registros en la tabla
        "contador" de la Base de Datos, crea/actualiza un reporte en
        .pdf y modifica el archivo de configuración .json
    """
    def btn_center_press(self,obj):
        if self.connection:
            #Fecha y hora del fin de la lectura
            fin_lectura = datetime.datetime.now()
            #El registro más actual
            MiCursor = self.connection.cursor()
            SQL = """
                SELECT * FROM contador
                WHERE id_contador = (
                    SELECT MAX(id_contador) FROM contador
                )
            """
            MiCursor.execute(SQL)
            num_registro = MiCursor.fetchone()
            if num_registro == None:
                num_registro = 0
            else:
                num_registro = int(num_registro[0])
            #Añadir el nuevo registro
            SQL = """
                INSERT INTO contador
                VALUES (%s,%s,%s,%s,%s)
            """
            MiCursor.execute(SQL,
                [num_registro+1,self.cont_pagina,self.cont_regresar,
                self.cont_continuar,fin_lectura]
            )
            self.connection.commit()
            #Crear el reporte en .pdf [612, 792]
            reporte = canvas.Canvas(f"Reporte@{self.Conf['NOM_LIBRO']}.pdf")
            SQL = 'SELECT * FROM contador'
            MiCursor.execute(SQL)
            #Ciclo que, cada página, dibuja 4 casillas con datos
            casilla = 0
            while True:
                #Si nos quedamos sin registros
                datos = MiCursor.fetchone()
                if datos == None:
                    if casilla != 0:
                        reporte.showPage()
                    break
                #Casilla con datos
                reporte.rect(100,582-160*casilla,412,110,stroke=1,fill=0)
                reporte.drawString(500,677-160*casilla,str(datos[0]))
                reporte.drawString(115,677-160*casilla,
                    "Página a retomar: "+str(datos[1])
                )
                reporte.drawString(115,657-160*casilla,
                    "Pulsaciones del botón \"Regresar\": "+str(datos[2])
                )
                reporte.drawString(115,637-160*casilla,
                    "Pulsaciones del botón \"Continuar\": "+str(datos[3])
                )
                reporte.drawString(115,617-160*casilla,
                    "Fecha y hora del fin de lectura: "+str(datos[4])
                )
                #Si llegamos a la última casilla
                if casilla == 3:
                    casilla = -1
                    reporte.showPage()
                casilla += 1
            reporte.save()
            MiCursor.close()
        else:
            print("ERROR: No se puedo realizar una conexión a la BD")
    
    """ Método para respuesta de eventos que modifica la etiqueta con
        lineas obtenidas de la tabla "libro" de la Base de Datos y,
        aumenta los contadores de "cont_pagina" y "cont_continuar"
    """
    def btn_right_press(self,obj):
        self.cont_continuar += 1
        self.cont_pagina += 1
        #Modificar texto a mostrar
        if self.leer_linea() != None:
            self.lbl_lector.text = self.leer_linea()
        self.status_btn()
    
    """ Método que calcula el número total de registros en la tabla
        "libro" de la Base de Datos y con ello inicializa un atributo
    """
    def total_pags(self):
        if self.connection:
            MiCursor = self.connection.cursor()
            SQL = 'SELECT COUNT(linea) FROM libro'
            MiCursor.execute(SQL)
            #De lista a entero con [] y int()
            self.total_paginas = int(MiCursor.fetchone()[0])
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
