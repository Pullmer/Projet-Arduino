class Controller:

        def __init__(self, ClientThread t, Labyrinthe labyrinthe, Ecran ecran):
                self.robot = t
                self.labyrinthe = labyrinthe
                self.ecran = ecran
                self.mode = "exploration"

        def refresh(self):
                segments = self.labyrinthe.getSegments()
                self.ecran.afficher(segments)


        def _set_mode(self, v):
                self.mode  =  v

                def _get_mode(self):
                        return self.mode