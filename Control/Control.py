from Model.Camara import ControlCamara
from Model.ReconocimientoFacial import ReconocimientoDeRostros
from Model.ReconocimientoVoz import ReconocimientoVoz
class Control:
    def __init__(self):
        self.camara = ControlCamara()
        self.reconocimiento = ReconocimientoDeRostros()
        self.reconVoz = ReconocimientoVoz()

    def iniciarCamara(self):
        self.camara.iniciar()
    
    def iniciarReconocimiento(self):
        self.reconocimiento.iniciar()
    
    def iniciarReconVoz(self):
        self.reconVoz.iniciarReconocimiento()