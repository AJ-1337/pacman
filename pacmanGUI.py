"""
Graphical user Interface to control and adjust 
parameters of the evolver class.
"""
import Tkinter as tk
import tkMessageBox


window = tk.Tk()
window.title("Pac-Man GUI")
window.geometry("400x400")
pacmanimage=tk.PhotoImage(file="pacman.gif")

def helloTest():
    """
    Testing to check button fuctionality
    """
    tkMessageBox.showinfo( "Testing Alert", "Hello World")
   
def setParameters():
    """
    Allows user to change a value of a function
    """
    tkMessageBox.showinfo( "Testing Alert", "This should set some sort of parameter for the neural network")

# The Pac-Man Background Image
P1 = tk.Label(window, image=pacmanimage).place(relx = 0.5, rely = 0.5, anchor = "center")

#The Fuctionality Buttons
B1 = tk.Button(window, text ="Button 1", command = helloTest)
B1.place(y = 50, x = 50, anchor = "nw")

B2 = tk.Button(window, text ="Button 2", command = setParameters)
B2.place(relx = 0.5, y = 50, anchor = "n")

B3 = tk.Button(window, text ="Button 3", command = setParameters)
B3.place(x = 350, y = 50, anchor = "ne")

B4 = tk.Button(window, text ="Button 4", command = setParameters)
B4.place(x = 50, rely = 0.5, anchor = "w")

B5 = tk.Button(window, text ="Button 5", command = setParameters)
B5.place(relx = 0.5, rely = 0.5, anchor = "center")

B6 = tk.Button(window, text ="Button 6", command = setParameters)
B6.place(x = 350, rely = 0.5, anchor = "e")

B7 = tk.Button(window, text ="Button 7", command = setParameters)
B7.place(x = 50, y = 350 , anchor = "sw")

B8 = tk.Button(window, text ="Button 8", command = setParameters)
B8.place(relx = 0.5 , y = 350, anchor = "s")

B9 = tk.Button(window, text ="Button 9", command = setParameters)
B9.place(x = 350, y = 350, anchor = "se")


window.mainloop()


