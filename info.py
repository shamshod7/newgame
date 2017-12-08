class Lobby(object):
    def __init__(self):
        self.game={}
        
        
class S_me4nik(object):
    def __init__(self):
        self.name='Скелет-мечник'
        self.hp=120
        self.mana=0
        self.damage=50
        self.cost=25
        self.type='dead'
        self.fromelectrodmg=0.8
        self.frombiodmg=0.8
        self.fromghostdmg=1.1
        self.fromdeaddmg=0.8
        self.fromfiredmg=1.1
        
        
class Pyos(object):
    def __init__(self):
        self.name='Pyos'
        self.hp=200
        self.mana=50
        self.damage=100
        self.cost=175
        self.type='bio'
        self.fromelectrodmg=1.2
        self.frombiodmg=1.0
        self.fromghostdmg=0.85
        self.fromdeaddmg=1.0
        self.fromfiredmg=1.0
        
class Phoenix(object):
    def __init__(self):
        self.name='Фениксадзе'
        self.hp=1
        self.mana=0
        self.damage=330
        self.cost=200
        self.type='fire'
        self.fromelectrodmg=1.0
        self.frombiodmg=1.0
        self.fromghostdmg=1.0
        self.fromdeaddmg=1.0
        self.fromfiredmg=1.0
        
        
class Electromagnit(object):
    def __init__(self):
        self.name='Электромагнитень'
        self.hp=200
        self.mana=100
        self.damage=125
        self.cost=200
        self.type='electro'
        self.fromelectrodmg=1.0
        self.frombiodmg=1.0
        self.fromghostdmg=1.2
        self.fromdeaddmg=1.0
        self.fromfiredmg=1.0
        

        
        
electromagnit=Electromagnit()
phoenix=Phoenix()        
pyos=Pyos()       
s_me4nik=S_me4nik()        
lobby = Lobby()
