import csv
import re

INPUT_FILE = 'data/DMV Driving Facts - Sheet1.csv'


class Fact:
    def __init__(self, line_num, fact):
        self.line_num = line_num
        self.fact = fact


class Answer:
    def __init__(self, answer_string):
        self.answer_string = answer_string
        self.guess = None
        self.is_correct = None


class Question:
    def __init__(self, fact, start_pos, end_pos, answer):
        self.fact = fact
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.answer = answer

    def render(self):
        s = self.fact.fact
        s = s[:self.start_pos] + '____' + s[self.end_pos:]
        s = s.replace('{', '')
        s = s.replace('}', '')
        return s


class Test:
    questions = []


def make_questions(facts, test):
    answer_pattern = r'({\d})'
    for fact in facts:
        answer_iter = re.finditer(answer_pattern, fact.fact)
        for match in answer_iter:
            question = Question(fact, match.start(), match.end(), match.group()[1:-1])
            test.questions.append(question)


def main():
    all_facts = []
    test = Test()
    with open(INPUT_FILE) as csvfile:
        reader = csv.reader(csvfile)
        first_line = True
        for row in reader:
            if first_line:
                first_line = False
            else:
                all_facts.append(Fact(row[0], row[1]))
    make_questions(all_facts, test)
    return test


if __name__ == '__main__':
    facts = main()
    print(facts)
