from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from OpcionesKivy import OpcionesKivy
from LectorRapidoKivy import LectorRapidoKivy

class InicioKivy(App):
    def build(self):
        MPantalla = ScreenManager()
        #Pantalla 1
        P1 = OpcionesKivy(name = "Opciones")
        P1.build(SM = MPantalla)
        #Pantalla 2
        P2 = LectorRapidoKivy(name = "Lector Rapido")
        P2.build(SM = MPantalla)
        #Agregar
        MPantalla.add_widget(P1)
        MPantalla.add_widget(P2)
        MPantalla.current = "Opciones"
        return MPantalla
        
if __name__ == '__main__':
	Miapp = InicioKivy()
	Miapp.run()
