import pickle


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.admin = False
        self.level = None
        self.saw_ans = []
        self.dlt = None
        self.varls = {}

    def __str__(self):
        return str(self.__dict__)


class Task:
    def __init__(self, name, text, exemples, level, link=None, answer=None):
        self.name = name
        self.text = text
        self.exemples = exemples
        self.level = level
        self.link = link
        self.answer = answer

    def __str__(self):
        return str(self.__dict__)


class Lesson:
    def __init__(self, name, about, text):
        self.name = name
        self.about = about
        self.text = text

    def __str__(self):
        return str(self.__dict__)

    def __len__(self):
        return (len(self.text.split('\n'))-1) // 20

    def page(self, k):
        return '\n'.join(self.text.split('\n')[k * 20: k * 20 + 20])


def load_all():
    with open('Pythonist_database.pkl', 'rb') as f:
        return pickle.load(f)
