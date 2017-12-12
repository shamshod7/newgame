class Lobby(object):
    def __init__(self):
        self.game={}
        
        
class S_me4nik(object):
    def __init__(self):
        self.name='Скелет-мечник'
        self.hp=65
        self.mana=0
        self.damage=55
        self.cost=90
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
        self.hp=400
        self.mana=0
        self.damage=0
        self.cost=100
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
        self.hp=25
        self.mana=0
        self.damage=350
        self.cost=130
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
        self.hp=180
        self.mana=80
        self.damage=70
        self.cost=145
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
        self.hp=135
        self.mana=0
        self.damage=40
        self.cost=125
        self.type='ghost'
        self.fromelectrodmg=1.5
        self.frombiodmg=0.75
        self.fromghostdmg=1.0
        self.fromdeaddmg=0.75
        self.fromfiredmg=0.9
        self.skill=None
        
manoed=Manoed()        
electromagnit=Electromagnit()
phoenix=Phoenix()        
pyos=Pyos()       
s_me4nik=S_me4nik()        
lobby = Lobby()
