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
    def __init__(self, fact, start_pos, end_pos, answer_string):
        self.fact = fact
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.answer = Answer(answer_string)

    def render(self):
        s = self.fact.fact
        s = s[:self.start_pos] + '____' + s[self.end_pos:]
        s = s.replace('{', '')
        s = s.replace('}', '')
        return s

    def ask(self, count, total):
        print(f'{count}/{total} {self.render()}')
        guess = input('Your answer>')
        if guess == 'q' or guess == 'Q':
            return True
        self.answer.guess = guess
        self.answer.is_correct = self.answer.guess == self.answer.answer_string
        if self.answer.is_correct:
            print('Correct!')
        else:
            print(f'Sorry, wrong answer.  The correct answer is {self.answer.answer_string}.')
        print()
        return False


class Test:
    questions = []


def ask_questions(test):
    total = len(test.questions)
    for i, q in enumerate(test.questions):
        quit_flag = q.ask(i+1, total)
        if quit_flag:
            return


def show_summary(test):
    total_correct = 0
    total_skipped = 0
    total_attempted = 0
    for q in test.questions:
        if q.answer.is_correct is None:
            total_skipped += 1
        else:
            total_attempted += 1
            if q.answer.is_correct:
                total_correct += 1
    print()
    summary = 'Summary'
    print(summary)
    print('-' * len(summary))
    print(f'Total questions: {total_skipped + total_attempted}')
    print(f'Attempted      : {total_attempted}')
    print(f'Skipped        : {total_skipped}')
    print(f'Correct        : {total_correct}')
    if total_attempted > 0:
        score = '{:.2f}'.format(total_correct / total_attempted)
    else:
        score = 'NaN'
    print(f'Score: {total_correct} / {total_attempted} = {score}')


def take_test(test):
    ask_questions(test)
    show_summary(test)


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
    # TODO HACK
    test.questions = test.questions[:10]
    take_test(test)


if __name__ == '__main__':
    facts = main()
    print(facts)
