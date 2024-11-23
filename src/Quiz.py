import enum
import random
import frozendict
from dataclasses import dataclass
import ParseQuiz

class QuestionType(enum.Enum):
    MULTIPLE_CHOICE = 0
    TRUE_FALSE = 1
    MATCHING = 2

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
class MatchingQuestion(BaseQuestion):
    matches: frozendict.frozendict[str, str]

type Question = MultipleChoiceQuestion | TrueFalseQuestion | MatchingQuestion

@dataclass(slots=True, repr=True)
class Quiz:
    questions: set[Question]
    topic: str
    def __init__(self, parsed_quiz: ParseQuiz.ParsedQuiz, question_types: set[QuestionType] = set(), num_questions: int = 20):
        if question_types == set():
            question_types = {QuestionType.MULTIPLE_CHOICE}
        self.questions: set[Question] = set()
        self.topic: str = parsed_quiz.topic
        for _ in range(num_questions):
            question_type = random.choice(list(question_types))
            match question_type:
                case QuestionType.MULTIPLE_CHOICE:
                    question = random.choice(list(parsed_quiz.questions))
                    self.questions.add(MultipleChoiceQuestion(
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
                    self.questions.add(TrueFalseQuestion(
                        question_text=f"True or False: {question.term} is {definition}?",
                        answer=is_correct
                    ))
                case QuestionType.MATCHING:
                    question_sample = random.sample(list(parsed_quiz.questions), 4)
                    self.questions.add(MatchingQuestion(
                        question_text="Match the term to its definition",
                        matches=frozendict.frozendict({q.term: q.definition for q in question_sample})
                    ))