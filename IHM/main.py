"""       Projet Arduino        """
"""     script de lancement     """

from tkinter import Tk, Frame, BOTH

from mainWindowClass import mainWindow

def main():
  
    root = Tk()
    root.geometry("250x150+300+300")
    app = mainWindow(root)
    root.mainloop()  


""" éxecute la fonction main (seulement si on lance le script main.py et pas si on ne fait que l'importer à partir d'un autre fichier) """
	
if __name__ == '__main__':
    main()  

"""coucou"""