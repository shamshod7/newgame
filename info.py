class Lobby(object):
    def __init__(self):
        self.game={}
        
        
class S_me4nik(object):
    def __init__(self):
        self.name='Скелет-мечник'
        self.hp=120
        self.mana=0
        self.damage=50
        self.cost=100
        self.type='dead'
        self.fromelectrodmg=0.8
        self.frombiodmg=0.8
        self.fromghostdmg=1.1
        self.fromdeaddmg=0.8
        
        
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
        

        
        

        
pyos=Pyos()       
s_me4nik=S_me4nik()        
lobby = Lobby()
