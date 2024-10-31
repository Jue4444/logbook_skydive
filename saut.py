# saut.py

class Saut:
    def __init__(self, date, lieu, avion, hauteur, voile, type_saut):
        self.date = date
        self.lieu = lieu
        self.avion = avion
        self.hauteur = hauteur
        self.voile = voile
        self.type_saut = type_saut

    def to_dict(self):
        return {
            "date": self.date,
            "lieu": self.lieu,
            "avion": self.avion,
            "hauteur": self.hauteur,
            "voile": self.voile,
            "type_saut": self.type_saut,
        }