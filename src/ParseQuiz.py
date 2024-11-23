import docx
from dataclasses import dataclass
import pathlib
import docx.document

@dataclass(frozen=True, slots=True, repr=True)
class ParsedQuestion:
    term: str
    definition: str

@dataclass(frozen=True, slots=True, repr=True)
class ParsedQuiz:
    topic: str
    questions: set[ParsedQuestion]

class FormatError(Exception):
    pass

class QuizDocument:
    def __init__(self, document_path: pathlib.Path):
        self.topic: str = document_path.stem
        self.document: docx.document.Document = docx.Document(str(document_path))
    
    def make_quiz(self) -> ParsedQuiz | FormatError:
        filtered_paragraphs = [p for p in self.document.paragraphs if p.text != ""]
        if len(filtered_paragraphs) < 4:
            return FormatError("Quiz must have at least 4 questions")
        questions = set()
        for paragraph in filtered_paragraphs:
            split_text = paragraph.text.split(": ")
            try:
                term, definition = split_text[0], split_text[1]
            except IndexError:
                return FormatError("Questions must be in format: '[term]: [definition]'")
            questions.add(ParsedQuestion(term, definition))
        return ParsedQuiz(self.topic, questions)
        