import pickle


with open('Pythonist_database.pkl', 'rb') as f:
    e1, e2, e3 = pickle.load(f)

with open('None.txt', 'r', encoding='utf8') as f:
    names = f.read().split('\n')

pk = [0]*24
for key in e3:
    pk[names.index(e3[key].name)] = [key, e3[key]]

new_les = {}
for l in pk:
    new_les[l[0]] = l[1]

with open('Pythonist_database.pkl', 'wb') as f:
    pickle.dump([e1, e2, new_les], f)

# for key, l in lessons.items():
#     new_text, k = '', 0
#     for c in l.text:
#         new_text += c
#         k += 1
#         if c == '\n':
#             k = 0
#         if k > 50 and c == ' ':
#             new_text += '\n'
#             k = 0
#     lessons[key].text = new_text