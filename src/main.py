import customtkinter as ctk
import tkinter.ttk as ttk
import typing
import random

def entry(main: typing.Callable[..., None]) -> None:
    if __name__ == '__main__':
        main()

class App(ctk.CTk):
    def __init__(self, title: str, size: tuple[int, int]):
        super().__init__()
        self.title(title)
        self.geometry(f"600x600")
        
        self.button = ctk.CTkButton(
            self,
            text="Click Me!",
            command=self.randomize_button_pos
        )
        self.button.place(relx=0.5,rely=0.5)
    
    def randomize_button_pos(self):
        self.button.place(relx=random.random(),rely=random.random())
        

@entry
def main() -> None: 
    app = App("Calculator", (240, 320))
    app.mainloop()