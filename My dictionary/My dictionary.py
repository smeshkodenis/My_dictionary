import random
import pickle

p_ans = 0
n_ans = 0
you_know = 0
steps = 0
if_wrong = {} #создается список для пары слов, в которой допущена ошибка. Каждая пара будет повторена


with open('counter.txt', 'r') as file:
    counter = int(file.read())

with open('pickle_1.txt','rb') as inp:
    my_dict = pickle.load(inp)





def add_to_repeat(a, b):
    with open('repeat.txt', 'a') as repeat:
        repeat.write(f'{a} = {b}; ')

def if_wrong_ans(src, st_o_rp):
    global if_wrong, steps, p_ans, n_ans
    if steps in if_wrong:
        a = if_wrong[steps][0]
        b = if_wrong[steps][1]
        print(a)
        ans = input()
        word_or_act(ans, a)

        if ans == 'STOP':
            stop(src, st_o_rp)
        elif ans == b:
            p_ans += 1
            print(f'Верно!')
            stat(a, 'start')
            print()
        else:
            n_ans+=1
            print(f'Неверно. Правильный ответ: << {b} >>')
            stat(a, 'start')
            if_wrong[steps+4] = (a, b)
            print()
        if_wrong.pop(steps)



def add_words(q):
    a = input("Слово на испанском: ")
    while a != '1':

        b = input("Перевод: ")
        my_dict[a] = [b, 0]
        save()
        print('Новое слово добавлено')
        print()
        if q == 1:
            a = '1'
        else:
            a = input("Слово на испанском: ")

    pass

def stat(rand_word, dict):
    if dict == 'start':
        print(f'+: {p_ans}   -: {n_ans}   {round(p_ans * 100 / (p_ans + n_ans), 1)} %   [{my_dict[rand_word][1]}]')
    elif dict == 'repeat':
        print(f'+: {p_ans}   -: {n_ans}   {round(p_ans * 100 / (p_ans + n_ans), 1)} %')


def word_or_act(a, b):
    if a == 'ADD':
        add_words(2)
        print(b)

def save():
    global counter, my_dict
    with open('counter.txt', 'w') as out:
        d = str(counter)
        out.write(f'{d}')

    with open('pickle_1.txt', 'wb') as out:
        pickle.dump(my_dict, out)



def stop(src, st_o_rp):

    print('Что вы хотите сделать?')
    print('Остановить урок - STOP')
    print('Добавить слово - ADD')
    print('Удалить слово - DEL')
    print('Посмотреть весь список слов - SHOW')
    act = input()
    if act == 'STOP':
        global b
        b = 0
    elif act == 'ADD':
        add_words(2)


    elif act == 'DEL':
        a = input('Введите слово на испанском, которое хотите удалить, или его перевод ')
        if a in my_dict.keys():
            my_dict.pop(a)
        elif a in my_dict.values():
            for item in my_dict.keys():
                if my_dict[item][0] == a:
                    my_dict.pop(item)
                    break
        save()
        print('Слово удалено из списка')

    elif act == 'SHOW':
        show(src, st_o_rp)
        '''my_dict = src
        print(f'Слов в списке: {len(my_dict)}')
        for item in my_dict.keys():
            print(f'{item} - {my_dict[item][0]} - [{my_dict[item][1]}]')'''
    print('')
    save()

def show(src, st_o_rp):
    my_dict = src
    if st_o_rp == 'start':
        print(f'Слов в списке: {len(my_dict)}')
        for item in my_dict.keys():
            print(f'{item} - {my_dict[item][0]} - [{my_dict[item][1]}]')
    else:
        print(f'Слов в списке: {len(my_dict)}')
        for item in my_dict.keys():
            print(f'{item} - {my_dict[item]}')







def start():
    global p_ans, n_ans, counter, if_wrong, steps
    if_wrong_ans(my_dict, 'start')
    steps += 1
    d = random.randint(0, 4)
    rand_word = random.choice(list(my_dict))
    if d in (1,3):
        print(rand_word)
        ans = input()
        word_or_act(ans, rand_word)

        if ans == 'STOP':
            stop(my_dict, 'start')
        elif ans == my_dict[rand_word][0]:
            p_ans+=1
            my_dict[rand_word][1]+=1
            print(f'Верно!')
            stat(rand_word, 'start')
            print()
            if my_dict[rand_word][1] > 9:
                counter += 1
                print(f'Поздравляю! Вы уже хорошо выучили слово {rand_word} - {my_dict[rand_word][0]}')
                print(f'Оно будет удалено из списка. Выучено слов: {counter}')
                add_to_repeat(rand_word, my_dict[rand_word][0])
                my_dict.pop(rand_word)
                save()
                print('Добавьте новое слово')
                add_words(1)
        else:
            n_ans+=1
            my_dict[rand_word][1] -= 1
            print(f'Неверно. Правильный ответ: << {my_dict[rand_word][0]} >>')
            stat(rand_word, 'start')
            if_wrong[steps + 4] = (rand_word, my_dict[rand_word][0])
            print()

    elif d in (0,2,4):
        print(my_dict[rand_word][0])
        ans = input()
        word_or_act(ans, my_dict[rand_word][0])
        if ans == 'STOP':
            stop(my_dict, 'start')
        elif ans == rand_word:
            p_ans+=1
            my_dict[rand_word][1] += 1
            print('Верно!')
            stat(rand_word, 'start')
            print()
            if my_dict[rand_word][1] > 9:
                counter += 1
                print(f'Поздравляю! Вы уже хорошо выучили слово {rand_word} - {my_dict[rand_word][0]}')
                print(f'Оно будет удалено из списка. Выучено слов: {counter}')
                add_to_repeat(rand_word, my_dict[rand_word][0])
                my_dict.pop(rand_word)
                save()
                print('Добавьте новое слово')
                add_words(1)
        else:
            n_ans+=1
            my_dict[rand_word][1] -= 1
            print(f'Неверно. Правильный ответ: << {rand_word} >>')
            stat(rand_word, 'start')
            if_wrong[steps + 4] = (rand_word, my_dict[rand_word][0])
            print()

def repeat():
    global p_ans, n_ans, counter
    d = random.randint(0, 4)
    my_dict = {}
    with open('repeat.txt', 'r') as file:
        my_dict_txt = file.read()

    my_dict_list = my_dict_txt.split(';')
    my_dict_list = [elem.split('=') for elem in my_dict_list]
    for e in my_dict_list:
        if len(e) >1:
            my_dict[e[0].strip()] = e[1].strip()

    rand_word = random.choice(list(my_dict))
    if d in (1, 3):
        print(rand_word)
        ans = input()
        if ans == 'STOP':
            stop(my_dict, 'repeat')
        elif ans == my_dict[rand_word]:
            p_ans+=1
            print(f'Верно!')
            stat(rand_word, 'repeat')
            print()
        else:
            n_ans+=1
            print(f'Неверно. Правильный ответ: << {my_dict[rand_word]} >>')
            stat(rand_word, 'repeat')
            print()

    elif d in (0,2,4):
        print(my_dict[rand_word])
        ans = input()
        if ans == 'STOP':
            stop(my_dict, 'repeat')
        elif ans == rand_word:
            p_ans+=1
            print('Верно!')
            stat(rand_word, 'repeat')
            print()

        else:
            n_ans+=1
            print(f'Неверно. Правильный ответ: << {rand_word} >>')
            stat(rand_word, 'repeat')
            print()

def change():
    with open('repeat.txt', 'r') as file:
        my_dict_txt = file.read()

    new_txt = my_dict_txt.replace(' - ', ' = ')

    with open('repeat.txt', 'w') as file1:
        file1.write(new_txt)

def del_any_word(word):
    with open('pickle_1.txt', 'rb') as inp:
        my_dict = pickle.load(inp)

    print(f'Слов в списке: {len(my_dict)}')
    for item in my_dict.keys():
        print(f'{item} - {my_dict[item][0]} - [{my_dict[item][1]}]')

    print()
    print()
    my_dict.pop(word)
    print(f'Слов в списке: {len(my_dict)}')
    for item in my_dict.keys():
        print(f'{item} - {my_dict[item][0]} - [{my_dict[item][1]}]')

    with open('pickle_1.txt', 'wb') as out:
        pickle.dump(my_dict, out)




b = 1
a = input('start or repeat?')
if a == 'start':
    while b != 0:
        start()
elif a == 'repeat':
    while b != 0:
        repeat()

else:
    del_any_word(input("Какое слово удалить? "))

#new_dict()


