class Lobby(object):
    def __init__(self):
        self.game={}
        
        
class S_me4nik(object):
    def __init__(self):
        self.name='Скелет-мечник'
        self.hp=120
        self.mana=0
        self.damage=50
        self.cost=150
        self.type='dead'
        self.fromelectrodmg=0.7
        self.frombiodmg=1.5
        self.fromghostdmg=1.1
        self.fromdeaddmg=1.0
        self.fromfiredmg=1.1
        self.skill=None
        
        
class Pyos(object):
    def __init__(self):
        self.name='Pyos'
        self.hp=200
        self.mana=50
        self.damage=100
        self.cost=130
        self.type='bio'
        self.fromelectrodmg=1.3
        self.frombiodmg=1.0
        self.fromghostdmg=0.8
        self.fromdeaddmg=1.1
        self.fromfiredmg=1.5
        self.skill=None
        
class Phoenix(object):
    def __init__(self):
        self.name='Феникадзе'
        self.hp=1
        self.mana=0
        self.damage=330
        self.cost=200
        self.type='fire'
        self.fromelectrodmg=0.5
        self.frombiodmg=0.7
        self.fromghostdmg=1.5
        self.fromdeaddmg=1.2
        self.fromfiredmg=1.0
        self.skill=None
        
        
class Electromagnit(object):
    def __init__(self):
        self.name='Электромагнитень'
        self.hp=190
        self.mana=100
        self.damage=105
        self.cost=175
        self.type='electro'
        self.fromelectrodmg=1.0
        self.frombiodmg=1.1
        self.fromghostdmg=0.8
        self.fromdeaddmg=1.5
        self.fromfiredmg=0.5
        self.skill=None
        
        
class Manoed(object):
    def __init__(self):
        self.name='Маноед'
        self.hp=85
        self.mana=0
        self.damage=70
        self.cost=165
        self.type='ghost'
        self.fromelectrodmg=1.5
        self.frombiodmg=0.75
        self.fromghostdmg=1.0
        self.fromdeaddmg=0.75
        self.fromfiredmg=0.9
        self.skill=None
        
        
electromagnit=Electromagnit()
phoenix=Phoenix()        
pyos=Pyos()       
s_me4nik=S_me4nik()        
lobby = Lobby()
