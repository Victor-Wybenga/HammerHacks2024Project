import customtkinter as ctk
import tkinter.ttk as ttk
import pathlib, random, pprint
import ParseQuiz, Quiz


class App(ctk.CTk):
    def __init__(self, title: str, size: tuple[int, int]):
        super().__init__()
        self.title(title)
        self.maxsize(*size)
        self.geometry(f"{size[0]}x{size[1]}")
        
        self.button = ctk.CTkButton(
            self,
            text="Click Me!",
            command=self.randomize_button_pos
        )
        self.button.pack()
    
    def randomize_button_pos(self):
        self.button.place(relx=random.random(), rely=random.random(), anchor="center")

def main() -> None:
    # TODO: Implement File Select
    document_path = pathlib.Path(__file__).parent / "examples" / "History Notes.docx"
    quiz_document = ParseQuiz.QuizDocument(document_path)
    parsed_quiz = quiz_document.make_quiz()
    if isinstance(parsed_quiz, ParseQuiz.FormatError):
        return
    
    quiz = Quiz.Quiz(parsed_quiz)
    pprint.pprint(quiz)

    app = App("Prep Quiz Maker", (800, 500))
    app.mainloop()

if __name__ == "__main__":
    main()