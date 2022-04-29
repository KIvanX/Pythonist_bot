import pickle
# import parser_ACMP
# import parser_Informatics
# import parser_Codeforces


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.level = None
        self.maked = []
        self.dlt = []
        self.varls = {}


class Task:
    def __init__(self, name, link, text, exemples, level, image=None, answer=None):
        self.name = name
        self.link = link
        self.exemples = exemples
        self.text = text
        self.level = level
        self.image = image
        self.answer = answer

    def __str__(self):
        return str(self.__dict__)

    def check(self):
        if 'acmp.ru' in self.link:
            return 'acmp'
            # return parser_ACMP.check_task(self.link)

        if 'informatics.msk.ru' in self.link:
            return 'informatics'
            # return parser_Informatics.check_task(self.link)

        if 'codeforces.com' in self.link:
            return 'codeforces'
            # return parser_Codeforces.check_task(self.link)


# def Data_Generator():
#     tasks = []
#     for i in range(101, 1001):
#         try:
#             name, link, text, exemples, level, image, answer = parser_ACMP.get_task(i)
#             tasks.append(Task(name, link, text, exemples, level, image, answer))
#             print(i, tasks[-1])
#         except Exception as e:
#             print(e)
#
#     with open('Pythonist_database.pkl', 'rb') as f:
#         _, tasks_old = pickle.load(f)
#
#     with open('Pythonist_database.pkl', 'wb') as f:
#         pickle.dump([{}, tasks_old + tasks], f)


def load_all():
    with open('Pythonist_database.pkl', 'rb') as f:
        return pickle.load(f)

# Data_Generator()


# for t in tasks:
#     print(t)
