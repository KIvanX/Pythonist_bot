import pickle

with open('..\Pythonist_database1.pkl', 'rb') as f:
    users, tasks, lessons = pickle.load(f)

# for k, v in lessons.items():
#     print(v.name)

with open('code.txt', 'r', encoding='utf-8') as f:
    names = list(f)

less = []
for k, v in lessons.items():
    less.append((k, v))

less.sort(key=lambda e: names.index(e[1].name+'\n'))

lessons_new = {}
for k, v in less:
    lessons_new[k] = v
    print(v.name)


