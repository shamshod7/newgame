class Lobby(object):
    def __init__(self):
        self.game={}
        
     
class S_me4nik(object):
    def __init__(self):
        self.name='Skilet-Qilichboz'
        self.hp=2
        self.mana=30
        self.damage=1
        self.cost=30
        self.type='dead'
        self.fromelectrodmg=1.0
        self.frombiodmg=2.0
        self.fromghostdmg=1.0
        self.fromdeaddmg=1.0
        self.fromfiredmg=1.0
        self.skill=None
        
        
class Pyos(object):
    def __init__(self):
        self.name='Pyos'
        self.hp=9
        self.mana=30
        self.damage=1
        self.cost=75
        self.type='bio'
        self.fromelectrodmg=1.0
        self.frombiodmg=1.0
        self.fromghostdmg=1.0
        self.fromdeaddmg=1.0
        self.fromfiredmg=2.0
        self.skill=None
        
class Phoenix(object):
    def __init__(self):
        self.name='Feniks'
        self.hp=1
        self.mana=30
        self.damage=6
        self.cost=60
        self.type='fire'
        self.fromelectrodmg=1
        self.frombiodmg=1
        self.fromghostdmg=2
        self.fromdeaddmg=1
        self.fromfiredmg=1
        self.skill=None
        
        
class Electromagnit(object):
    def __init__(self):
        self.name='Elektromagniten'
        self.hp=6
        self.mana=80
        self.damage=3
        self.cost=65
        self.type='electro'
        self.fromelectrodmg=1.0
        self.frombiodmg=1.0
        self.fromghostdmg=1
        self.fromdeaddmg=2
        self.fromfiredmg=1
        self.skill=None
        
        
class Manoed(object):
    def __init__(self):
        self.name='Monoed'
        self.hp=4
        self.mana=30
        self.damage=2
        self.cost=45
        self.type='ghost'
        self.fromelectrodmg=2
        self.frombiodmg=1
        self.fromghostdmg=1.0
        self.fromdeaddmg=1
        self.fromfiredmg=1
        self.skill=None
        
        
class Tiranozavr(object):  
    def __init__(self):
        self.name='Tiranozavr'
        self.hp=7
        self.mana=30
        self.damage=3
        self.cost=100
        self.type='bio'
        self.fromelectrodmg=1
        self.frombiodmg=1.0
        self.fromghostdmg=1
        self.fromdeaddmg=1
        self.fromfiredmg=2
        self.skill=None
        

class S4upakabra(object):
    def __init__(self):
        self.name='Chupakabra'
        self.hp=3
        self.mana=55
        self.damage=4
        self.cost=50
        self.type='dead'
        self.fromelectrodmg=1
        self.frombiodmg=2
        self.fromghostdmg=1
        self.fromdeaddmg=1.0
        self.fromfiredmg=1.0
        self.skill=None
        
        
class Golem(object):
    def __init__(self):
        self.name='Olovli Golem'
        self.hp=13
        self.mana=100
        self.damage=2
        self.cost=150
        self.type='fire'
        self.fromelectrodmg=1
        self.frombiodmg=1
        self.fromghostdmg=2
        self.fromdeaddmg=1
        self.fromfiredmg=1
        self.skill=None



        
        
class Vsadnik(object):
    def __init__(self):
        self.name='Boshsiz CHavandoz'
        self.hp=6
        self.mana=50
        self.damage=3
        self.cost=70
        self.type='ghost'
        self.fromelectrodmg=2
        self.frombiodmg=1
        self.fromghostdmg=1.0
        self.fromdeaddmg=1
        self.fromfiredmg=1
        self.skill=None
        
        
       
class Soulcatcher(object):
    def __init__(self):
        self.name='Qora Ajal'
        self.hp=5
        self.mana=50
        self.damage=3
        self.cost=70
        self.type='dead'
        self.fromelectrodmg=1
        self.frombiodmg=2
        self.fromghostdmg=1
        self.fromdeaddmg=1.0
        self.fromfiredmg=1.0
        self.skill=None
        
        
        
class Zombie(object):
    def __init__(self):
        self.name='Zombi'
        self.hp=7
        self.mana=50
        self.damage=1
        self.cost=65
        self.type='dead'
        self.fromelectrodmg=1
        self.frombiodmg=2
        self.fromghostdmg=1
        self.fromdeaddmg=1.0
        self.fromfiredmg=1.0
        self.skill=None
    
    
    
    
    

        
        
        



zombie=Zombie()
soulcatcher=Soulcatcher()
vsadnik=Vsadnik()
golem=Golem()
s4upakabra=S4upakabra()        
tiranozavr=Tiranozavr()        
manoed=Manoed()        
electromagnit=Electromagnit()
phoenix=Phoenix()        
pyos=Pyos()       
s_me4nik=S_me4nik()        
lobby = Lobby()
