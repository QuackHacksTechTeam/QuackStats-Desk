
from gui.app import App 
from controller.controller import Controller 

def main(): 
    controller = Controller()
    app = App(controller)
    app.mainloop()

if __name__ == "__main__": 
    main()

