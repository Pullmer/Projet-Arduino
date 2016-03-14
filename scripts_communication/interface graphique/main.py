from ecran import *
from labyrinthe import *
from controller import *

labyrinthe = Labyrinthe()
controller = Controller(labyrinthe)
ecran = Ecran(controller)
ecran.mainloop()
