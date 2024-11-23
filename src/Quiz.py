import enum
import random
from dataclasses import dataclass
import ParseQuiz

class QuestionType(enum.Enum):
    MULTIPLE_CHOICE = 0
    TRUE_FALSE = 1

@dataclass(frozen=True, slots=True, repr=True)
class BaseQuestion:
    question_text: str

@dataclass(frozen=True, slots=True, repr=True)
class MultipleChoiceQuestion(BaseQuestion):
    choices: frozenset[str]
    answer: str

@dataclass(frozen=True, slots=True, repr=True)
class TrueFalseQuestion(BaseQuestion):
    answer: bool

@dataclass(frozen=True, slots=True, repr=True)
class MultipleChoiceAnswer:
    answer: str

@dataclass(frozen=True, slots=True, repr=True)
class TrueFalseAnswer:
    answer: bool

type Question = MultipleChoiceQuestion | TrueFalseQuestion
type Answer = MultipleChoiceAnswer | TrueFalseAnswer

@dataclass(slots=True, repr=True)
class Quiz:
    questions: list[Question]
    topic: str
    def __init__(self, parsed_quiz: ParseQuiz.ParsedQuiz, num_questions: int = 20):
        self.questions: list[Question] = []
        self.topic: str = f"{parsed_quiz.topic} Test"
        for _ in range(num_questions):

            question_type = random.choice([QuestionType.MULTIPLE_CHOICE, QuestionType.TRUE_FALSE])
            match question_type:
                case QuestionType.MULTIPLE_CHOICE:
                    reverse = random.choice((True, False))
                    question = random.choice(list(parsed_quiz.questions))
                    if reverse:
                        self.questions.append(MultipleChoiceQuestion(
                            question_text=f"What is the definition for {question.term}?",
                            choices=frozenset((question.term, *random.sample([q.definition for q in parsed_quiz.questions], 3))),
                            answer=question.term
                        ))
                    else:
                        self.questions.append(MultipleChoiceQuestion(
                            question_text=f"What is the term for {question.definition}?",
                            choices=frozenset((question.term, *random.sample([q.term for q in parsed_quiz.questions], 3))),
                            answer=question.term
                        ))
                case QuestionType.TRUE_FALSE:
                    question = random.choice(list(parsed_quiz.questions))
                    is_correct = random.choice((True, False))
                    definition = question.definition
                    if not is_correct:
                        definition = random.choice([q.definition for q in parsed_quiz.questions if q != question])
                    self.questions.append(TrueFalseQuestion(
                        question_text=f"True or False: '{question.term}' is {definition}?",
                        answer=is_correct
                    ))

def is_correct(question: Question, answer: Answer) -> bool:
    match question:
        case MultipleChoiceQuestion():
            assert isinstance(answer, MultipleChoiceAnswer)
            return answer.answer == question.answer
        case TrueFalseQuestion():
            assert isinstance(answer, TrueFalseAnswer)
            return answer.answer == question.answer
