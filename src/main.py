import customtkinter as ctk
import tkinter.ttk as ttk
import pathlib, random, pprint
import ParseQuiz, Quiz
import frozendict

class StartScreen(ttk.Frame):
    ...
    def __init__(self, master):
        self.title = ttk.Label(
            self, 
            text="Help! I have a test tommorrow and I forgot to study!", 
            font=("Papyrus", 20)
        )

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

def main() -> None:
    # TODO: Implement File Select
    document_path = pathlib.Path(__file__).parent / "examples" / "History Notes.docx"
    quiz_document = ParseQuiz.QuizDocument(document_path)
    parsed_quiz = quiz_document.make_quiz()
    if isinstance(parsed_quiz, ParseQuiz.FormatError):
        return
    
    quiz = Quiz.Quiz(parsed_quiz, question_types={
        Quiz.QuestionType.MULTIPLE_CHOICE, 
        Quiz.QuestionType.TRUE_FALSE, 
        Quiz.QuestionType.MATCHING
    })
        

    app = App("Help! I have a test tommorrow and I forgot to study!", (800, 500))
    app.mainloop()

if __name__ == "__main__":
    main()