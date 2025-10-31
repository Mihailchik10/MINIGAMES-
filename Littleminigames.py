#!/usr/bin/env python3
# minigames_hub_extended.py
# All-in-one minigames hub in pure Python (standard library only)
# Includes many minigames; no external modules required.

import random
import time
import os
import sys

# Utilities
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_int(prompt, minv=None, maxv=None):
    while True:
        try:
            s = input(prompt).strip()
            if s == '':
                return None
            v = int(s)
            if (minv is not None and v < minv) or (maxv is not None and v > maxv):
                print(f'Введите число от {minv} до {maxv}.')
                continue
            return v
        except ValueError:
            print('Введите целое число.')

def press_enter():
    input('\nНажмите Enter, чтобы продолжить...')
def safe_print(s):
    """
    Вывод с небольшой паузой — чтобы текст успевал прочитаться.
    """
    print(s)
    time.sleep(0.6)
def input_choice(prompt, choices):
    """
    Показать варианты choices пользователю и вернуть выбранный элемент (строку).
    Если ввод пустой — вернуть None.
    """
    print(prompt)
    for i, c in enumerate(choices, 1):
        print(f'{i}. {c}')
    sel = input_int('Выберите номер (Enter - пропуск): ', 1, len(choices))
    if sel is None:
        return None
    return choices[sel - 1]
def names_list(n):
    """
    Вернуть список имён игроков длины n, где первый — 'You', остальные P2..Pn.
    Например: n=4 -> ['You','P2','P3','P4']
    """
    if n is None or n < 1:
        return ['You']
    return ['You'] + [f'P{i}' for i in range(2, n+1)]
def choose_option(prompt, options):
    """
    Показать список options пользователю, запросить номер и вернуть индекс (0-based).
    Если ввод пустой или некорректный — возвращает None.
    """
    print(prompt)
    for i, o in enumerate(options, 1):
        print(f'{i}. {o}')
    sel = input_int('Выберите номер (Enter = пропуск): ', 1, len(options))
    if sel is None:
        return None
    return sel - 1

# -------------------------
# Game 1: Math Quiz
# -------------------------
def math_quiz():
    clear()
    print('=== Math Quiz ===')
    rounds = input_int('Сколько вопросов? (по умолчанию 5): ', 1) or 5
    max_val = input_int('Максимальное число (по умолчанию 12): ', 2) or 12
    ops = {'+': lambda a,b: a+b, '-': lambda a,b: a-b, '*': lambda a,b: a*b}
    score = 0
    for i in range(1, rounds+1):
        a = random.randint(1, max_val)
        b = random.randint(1, max_val)
        op = random.choice(list(ops.keys()))
        correct = ops[op](a, b)
        ans = input_int(f'Вопрос {i}/{rounds}: {a} {op} {b} = ')
        if ans is None:
            print(f'Пропуск. Правильный ответ: {correct}')
        elif ans == correct:
            print('Верно!')
            score += 1
        else:
            print(f'Неверно. Правильный ответ: {correct}')
    print(f'\nВы набрали {score}/{rounds}')
    press_enter()

# -------------------------
# Game 2: Guess the Number
# -------------------------
def guess_number():
    clear()
    print('=== Guess the Number ===')
    low = input_int('Нижняя граница (по умолчанию 1): ') or 1
    high = input_int('Верхняя граница (по умолчанию 100): ') or 100
    secret = random.randint(low, high)
    tries = 0
    while True:
        g = input_int(f'Угадайте число между {low} и {high} (или пусто для выхода): ')
        if g is None:
            print(f'Вы вышли. Загаданное число было {secret}.')
            break
        tries += 1
        if g < secret:
            print('Слишком мало.')
        elif g > secret:
            print('Слишком много.')
        else:
            print(f'Угадали за {tries} попыток! Поздравляю.')
            break
    press_enter()

# -------------------------
# Game 3: Minesweeper (Сапёр)
# -------------------------
def minesweeper():
    clear()
    print('=== Minesweeper (Сапёр) ===')
    rows = input_int('Рядов (по умолчанию 8): ', 2) or 8
    cols = input_int('Столбцов (по умолчанию 8): ', 2) or 8
    max_mines = rows*cols - 1
    mines_count = input_int(f'Количество мин (по умолчанию 10): ', 1, max_mines) or min(10, max_mines)

    board = [[0]*cols for _ in range(rows)]
    mine_positions = set()
    while len(mine_positions) < mines_count:
        r = random.randrange(rows)
        c = random.randrange(cols)
        if (r,c) not in mine_positions:
            mine_positions.add((r,c))
            board[r][c] = 'M'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'M': continue
            cnt = 0
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'M':
                        cnt += 1
            board[r][c] = cnt

    revealed = [[False]*cols for _ in range(rows)]
    flagged = [[False]*cols for _ in range(rows)]
    def render():
        clear()
        hdr = '   ' + ' '.join(f'{c:2d}' for c in range(cols))
        print(hdr)
        for r in range(rows):
            line = f'{r:2d} '
            for c in range(cols):
                if flagged[r][c]:
                    line += ' F'
                elif not revealed[r][c]:
                    line += ' #'
                else:
                    v = board[r][c]
                    if v == 0:
                        line += ' .'
                    elif v == 'M':
                        line += ' *'
                    else:
                        line += f' {v}'
            print(line)
    remaining = rows*cols - mines_count
    while True:
        render()
        print('\nКоманды: r row col  - открыть; f row col - пометить/снять флаг; q - выйти')
        cmd = input('> ').strip().lower()
        if cmd == 'q' or cmd == '':
            print('Выход из Сапёра.')
            break
        parts = cmd.split()
        if len(parts) < 3:
            print('Неверная команда.')
            time.sleep(0.6)
            continue
        action, *rest = parts
        try:
            row = int(rest[0]); col = int(rest[1])
        except:
            print('Неверные координаты.')
            time.sleep(0.6)
            continue
        if not (0 <= row < rows and 0 <= col < cols):
            print('Координаты вне поля.')
            time.sleep(0.6)
            continue
        if action == 'f':
            flagged[row][col] = not flagged[row][col]
            continue
        if action == 'r':
            if flagged[row][col]:
                print('Сначала снимите флаг.')
                time.sleep(0.6)
                continue
            if revealed[row][col]:
                print('Уже открыта.')
                time.sleep(0.6)
                continue
            if board[row][col] == 'M':
                for r,c in mine_positions:
                    revealed[r][c] = True
                render()
                print('\nБах! Вы подорвались на мине. Игра окончена.')
                break
            stack = [(row,col)]
            opened = 0
            while stack:
                r,c = stack.pop()
                if revealed[r][c]: continue
                revealed[r][c] = True
                opened += 1
                if board[r][c] == 0:
                    for dr in (-1,0,1):
                        for dc in (-1,0,1):
                            nr, nc = r+dr, c+dc
                            if 0 <= nr < rows and 0 <= nc < cols and not revealed[nr][nc]:
                                stack.append((nr,nc))
            remaining -= opened
            if remaining <= 0:
                render()
                print('\nПоздравляю! Вы открыли все безопасные клетки и выиграли!')
                break
    press_enter()

# -------------------------
# Game 4: Dogonalki (Догонялки) - simple chase
# -------------------------
def dogonalki():
    clear()
    print('=== Догонялки ===')
    length = input_int('Длина трассы (по умолчанию 20): ', 5) or 20
    player = 0
    chaser = -3
    max_turns = input_int('Максимум ходов до ничьи (по умолчанию 200): ', 10) or 200
    turn = 0
    print('Правила: вы - игрок (P), преследователь - (C). Ход: b (бежать) или s (замедлиться).')
    press_enter()
    while turn < max_turns:
        turn += 1
        clear()
        print(f'Ход {turn}')
        track = ['.']*length
        if 0 <= player < length:
            track[player] = 'P'
        if 0 <= chaser < length:
            if track[chaser] == 'P': track[chaser] = 'X'
            else: track[chaser] = 'C'
        print(''.join(track))
        move = input('Ваш ход: (b) бежать, (s) замедлиться, (q) выйти: ').strip().lower()
        if move == 'q' or move == '':
            print('Выход.')
            break
        if move == 'b':
            player += random.randint(1,3)
        else:
            player += random.randint(0,1)
        dist = player - chaser
        if dist <= 2:
            chaser += random.randint(1,3)
        else:
            chaser += random.randint(1,2)
        player = min(player, length-1)
        chaser = min(chaser, length-1)
        if chaser >= player:
            clear()
            print('Преследователь догнал вас! Вы проиграли.')
            break
        if player >= length-1:
            clear()
            print('Вы добежали до финиша и спаслись! Победа!')
            break
    else:
        print('Максимум ходов достигнут — ничья.')
    press_enter()

# -------------------------
# Game 5: Hide & Seek (Прятки)
# -------------------------
def hide_and_seek():
    clear()
    print('=== Hide & Seek (Прятки) ===')
    size = input_int('Число мест для пряток (по умолчанию 10): ', 5) or 10
    rounds = input_int('Сколько раундов? (по умолчанию 2): ', 1) or 2
    score_player = 0
    score_ai = 0
    for r in range(1, rounds+1):
        clear()
        print(f'Раунд {r}/{rounds}: вы прячетесь, ИИ ищет.')
        hiding_spot = input_int(f'Выберите место для прятки 0..{size-1}: ', 0, size-1)
        if hiding_spot is None:
            hiding_spot = random.randrange(size)
            print(f'Вы случайно выбрали {hiding_spot}')
        print('ИИ начинает искать...')
        time.sleep(0.6)
        search_order = list(range(size))
        random.shuffle(search_order)
        found = False
        for i, spot in enumerate(search_order, start=1):
            print(f'ИИ проверяет место {spot}...')
            time.sleep(0.3)
            if spot == hiding_spot:
                print(f'ИИ нашёл вас через {i} попыток!')
                score_ai += 1
                found = True
                break
        if not found:
            print('ИИ не нашёл вас. Вы выиграли раунд.')
            score_player += 1
        press_enter()
        clear()
        print(f'Раунд {r}/{rounds}: теперь ИИ прячется, вы ищете.')
        ai_spot = random.randrange(size)
        attempts = size//2 + 1
        for a in range(1, attempts+1):
            guess = input_int(f'Попытка {a}/{attempts}: ваш вариант: ', 0, size-1)
            if guess is None:
                print(f'Вы пасуете. ИИ был в {ai_spot}.')
                score_ai += 1
                break
            if guess == ai_spot:
                print('Вы нашли ИИ! Вы выиграли раунд.')
                score_player += 1
                break
            else:
                print('Неправильно.')
        else:
            print(f'Попытки кончились. ИИ выиграл раунд. Был в {ai_spot}.')
            score_ai += 1
        press_enter()
    clear()
    print('Итог:')
    print(f'Ваши очки: {score_player}, ИИ: {score_ai}')
    if score_player > score_ai:
        print('Вы победили!')
    elif score_player < score_ai:
        print('ИИ победил.')
    else:
        print('Ничья.')
    press_enter()

# -------------------------
# Game 6: Snakes and Ladders
# -------------------------
def snakes_and_ladders():
    clear()
    print('=== Snakes and Ladders (Змеи и Лестницы) ===')
    players_count = input_int('Число игроков (1-4): ', 1, 4) or 2
    names = []
    for i in range(players_count):
        n = input(f'Имя игрока {i+1} (Enter для "Player{i+1}"): ').strip() or f'Player{i+1}'
        names.append(n)
    while len(names) < 2:
        names.append(f'CPU{len(names)+1}')
    size = 100
    ladders = {2:38,7:14,8:31,15:26,28:84,21:42,36:44,51:67,71:91,78:98,87:94}
    snakes = {16:6,46:25,49:11,62:19,64:60,74:53,89:68,92:88,95:75,99:80}
    positions = {name:0 for name in names}
    turn = 0
    def roll(): return random.randint(1,6)
    while True:
        clear()
        print('Позиции:')
        for n in names:
            print(f'{n}: {positions[n]}', end='  ')
        print('\n')
        cur = names[turn % len(names)]
        print(f'Ход игрока: {cur}')
        if cur.startswith('CPU'):
            time.sleep(0.6)
            r = roll()
            print(f'CPU бросил {r}')
        else:
            _ = input('Нажмите Enter чтоб бросить кубик...')
            r = roll()
            print(f'Вы бросили {r}')
        positions[cur] += r
        if positions[cur] > size:
            positions[cur] = size - (positions[cur] - size)
        if positions[cur] in ladders:
            print(f'Лестница! {positions[cur]} -> {ladders[positions[cur]]}')
            positions[cur] = ladders[positions[cur]]
        elif positions[cur] in snakes:
            print(f'Змея! {positions[cur]} -> {snakes[positions[cur]]}')
            positions[cur] = snakes[positions[cur]]
        if positions[cur] == size:
            print(f'\n{cur} достиг клетки {size} и победил! Поздравляем!')
            break
        turn += 1
        time.sleep(0.8)
    press_enter()

# -------------------------
# New Game A: "Прятки-догонялки вирус"
# Description: Infection hide-chase: players hide; infected AI can infect found players who then chase others.
# -------------------------
def hide_chase_virus():
    clear()
    print('=== Прятки-догонялки ВИРУС ===')
    places = input_int('Число мест (по умолчанию 12): ', 5) or 12
    players = ['You'] + [f'NPC{i}' for i in range(1,4)]
    infected = set()
    # initial infected NPC
    infected.add(random.choice(players[1:]))
    hidden_spots = {p: random.randrange(places) for p in players}
    print(f'Игроки: {", ".join(players)}')
    print(f'Первоначально заражён: {", ".join(infected)}')
    rounds = input_int('Сколько раундов? (по умолчанию 3): ', 1) or 3
    score = {p:0 for p in players}
    for rnd in range(1, rounds+1):
        clear()
        print(f'Раунд {rnd}/{rounds}')
        # players choose spots (you choose)
        spot_you = input_int(f'Выберите место 0..{places-1} (Enter для случайного): ', 0, places-1)
        if spot_you is None:
            spot_you = random.randrange(places)
        hidden_spots['You'] = spot_you
        for npc in players[1:]:
            hidden_spots[npc] = random.randrange(places)
        print('ИИ ищет по очереди. Инфицированные при обнаружении заражают.')
        order = players[1:] + ['You']  # NPCs search first
        found_order = []
        for seeker in order:
            # seeker searches sequentially over spots
            search = list(range(places))
            random.shuffle(search)
            for idx, s in enumerate(search, start=1):
                # check each target
                targets = [p for p in players if hidden_spots[p] == s and p != seeker]
                if targets:
                    for t in targets:
                        found_order.append((seeker, t))
                        # if seeker infected -> target becomes infected
                        if seeker in infected:
                            infected.add(t)
                        # if target infected -> seeker becomes infected
                        if t in infected:
                            infected.add(seeker)
                    break
            time.sleep(0.15)
        # scoring: survivors (non-infected) get points, infected lose points
        for p in players:
            if p in infected:
                score[p] -= 1
            else:
                score[p] += 1
        clear()
        print('Результаты раунда:')
        print('Найденные пары (seeker -> found):')
        for s,f in found_order:
            print(f'  {s} -> {f}')
        print('Заражённые сейчас:', ', '.join(sorted(infected)))
        print('Счёт:')
        for p in players:
            print(f'  {p}: {score[p]}')
        press_enter()
    clear()
    print('Итоговая инфекция и счёт:')
    print('Заражённые:', ', '.join(sorted(infected)))
    for p in players:
        print(f'  {p}: {score[p]}')
    press_enter()

# -------------------------
# New Game B: "Бункер"
# Description: Resource management turns: allocate resources to survive waves.
# -------------------------
def bunker():
    clear()
    print('=== Бункер ===')
    rounds = input_int('Сколько волн? (по умолчанию 6): ', 1) or 6
    resources = {'food': 10, 'water': 10, 'ammo': 5, 'morale': 5}
    survivors = 5
    print('Вы — управляющий бункером. Распределяйте ресурсы каждый раунд.')
    press_enter()
    for rnd in range(1, rounds+1):
        clear()
        print(f'Волна {rnd}/{rounds}')
        print('Состояние бункера:')
        for k,v in resources.items():
            print(f'  {k}: {v}')
        print(f'Выживших: {survivors}')
        # random event affects needs
        event = random.choice(['raiders','sickness','storm','quiet'])
        print(f'Событие в этот раунд: {event}')
        # player allocates small amounts to mitigate
        print('Распределите 3 единицы ресурсов на приоритеты: food, water, ammo, morale')
        alloc = {'food':0,'water':0,'ammo':0,'morale':0}
        points = 3
        while points > 0:
            print(f'Осталось очков: {points}')
            choice = input('Куда потратить (food/water/ammo/morale or Enter сброс): ').strip().lower()
            if choice == '':
                break
            if choice in alloc:
                alloc[choice] += 1
                points -= 1
            else:
                print('Неверно.')
        # apply allocations and baseline consumption
        resources['food'] = max(0, resources['food'] + alloc['food'] - survivors//2)
        resources['water'] = max(0, resources['water'] + alloc['water'] - survivors//2)
        resources['ammo'] = max(0, resources['ammo'] + alloc['ammo'] - (1 if event=='raiders' else 0))
        resources['morale'] = max(0, resources['morale'] + alloc['morale'] - (1 if event in ('sickness','storm') else 0))
        # event resolution
        if event == 'raiders':
            if resources['ammo'] >= 1:
                print('Вы отбили рейдеров.')
                resources['ammo'] = max(0, resources['ammo'] - 1)
            else:
                lost = random.randint(1,3)
                survivors = max(0, survivors - lost)
                print(f'Рейдеры нанесли потери: -{lost} выживших.')
        elif event == 'sickness':
            if resources['water'] >= survivors//3:
                print('С болезнью справились.')
                resources['water'] = max(0, resources['water'] - 1)
            else:
                lost = random.randint(0,2)
                survivors = max(0, survivors - lost)
                print(f'Болезнь унесла: -{lost} выживших.')
        elif event == 'storm':
            print('Шторм повредил запасы.')
            resources['food'] = max(0, resources['food'] - 1)
            resources['water'] = max(0, resources['water'] - 1)
            resources['morale'] = max(0, resources['morale'] - 1)
        else:
            print('Тихая ночь. Ничего особенного.')
        # morale check: if morale low, survivors may leave
        if resources['morale'] <= 0 and survivors > 0:
            leave = random.choice([0,1])
            if leave:
                survivors -= 1
                print('Один выживший покинул бункер из-за низкого морального духа.')
        time.sleep(1)
        if survivors <= 0:
            print('Все выжившие потеряны. Конец игры.')
            break
        press_enter()
    clear()
    print('Конец подсчёта. Финальное состояние:')
    print(f'Выживших: {survivors}')
    for k,v in resources.items():
        print(f'  {k}: {v}')
    press_enter()

# -------------------------
# New Game C: "Догонялки с мячом"
# Description: Chase where ball can be passed; if you have the ball and reach goal you win; chaser tries to tackle.
# -------------------------
def chase_with_ball():
    clear()
    print('=== Догонялки с мячом ===')
    length = input_int('Длина поля (по умолчанию 20): ', 8) or 20
    player = 0
    chaser = -4
    ball_holder = 'You'  # You start with ball
    npc_pos = {'You':player, 'Chaser':chaser}
    max_turns = input_int('Максимум ходов (по умолчанию 150): ', 10) or 150
    turn = 0
    print('Правила: у вас мяч (B). Вы можете бежать (b), передать (p) или замедлиться (s).')
    print('Если преследователь догонит вас и утащит мяч, вы проиграли.')
    press_enter()
    while turn < max_turns:
        turn += 1
        clear()
        npc_pos['You'] = player
        npc_pos['Chaser'] = chaser
        field = ['.']*length
        if 0 <= chaser < length:
            field[chaser] = 'C'
        if 0 <= player < length:
            field[player] = 'P' if ball_holder!='You' else 'B'  # show B if you have ball
        print(''.join(field))
        action = input('Ваш ход: (b) бежать, (p) передать (риск), (s) замедлиться, (q) выйти: ').strip().lower()
        if action == 'q' or action == '':
            print('Выход.')
            break
        if action == 'b':
            step = random.randint(1,3)
            player += step
            print(f'Вы пробежали {step} клеток.')
        elif action == 's':
            step = random.randint(0,1)
            player += step
            print(f'Вы медленно продвинулись на {step}.')
        elif action == 'p':
            # pass: 50% success to pass forward 2..4 cells to a "ally" (imaginary), else drop and chaser gets ball
            success = random.random() < 0.6
            if success:
                advance = random.randint(2,4)
                player += advance
                print(f'Передача успешна, вы продвинулись на {advance} (символический приём).')
            else:
                print('Передача неудачна! Мяч у преследователя.')
                ball_holder = 'Chaser'
        # chaser moves towards player with chance to tackle if close
        dist = player - chaser
        if ball_holder == 'Chaser':
            # chaser carrying ball tries to return you backwards (simulate)
            chaser += random.randint(1,3)
        else:
            if dist <= 2:
                chaser += random.randint(1,3)
            else:
                chaser += random.randint(1,2)
        # if chaser catches player
        if chaser >= player:
            # if chaser catches and you had ball, ball transfers
            if ball_holder == 'You':
                ball_holder = 'Chaser'
                print('Преследователь догнал вас и отобрал мяч!')
            else:
                print('Преследователь догнал вас!')
            press_enter()
            clear()
            print('Вы проиграли. Попробуйте ещё раз.')
            break
        # if player reaches end with ball
        if player >= length-1 and ball_holder == 'You':
            clear()
            print('Вы добежали до зоны и забили/добились цели с мячом. Победа!')
            break
        # chaser may drop ball randomly
        if ball_holder == 'Chaser' and random.random() < 0.3:
            print('Преследователь уронил мяч. Вы можете подобрать его!')
            if abs(player - chaser) <= 2:
                ball_holder = 'You'
                print('Вы подобрали мяч!')
        player = min(player, length-1)
        chaser = min(chaser, length-1)
        time.sleep(0.6)
    else:
        print('Максимум ходов достигнут — ничья.')
    press_enter()

# -------------------------
# New Game D: "Выживание"
# Description: Turn-based survival: scavenging, threats, hunger and fatigue. Goal: survive N дней.
# -------------------------
def survival_game():
    clear()
    print('=== Выживание ===')
    days = input_int('Сколько дней вы хотите выживать? (по умолчанию 7): ', 1) or 7
    hunger = 0   # 0 good, higher bad
    fatigue = 0
    health = 10
    supplies = {'food':5, 'wood':3, 'water':5}
    day = 0
    print('Цель: пройти заданное число дней, управляя запасами и состоянием.')
    press_enter()
    while day < days and health > 0:
        day += 1
        clear()
        print(f'День {day}/{days}')
        print(f'Здоровье: {health}, Голод: {hunger}, Усталость: {fatigue}')
        print('Запасы:', supplies)
        action = input('Действие на день: (s) собирать, (r) отдыхать, (h) охотиться, (q) выйти: ').strip().lower()
        if action == 'q' or action == '':
            print('Вы сдались. Выход из игры.')
            break
        if action == 's':
            # scavenge: small chance for food/wood/water, risk of injury
            food_found = random.randint(0,2)
            wood_found = random.randint(0,2)
            water_found = random.randint(0,1)
            supplies['food'] += food_found
            supplies['wood'] += wood_found
            supplies['water'] += water_found
            print(f'Вы нашли: food+{food_found}, wood+{wood_found}, water+{water_found}')
            if random.random() < 0.15:
                injury = random.randint(1,3)
                health -= injury
                print(f'Вы поранились: -{injury} здоровья.')
            hunger += 1
            fatigue += 1
        elif action == 'r':
            # rest: recover fatigue and small health
            fatigue = max(0, fatigue-2)
            health = min(10, health+1)
            print('Отдых помог: усталость -2, здоровье +1')
            hunger += 1
        elif action == 'h':
            # hunt: chance for more food, risk higher injury
            success = random.random() < 0.65
            if success:
                gained = random.randint(1,4)
                supplies['food'] += gained
                print(f'Успешная охота: food+{gained}')
            else:
                print('Охота не удалась.')
            if random.random() < 0.2:
                injury = random.randint(1,4)
                health -= injury
                print(f'Вы поранились: -{injury} здоровья.')
            hunger += 1
            fatigue += 2
        # consume daily
        if supplies['food'] > 0 and supplies['water'] > 0:
            supplies['food'] = max(0, supplies['food'] - 1)
            supplies['water'] = max(0, supplies['water'] - 1)
            hunger = max(0, hunger-1)
        else:
            # lack of vital resources increases hunger and health loss
            hunger += 2
            health -= 1
            print('Недостаточно еды/воды: здоровье снижается.')
        # if hunger too high, health drops
        if hunger >= 5:
            health -= 1
            print('Сильный голод: здоровье -1')
        # random threat (wild animal, raider)
        if random.random() < 0.12:
            threat = random.choice(['wolf','raiders','storm'])
            if threat == 'wolf':
                print('Волк напал!')
                if supplies['wood'] >= 1 and random.random() < 0.5:
                    supplies['wood'] -= 1
                    print('Вы отогнали волка, потеряв немного дров.')
                else:
                    dmg = random.randint(1,3)
                    health -= dmg
                    print(f'Волк нанёс урон: -{dmg} здоровья.')
            elif threat == 'raiders':
                print('Отряд рейдеров напал!')
                if supplies['ammo'] if 'ammo' in supplies else False:
                    pass
                lost_food = min(supplies['food'], random.randint(0,2))
                supplies['food'] -= lost_food
                health -= 0
                print(f'Рейдеры украли food-{lost_food}.')
            else:
                print('Шторм. Усложнение дня: усталость +1.')
                fatigue += 1
        # fatigue effects
        if fatigue >= 6:
            health -= 1
            print('Крайняя усталость: здоровье -1')
        print(f'Итог дня: здоровье={health}, голод={hunger}, усталость={fatigue}, запасы={supplies}')
        time.sleep(0.8)
        if health <= 0:
            print('Вы не выжили...')
            break
        press_enter()
    clear()
    if health > 0 and day >= days:
        print(f'Поздравляем! Вы выжили {days} дней.')
    else:
        print('К сожалению, вы не выжили.')
    press_enter()
# -----------------------
# Game: Рельсы (Rails) - логическая головоломка по переключению стрелок
# -----------------------
def rails_game():
    clear()
    print('=== Рельсы ===')
    print('Вам дано рельсовое разветвление: простая строка станций с переключателями.')
    n = input_int('Длина секции (по умолчанию 8): ', 4) or 8
    switches = [random.choice([0,1]) for _ in range(n)]  # 0 -> left, 1 -> right
    target_pos = random.randrange(n)
    start = 0
    print('Цель: провести поезд от старта до целевой позиции, управляя переключателями.')
    print('Нумерация позиций 0..', n-1)
    press_enter()
    while True:
        clear()
        print('Switches:', ' '.join(str(s) for s in switches))
        print('Start at 0, target at', target_pos)
        cmd = input('Команды: t i - переключить i; r - запустить поезд; q - выйти\n> ').strip().lower()
        if cmd == 'q' or cmd == '':
            break
        if cmd == 'r':
            pos = start
            visited = [pos]
            steps = 0
            while 0 <= pos < n and steps < 100:
                # move: if switch 0 -> pos+1, if 1 -> pos-1 (simple behavior)
                if switches[pos] == 0:
                    pos = pos + 1
                else:
                    pos = pos - 1
                visited.append(pos)
                steps += 1
                if pos == target_pos:
                    break
            if pos == target_pos:
                print('Поезд прибыл в цель! Маршрут:', visited)
            else:
                print('Поезд сошёл с маршрута или зациклился. Маршрут:', visited)
            press_enter()
            continue
        parts = cmd.split()
        if len(parts) == 2 and parts[0] == 't':
            try:
                i = int(parts[1])
                if 0 <= i < n:
                    switches[i] = 1 - switches[i]
                    print('Переключено.')
                else:
                    print('Индекс вне диапазона.')
            except:
                print('Неверный индекс.')
            time.sleep(0.5)
            continue
        print('Неверная команда.')
        time.sleep(0.5)

# -----------------------
# Game: Гонки (Racing) - текстовая гонка с управлением ускорением/торможением
# -----------------------
def racing_game():
    clear()
    print('=== Гонки ===')
    length = input_int('Длина трассы (по умолчанию 50): ', 20) or 50
    player_pos = 0
    players = {'You': player_pos, 'Rival': -3}
    speed = {'You':0, 'Rival':0}
    max_turns = input_int('Макс ходов (по умолчанию 200): ', 10) or 200
    turn = 0
    print('Вы управляете скоростью: a - ускориться, d - притормозить, n - нейтрально.')
    press_enter()
    while turn < max_turns:
        turn += 1
        clear()
        print(f'Ход {turn}')
        print('Позиции: You:', players['You'], 'Rival:', players['Rival'])
        action = input('Ваш ход (a/d/n, q выйти): ').strip().lower()
        if action == 'q' or action == '':
            break
        if action == 'a':
            speed['You'] += 1
        elif action == 'd':
            speed['You'] = max(0, speed['You'] - 1)
        elif action == 'n':
            pass
        # rival AI: random small accel or maintain
        if random.random() < 0.6:
            speed['Rival'] += random.choice((0,1))
        else:
            speed['Rival'] = max(0, speed['Rival'] - 1)
        # apply speed with chance of slip if too fast
        for p in players:
            sp = speed[p]
            move = sp + random.randint(0,1) - (1 if sp>5 and random.random()<0.2 else 0)
            players[p] += move
        # track boundaries
        if players['You'] >= length:
            clear()
            print('Вы финишировали первыми! Победа!')
            break
        if players['Rival'] >= length:
            clear()
            print('Соперник финишировал первым. Вы проиграли.')
            break
        time.sleep(0.3)
    else:
        print('Время вышло — ничья.')
    press_enter()

# -----------------------
# Game: Вышибалы (Dodgeball) - простая командная игра: выбор цели/уклонение
# -----------------------
def dodgeball():
    clear()
    print('=== Вышибалы ===')
    team_you = ['You'] + [f'P{i}' for i in range(1,3)]
    team_enemy = [f'E{i}' for i in range(1,4)]
    hits = {p:0 for p in team_you+team_enemy}
    print('Цель: вывести всех противников из игры. Каждому игроку 2 жизни.')
    press_enter()
    round_no = 0
    while True:
        round_no += 1
        clear()
        print(f'Раунд {round_no}')
        print('Ваши:', team_you)
        print('Враги:', team_enemy)
        # You choose target
        if not team_enemy:
            print('Все враги выведены — вы победили!')
            break
        if not team_you:
            print('Ваша команда выбита — вы проиграли.')
            break
        target = None
        print('Ваша очередь. Выберите цель из:', ', '.join(team_enemy))
        t = input('Цель (имя или Enter случайно): ').strip()
        if t == '':
            target = random.choice(team_enemy)
        elif t in team_enemy:
            target = t
        else:
            print('Неверная цель, выбирается случайная.')
            target = random.choice(team_enemy)
        # throw success depends on accuracy and dodge
        throw_success = random.random() < 0.65
        dodge = random.random() < 0.35
        if throw_success and not dodge:
            hits[target] += 1
            print(f'Вы попали по {target}! Урон #{hits[target]}.')
            if hits[target] >= 2:
                team_enemy.remove(target)
                print(f'{target} выведен из игры!')
        else:
            print('Промах или уклонение.')
        # enemies act: each enemy targets random team member
        for e in list(team_enemy):
            if not team_you:
                break
            tgt = random.choice(team_you)
            succ = random.random() < 0.55
            if succ and random.random() > 0.3:
                hits[tgt] += 1
                print(f'{e} попал по {tgt} (урон #{hits[tgt]})')
                if hits[tgt] >= 2:
                    if tgt == 'You':
                        team_you.remove('You')
                        print('Вы выведены из игры!')
                    else:
                        team_you.remove(tgt)
                        print(f'{tgt} выбыл.')
            else:
                print(f'{e} промахнулся по {tgt}.')
        press_enter()

# -----------------------
# Game: Туман (Fog) - навигация по сетке с ограниченной видимостью
# -----------------------
def fog_game():
    clear()
    print('=== Туман ===')
    size = input_int('Размер поля (по умолчанию 8): ', 4) or 8
    player = [0, 0]
    goal = [size-1, size-1]
    obstacles = {(random.randrange(size), random.randrange(size)) for _ in range(size)}
    if (0,0) in obstacles: obstacles.remove((0,0))
    if (goal[0],goal[1]) in obstacles: obstacles.remove((goal[0],goal[1]))
    view = 1  # visibility radius
    print('Двигайтесь к цели в правом нижнем углу. Видимость ограничена.')
    press_enter()
    while True:
        clear()
        # render small area around player
        for r in range(size):
            line = ''
            for c in range(size):
                if abs(r-player[0])<=view and abs(c-player[1])<=view:
                    if [r,c] == goal:
                        line += ' G'
                    elif (r,c) in obstacles:
                        line += ' #'
                    elif [r,c] == player:
                        line += ' P'
                    else:
                        line += ' .'
                else:
                    line += ' ?'
            print(line)
        if player == goal:
            print('Вы достигли цели. Победа!')
            break
        cmd = input('Ход (w/a/s/d), q - выйти: ').strip().lower()
        if cmd == 'q' or cmd == '':
            break
        if cmd == 'w' and player[0]>0: player[0]-=1
        if cmd == 's' and player[0]<size-1: player[0]+=1
        if cmd == 'a' and player[1]>0: player[1]-=1
        if cmd == 'd' and player[1]<size-1: player[1]+=1
        # random fog event: visibility change
        if random.random() < 0.12:
            if random.random() < 0.5:
                view = max(0, view-1)
                print('Туман усилился. Видимость уменьшилась.')
            else:
                view = min(size, view+1)
                print('Туман рассеялся. Видимость выросла.')
            time.sleep(0.6)
    press_enter()

# -----------------------
# Game: Рейд (Raid) - командный штурм с выбором стратегии
# -----------------------
def raid_game():
    clear()
    print('=== Рейд ===')
    team = ['Alpha', 'Bravo', 'Charlie']
    enemy_strength = input_int('Сила обороны (1-10, по умолчанию 5): ', 1, 10) or 5
    print('Вы командир рейда. Выберите стратегию: stealth (скрытно), frontal (в лоб), diversion (отвлекающий).')
    strat = input('Стратегия (stealth/frontal/diversion): ').strip().lower()
    success_chance = 0.5
    if strat == 'stealth':
        success_chance += 0.15
    elif strat == 'frontal':
        success_chance -= 0.1
    elif strat == 'diversion':
        success_chance += 0.05
    # adjust by enemy_strength
    success_chance -= (enemy_strength-5)*0.05
    result = random.random() < success_chance
    clear()
    if result:
        print('Рейд успешен! Цели достигнуты.')
    else:
        losses = random.randint(0, len(team))
        print(f'Рейд провалился. Потери команды: {losses}.')
    press_enter()

# -----------------------
# Game: Термометр (Thermometer) - угадай корректное значение с подсказками теплее/холоднее
# -----------------------
def thermometer_game():
    clear()
    print('=== Термометр ===')
    secret = random.randint(1,100)
    prev_diff = None
    attempts = 0
    while True:
        guess = input_int('Угадайте число 1..100 (Enter выход): ', 1, 100)
        if guess is None:
            print('Вы вышли. Было:', secret)
            break
        attempts += 1
        diff = abs(secret - guess)
        if diff == 0:
            print(f'Угадали за {attempts} попыток!')
            break
        if prev_diff is None:
            print('Теплее' if diff <= 20 else 'Холодно')
        else:
            if diff < prev_diff:
                print('Теплее')
            elif diff > prev_diff:
                print('Холоднее')
            else:
                print('Так же')
        prev_diff = diff
    press_enter()

# -----------------------
# Game: Змейка (Snake) - простейшая консольная змейка (без curses)
# Note: movement is turn-based; player inputs direction each step.
# -----------------------
def snake_game():
    clear()
    print('=== Змейка ===')
    size = input_int('Размер поля (по умолчанию 10): ', 5) or 10
    snake = [(size//2, size//2)]
    direction = (0,1)  # starts moving right
    food = (random.randrange(size), random.randrange(size))
    score = 0
    print('Управление: w/a/s/d шаг за шагом. Цель: съесть как можно больше еды.')
    press_enter()
    while True:
        clear()
        grid = [['.' for _ in range(size)] for __ in range(size)]
        for x,y in snake:
            grid[x][y] = 'S'
        fx,fy = food
        grid[fx][fy] = 'F'
        for r in range(size):
            print(' '.join(grid[r]))
        print('Score:', score)
        cmd = input('Ввод (w/a/s/d), q - выход: ').strip().lower()
        if cmd == 'q' or cmd == '':
            break
        if cmd == 'w': direction = (-1,0)
        if cmd == 's': direction = (1,0)
        if cmd == 'a': direction = (0,-1)
        if cmd == 'd': direction = (0,1)
        head = snake[0]
        new_head = (head[0]+direction[0], head[1]+direction[1])
        # check collisions
        if not (0 <= new_head[0] < size and 0 <= new_head[1] < size) or new_head in snake:
            clear()
            print('Вы врезались. Игра окончена. Счёт:', score)
            break
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            # spawn new food not on snake
            attempts = 0
            while True:
                f = (random.randrange(size), random.randrange(size))
                if f not in snake:
                    food = f
                    break
                attempts += 1
                if attempts > 100:
                    # no space left
                    break
        else:
            snake.pop()
    press_enter()

# -----------------------
# Game: Решение поезда (Trolley Problem) - моральный выбор с последствиями
# -----------------------
def trolley_game():
    clear()
    print('=== Решение поезда ===')
    print('Вы — оператор стрелки. Поезд движется по рельсам. Вы можете переключить путь.')
    scenario = random.choice([
        {'left':3, 'right':1},
        {'left':5, 'right':2},
        {'left':1, 'right':0},
        {'left':0, 'right':1},
    ])
    print('На левой ветке находится', scenario['left'], 'человек(а).')
    print('На правой ветке находится', scenario['right'], 'человек(а).')
    choice = input('Переключить на правую ветку? (y/n): ').strip().lower()
    if choice in ('y','yes','д','да'):
        killed = scenario['right']
        saved = scenario['left']
        print('Вы переключили поезд. Умерло', killed, 'человек(а).')
    else:
        killed = scenario['left']
        saved = scenario['right']
        print('Вы ничего не сделали. Умерло', killed, 'человек(а).')
    # moral consequence: reputation measure randomly affected
    rep = random.randint(-5,5) + (saved - killed)
    print('Моральные последствия (символически): репутация', rep)
    press_enter()

# -----------------------
# Game: Живой автомобиль (Living Car) - автомобиль с параметрами; управлять чтобы добраться до цели
# -----------------------
def living_car():
    clear()
    print('=== Живой автомобиль ===')
    distance = input_int('Дистанция до цели (по умолчанию 30): ', 5) or 30
    fuel = input_int('Запас топлива (по умолчанию 10): ', 1) or 10
    integrity = 10  # здоровье машины
    position = 0
    print('Каждый ход: drive (ехать), refuel (пополнить рискованно), repair (починить с шансом).')
    press_enter()
    while position < distance and integrity > 0:
        clear()
        print(f'Позиция: {position}/{distance}, топливо: {fuel}, прочность: {integrity}')
        cmd = input('Действие (drive/refuel/repair/q): ').strip().lower()
        if cmd == 'q' or cmd == '':
            break
        if cmd == 'drive':
            if fuel <= 0:
                print('Нет топлива.')
            else:
                move = random.randint(2,5)
                position += move
                fuel -= 1
                # road hazard
                if random.random() < 0.15:
                    dmg = random.randint(1,3)
                    integrity -= dmg
                    print(f'Дорожная опасность повредила авто -{dmg} прочности.')
                print(f'Вы проехали {move}.')
        elif cmd == 'refuel':
            # refuel risky: chance to gain 3 fuel, else lose integrity
            if random.random() < 0.7:
                fuel += 3
                print('Удачная дозаправка: +3 топлива.')
            else:
                dmg = random.randint(1,2)
                integrity -= dmg
                print(f'Неудачная заправка: повреждение -{dmg}.')
        elif cmd == 'repair':
            # repair consumes a turn, small chance to restore integrity
            if random.random() < 0.6:
                heal = random.randint(1,3)
                integrity = min(10, integrity + heal)
                print(f'Ремонт удался: +{heal} прочности.')
            else:
                print('Ремонт не удался.')
        # random event: fuel leak
        if random.random() < 0.08:
            fuel_loss = 1
            fuel = max(0, fuel - fuel_loss)
            print('Утечка топлива: -1.')
        time.sleep(0.6)
    clear()
    if position >= distance and integrity > 0:
        print('Вы доехали до цели. Машина жива. Победа!')
    elif integrity <= 0:
        print('Машина вышла из строя. Проигрыш.')
    else:
        print('Игра окончена.')
    press_enter()
# -----------------------
# 1) Живой автомобиль с глазами на лобовом стекле и ртом
#    (Living Car with eyes and mouth) - flavor + simple state machine
# -----------------------
def living_car_with_face():
    clear()
    print('=== Живой автомобиль с глазами на лобовом стекле и ртом ===')
    distance = input_int('Дистанция (по умолчанию 25): ', 5) or 25
    fuel = input_int('Топливо (по умолчанию 8): ', 1) or 8
    mood = 5  # 0..10
    pos = 0
    print('Автомобиль "живой": его глаза моргают, рот реагирует на события.')
    press_enter()
    while pos < distance and fuel > 0 and mood > 0:
        clear()
        eyes = 'o o' if random.random() > 0.12 else '- -'  # blink sometimes
        mouth = ':)' if mood >= 5 else ':('
        print(f'Eyes: {eyes}   Mouth: {mouth}')
        print(f'Позиция: {pos}/{distance}  Топливо: {fuel}  Настроение: {mood}/10')
        action = input('Действие: drive/refuel/talk/exit: ').strip().lower()
        if action == 'exit' or action == '':
            break
        if action == 'drive':
            if fuel <= 0:
                print('Нет топлива!')
            else:
                step = random.randint(2,4)
                pos += step
                fuel -= 1
                mood = max(0, mood - (0 if random.random() < 0.8 else 1))
                print(f'Едем: +{step}')
        elif action == 'refuel':
            if random.random() < 0.75:
                gained = random.randint(2,4)
                fuel += gained
                mood = min(10, mood + 1)
                print(f'Заправлено +{gained}. Машина довольна.')
            else:
                mood -= 1
                print('Плохая заправка — машина обиделась.')
        elif action == 'talk':
            phrase = input('Что сказать машине? ')
            # simple sentiment: short happy words increase mood
            if any(w in phrase.lower() for w in ('хорошо','молодец','добра','класс','спасибо')):
                mood = min(10, mood + 2)
                print('Машина улыбается!')
            else:
                mood = min(10, mood + 0)
                print('Машина издаёт: vroom.')
        # random events
        if random.random() < 0.1:
            print('Машина подмигнула вам!')
            mood = min(10, mood + 1)
        time.sleep(0.6)
    clear()
    if pos >= distance:
        print('Вы доехали! Машина ликует: O O  :D')
    elif fuel <= 0:
        print('Вы встали без топлива. Машина грустит :(')
    elif mood <= 0:
        print('Машина совсем расстроена и отказывается ехать.')
    press_enter()

# -----------------------
# 2) Красный свет - зелёный свет (Red Light, Green Light)
# -----------------------
def red_green_light():
    clear()
    print('=== Красный свет - зелёный свет ===')
    distance = input_int('Расстояние до финиша (по умолчанию 15): ', 5) or 15
    pos = 0
    rounds = 0
    print('В зелёный ходите (w), на красный нельзя двигаться — будете пойманы.')
    press_enter()
    while pos < distance:
        rounds += 1
        green = random.random() < 0.6  # chance green
        state = 'ЗЕЛЁНЫЙ' if green else 'КРАСНЫЙ'
        clear()
        print(f'Раунд {rounds}. Свет: {state}. Позиция: {pos}/{distance}')
        cmd = input('Ввод (w - шаг, s - стоять, q - выход): ').strip().lower()
        if cmd == 'q' or cmd == '':
            break
        if cmd == 'w':
            if green:
                pos += 1
                print('Вы шагнули вперёд.')
            else:
                print('Ой! На красный — вас заметили. Вы проиграли.')
                press_enter()
                return
        else:
            print('Стоите на месте.')
        time.sleep(0.4)
    if pos >= distance:
        print('Вы добрались до финиша! Победа.')
    press_enter()

# -----------------------
# 3) Третий лишний (Odd One Out) - простая викторина
# -----------------------
def odd_one_out():
    clear()
    print('=== Третий лишний ===')
    rounds = input_int('Сколько раундов? (по умолчанию 5): ', 1) or 5
    score = 0
    examples = [
        (['apple','pear','carrot'], 'carrot'),
        (['cat','dog','car'], 'car'),
        (['red','blue','circle'], 'circle'),
        (['lion','tiger','shark'], 'shark'),
        (['hammer','screwdriver','banana'], 'banana'),
    ]
    for i in range(rounds):
        pair = random.choice(examples)
        items = pair[0]
        odd = pair[1]
        shuffled = items[:]
        random.shuffle(shuffled)
        print(f'Найдите лишний: {", ".join(shuffled)}')
        ans = input('Ваш ответ: ').strip().lower()
        if ans == odd:
            print('Верно!')
            score += 1
        else:
            print(f'Неверно. Правильный: {odd}')
        time.sleep(0.4)
    print(f'Итог: {score}/{rounds}')
    press_enter()

# -----------------------
# 4) Сахарные соты (Sugar Hives) - match puzzle: pick adjacent to form triples
# -----------------------
def sugar_hives():
    clear()
    print('=== Сахарные соты ===')
    rows = input_int('Рядов (по умолчанию 5): ', 3) or 5
    cols = input_int('Столбцов (по умолчанию 6): ', 3) or 6
    types = ['*', '#', '@', '%']
    grid = [[random.choice(types) for _ in range(cols)] for __ in range(rows)]
    score = 0
    def render():
        clear()
        for r in range(rows):
            print(' '.join(grid[r]))
        print('Score:', score)
    press_enter()
    while True:
        render()
        print('Выберите две соседние клетки, чтобы попытаться создать тройку.')
        cmd = input('Формат: r1 c1 r2 c2 (Enter выйти): ').strip()
        if cmd == '':
            break
        parts = cmd.split()
        if len(parts) != 4:
            print('Неверный ввод.')
            time.sleep(0.5); continue
        r1,c1,r2,c2 = map(int, parts)
        if not (0<=r1<rows and 0<=r2<rows and 0<=c1<cols and 0<=c2<cols):
            print('Координаты вне диапазона. Начинайте с 0.')
            time.sleep(0.5); continue
        # swap
        grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
        # check for any triples horizontally or vertically
        removed = False
        to_remove = [[False]*cols for _ in range(rows)]
        # horizontal
        for r in range(rows):
            run_char = None; run_len = 0; run_start = 0
            for c in range(cols):
                ch = grid[r][c]
                if ch == run_char:
                    run_len += 1
                else:
                    if run_len >= 3:
                        for k in range(run_start, run_start+run_len):
                            to_remove[r][k] = True
                    run_char = ch; run_len = 1; run_start = c
            if run_len >= 3:
                for k in range(run_start, run_start+run_len):
                    to_remove[r][k] = True
        # vertical
        for c in range(cols):
            run_char = None; run_len = 0; run_start = 0
            for r in range(rows):
                ch = grid[r][c]
                if ch == run_char:
                    run_len += 1
                else:
                    if run_len >= 3:
                        for k in range(run_start, run_start+run_len):
                            to_remove[k][c] = True
                    run_char = ch; run_len = 1; run_start = r
            if run_len >= 3:
                for k in range(run_start, run_start+run_len):
                    to_remove[k][c] = True
        # remove and collapse
        rem_count = sum(1 for r in range(rows) for c in range(cols) if to_remove[r][c])
        if rem_count == 0:
            print('Нет тройки — обмен отменён.')
            # swap back
            grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
            time.sleep(0.6)
        else:
            removed = True
            score += rem_count
            print(f'Удалено {rem_count}!')
            for c in range(cols):
                col_stack = [grid[r][c] for r in range(rows) if not to_remove[r][c]]
                # fill from bottom
                for r in range(rows-1, -1, -1):
                    val = col_stack.pop() if col_stack else random.choice(types)
                    grid[r][c] = val
            time.sleep(0.6)
    print('Игра окончена. Счёт:', score)
    press_enter()

# -----------------------
# 5) Последний выживший (Last Survivor) - simple elimination rounds
# -----------------------
def last_survivor():
    clear()
    print('=== Последний выживший ===')
    n = input_int('Игроков (включая вас) (по умолчанию 8): ', 2) or 8
    players = ['You'] + [f'P{i}' for i in range(2, n+1)]
    alive = set(players)
    round_no = 0
    while len(alive) > 1:
        round_no += 1
        clear()
        print(f'Раунд {round_no}. Живые: {len(alive)} -> {", ".join(sorted(alive))}')
        action = input('Нажмите Enter чтобы сыграть раунд, q - выйти: ').strip().lower()
        if action == 'q':
            break
        # random elimination based on skill/fortune
        elim_count = random.randint(1, max(1, len(alive)//4))
        eliminated = random.sample(list(alive), elim_count)
        for e in eliminated:
            alive.remove(e)
        print('Выбыло:', ', '.join(eliminated))
        time.sleep(0.8)
    if 'You' in alive:
        print('Вы — последний выживший! Победа!')
    else:
        print('Вы не выдержали. Игра окончена.')
    press_enter()

# -----------------------
# 6) Стеклянный мост (Glass Bridge) - choose safe tiles
# -----------------------
def glass_bridge():
    clear()
    print('=== Стеклянный мост ===')
    length = input_int('Длина моста (по умолчанию 12): ', 4) or 12
    # each step has two tiles (left/right), only one safe
    safe = [random.choice(['L','R']) for _ in range(length)]
    pos = 0
    print('На каждом шаге выберите L или R. Неправильный шаг — падение.')
    press_enter()
    while pos < length:
        clear()
        print(f'Шаг {pos+1}/{length}')
        choice = input('Выберите (L/R): ').strip().upper()
        if choice == '':
            print('Вы вышли.')
            break
        if choice not in ('L','R'):
            print('Неверный ввод.')
            time.sleep(0.5); continue
        if choice == safe[pos]:
            print('Удачно! Идём дальше.')
            pos += 1
        else:
            print('Хруст! Вы упали через стекло.')
            press_enter()
            return
    print('Вы прошли мост. Ура!')
    press_enter()

# -----------------------
# 7) Драка (Fight) - simple turn-based with choices
# -----------------------
def fight_game():
    clear()
    print('=== Драка ===')
    enemy_hp = random.randint(8,15)
    your_hp = random.randint(8,15)
    print(f'Противник HP: {enemy_hp}. Ваш HP: {your_hp}.')
    press_enter()
    while enemy_hp>0 and your_hp>0:
        clear()
        print(f'Ваш HP: {your_hp}  Противник HP: {enemy_hp}')
        move = choose('Выберите действие:', ['удар', 'блок', 'спец (риск)'])
        if move == 'удар':
            dmg = random.randint(2,5)
            enemy_hp -= dmg
            print(f'Вы нанесли {dmg}')
        elif move == 'блок':
            print('Вы в блоке, уменьшаете следующий урон.')
            # next enemy attack reduced
            block = True
        else:
            if random.random() < 0.6:
                dmg = random.randint(5,9)
                enemy_hp -= dmg
                print(f'Удачный спец: {dmg}')
            else:
                back = random.randint(1,4)
                your_hp -= back
                print(f'Провал спец — вы получили {back}')
        # enemy turn
        if enemy_hp <= 0: break
        eact = random.choice(['hit','hit','hit','heavy','miss'])
        if eact == 'hit':
            dmg = random.randint(1,4)
            if move == 'блок':
                dmg = max(0, dmg-2)
            your_hp -= dmg
            print(f'Противник нанес {dmg}')
        elif eact == 'heavy':
            dmg = random.randint(3,6)
            your_hp -= dmg
            print(f'Сильный удар! -{dmg}')
        else:
            print('Противник промахнулся.')
        time.sleep(0.8)
    if your_hp > 0:
        print('Вы победили в драке!')
    else:
        print('Вы потерпели поражение.')
    press_enter()

# -----------------------
# 8) Сумо (Sumo) - push opponent off ring (1D)
# -----------------------
def sumo():
    clear()
    print('=== Сумо ===')
    ring = input_int('Размер ринга (по умолчанию 9): ', 5) or 9
    center = ring//2
    pos_you = center - 1
    pos_enemy = center + 1
    print('Цель: вытолкнуть противника за грань (0..n-1). Управление: l/r push.')
    press_enter()
    while 0 <= pos_you < ring and 0 <= pos_enemy < ring:
        clear()
        field = ['.']*ring
        field[pos_you] = 'Y'
        field[pos_enemy] = 'E'
        print(''.join(field))
        action = input('Ваш ход (l/r/q): ').strip().lower()
        if action == 'q' or action == '':
            break
        # player attempt to push towards enemy
        if action == 'r' and pos_you < pos_enemy:
            # attempt to push enemy right
            if random.random() < 0.6:
                pos_enemy += 1
                print('Вы толкнули противника!')
            else:
                pos_you -= 1
                print('Промах — вы теряете равновесие и отходите назад.')
        elif action == 'l' and pos_you > pos_enemy:
            if random.random() < 0.6:
                pos_enemy -= 1
                print('Вы толкнули противника!')
            else:
                pos_you += 1
                print('Промах — отступаете.')
        else:
            print('Неверное направление для толчка.')
        # enemy AI tries to push you back
        if 0 <= pos_enemy < ring and 0 <= pos_you < ring:
            if random.random() < 0.65:
                # attempts to push towards your side
                if pos_enemy > pos_you:
                    pos_you -= 1
                else:
                    pos_you += 1
                print('Противник ответил толчком.')
        time.sleep(0.6)
    if not (0 <= pos_enemy < ring):
        print('Противник вылетел — вы победили!')
    elif not (0 <= pos_you < ring):
        print('Вы вылетели — проигрыш.')
    else:
        print('Игра закончена.')
    press_enter()

# -----------------------
# 9) Карате (Karate) - quick reflex mini-game (timing)
# -----------------------
def karate():
    clear()
    print('=== Карате ===')
    rounds = input_int('Раундов (по умолчанию 5): ', 1) or 5
    score = 0
    print('Ждите сигнала "STRIKE!" и нажмите Enter как можно быстрее.')
    press_enter()
    for r in range(rounds):
        clear()
        wait = random.uniform(1.0, 3.0)
        print(f'Раунд {r+1}/{rounds}: готовьтесь...')
        time.sleep(wait)
        t0 = time.time()
        print('STRIKE! Нажмите Enter!')
        input()
        dt = time.time() - t0
        print(f'Ваша реакция: {dt:.3f}s')
        if dt < 0.3:
            print('Отлично!')
            score += 2
        elif dt < 0.6:
            print('Хорошо.')
            score += 1
        else:
            print('Медленно.')
        time.sleep(0.6)
    print('Итоговый счёт:', score)
    press_enter()

# -----------------------
# 10) Всё оживает! (Everything Comes Alive) - randomized "items" with behaviors
# -----------------------
def everything_alive():
    clear()
    print('=== Всё оживает! ===')
    items = ['стул', 'лампа', 'часы', 'картина', 'клавиатура']
    living = {name: {'mood': random.randint(0,5)} for name in items}
    rounds = input_int('Сколько раундов наблюдать? (по умолчанию 8): ', 1) or 8
    print('Предметы получают настроение и действуют случайно.')
    press_enter()
    for r in range(rounds):
        clear()
        print(f'Раунд {r+1}/{rounds}')
        for name, state in living.items():
            # random action based on mood
            act_roll = random.random()
            if act_roll < 0.2:
                action = 'шевелится'
                state['mood'] = min(10, state['mood']+1)
            elif act_roll < 0.5:
                action = 'звенит' if name == 'часы' else 'мигает' if name == 'лампа' else 'скрипит'
                state['mood'] = max(0, state['mood']-1)
            else:
                action = 'молчит'
            print(f'{name.capitalize()} [{state["mood"]}/10]: {action}')
        # possible interaction: items influence each other
        if random.random() < 0.3:
            a,b = random.sample(items,2)
            living[a]['mood'] = min(10, living[a]['mood'] + 1)
            living[b]['mood'] = max(0, living[b]['mood'] - 1)
            print(f'Взаимодействие: {a} подтолкнул {b}.')
        time.sleep(1.0)
    print('Наблюдение окончено.')
    press_enter()
# -----------------------
# Game: Болтай с ожившими предметами
# Care for, observe and talk to your living items.
# -----------------------
def chat_with_items():
    clear()
    print('=== Болтай с ожившими предметами ===')
    items = {
        'стул': {'mood': 5, 'hunger': 0},
        'лампа': {'mood': 4, 'hunger': 0},
        'часы': {'mood': 6, 'hunger': 0}
    }
    rounds = input_int('Сколько взаимодействий? (по умолчанию 8): ', 1) or 8
    print('Вы можете кормить, ремонтировать, говорить и наблюдать. Цель: поддерживать настроение выше 3.')
    press_enter()
    for r in range(1, rounds+1):
        clear()
        print(f'Раунд {r}/{rounds}')
        for name, st in items.items():
            print(f' - {name}: настроение {st["mood"]}/10, голод {st["hunger"]}')
        choice = input('Выберите предмет для взаимодействия (имя) или "all" (Enter для случайного): ').strip().lower()
        if choice == '':
            choice = random.choice(list(items.keys()))
            print('Автовыбор:', choice)
        if choice == 'all':
            targets = list(items.keys())
        elif choice in items:
            targets = [choice]
        else:
            print('Неверный выбор.')
            time.sleep(0.6)
            continue
        action = input('Действие: talk/feed/fix/watch: ').strip().lower()
        for t in targets:
            st = items[t]
            if action == 'talk':
                # random positive or neutral effect
                if random.random() < 0.6:
                    delta = 1
                    st['mood'] = min(10, st['mood'] + delta)
                    print(f'Вы поговорили с {t}. Настроение +{delta}.')
                else:
                    print(f'{t} молчит...')
            elif action == 'feed':
                st['hunger'] = max(0, st['hunger'] - 1)
                st['mood'] = min(10, st['mood'] + 1)
                print(f'Покормили {t}.')
            elif action == 'fix':
                if random.random() < 0.7:
                    st['mood'] = min(10, st['mood'] + 2)
                    print(f'Починили {t}. Он радуется!')
                else:
                    st['mood'] = max(0, st['mood'] -1)
                    print(f'Ремонт прошёл плохо. {t} расстроен.')
            elif action == 'watch':
                # observationally learn: maybe increase mood
                if random.random() < 0.4:
                    st['mood'] = min(10, st['mood'] + 1)
                    print(f'{t} заметил вашу заботу. Настроение +1.')
                else:
                    print(f'Вы просто наблюдали за {t}.')
            else:
                print('Неизвестное действие.')
        # natural decay / random
        for st in items.values():
            if random.random() < 0.25:
                st['mood'] = max(0, st['mood'] - 1)
                st['hunger'] = min(5, st['hunger'] + 1)
        time.sleep(0.8)
    clear()
    print('Итоги заботы:')
    for name, st in items.items():
        print(f'{name}: настроение {st["mood"]}/10, голод {st["hunger"]}')
    press_enter()

# -----------------------
# Game: Комнаты
# Move through rooms and hide to survive monsters.
# -----------------------
def rooms_game():
    clear()
    print('=== Комнаты ===')
    count = input_int('Сколько комнат (по умолчанию 10): ', 5) or 10
    rooms = [{'monster': (random.random() < 0.25), 'searched': False} for _ in range(count)]
    player = 0
    hiding = False
    print('Вы перемещаетесь по комнатам 0..N-1. Если в комнате монстр и вы не спрятаны — вам повезёт не всегда.')
    press_enter()
    while True:
        clear()
        print(f'Комната {player}/{count-1}  {"(спрятан)" if hiding else ""}')
        print('Соседние комнаты: ', end='')
        if player>0: print(player-1, end=' ')
        print(player+1 if player<count-1 else '', end='\n')
        cmd = input('Действия: move <L/R>, hide, search, q: ').strip().lower()
        if cmd == 'q' or cmd == '':
            break
        if cmd.startswith('move'):
            parts = cmd.split()
            if len(parts) == 2 and parts[1].upper() in ('L','R'):
                dirc = parts[1].upper()
                target = player-1 if dirc=='L' else player+1
                if 0 <= target < count:
                    player = target
                    hiding = False
                    print('Вы вошли в комнату', player)
                    # check monster
                    if rooms[player]['monster']:
                        if hiding:
                            print('Монстр не заметил вас (всё ещё спрятаны).')
                        else:
                            # encounter: chance to escape if you moved quickly
                            if random.random() < 0.5:
                                print('Вам повезло — монстр не заметил!')
                            else:
                                print('Монстр заметил вас и съел. Конец игры.')
                                press_enter()
                                return
                else:
                    print('Нельзя туда идти.')
            else:
                print('Неправильное направление. move L или move R.')
        elif cmd == 'hide':
            hiding = True
            print('Вы спрятались в комнате.')
        elif cmd == 'search':
            if rooms[player]['searched']:
                print('Уже обыскано.')
            else:
                rooms[player]['searched'] = True
                if random.random() < 0.4:
                    print('Вы нашли полезный предмет (еда).')
                else:
                    print('Пусто.')
        else:
            print('Неизвестная команда.')
        time.sleep(0.6)

# -----------------------
# Game: Монстр
# Move on grid, avoid monster chasing you.
# -----------------------
def monster_game():
    clear()
    print('=== Монстр ===')
    size = input_int('Размер стороны поля (по умолчанию 7): ', 4) or 7
    player = [0, 0]
    monster = [size-1, size-1]
    steps = 0
    print('Уходите от монстра. Двигайтесь w/a/s/d. Доберитесь до противоположного угла, чтобы выжить.')
    press_enter()
    while True:
        clear()
        for r in range(size):
            line = ''
            for c in range(size):
                if [r,c] == player: line += 'P '
                elif [r,c] == monster: line += 'M '
                elif [r,c] == [size-1, size-1]: line += 'G '
                else: line += '. '
            print(line)
        if player == monster:
            print('Монстр поймал вас. Вы проиграли.')
            press_enter()
            return
        if player == [size-1, size-1]:
            print('Вы добрались до точки спасения. Победа!')
            press_enter()
            return
        cmd = input('Ход (w/a/s/d, q выход): ').strip().lower()
        if cmd == 'q' or cmd == '':
            break
        if cmd == 'w' and player[0]>0: player[0]-=1
        if cmd == 's' and player[0]<size-1: player[0]+=1
        if cmd == 'a' and player[1]>0: player[1]-=1
        if cmd == 'd' and player[1]<size-1: player[1]+=1
        # monster moves towards player (simple greedy)
        if monster[0] < player[0]: monster[0] += 1
        elif monster[0] > player[0]: monster[0] -= 1
        if monster[1] < player[1]: monster[1] += 1
        elif monster[1] > player[1]: monster[1] -= 1
        # occasional monster sprint
        if random.random() < 0.12:
            if monster[0] < player[0]: monster[0] += 1
            elif monster[0] > player[0]: monster[0] -= 1
        steps += 1

# -----------------------
# Game: Катастрофа
# Survive natural disasters for N turns.
# -----------------------
def catastrophe():
    clear()
    print('=== Катастрофа ===')
    days = input_int('Сколько дней выжить? (по умолчанию 7): ', 1) or 7
    health = 10
    supplies = 5
    for d in range(1, days+1):
        clear()
        print(f'День {d}/{days}. Здоровье {health}, запасы {supplies}.')
        event = random.choice(['earthquake','flood','heat','drought','calm'])
        print('Сегодня: ', event)
        action = input('Действие: prepare/use/rest (Enter пропустить): ').strip().lower()
        if action == 'prepare' and supplies>0:
            supplies -= 1
            print('Вы подготовились, риск снизился.')
            mitigate = True
        else:
            mitigate = False
        # resolve event
        if event == 'earthquake':
            dmg = 3 if not mitigate else 1
            health -= dmg
            print(f'Землетрясение: -{dmg} здоровья.')
        elif event == 'flood':
            if not mitigate:
                supplies = max(0, supplies-2)
                print('Наводнение: потеря запасов.')
            else:
                print('Подготовка помогла.')
        elif event == 'heat':
            health -= 1
            supplies = max(0, supplies-1)
            print('Жара: -1 здоровье, -1 запасы.')
        elif event == 'drought':
            supplies = max(0, supplies-2)
            if supplies==0:
                health -= 2
                print('Засуха, нехватка ресурсов: -2 здоровья.')
            else:
                print('Справились с засухой.')
        else:
            print('Спокойный день.')
        if health <= 0:
            print('Вы не пережили катастрофию...')
            press_enter()
            return
        time.sleep(0.8)
        press_enter()
    print('Вы выжили в серии катастроф. Поздравляю!')
    press_enter()

# -----------------------
# Game: Преследование (player is chaser)
# Like dogonalki but player chases AI who runs away.
# -----------------------
def pursuit_player_chaser():
    clear()
    print('=== Преследование (ты — преследователь) ===')
    length = input_int('Длина трека (по умолчанию 25): ', 10) or 25
    runner = 0
    chaser = -3
    print('Вы — C (преследователь). Бегун — R. Команды: run (двигаться быстрее) или sneak (медленнее).')
    press_enter()
    turn = 0
    while True:
        turn += 1
        clear()
        track = ['.']*length
        if 0 <= runner < length: track[runner] = 'R'
        if 0 <= chaser < length:
            if track[chaser] == 'R': track[chaser] = 'X'
            else: track[chaser] = 'C'
        print(''.join(track))
        move = input('Ваш ход (run/sneak/q): ').strip().lower()
        if move == 'q' or move == '':
            break
        if move == 'run':
            chaser += random.randint(2,4)
        else:
            chaser += random.randint(0,2)
        # runner moves away trying to keep distance
        dist = chaser - runner
        if dist >= -2:
            runner += random.randint(1,3)  # runs faster if close
        else:
            runner += random.randint(0,2)
        runner = min(runner, length-1)
        chaser = min(chaser, length-1)
        if chaser >= runner:
            clear()
            print('Вы догнали бегуна! Победа.')
            press_enter()
            return
        if runner >= length-1:
            clear()
            print('Бегун добежал до финиша и спасся.')
            press_enter()
            return
        time.sleep(0.5)

# -----------------------
# Game: Преследование с мячом (player chaser)
# Player tries to take ball from runner and reach goal.
# -----------------------
def pursuit_with_ball_player_chaser():
    clear()
    print('=== Преследование с мячом (ты — преследователь) ===')
    length = input_int('Длина поля (по умолчанию 22): ', 10) or 22
    runner = 0
    chaser = -3
    ball_holder = 'Runner'
    print('Вы — преследователь (C). Бегун (R) обычно держит мяч. Догоните и заберите мяч!')
    press_enter()
    while True:
        clear()
        field = ['.']*length
        if 0 <= runner < length:
            field[runner] = 'R' if ball_holder!='Runner' else 'B'  # B means runner has ball
        if 0 <= chaser < length:
            field[chaser] = 'C'
        print(''.join(field))
        action = input('Ваш ход (run/sneak/tackle/q): ').strip().lower()
        if action == 'q' or action == '':
            break
        if action == 'run':
            chaser += random.randint(2,4)
        elif action == 'sneak':
            chaser += random.randint(0,2)
        elif action == 'tackle':
            # attempt to steal if close
            if abs(chaser - runner) <= 2 and random.random() < 0.6:
                ball_holder = 'Chaser'
                print('Ура! Вы отобрали мяч.')
            else:
                print('Тэкл не удался.')
        # runner moves
        if ball_holder == 'Runner':
            runner += random.randint(1,3)
        else:
            # runner may try to recover ball or stop moving faster
            runner += random.randint(0,2)
        runner = min(runner, length-1)
        chaser = min(chaser, length-1)
        if chaser >= runner and ball_holder == 'Chaser':
            clear()
            print('Вы догнали бегуна и отобрали мяч — победа!')
            press_enter()
            return
        if runner >= length-1 and ball_holder == 'Runner':
            clear()
            print('Бегун с мячом дошёл до финиша — вы проиграли.')
            press_enter()
            return
        time.sleep(0.6)

# -----------------------
# Game: Сказка
# Perform actions that help heroes from different tales.
# -----------------------
def fairy_tale():
    clear()
    print('=== Сказка ===')
    heroes = [
        {'name':'Иван-дурак','need':'find a magic sword'},
        {'name':'Царь-девица','need':'find a lost jewel'},
        {'name':'Коловрат','need':'defeat a dragon'}
    ]
    score = 0
    print('Вы встречаете героев и можете совершить одно событие, которое поможет им.')
    press_enter()
    for h in heroes:
        clear()
        print(f'Герой: {h["name"]}. Ему нужно: {h["need"]}')
        action = choose = input('Как поможете? (gift/action/trick/skip): ').strip().lower()
        if action == 'gift':
            print('Вы подарили полезный предмет.')
            score += 1
        elif action == 'action':
            success = random.random() < 0.6
            if success:
                print('Ваша помощь оказалась эффективной!')
                score += 2
            else:
                print('Попытка неудачна.')
        elif action == 'trick':
            if random.random() < 0.4:
                print('Вы хитро обманули врагов — полезный эффект.')
                score += 1
            else:
                print('Хитрость вернулась бумерангом.')
                score -= 1
        else:
            print('Пропуск.')
        time.sleep(0.7)
    clear()
    print('Итоговая помощь героям. Очки доблести:', score)
    press_enter()

# -----------------------
# Game: Проклятие
# Each round roam the house; each round an effect appears (positive or negative).
# -----------------------
def curse_game():
    clear()
    print('=== Проклятие ===')
    rooms = input_int('Сколько комнат в доме (по умолчанию 6): ', 3) or 6
    day_limit = input_int('Сколько раундов бродить? (по умолчанию 10): ', 1) or 10
    player_room = 0
    health = 10
    curses = [
        ('shadow', lambda h: (h-2, 'Тень укусила вас: -2 здоровья.')),
        ('blessing', lambda h: (h+2, 'Таинство помогло: +2 здоровья.')),
        ('freeze', lambda h: (h-1, 'Замерзание: -1 здоровья.')),
        ('feast', lambda h: (h+1, 'Неожиданная еда: +1 здоровья.')),
        ('curse_sleep', lambda h: (max(0,h-1), 'Проклятье усталости: -1 здоровья.')),
        ('mana', lambda h: (h+1, 'Магия наполнила вас: +1 здоровья.')),
    ]
    print('Вы бродите по дому. В каждой комнате каждый раунд может проявиться эффект.')
    press_enter()
    for day in range(1, day_limit+1):
        clear()
        print(f'Раунд {day}/{day_limit}. Комната {player_room}. Здоровье: {health}')
        print('Доступные команды: move L/R, stay, q - выход')
        cmd = input('> ').strip().lower()
        if cmd == 'q' or cmd == '':
            break
        if cmd.startswith('move'):
            parts = cmd.split()
            if len(parts)==2 and parts[1].upper() in ('L','R'):
                nr = player_room-1 if parts[1].upper()=='L' else player_room+1
                if 0 <= nr < rooms:
                    player_room = nr
                    print('Вы вошли в комнату', player_room)
                else:
                    print('Нельзя идти туда.')
            else:
                print('Неверная команда move L или move R.')
        elif cmd == 'stay':
            print('Вы остаетесь на месте и наблюдаете.')
        else:
            print('Неверная команда.')
        # effect appears
        effect = random.choice(curses)
        health, msg = effect[1](health)
        print('Эффект:', msg)
        # sometimes the effect spreads creating room-wide persistent modifier
        if random.random() < 0.12:
            print('Эффект закрепился в комнате — будьте внимательны при следующем входе.')
            # simulate by immediate extra penalty/bonus next time (simple: immediate)
            if random.random() < 0.5:
                health += 1
                print('Доп. благотворный эффект +1')
            else:
                health -= 1
                print('Доп. вредный эффект -1')
        time.sleep(0.8)
        if health <= 0:
            print('Вы погибли от проклятия...')
            press_enter()
            return
        press_enter()
    print('Вы прошли через проклятие. Финальное здоровье:', health)
    press_enter()

# -----------------------
# Helper choose func used in fairy_tale fallback
# -----------------------
def choose(prompt, options):
    print(prompt)
    for i, o in enumerate(options, 1):
        print(f'{i}. {o}')
    sel = input_int('Выберите номер: ', 1, len(options))
    if sel is None:
        return options[0]
    return options[sel-1]
# -----------------------
# Game: Настолка "Бункер"
# Description:
# - 7 players (including you); there are 2 spots (places) meaning some mechanic? 
# Interpretation: 7 players assigned fake "age" and "profession" traits; each player in turn reveals their age & profession.
#   Then, in player turns, they may reveal any one of: Hobby / Phobia / Health / Fact / Occupation (we already have occupation -> profession; treat Occupation as secondary)
# - After all reveals, group votes; the player with most votes is eliminated.
# Implemented in purely textual manner with random NPC attributes and simple voting.
# -----------------------
def bunker_boardgame():
    clear()
    print('=== Настолка "Бункер" ===')
    # Setup 7 players (You + 6 NPCs). "Мест 2" interpreted that there are 2 survival spots? We'll treat final stage as 2 survivors left safe.
    n_players = 7
    names = ['You'] + [f'NPC{i}' for i in range(1, n_players)]
    # random attributes pool
    professions = ['Врач','Инженер','Фермер','Учитель','Программист','Повар','Художник','Пилот']
    hobbies = ['рыбалка','шахматы','садоводство','танцы','чтение','видеоигры','кулинария']
    phobias = ['акрофобия','клаустрофобия','аквафобия','арахнофобия','аэрофобия']
    healths = ['здоров','аллергия','астма','сердечное','хроническая усталость']
    facts = ['бегает марафон','говорит 4 языка','участвовал в конкурсе','выращивал редкие растения']
    occupations = ['менеджер','фрилансер','солдат','администратор','архитектор']

    players = []
    for nm in names:
        profile = {
            'name': nm,
            'age': random.randint(18,70) if nm!='You' else None,  # you will be prompted
            'profession': random.choice(professions) if nm!='You' else None,
            'hobby': random.choice(hobbies),
            'phobia': random.choice(phobias),
            'health': random.choice(healths),
            'fact': random.choice(facts),
            'occupation': random.choice(occupations),
        }
        players.append(profile)

    # If player is You, ask for age/profession (optional)
    clear()
    print('Введите, пожалуйста, ваш возраст и профессию (можно оставить пустым для авто).')
    a = input('Ваш возраст (Enter — случайно): ').strip()
    if a.isdigit():
        players[0]['age'] = int(a)
    else:
        players[0]['age'] = random.randint(18,70)
    p = input('Ваша профессия (Enter — случайно): ').strip()
    players[0]['profession'] = p if p else random.choice(professions)

    press_enter()

    # Round: each player reveals basic info (age/profession). Then each in turn may reveal one of five detailed categories.
    clear()
    print('Раунд раскрытий: каждый игрок по очереди показывает возраст и профессию.')
    for prof in players:
        print(f"{prof['name']}: возраст {prof['age']}, профессия {prof['profession']}")
        time.sleep(0.5)
    press_enter()

    details = ['hobby','phobia','health','fact','occupation']
    print('Теперь по очереди каждый игрок может раскрыть один подробный пункт: Хобби, Фобия, Здоровье, Факт или Занятие.')
    revealed = {pl['name']: {} for pl in players}
    for pl in players:
        clear()
        print(f"Ход игрока: {pl['name']}")
        # NPC chooses randomly; You choose
        if pl['name'] == 'You':
            opt_idx = choose_option('Что раскрыть?', ['Hobby','Phobia','Health','Fact','Occupation','Skip'])
            if opt_idx is None or opt_idx==5:
                print('Пропуск.')
            else:
                key = details[opt_idx]
                revealed[pl['name']][key] = pl[key]
                print(f'Вы раскрыли: {key} -> {pl[key]}')
        else:
            key = random.choice(details)
            revealed[pl['name']][key] = pl[key]
            print(f'{pl["name"]} раскрыл {key}: {pl[key]}')
        time.sleep(0.7)
    press_enter()

    # After all reveals, voting: players vote who to eliminate. NPCs vote with some heuristic: pick someone with suspicious phobia or low health or random.
    clear()
    print('Начинается голосование! Тот, кто набрал больше всего голосов — выбывает. (2 места в бункере — значит выбывает 5, остаются 2)')
    votes = {pl['name']:0 for pl in players}
    for voter in players:
        if voter['name'] == 'You':
            # show profiles briefly for user decision
            print('Игроки и раскрытые детали:')
            for pl in players:
                print(f' - {pl["name"]}: возраст {pl["age"]}, профессия {pl["profession"]}, раскрыто: {revealed[pl["name"]]}')
            choice = input('За кого голосуете? Введите имя: ').strip()
            if choice not in votes:
                choice = random.choice(list(votes.keys()))
                print('Неверное имя — голос случайно за', choice)
            votes[choice] += 1
        else:
            # NPC heuristic
            # target players with low health or weird phobia or hobby mismatch
            candidates = [p for p in players if p['name'] != voter['name']]
            # weight: if revealed shows unhealthy or odd phobia increase weight
            weights = []
            for c in candidates:
                w = 1.0
                r = revealed[c['name']]
                if 'health' in r and ('серд' in r['health'] or 'хро' in r['health']):
                    w += 2.0
                if 'phobia' in r and r['phobia'] in ('арахнофобия','аквафобия'):
                    w += 1.0
                if c['name'] == 'You':
                    w += 0.5  # slight bias
                weights.append(w)
            # choose by weights
            total = sum(weights)
            pick = random.random() * total
            acc = 0
            for cand, wt in zip(candidates, weights):
                acc += wt
                if pick <= acc:
                    votes[cand['name']] += 1
                    break
    # Tally and eliminate until 2 remain
    sorted_votes = sorted(votes.items(), key=lambda x: (-x[1], x[0]))
    clear()
    print('Результаты голосования:')
    for name, v in sorted_votes:
        print(f'{name}: {v} голос(ов)')
    # Determine eliminated: keep top 2 survivors by random tie-breaker
    # We should eliminate n_players - 2
    to_eliminate_count = len(players) - 2
    # Rank by votes descending; if tie among boundary, random tiebreak
    ranked = sorted(votes.items(), key=lambda x: (-x[1], random.random()))
    eliminated = [name for name, _ in ranked[:to_eliminate_count]]
    survivors = [name for name, _ in ranked[to_eliminate_count:]]
    print('\nВыбывают:', ', '.join(eliminated))
    print('Остаются в бункере:', ', '.join(survivors))
    press_enter()

# -----------------------
# Game: Предатель (Traitor)
# Simple social deduction: there is 1 traitor among NPCs including maybe you. If you're traitor you act accordingly.
# Implement: roles assigned; night phase: traitor eliminates, day: accuse and vote to eject.
# -----------------------
def traitor_game():
    clear()
    print('=== Предатель ===')
    players = ['You'] + [f'P{i}' for i in range(1,6)]
    n = len(players)
    roles = {}
    # assign 1 traitor randomly; player could be traitor
    traitor = random.choice(players)
    for p in players:
        roles[p] = 'Traitor' if p == traitor else 'Innocent'
    print('Роли распределены. Ночное действие: предатель выбирает жертву.')
    press_enter()
    # night: traitor eliminates one (if traitor is You, ask)
    if roles['You'] == 'Traitor':
        print('Вы — предатель. Выберите жертву.')
        for i,p in enumerate(players):
            if p != 'You':
                print(i, p)
        idx = input_int('Введите индекс жертвы: ', 0, n-1)
        victim = players[idx] if idx is not None and players[idx] != 'You' else random.choice([p for p in players if p!='You'])
        print('Вы убили', victim)
    else:
        # traitor picks random victim (not himself)
        victim = random.choice([p for p in players if p != traitor])
        print('Ночью кто-то был убит:', victim)
    # remove victim
    alive = [p for p in players if p != victim]
    press_enter()
    # day: discuss and vote (simplified)
    print('Днём происходит обвинение. Каждый голосует за предполагаемого предателя.')
    votes = {p:0 for p in alive}
    for voter in alive:
        if voter == 'You':
            print('Кто остался жив? ', ', '.join(alive))
            choice = input('За кого голосуете (имя): ').strip()
            if choice not in votes:
                choice = random.choice([p for p in alive if p!='You'])
                print('Неверно, выбирается случайно:', choice)
            votes[choice] += 1
        else:
            # NPCs random suspicion, bias towards unusual names or those not themselves
            candidates = [p for p in alive if p != voter]
            pick = random.choice(candidates)
            votes[pick] += 1
    sorted_votes = sorted(votes.items(), key=lambda x: (-x[1], random.random()))
    accused, vcount = sorted_votes[0]
    clear()
    print('Голосование завершено. Обвинён:', accused, 'с', vcount, 'голами.')
    if roles.get(accused) == 'Traitor':
        print('Предатель найден! Победа мирных.')
    else:
        print('Неправильный выбор. Предатель остался на свободе.' )
    press_enter()

# -----------------------
# Game: Страх (Fear)
# Small psychological test: choose options; fear meter rises; survive choices.
# -----------------------
def fear_game():
    clear()
    print('=== Страх ===')
    fear = 0
    rounds = input_int('Сколько испытаний (по умолчанию 6): ', 1) or 6
    for r in range(1, rounds+1):
        clear()
        print(f'Испытание {r}/{rounds}. Уровень страха: {fear}/10')
        scenario = random.choice([
            ('темный коридор', 2),
            ('шум в подвале', 3),
            ('тень в окне', 1),
            ('странный шёпот', 4),
            ('движущийся шкаф', 3)
        ])
        print('Сценарий:', scenario[0])
        action = input('Выбор: Investigate / Run / Hide (i/r/h): ').strip().lower()
        if action == 'i':
            # increase or decrease randomly
            if random.random() < 0.4:
                fear = max(0, fear - 1)
                print('Вы храбры — страх уменьшается.')
            else:
                fear += scenario[1]
                print('Вы встревожены — страх растёт.')
        elif action == 'r':
            fear = max(0, fear - 1)
            print('Вы убегаете — стресс снижается, но усталость растёт.')
        else:
            fear += 1
            print('Вы прячетесь — страх медленно нарастает.')
        if fear >= 10:
            print('Страх достиг критического уровня — вы потеряли сознание.')
            press_enter()
            return
        time.sleep(0.6)
    print('Вы прошли испытания страхом. Уровень страха:', fear)
    press_enter()

# -----------------------
# Game: Паук (Spider)
# Mini-puzzle: traverse web cells without stepping on spider legs; small grid
# -----------------------
def spider_game():
    clear()
    print('=== Паук ===')
    size = input_int('Размер сети (сторона, по умолчанию 7): ', 5) or 7
    player = [0, size//2]
    # spider occupies center and has "legs" on nearby cells
    spider = [size//2, size//2]
    def legs_positions():
        poss = []
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr==0 and dc==0: continue
                rr, cc = spider[0]+dr, spider[1]+dc
                if 0 <= rr < size and 0 <= cc < size:
                    poss.append([rr,cc])
        return poss
    legs = legs_positions()
    print('Пройдите от левого края до правого, избегая ног паука (помечены X).')
    press_enter()
    while True:
        clear()
        for r in range(size):
            line = ''
            for c in range(size):
                if [r,c] == player: line += 'P '
                elif [r,c] == spider: line += 'S '
                elif [r,c] in legs: line += 'X '
                else: line += '. '
            print(line)
        if player[1] >= size-1:
            print('Вы добрались до края сети. Успех!')
            break
        cmd = input('Ход (w/a/s/d, q выход): ').strip().lower()
        if cmd == 'q' or cmd == '':
            break
        if cmd == 'w' and player[0]>0: player[0]-=1
        if cmd == 's' and player[0]<size-1: player[0]+=1
        if cmd == 'a' and player[1]>0: player[1]-=1
        if cmd == 'd' and player[1]<size-1: player[1]+=1
        # check if on leg
        if player in legs:
            print('Вы наступили на ногу паука — он укусил! Вы проиграли.')
            press_enter()
            return
        # occasional spider move/shuffle legs
        if random.random() < 0.2:
            # spider shifts one cell randomly
            spider[0] = min(size-1, max(0, spider[0] + random.choice([-1,0,1])))
            spider[1] = min(size-1, max(0, spider[1] + random.choice([-1,0,1])))
            legs = legs_positions()
        time.sleep(0.2)
    press_enter()

# -----------------------
# Game: День рождение (Birthday)
# Mini-game: organize party with tasks (cake, guests, games). Manage mood points.
# -----------------------
def birthday_game():
    clear()
    print('=== День рождения ===')
    days = 1
    mood = 5
    tasks = ['cake','music','guests','decor']
    completed = []
    print('Подготовьте праздник: выполните задачи для повышения настроения.')
    press_enter()
    for t in tasks:
        clear()
        print('Текущая задача:', t)
        act = input('Действие: do / skip (Enter skip): ').strip().lower()
        if act == 'do':
            success = random.random() < 0.8
            if success:
                mood += 1
                completed.append(t)
                print('Успешно выполнено!')
            else:
                mood -= 1
                print('Задача прошла не идеально.')
        else:
            print('Пропуск.')
        time.sleep(0.6)
    clear()
    print('Праздник готов! Выполнено:', ', '.join(completed))
    print('Итоговое настроение гостей:', mood)
    press_enter()

# -----------------------
# Game: Стоматолог (Dentist)
# Quick reflex: press Enter within short time window when drill sound occurs
# -----------------------
def dentist_game():
    clear()
    print('=== Стоматолог ===')
    rounds = input_int('Сколько процедур (по умолчанию 4): ', 1) or 4
    score = 0
    print('Реагируйте когда услышите "DRILL!" — нажмите Enter как можно быстрее.')
    press_enter()
    for i in range(rounds):
        clear()
        wait = random.uniform(0.8, 2.5)
        print('Ожидайте сигнал...')
        time.sleep(wait)
        t0 = time.time()
        print('DRILL! Нажмите Enter!')
        input()
        dt = time.time() - t0
        print(f'Ваша реакция: {dt:.3f}s')
        if dt < 0.35:
            score += 2
            print('Отлично — быстро.')
        elif dt < 0.7:
            score += 1
            print('Нормально.')
        else:
            print('Медленно; неприятно.')
        time.sleep(0.6)
    print('Результат процедур, очки:', score)
    press_enter()

# -----------------------
# Game: Аквафобия (Aquaphobia)
# Manage breath & panic while water rises. Choose actions to get air or calm down.
# -----------------------
def aquaphobia():
    clear()
    print('=== Аквафобия ===')
    breath = 10
    panic = 0
    oxygen_sources = 3
    rounds = input_int('Сколько шагов (по умолчанию 8): ', 3) or 8
    for r in range(1, rounds+1):
        clear()
        print(f'Раунд {r}/{rounds}. Дыхание: {breath}, Паника: {panic}, Источников O2: {oxygen_sources}')
        action = input('Действия: calm (умиротвориться), search (искать кислород), swim (двигаться вперед) [c/s/w]: ').strip().lower()
        if action == 'c':
            panic = max(0, panic - 1)
            breath = min(10, breath + 1)
            print('Вы стараетесь успокоиться.')
        elif action == 's':
            if oxygen_sources > 0 and random.random() < 0.6:
                oxygen_sources -= 1
                breath = min(10, breath + 3)
                print('Нашли пузырь воздуха!')
            else:
                breath = max(0, breath - 1)
                panic += 1
                print('Поиск не дал результата.')
        else:
            # swim
            if random.random() < 0.6:
                breath = max(0, breath - 1)
                print('Вы продвинулись.')
            else:
                panic += 1
                breath = max(0, breath - 2)
                print('Затруднение при плавании.')
        if breath <= 0 or panic >= 10:
            print('Паника/удушье привели к потере сознания.')
            press_enter()
            return
        time.sleep(0.6)
    print('Вы пережили этот водный ужас. Поздравляем.')
    press_enter()

# -----------------------
# Game: Арахнофобия (Arachnophobia)
# Avoid spiders appearing in rooms; make choices whether to confront or avoid.
# -----------------------
def arachnophobia():
    clear()
    print('=== Арахнофобия ===')
    rooms = input_int('Число комнат (по умолчанию 8): ', 3) or 8
    player = 0
    courage = 5
    while player < rooms:
        clear()
        print(f'Комната {player+1}/{rooms}. Смелость: {courage}/10')
        has_spider = random.random() < 0.5
        if has_spider:
            print('В комнате паук!')
            choice = input('Confront or avoid? (c/a): ').strip().lower()
            if choice == 'c':
                # chance to kill spider and increase courage
                if random.random() < 0.6:
                    courage = min(10, courage+1)
                    print('Вы убили паука. Отвага +1.')
                else:
                    courage = max(0, courage-2)
                    print('Паук испугал вас — смелость -2.')
            else:
                # avoid reduces progress but safe
                print('Вы обошли комнату стороной.')
                player += 0  # no advance
        else:
            print('Пустая комната. Можете пройти.')
            player += 1
        time.sleep(0.6)
        if courage <= 0:
            print('Страх превзошёл вас. Игра окончена.')
            press_enter()
            return
    print('Вы прошли все комнаты. Отлично!')
    press_enter()

# -----------------------
# Game: Клаустрофобия (Claustrophobia)
# Escape shrinking space: each turn area reduces; perform actions to expand or survive
# -----------------------
def claustrophobia():
    clear()
    print('=== Клаустрофобия ===')
    size = input_int('Начальный объём (единиц, по умолчанию 10): ', 3) or 10
    space = size
    health = 10
    while space > 0 and health > 0:
        clear()
        print(f'Текущее пространство: {space}, здоровье: {health}')
        action = input('Действие: expand (попытаться расширить), conserve (экономить) [e/c]: ').strip().lower()
        if action == 'e':
            if random.random() < 0.5:
                gained = random.randint(1,3)
                space += gained
                print(f'Удачно! Площадь +{gained}.')
            else:
                health -= 1
                print('Попытка привела к травме: -1 здоровья.')
        else:
            # conserve: reduce damage but space shrinks slower
            if random.random() < 0.6:
                space -= 1
                print('Вы сжались — пространство уменьшилось немного.')
            else:
                space -= 2
                health -= 1
                print('Сокращение пространства болезненно.')
        # natural shrink
        space -= 1
        if space <= 0:
            print('Пространство сократилось — вы зажаты.')
            press_enter()
            return
        time.sleep(0.6)
    if health > 0:
        print('Вы выжили в тесноте и нашли выход.')
    else:
        print('Вы не смогли выдержать — конец.')
    press_enter()
# -----------------------
# 1) Lumber Jack
# Chop trees rhythmically: press Enter quickly N times before timer.
# -----------------------
def lumber_jack():
    clear()
    print('=== Lumber Jack ===')
    chops_needed = input_int('Сколько рубок требуется (по умолчанию 10): ', 1) or 10
    time_limit = input_int('Время в секундах (по умолчанию 8): ', 1) or 8
    print(f'У вас {time_limit} секунд чтобы сделать {chops_needed} рубок (нажимайте Enter).')
    press_enter()
    start = time.time()
    chops = 0
    while time.time() - start < time_limit and chops < chops_needed:
        try:
            input()
        except KeyboardInterrupt:
            break
        chops += 1
        print(f'Рубка #{chops}')
    elapsed = time.time() - start
    if chops >= chops_needed:
        print('Вы успели! Дровосек победил.')
    else:
        print('Не успели. Сделано', chops)
    print(f'Время: {elapsed:.2f}s')
    press_enter()

# -----------------------
# 2) Pizza Memory
# Show sequence of pizza toppings, player repeats.
# -----------------------
def pizza_memory():
    clear()
    print('=== Pizza Memory ===')
    toppings = ['cheese','tomato','mushroom','pepperoni','olive','onion','basil']
    level = input_int('Уровней (по умолчанию 5): ', 1) or 5
    seq = []
    for lv in range(1, level+1):
        seq.append(random.choice(toppings))
        clear()
        print(f'Уровень {lv}: запомните последовательность:')
        print(' '.join(seq))
        time.sleep(max(1.0, 2.0 - lv*0.1))
        clear()
        ans = input('Введите последовательность через пробел: ').strip().lower().split()
        if ans != seq:
            print('Неверно. Правильная была:', ' '.join(seq))
            press_enter()
            return
        print('Верно!')
        time.sleep(0.6)
    print('Вы прошли все уровни пицца-памяти. Молодец!')
    press_enter()

# -----------------------
# 3) Food Memory
# Classic sequence memory with food items.
# -----------------------
def food_memory():
    clear()
    print('=== Food Memory ===')
    foods = ['apple','banana','bread','cheese','cake','egg','fish','tomato']
    rounds = input_int('Раундов (по умолчанию 6): ', 1) or 6
    seq = []
    for r in range(rounds):
        seq.append(random.choice(foods))
        clear()
        print('Запомните:')
        print(' '.join(seq))
        time.sleep(1.5)
        clear()
        ans = input('Введите через пробел: ').strip().lower().split()
        if ans != seq:
            print('Промах. Правильно:', ' '.join(seq))
            press_enter()
            return
        print('OK')
        time.sleep(0.4)
    print('Вы отличны запомнили еду!')
    press_enter()

# -----------------------
# 4) Sound Memory
# Represent sounds by short words; player repeats sequence.
# -----------------------
def sound_memory():
    clear()
    print('=== Sound Memory ===')
    sounds = ['beep','boop','ding','buzz','click','tock']
    rounds = input_int('Раундов (по умолчанию 5): ', 1) or 5
    seq = []
    for r in range(rounds):
        seq.append(random.choice(sounds))
        clear()
        print('Sequence:')
        for s in seq:
            print(s.upper())
            time.sleep(0.6)
            clear()
        ans = input('Введите последовательность через пробел: ').strip().lower().split()
        if ans != seq:
            print('Неправильно. Правильно:', ' '.join(seq))
            press_enter()
            return
        print('Верно.')
        time.sleep(0.5)
    print('Вы прошли Sound Memory!')
    press_enter()

# -----------------------
# 5) Memory (classic card pairs)
# -----------------------
def memory_classic():
    clear()
    print('=== Memory (Pairs) ===')
    size = input_int('Количество пар (по умолчанию 6): ', 2) or 6
    cards = list(range(size)) * 2
    random.shuffle(cards)
    revealed = [False]*len(cards)
    tries = 0
    while not all(revealed):
        clear()
        print('Карты:')
        for i, val in enumerate(cards):
            if revealed[i]:
                print(f'[{val}]', end=' ')
            else:
                print(f'[{i}]', end=' ')
        print()
        a = input_int('Выберите карту A (индекс): ', 0, len(cards)-1)
        b = input_int('Выберите карту B (индекс): ', 0, len(cards)-1)
        if a is None or b is None or a==b:
            print('Неверный выбор.')
            time.sleep(0.6)
            continue
        tries += 1
        if cards[a] == cards[b]:
            print('Пара! (',cards[a],')')
            revealed[a]=revealed[b]=True
        else:
            print('Не пара:', cards[a], cards[b])
        time.sleep(0.8)
    print('Всё открыто! Попыток:', tries)
    press_enter()

# -----------------------
# 6) Liar's Bar
# Social bluff game: bartender states drink properties; player calls truth/lie.
# -----------------------
def liars_bar():
    clear()
    print('=== Liar\'s Bar ===')
    drinks = ['Mojito','Coffee','Tea','Beer','Wine','Smoothie']
    rounds = input_int('Раундов (по умолчанию 6): ', 1) or 6
    score = 0
    facts_database = {
        'Mojito': ['mint','rum','lime'],
        'Coffee': ['beans','caffeine','hot'],
        'Tea': ['leaves','hot','herbal'],
        'Beer': ['barley','hops','fermented'],
        'Wine': ['grapes','fermented','vintage'],
        'Smoothie': ['fruit','blender','cold']
    }
    for r in range(rounds):
        drink = random.choice(drinks)
        real_fact = random.choice(facts_database[drink])
        lie = random.choice(['contains nuts','served frozen','made of stone','contains sugar'])  # generic lies
        # randomly choose to present true or false statement
        if random.random() < 0.5:
            statement = f'{drink} contains {real_fact}'
            truth = True
        else:
            statement = f'{drink} {lie}'
            truth = False
        clear()
        print('Бармен: "', statement, '"')
        ans = input('Правда или ложь? (t/f): ').strip().lower()
        if (ans == 't' and truth) or (ans == 'f' and not truth):
            print('Вы правы!')
            score += 1
        else:
            print('Ошибаетесь.')
        time.sleep(0.6)
    print('Итоговый счёт:', score)
    press_enter()

# -----------------------
# 7) Hitman
# Simple assassination puzzle: choose correct target by clues.
# -----------------------
def hitman():
    clear()
    print('=== Hitman ===')
    suspects = ['A','B','C','D']
    traits = {
        'A': {'hat':True, 'scar':False},
        'B': {'hat':False,'scar':True},
        'C': {'hat':True, 'scar':True},
        'D': {'hat':False,'scar':False},
    }
    clue = random.choice([
        ('killer wore hat', lambda s: s['hat']),
        ('killer has scar', lambda s: s['scar']),
    ])
    clear()
    print('Улики: ', clue[0])
    possible = [k for k,v in traits.items() if clue[1](v)]
    print('Кто это может быть?', ', '.join(suspects))
    choice = input('Выберите подозреваемого: ').strip().upper()
    if choice in possible:
        print('Успешно — вы нашли цель.')
    else:
        print('Промах — неверный выбор. Возможные:', ', '.join(possible))
    press_enter()

# -----------------------
# 8) True or False
# Series of statements: user answers.
# -----------------------
def true_or_false():
    clear()
    print('=== True or False ===')
    Q = [
        ('The Earth orbits the Sun', True),
        ('Python is a snake only', False),
        ('Water boils at 100C at sea level', True),
        ('Humans can breathe in outer space without aid', False),
    ]
    random.shuffle(Q)
    score = 0
    for stmt, truth in Q:
        ans = input(f'{stmt} (t/f): ').strip().lower()
        if (ans=='t' and truth) or (ans=='f' and not truth):
            score += 1
            print('OK')
        else:
            print('Wrong')
        time.sleep(0.4)
    print('Score:', score, '/', len(Q))
    press_enter()

# -----------------------
# 9) Death Columns
# Columns of numbers descend; player removes columns to avoid overflow.
# Simple turn-based simulation.
# -----------------------
def death_columns():
    clear()
    print('=== Death Columns ===')
    cols = input_int('Кол-во колонн (по умолчанию 5): ', 2) or 5
    limit = input_int('Макс высота до смерти (по умолчанию 6): ', 3) or 6
    heights = [0]*cols
    turn = 0
    while True:
        turn += 1
        clear()
        print('Turn', turn)
        print('Heights:', heights)
        # new blocks fall
        for i in range(cols):
            if random.random() < 0.5:
                heights[i] += 1
        print('После падения:', heights)
        if any(h >= limit for h in heights):
            print('Одна колонна достигла лимита. Game over.')
            press_enter()
            return
        # player removes a column piece
        rem = input_int(f'Какую колонну уменьшить 0..{cols-1}? (Enter - пропустить): ', 0, cols-1)
        if rem is not None:
            if heights[rem] > 0:
                heights[rem] -= 1
                print('Уменьшили колонну', rem)
            else:
                print('Колонна уже пуста.')
        else:
            print('Пропуск.')
        time.sleep(0.6)

# -----------------------
# 10) Guess the Word
# Hangman-style simple guess the word.
# -----------------------
def guess_the_word():
    clear()
    print('=== Guess the Word ===')
    words = ['python','banana','puzzle','guitar','suspicious','memory', "fight", "lumber", "movie", "baker", "hospital", "nurse", "down", "righty", "cursor", "mouse", "turbowarp", "scratch", "csharp", "common"]
    word = random.choice(words)
    guessed = set()
    attempts = 7
    while attempts > 0:
        display = ''.join(ch if ch in guessed else '_' for ch in word)
        print('Word:', display)
        if all(ch in guessed for ch in word):
            print('Вы угадали слово!', word)
            press_enter()
            return
        ch = input('Введите букву: ').strip().lower()
        if not ch or len(ch)!=1:
            print('Введите одну букву.')
            continue
        if ch in guessed:
            print('Уже пробовали.')
            continue
        if ch in word:
            guessed.add(ch)
            print('Есть такая буква!')
        else:
            attempts -= 1
            print('Неправильно. Осталось попыток:', attempts)
        time.sleep(0.4)
    print('Попытки закончились. Слово было:', word)
    press_enter()

# -----------------------
# 11) Who's SUS? (social deduction simplified)
# Players vote to find impostor among NPCs; one impostor randomly assigned.
# -----------------------
def whos_sus():
    clear()
    print('=== Who\'s SUS? ===')
    n = input_int('Игроков (включая вас) (по умолчанию 7): ', 3) or 7
    players = ['You'] + [f'P{i}' for i in range(1,n)]
    impostor = random.choice(players)
    print('В игре один самозванец. Соберите доказательства и голосуйте.')
    press_enter()
    # quick clue rounds
    clues = {p:0 for p in players}
    for r in range(3):
        for p in players:
            if p == impostor:
                # impostor sometimes suspicious
                if random.random() < 0.6:
                    clues[p] += 1
            else:
                if random.random() < 0.2:
                    clues[p] += 1
    # show clues count to player
    print('Подсчёт подозрительности (для наглядности):')
    for p in players:
        print(p, 'suspicion:', clues[p])
    # vote
    votes = {p:0 for p in players}
    for p in players:
        if p == 'You':
            choice = input('За кого голосуете?: ').strip()
            if choice not in votes:
                choice = random.choice([x for x in players if x!='You'])
                print('Неверный ввод, выбран:', choice)
            votes[choice] += 1
        else:
            # NPC votes for highest suspicion (with some randomness)
            max_sus = max(clues.values())
            candidates = [pl for pl, s in clues.items() if s == max_sus and pl != p]
            pick = random.choice(candidates) if candidates else random.choice([pl for pl in players if pl!=p])
            votes[pick] += 1
    result = sorted(votes.items(), key=lambda x: -x[1])[0][0]
    print('Голосование завершено. Выбывший:', result)
    if result == impostor:
        print('Импостор найден! Мирные победили.')
    else:
        print('Увы, ошиблись. Импостор остался.')
    press_enter()

# -----------------------
# 12) Мафия (classic simplified)
# Roles: mafia(s), doctor, detective, townspeople. Night kills, day vote.
# -----------------------
def mafia_game():
    clear()
    print('=== Мафия ===')
    n = input_int('Игроков (включая вас) (по умолчанию 7): ', 5) or 7
    names = ['You'] + [f'P{i}' for i in range(1, n)]
    roles = {}
    # Assign roles: 1 mafia (maybe you), 1 detective, 1 doctor, rest town
    mafia = random.choice(names)
    remaining = [p for p in names if p != mafia]
    detective = random.choice(remaining)
    remaining = [p for p in remaining if p != detective]
    doctor = random.choice(remaining)
    for p in names:
        if p == mafia:
            roles[p] = 'Mafia'
        elif p == detective:
            roles[p] = 'Detective'
        elif p == doctor:
            roles[p] = 'Doctor'
        else:
            roles[p] = 'Town'
    alive = set(names)
    day = 1
    # simple loop: night kills one (mafia chooses), doctor may save, detective may check
    while True:
        # check win conditions
        maf_count = sum(1 for p in alive if roles[p]=='Mafia')
        town_count = sum(1 for p in alive if roles[p]!='Mafia')
        if maf_count == 0:
            print('Мафия уничтожена. Горожане победили!')
            press_enter()
            return
        if maf_count >= town_count:
            print('Мафия взяла верх. Мафия победила.')
            press_enter()
            return
        clear()
        print(f'Ночь {day}. Живые: {", ".join(sorted(alive))}')
        # Mafia chooses victim
        if mafia in alive:
            if mafia == 'You':
                print('Вы — мафия. Выберите жертву:')
                target = input('Имя жертвы: ').strip()
                if target not in alive or target == 'You':
                    target = random.choice([p for p in alive if p!='You'])
                    print('Неверное имя. Случайно выбран:', target)
            else:
                target = random.choice([p for p in alive if p != mafia])
            print('Мафия выбрала жертву.')
        else:
            target = None
        # Doctor chooses to save
        if doctor in alive:
            if doctor == 'You':
                save = input('Кого вы спасаете? (Enter - никого): ').strip()
                if save not in alive:
                    save = None
            else:
                save = random.choice(list(alive))
        else:
            save = None
        # Detective checks
        if detective in alive:
            if detective == 'You':
                check = input('Кого проверить? (Enter - пропустить): ').strip()
                if check not in alive:
                    print('Пропуск проверки.')
                else:
                    print(check, 'role is', roles[check])
            else:
                chk = random.choice(list(alive))
                # NPC detective learns role but we don't show
        # resolve night
        if target and target != save:
            print('Ночью убит:', target)
            alive.remove(target)
        else:
            print('Никто не погиб ночью.')
        press_enter()
        # Day: vote to lynch
        clear()
        print('День. Живые:', ', '.join(sorted(alive)))
        votes = {p:0 for p in alive}
        for voter in list(alive):
            if voter == 'You':
                choice = input('За кого голосуете? ').strip()
                if choice not in votes:
                    choice = random.choice([p for p in alive if p!=voter])
                    print('Неверный выбор, голос за', choice)
            else:
                # NPCs suspicious of those with role mafia more likely (but they don't know)
                # random vote
                choice = random.choice([p for p in alive if p!=voter])
            votes[choice] += 1
        lynch = sorted(votes.items(), key=lambda x: -x[1])[0][0]
        print('Выбывший по голосованию:', lynch)
        if lynch in alive:
            alive.remove(lynch)
        press_enter()
        day += 1
# -----------------------
# 1) Оживший мир
# Walk and talk with items encountered on the path.
# -----------------------
def living_world():
    clear()
    print('=== Оживший мир ===')
    steps = input_int('Сколько шагов пройти? (по умолчанию 10): ', 1) or 10
    items = ['стул','фонарь','камень','дерево','часы','книга','мяч','окно']
    mood = 5
    for s in range(1, steps+1):
        clear()
        item = random.choice(items)
        print(f'Шаг {s}/{steps}. На пути вы встретили: {item}')
        action = input('Действие: talk / ignore / touch (t/i/с): ').strip().lower()
        if action == 't' or action == 'talk':
            if random.random() < 0.7:
                mood = min(10, mood + 1)
                print(f'{item} ответил! Настроение +1.')
            else:
                mood = max(0, mood - 1)
                print(f'{item} молчит. Настроение -1.')
        elif action == 'с' or action == 'touch':
            if random.random() < 0.3:
                mood = max(0, mood - 2)
                print(f'{item} ужалил вас! -2.')
            else:
                mood = min(10, mood + 0)
                print(f'{item} тронулось — ничего особенного.')
        else:
            print('Вы прошли мимо.')
        time.sleep(0.6)
    print('Прогулка окончена. Настроение:', mood)
    press_enter()

# -----------------------
# 2) Русская рулетка
# -----------------------
def russian_roulette():
    clear()
    print('=== Русская рулетка ===')
    chambers = input_int('Кол-во патронов в барабане (1..6, по умолчанию 6): ', 1, 6) or 6
    bullets = input_int('Сколько патронов зарядить (по умолчанию 1): ', 0, chambers) or 1
    players = input_int('Игроков (включая вас) (по умолчанию 3): ', 2) or 3
    order = ['You'] + [f'P{i}' for i in range(2, players+1)]
    idx = 0
    chamber_positions = [0]*chambers
    for _ in range(bullets):
        pos = random.randrange(chambers)
        chamber_positions[pos] = 1
    while True:
        current = order[idx % players]
        print(f'Ход: {current}. Нажмите Enter чтобы крутнуть курок и нажать на спуск.')
        input()
        shot = random.choice(chamber_positions)
        if shot == 1:
            print(f'{current} убит!')
            if current == 'You':
                print('Вы проиграли.')
                press_enter()
                return
            else:
                order.remove(current)
                players -= 1
                idx = idx % players
                if players == 1:
                    print('Оставшийся игрок победил:', order[0])
                    press_enter()
                    return
        else:
            print(f'{current} жив.')
            idx += 1
        time.sleep(0.5)

# -----------------------
# 3) Интерпретация
# Show ambiguous statement; player interprets; scoring random.
# -----------------------
def interpretation_game():
    clear()
    print('=== Интерпретация ===')
    prompts = [
        'Кот сидит на крыше.',
        'Часы остановились на трёх.',
        'Дождь звучит как музыка.',
        'Окно смотрит на город.'
    ]
    p = random.choice(prompts)
    print('Фраза для интерпретации:', p)
    ans = input('Расскажите вашу интерпретацию: ')
    score = min(10, max(0, len(ans.split())//2 + random.randint(-1,2)))
    print('Оценка интерпретации:', score, '/10')
    press_enter()

# -----------------------
# 4) Репутация
# Simple reputation simulator based on choices.
# -----------------------
def reputation():
    clear()
    print('=== Репутация ===')
    rep = 50  # 0..100
    rounds = input_int('Раундов (по умолчанию 6): ', 1) or 6
    for r in range(rounds):
        clear()
        print(f'Репутация: {rep}/100')
        scenario = random.choice([
            ('Помог человеку с сумкой', 10),
            ('Распространение слухов', -12),
            ('Пожертвование в фонд', 8),
            ('Опоздание на встречу', -5),
        ])
        print('Событие:', scenario[0])
        choice = input('Выбор: act / skip (a/s): ').strip().lower()
        if choice == 'a':
            rep = min(100, rep + scenario[1])
            print('Действие выполнено.')
        else:
            rep = max(0, rep - 3)
            print('Вы пропустили — + последствий.')
        time.sleep(0.6)
    print('Финальная репутация:', rep)
    press_enter()

# -----------------------
# 5) Танки
# Simple grid tank duel vs AI.
# -----------------------
def tanks_game():
    clear()
    print('=== Танки ===')
    size = input_int('Размер поля (по умолчанию 7): ', 5) or 7
    player = [0, 0]
    enemy = [size-1, size-1]
    player_hp = 3
    enemy_hp = 3
    while player_hp > 0 and enemy_hp > 0:
        clear()
        for r in range(size):
            row = ''
            for c in range(size):
                if [r,c] == player: row += 'P '
                elif [r,c] == enemy: row += 'E '
                else: row += '. '
            print(row)
        print(f'Your HP: {player_hp}  Enemy HP: {enemy_hp}')
        cmd = input('move (w/a/s/d) or fire (f): ').strip().lower()
        if cmd in ('w','a','s','d'):
            if cmd=='w' and player[0]>0: player[0]-=1
            if cmd=='s' and player[0]<size-1: player[0]+=1
            if cmd=='a' and player[1]>0: player[1]-=1
            if cmd=='d' and player[1]<size-1: player[1]+=1
        elif cmd == 'f':
            # fire: if enemy in same row or col within 2 cells -> hit
            if player[0]==enemy[0] and abs(player[1]-enemy[1])<=2 or player[1]==enemy[1] and abs(player[0]-enemy[0])<=2:
                enemy_hp -= 1
                print('Попадание!')
            else:
                print('Промах.')
        # enemy AI simple
        if random.random() < 0.7:
            # move towards
            if enemy[0] < player[0]: enemy[0]+=1
            elif enemy[0] > player[0]: enemy[0]-=1
            if enemy[1] < player[1]: enemy[1]+=1
            elif enemy[1] > player[1]: enemy[1]-=1
        else:
            if random.random() < 0.5 and (enemy[0]==player[0] or enemy[1]==player[1]):
                # enemy fires
                if enemy[0]==player[0] and abs(enemy[1]-player[1])<=2 or enemy[1]==player[1] and abs(enemy[0]-player[0])<=2:
                    player_hp -=1
                    print('Враг попал в вас!')
        time.sleep(0.5)
    if player_hp>0:
        print('Вы победили танковый бой!')
    else:
        print('Ваш танк уничтожен.')
    press_enter()

# -----------------------
# 6) Симулятор компьютерного вируса
# Manage infection spread limited to a small network.
# -----------------------
def virus_simulator():
    clear()
    print('=== Симулятор компьютерного вируса ===')
    nodes = input_int('Число компьютеров в сети (по умолчанию 10): ', 3) or 10
    infected = set([random.randrange(nodes)])
    protected = set()
    rounds = input_int('Раундов распространения (по умолчанию 8): ', 1) or 8
    for r in range(1, rounds+1):
        clear()
        print(f'Раунд {r}/{rounds}')
        print('Инфицированы:', sorted(infected))
        action = input('Вы можете патчить один комп или наблюдать (patch <id> / skip): ').strip().lower()
        if action.startswith('patch'):
            parts = action.split()
            if len(parts)==2 and parts[1].isdigit():
                pid = int(parts[1])
                if 0<=pid<nodes:
                    protected.add(pid)
                    if pid in infected:
                        infected.remove(pid)
                    print('Компонент патчен.')
                else:
                    print('Неверный ID.')
            else:
                print('Неверная команда.')
        # spreading
        new_inf = set()
        for node in range(nodes):
            if node in infected:
                # attempt to infect neighbors
                for _ in range(2):
                    target = random.randrange(nodes)
                    if target not in protected and random.random() < 0.4:
                        new_inf.add(target)
        infected |= new_inf
        time.sleep(0.6)
        if len(infected) == nodes:
            print('Вирус захватил сеть полностью.')
            press_enter()
            return
    print('Симуляция окончена. Инфицировано:', len(infected), 'из', nodes)
    press_enter()

# -----------------------
# 7) Симулятор стройки
# Manage building project resources and progress.
# -----------------------
def construction_simulator():
    clear()
    print('=== Симулятор стройки ===')
    progress = 0
    budget = 100
    workers = 5
    days = input_int('Сколько дней вести стройку? (по умолчанию 10): ', 1) or 10
    for d in range(1, days+1):
        clear()
        print(f'День {d}/{days}. Прогресс: {progress}%. Бюджет: {budget}. Рабочих: {workers}')
        action = input('Действие: hire / fire / invest / work (h/f/i/w): ').strip().lower()
        if action == 'h':
            cost = 10
            if budget >= cost:
                workers += 1
                budget -= cost
                print('Наняли рабочего.')
            else:
                print('Не хватает бюджета.')
        elif action == 'f':
            if workers > 1:
                workers -= 1
                print('Уволили рабочего.')
            else:
                print('Минимум рабочих уже.')
        elif action == 'i':
            invest = min(budget, 20)
            budget -= invest
            progress += invest//2
            print('Инвестировали', invest)
        else:
            # work
            gained = workers * random.randint(1,3)
            progress += gained
            budget += workers * random.randint(0,2)
            print('Работа продвинулась на', gained)
        progress = min(100, progress)
        time.sleep(0.5)
        if progress >= 100:
            print('Стройка завершена успешно!')
            press_enter()
            return
    print('Время закончилось. Прогресс:', progress)
    press_enter()

# -----------------------
# 8) Школа
# Attend classes and pass tests.
# -----------------------
def school_simulator():
    clear()
    print('=== Школа ===')
    energy = 10
    knowledge = 0
    days = input_int('Дней в школе (по умолчанию 5): ', 1) or 5
    for d in range(1, days+1):
        clear()
        print(f'День {d}/{days}. Энергия: {energy}. Знания: {knowledge}')
        action = input('Учиться / Пропустить / Спать (study/skip/sleep): ').strip().lower()
        if action == 'study':
            energy -= 2
            knowledge += random.randint(1,4)
            print('Вы учились.')
        elif action == 'sleep':
            energy = min(10, energy + 3)
            print('Вы поспали.')
        else:
            energy -= 1
            print('Вы прогуливали.')
        if energy <= 0:
            print('Вы упали от усталости и пропустили экзамен.')
            press_enter()
            return
        time.sleep(0.5)
    print('Экзамен! Знания:', knowledge)
    if knowledge >= 8:
        print('Вы успешно сдали экзамен!')
    else:
        print('Неуд — нужно больше учиться.')
    press_enter()

# -----------------------
# 9) Сложный Math Quiz
# Hard arithmetic questions.
# -----------------------
def hard_math_quiz():
    clear()
    print('=== Сложный Math Quiz ===')
    rounds = input_int('Вопросов (по умолчанию 7): ', 1) or 7
    score = 0
    ops = ['+','-','*','/','^']
    for _ in range(rounds):
        a = random.randint(2,50)
        b = random.randint(2,20)
        op = random.choice(ops)
        if op == '^':
            correct = a ** (random.randint(2,3))
            q = f'{a} ^ ? = {correct} (найдите степень?)'
            # ask exponent guess - simplified: ask power being 2 or 3
            ans = input(q + ' Ваш ответ (число): ').strip()
            try:
                if int(ans) in (2,3) and a**int(ans) == correct:
                    score += 1
            except:
                pass
        elif op == '/':
            correct = round(a / b, 3)
            ans = input(f'{a} / {b} = ? (округлить до 3 знаков): ').strip()
            try:
                if abs(float(ans) - correct) < 1e-3:
                    score += 1
            except:
                pass
        else:
            expr = f'{a}{op}{b}'
            correct = eval(expr)
            ans = input(f'{expr} = ').strip()
            try:
                if float(ans) == float(correct):
                    score += 1
            except:
                pass
        print('Текущий счёт:', score)
        time.sleep(0.4)
    print('Итоговый счёт:', score, '/', rounds)
    press_enter()

# -----------------------
# 10) Кликер
# Simple clicker (press Enter many times to increase score)
# -----------------------
def clicker():
    clear()
    print('=== Кликер ===')
    target = input_int('Сколько кликов цель? (по умолчанию 50): ', 1) or 50
    score = 0
    start = time.time()
    print('Нажимайте Enter для клика. Ctrl+C чтобы выйти.')
    try:
        while score < target:
            input()
            score += 1
            if score % 10 == 0:
                print('Кликов:', score)
    except KeyboardInterrupt:
        pass
    elapsed = time.time() - start
    print(f'Готово! Клики: {score}. Время: {elapsed:.2f}s')
    press_enter()

# -----------------------
# 11) Math Quiz на время
# Solve as many arithmetic problems as possible in time limit.
# -----------------------
def timed_math_quiz():
    clear()
    print('=== Math Quiz на время ===')
    tlimit = input_int('Время в секундах (по умолчанию 20): ', 5) or 20
    start = time.time()
    score = 0
    while time.time() - start < tlimit:
        a = random.randint(1,20)
        b = random.randint(1,20)
        op = random.choice(['+','-','*'])
        correct = eval(f'{a}{op}{b}')
        ans = input(f'{a} {op} {b} = ').strip()
        if ans == '':
            break
        try:
            if int(ans) == correct:
                score += 1
        except:
            pass
    print('Время вышло или вы остановились. Очки:', score)
    press_enter()

# -----------------------
# 12) Очень сложный Math Quiz
# Many-digit operations, modular arithmetic.
# -----------------------
def very_hard_math_quiz():
    clear()
    print('=== Очень сложный Math Quiz ===')
    rounds = input_int('Вопросов (по умолчанию 5): ', 1) or 5
    score = 0
    for _ in range(rounds):
        a = random.randint(100,999)
        b = random.randint(10,99)
        mod = random.randint(2,50)
        correct = (a * b) % mod
        ans = input(f'({a} * {b}) mod {mod} = ').strip()
        try:
            if int(ans) == correct:
                score += 1
        except:
            pass
    print('Счёт:', score, '/', rounds)
    press_enter()

# -----------------------
# 13) Math Quiz но с другими игроками
# Simulate multiple players answering with random skill.
# -----------------------
def math_quiz_vs_players():
    clear()
    print('=== Math Quiz но с другими игроками ===')
    players = input_int('Сколько игроков включая вас? (по умолчанию 4): ', 2) or 4
    pnames = ['You'] + [f'P{i}' for i in range(2, players+1)]
    rounds = input_int('Раундов (по умолчанию 6): ', 1) or 6
    scores = {p:0 for p in pnames}
    skills = {p: random.uniform(0.3,0.9) for p in pnames}
    skills['You'] = 0.7  # default human skill estimate
    for r in range(rounds):
        a,b = random.randint(1,50), random.randint(1,50)
        correct = a + b
        print(f'Вопрос {r+1}: {a} + {b} = ?')
        # You answer
        ans = input('Ваш ответ: ').strip()
        try:
            if int(ans) == correct:
                scores['You'] += 1
        except:
            pass
        # NPCs answer probabilistically
        for p in pnames:
            if p == 'You': continue
            if random.random() < skills[p]:
                scores[p] += 1
        time.sleep(0.3)
    print('Итоги:')
    for p in pnames:
        print(p, scores[p])
    press_enter()

# -----------------------
# 14) Планетарий
# Show solar system facts and short quiz.
# -----------------------
def planetarium():
    clear()
    print('=== Планетарий ===')
    facts = {
        'Mercury': 'closest to Sun',
        'Venus': 'hottest planet',
        'Earth': 'has life',
        'Mars': 'red planet',
        'Jupiter': 'largest planet',
        'Saturn': 'has rings',
        'Uranus': 'tilted axis',
        'Neptune': 'far blue'
    }
    for k,v in facts.items():
        print(f'{k}: {v}')
    q = random.choice(list(facts.items()))
    ans = input(f'Вопрос: что за планета — "{q[1]}"? ').strip()
    if q[0].lower() == ans.lower():
        print('Верно!')
    else:
        print('Неверно. Правильный ответ:', q[0])
    press_enter()

# -----------------------
# 15) Ожившие планеты
# Planets talk; interaction to increase cosmic harmony.
# -----------------------
def living_planets():
    clear()
    print('=== Ожившие планеты ===')
    planets = ['Mercury','Venus','Earth','Mars','Jupiter','Saturn']
    moods = {p: random.randint(0,5) for p in planets}
    turns = input_int('Раундов встречи (по умолчанию 6): ', 1) or 6
    for t in range(turns):
        clear()
        p = random.choice(planets)
        print(f'{p} [{moods[p]}/10] говорит: "..."')
        action = input('Слушать / Игнорировать / Петь (l/i/s): ').strip().lower()
        if action == 'l':
            moods[p] = min(10, moods[p]+2)
            print(p, 'рады.')
        elif action == 's':
            moods[p] = min(10, moods[p]+1)
            print('Музыка понравилась.')
        else:
            moods[p] = max(0, moods[p]-1)
            print('Обида.')
        time.sleep(0.6)
    print('Итоги настроений:')
    for p in planets:
        print(p, moods[p])
    press_enter()

# -----------------------
# 16) Звёзды
# Mini star observation: guess constellation pieces
# -----------------------
def stars_game():
    clear()
    print('=== Звёзды ===')
    constellations = {
        'Orion': ['Betelgeuse','Rigel','Bellatrix'],
        'Ursa Major': ['Dubhe','Merak','Phecda'],
        'Lyra': ['Vega','Sheliak']
    }
    chosen = random.choice(list(constellations.items()))
    print('Угадайте одну звезду из созвездия:', chosen[0])
    ans = input('Введите имя звезды: ').strip()
    if ans in chosen[1]:
        print('Правильно!')
    else:
        print('Неверно. Варианты:', ', '.join(chosen[1]))
    press_enter()

# -----------------------
# 17) Блеск
# Tiny game: polish gems by repeated actions
# -----------------------
def shine_game():
    clear()
    print('=== Блеск ===')
    gems = input_int('Сколько камней? (по умолчанию 3): ', 1) or 3
    shiny = [0]*gems
    target = 5
    while max(shiny) < target:
        clear()
        print('Состояние камней:', shiny)
        i = input_int(f'Какой камень отполировать (0..{gems-1}) (Enter выйти): ', 0, gems-1)
        if i is None:
            break
        shiny[i] += 1
        print('Полируете...')
        time.sleep(0.3)
    print('Итог:', shiny)
    press_enter()

# -----------------------
# 18) Quiz / variants
# Basic quiz data reused for several modes.
# -----------------------
QUIZ_QS = [
    ('Столица Франции?', 'Париж'),
    ('2+2*2 = ?', '6'),
    ('Какой газ необходим для дыхания?', 'Кислород'),
    ('Сколько дней в феврале в невисокосном году?', '28'),
    ('Кто написал "Евгений Онегин"?', 'Пушкин'),
]

def quiz_basic(rounds=5, hard=False, timed=False, vs_players=1):
    clear()
    print('=== Quiz ===')
    players = ['You'] + [f'P{i}' for i in range(2, vs_players+1)]
    scores = {p:0 for p in players}
    start_time = time.time()
    for i in range(rounds):
        q,a = random.choice(QUIZ_QS if not hard else (QUIZ_QS + [
            ('Кто открыл закон тяготения?', 'Ньютон'),
            ('sin(90°)=?', '1')
        ]))
        if timed:
            tlimit = 8
            print(f'Время на ответ: {tlimit}s')
            t0 = time.time()
        print('Вопрос:', q)
        # user input (timed or not)
        if timed:
            # simple timed input: allow pressing enter; we measure time after answer
            ans = input('Ваш ответ: ').strip()
            dt = time.time() - t0
            if dt > tlimit:
                print('Время вышло.')
                ans = ''
        else:
            ans = input('Ваш ответ: ').strip()
        if ans.lower() == a.lower():
            scores['You'] += 1
        # other players answer randomly with lower accuracy if many players
        for p in players:
            if p == 'You': continue
            prob = 0.6 if not hard else 0.35
            if random.random() < prob:
                scores[p] += 1
        time.sleep(0.4)
    print('Результаты:')
    for p in players:
        print(p, scores[p])
    press_enter()

# Wrappers for quiz variants
def quiz_easy():
    quiz_basic(rounds=5, hard=False, timed=False, vs_players=1)

def quiz_hard():
    quiz_basic(rounds=7, hard=True, timed=False, vs_players=1)

def quiz_timed():
    quiz_basic(rounds=6, hard=False, timed=True, vs_players=1)

def quiz_very_hard():
    quiz_basic(rounds=8, hard=True, timed=True, vs_players=1)

def quiz_vs_players():
    n = input_int('Сколько игроков (включая вас) (по умолчанию 4): ', 2) or 4
    quiz_basic(rounds=6, hard=False, timed=False, vs_players=n)
# -----------------------
# Multiplayer helper simulator
# NPCs act with simple probabilistic logic to emulate other players.
# -----------------------
def simulate_npc_choice(npc_name, choices, bias=None):
    # bias: optional dict mapping choice->weight increase
    weights = []
    for c in choices:
        w = 1.0
        if bias and c in bias:
            w += bias[c]
        # small variability based on npc "personality"
        w *= random.uniform(0.7, 1.3)
        weights.append(w)
    total = sum(weights)
    pick = random.random() * total
    acc = 0
    for c, w in zip(choices, weights):
        acc += w
        if pick <= acc:
            return c
    return random.choice(choices)

# -----------------------
# 1) Сапёр с другими игроками (multiplayer Minesweeper race)
# Each player in turn reveals a cell on shared board; the one who hits mine is out.
# Last remaining wins.
# -----------------------
def minesweeper_vs_players():
    clear()
    print('=== Сапёр с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ', 2) or 4
    rows = input_int('Строки (по умолчанию 6): ', 3) or 6
    cols = input_int('Столбцы (по умолчанию 8): ', 3) or 8
    mines_count = input_int('Число мин (по умолчанию 8): ', 1, rows*cols-1) or 8
    names = names_list(n)
    board = [[0]*cols for _ in range(rows)]
    mined = set()
    # place mines
    while len(mined) < mines_count:
        r = random.randrange(rows); c = random.randrange(cols)
        mined.add((r,c))
    # compute numbers
    for r in range(rows):
        for c in range(cols):
            if (r,c) in mined:
                board[r][c] = -1
            else:
                cnt = 0
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if dr==0 and dc==0: continue
                        nr, nc = r+dr, c+dc
                        if 0<=nr<rows and 0<=nc<cols and (nr,nc) in mined:
                            cnt += 1
                board[r][c] = cnt
    revealed = [[False]*cols for _ in range(rows)]
    alive = names[:]
    turn = 0
    while len(alive) > 1:
        current = alive[turn % len(alive)]
        clear()
        print('Текущие игроки:', ', '.join(alive))
        # display small part of board as indices
        print('Карта (x,y): нераскрытые показаны индексом, раскрытые - число или M')
        for r in range(rows):
            line = ''
            for c in range(cols):
                if revealed[r][c]:
                    line += f'{("M" if board[r][c]==-1 else board[r][c])} '
                else:
                    line += f'[{r},{c}] '
            print(line)
        print('Ход:', current)
        if current == 'You':
            sel_r = input_int('Выберите строку: ', 0, rows-1)
            sel_c = input_int('Выберите столбец: ', 0, cols-1)
            if sel_r is None or sel_c is None:
                print('Пропуск хода.')
                sel = None
            else:
                sel = (sel_r, sel_c)
        else:
            # NPC picks random unrevealed
            choices = [(r,c) for r in range(rows) for c in range(cols) if not revealed[r][c]]
            sel = random.choice(choices) if choices else None
            print(f'{current} выбирает {sel}')
            time.sleep(0.6)
        if sel is None:
            turn += 1
            continue
        r,c = sel
        if revealed[r][c]:
            print('Уже открыто — теряется ход.')
            turn += 1
            time.sleep(0.6)
            continue
        revealed[r][c] = True
        if board[r][c] == -1:
            print(f'Бах! {current} подорвался на мине и выбывает.')
            alive.remove(current)
            time.sleep(1.0)
            # after mine explosion, continue with same next index (no increment)
            # if current removed, turn remains same index
            continue
        else:
            print(f'Открыто число: {board[r][c]}')
        turn += 1
        time.sleep(0.7)
    clear()
    if alive:
        print('Победитель:', alive[0])
    else:
        print('Никто не остался жив.')
    press_enter()

# -----------------------
# 2) Догонялки с другими игроками (multiplayer chase)
# Players move on a linear track; chaser is random player or can be You.
# -----------------------
def chase_vs_players():
    clear()
    print('=== Догонялки с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 5): ', 2) or 5
    length = input_int('Длина трека (по умолчанию 30): ', 10) or 30
    names = names_list(n)
    # choose chaser randomly
    chaser = random.choice(names)
    positions = {p: 0 for p in names}
    finished = set()
    print('Chaser:', chaser)
    press_enter()
    while True:
        for p in names:
            if p in finished:
                continue
            if p == 'You':
                # move choice: run or sneak
                move = input('Ваш ход: run/sneak (r/s): ').strip().lower()
                if move == 'r':
                    positions[p] += random.randint(2,4)
                else:
                    positions[p] += random.randint(0,2)
            else:
                # NPC logic: if chaser close, run faster
                dist = positions[chaser] - positions[p]
                if dist >= -3:
                    positions[p] += random.randint(1,3)
                else:
                    positions[p] += random.randint(0,2)
            # chaser moves (if not current)
            if p == chaser:
                # chaser moves towards nearest target
                targets = [q for q in names if q!=chaser and q not in finished]
                if targets:
                    nearest = min(targets, key=lambda t: positions[chaser]-positions[t])
                    # move forward
                    positions[chaser] += random.randint(2,4)
            # check catches
            for q in names:
                if q != chaser and positions[chaser] >= positions[q] and q not in finished:
                    print(f'{chaser} поймал {q}!')
                    finished.add(q)
            # check finishers
            for q in names:
                if positions[q] >= length:
                    finished.add(q)
            # small display
        # show status
        clear()
        for p in names:
            print(p, positions[p], '(caught)' if p in finished else '')
        time.sleep(0.6)
        # end condition: only chaser or one remains not caught
        alive = [p for p in names if p not in finished]
        if len(alive) <= 1:
            print('Игра окончена. Выжившие:', alive)
            press_enter()
            return

# -----------------------
# 3) Догонялки с мячом с другими игроками
# Similar to chase_vs_players but ball possession modeled; winner is who reaches goal with ball.
# -----------------------
def chase_ball_vs_players():
    clear()
    print('=== Догонялки с мячом с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 5): ', 2) or 5
    length = input_int('Длина трека (по умолчанию 28): ', 10) or 28
    names = names_list(n)
    ball_holder = random.choice(names)
    positions = {p: 0 for p in names}
    print('Начинающий с мячом:', ball_holder)
    press_enter()
    while True:
        for p in names:
            if positions[p] >= length:
                continue
            if p == 'You':
                action = input('Ваш ход: run/sneak/throw (r/s/t): ').strip().lower()
                if action == 'r':
                    positions[p] += random.randint(2,4)
                elif action == 't' and ball_holder == 'You':
                    # attempt to throw to someone ahead
                    targets = [q for q in names if q != 'You']
                    receiver = input('Кому бросаете? (имя) или Enter случайно: ').strip()
                    if receiver not in names:
                        receiver = random.choice(targets)
                    if random.random() < 0.6:
                        ball_holder = receiver
                        print('Передача успешна — мяч у', receiver)
                else:
                    positions[p] += random.randint(0,2)
            else:
                # NPC behavior
                if ball_holder == p:
                    positions[p] += random.randint(1,3)
                    # chance to pass to a player ahead for strategy
                    if random.random() < 0.2:
                        candidates = [q for q in names if positions[q] > positions[p]]
                        if candidates:
                            ball_holder = random.choice(candidates)
                else:
                    positions[p] += random.randint(0,2)
        # check someone reached finish with ball
        for p in names:
            if positions[p] >= length and ball_holder == p:
                print('Игрок', p, 'добрался до финиша с мячом — победа!')
                press_enter()
                return
        # status
        clear()
        for p in names:
            print(p, positions[p], '(ball)' if p==ball_holder else '')
        time.sleep(0.6)

# -----------------------
# 4) Кликер с другими игроками (simulated idle multiplayer)
# Each player has click rate; run for time and see totals.
# -----------------------
def clicker_vs_players():
    clear()
    print('=== Кликер с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ', 2) or 4
    duration = input_int('Время в секундах (по умолчанию 10): ', 3) or 10
    names = names_list(n)
    scores = {p:0 for p in names}
    start = time.time()
    print('Нажимайте Enter как можно быстрее. ИГРА старт!')
    # NPC click rates:
    rates = {p: random.uniform(0.8, 2.5) for p in names if p != 'You'}
    try:
        while time.time() - start < duration:
            # NPC accumulate
            for p, r in rates.items():
                scores[p] += int(r * 0.2)  # tick
            input_timeout = duration - (time.time() - start)
            # let user press Enter once per loop to add clicks
            # we can't do non-blocking easily here without extra modules, so count Enter presses manually
            input()  # counts as one click
            scores['You'] += 1
    except KeyboardInterrupt:
        pass
    clear()
    print('Результаты кликера:')
    for p in names:
        print(p, scores[p])
    press_enter()

# -----------------------
# 5) Memory с другими игроками (pairs game with simulated opponents)
# Players take turns revealing two cards; NPCs have memory strength.
# -----------------------
def memory_vs_players():
    clear()
    print('=== Memory с другими игроками ===')
    n_players = input_int('Игроков (включая вас) (по умолчанию 4): ', 2) or 4
    pairs = input_int('Пар карт (по умолчанию 8): ', 2) or 8
    names = names_list(n_players)
    cards = list(range(pairs)) * 2
    random.shuffle(cards)
    revealed = [False] * (pairs*2)
    scores = {p:0 for p in names}
    # NPC memory: how many known card positions they remember
    memory = {p: {} for p in names}
    turn = 0
    while not all(revealed):
        current = names[turn % len(names)]
        clear()
        print('Текущий игрок:', current)
        # show board indices
        for i, val in enumerate(cards):
            if revealed[i]:
                print(f'[{val}]', end=' ')
            else:
                print(f'[{i}]', end=' ')
        print()
        if current == 'You':
            a = input_int('Выберите карту A индекс: ', 0, len(cards)-1)
            b = input_int('Выберите карту B индекс: ', 0, len(cards)-1)
        else:
            # NPC tries to use memory to find pair
            # memory[current] maps value->index known
            known_pairs = [(v, idx) for v, idx in memory[current].items() if idx is not None and not revealed[idx]]
            if known_pairs:
                # try to select known pair if two indices known for same value across memory?
                # simplified: pick random unrevealed indices
                choices = [i for i in range(len(cards)) if not revealed[i]]
                a = random.choice(choices)
                b = random.choice([i for i in choices if i != a])
            else:
                choices = [i for i in range(len(cards)) if not revealed[i]]
                a = random.choice(choices)
                b = random.choice([i for i in choices if i != a])
            print(f'{current} выбирает {a} и {b}')
            time.sleep(0.6)
        if a is None or b is None or a==b:
            print('Неправильный выбор — ход пропущен.')
            turn += 1
            time.sleep(0.6)
            continue
        # reveal
        val_a, val_b = cards[a], cards[b]
        revealed[a] = revealed[a]
        revealed[b] = revealed[b]
        print('Открыто:', val_a, val_b)
        # NPCs update memory
        for p in names:
            if p != current:
                if not revealed[a]:
                    memory[p][val_a] = a
                if not revealed[b]:
                    memory[p][val_b] = b
        # check match
        if val_a == val_b:
            print(current, 'нашёл пару!')
            scores[current] += 1
            revealed[a] = revealed[b] = True
            # current gets another turn (do not increment)
        else:
            # no match, but update current's memory
            memory[current][val_a] = a
            memory[current][val_b] = b
            turn += 1
        time.sleep(0.8)
    clear()
    print('Итоги Memory:')
    for p in names:
        print(p, scores[p])
    press_enter()

# -----------------------
# 6) Pizza Memory с другими игроками
# Sequence memory where multiple players attempt to reproduce sequence; best accuracy wins.
# -----------------------
def pizza_memory_vs_players():
    clear()
    print('=== Pizza Memory с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ', 2) or 4
    levels = input_int('Уровней (по умолчанию 5): ', 1) or 5
    names = names_list(n)
    toppings = ['cheese','tomato','mushroom','pepperoni','olive','onion','basil']
    seq = []
    scores = {p:0 for p in names}
    for lv in range(1, levels+1):
        seq.append(random.choice(toppings))
        clear()
        print('Последовательность:')
        print(' '.join(seq))
        time.sleep(1.5)
        clear()
        # each player attempts
        for p in names:
            if p == 'You':
                ans = input('Введите последовательность через пробел: ').strip().lower().split()
                correct = ans == seq
            else:
                # NPC reproduces with some error probability decreasing with level
                accuracy = max(0.2, 1.0 - lv*0.12 + random.uniform(-0.1, 0.1))
                if random.random() < accuracy:
                    correct = True
                else:
                    correct = False
                print(p, 'ответил', 'верно' if correct else 'неверно')
            if correct:
                scores[p] += 1
        time.sleep(0.7)
    clear()
    print('Итоги Pizza Memory:')
    for p in names:
        print(p, scores[p])
    press_enter()

# -----------------------
# 7) Food Memory с другими игроками
# Same as Pizza Memory with food items.
# -----------------------
def food_memory_vs_players():
    clear()
    print('=== Food Memory с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ', 2) or 4
    rounds = input_int('Раундов (по умолчанию 6): ', 1) or 6
    names = names_list(n)
    foods = ['apple','banana','bread','cheese','cake','egg','fish','tomato']
    seq = []
    scores = {p:0 for p in names}
    for r in range(rounds):
        seq.append(random.choice(foods))
        clear()
        print('Запомните:')
        print(' '.join(seq))
        time.sleep(1.2)
        clear()
        for p in names:
            if p == 'You':
                ans = input('Введите через пробел: ').strip().lower().split()
                correct = ans == seq
            else:
                accuracy = max(0.3, 1 - r*0.13 + random.uniform(-0.1,0.1))
                correct = random.random() < accuracy
                print(p, '->', 'верно' if correct else 'неверно')
            if correct:
                scores[p] += 1
        time.sleep(0.6)
    clear()
    print('Итоги Food Memory:')
    for p in names:
        print(p, scores[p])
    press_enter()

# -----------------------
# 8) Sound Memory с другими игроками
# -----------------------
def sound_memory_vs_players():
    clear()
    print('=== Sound Memory с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ', 2) or 4
    rounds = input_int('Раундов (по умолчанию 5): ', 1) or 5
    names = names_list(n)
    sounds = ['beep','boop','ding','buzz','click','tock']
    seq = []
    scores = {p:0 for p in names}
    for r in range(rounds):
        seq.append(random.choice(sounds))
        clear()
        for s in seq:
            print(s.upper())
            time.sleep(0.5)
            clear()
        for p in names:
            if p == 'You':
                ans = input('Введите последовательность через пробел: ').strip().lower().split()
                correct = ans == seq
            else:
                accuracy = max(0.2, 1 - r*0.15 + random.uniform(-0.1,0.1))
                correct = random.random() < accuracy
                print(p, '->', 'верно' if correct else 'неверно')
            if correct:
                scores[p] += 1
        time.sleep(0.5)
    clear()
    print('Итоги Sound Memory:')
    for p in names:
        print(p, scores[p])
    press_enter()

# -----------------------
# 9) Симулятор стройки с другими игроками
# Team-building construction simulator where players contribute.
# -----------------------
def construction_vs_players():
    clear()
    print('=== Симулятор стройки с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ', 1) or 4
    days = input_int('Дней (по умолчанию 10): ', 1) or 10
    names = names_list(n)
    progresses = {p:0 for p in names}
    budget = 200
    for d in range(1, days+1):
        clear()
        print(f'День {d}/{days}. Бюджет: {budget}')
        for p in names:
            if p == 'You':
                action = input('Вкладываться или отдыхать? invest/rest (i/r): ').strip().lower()
                if action == 'i' and budget > 0:
                    invest = min(20, budget)
                    progress = invest // 2 + random.randint(0,5)
                    progresses[p] += progress
                    budget -= invest
                    print('Вы вложили', invest, 'прогресс', progress)
                else:
                    print('Вы отдыхали.')
            else:
                # NPC contribution depends on random willingness
                if random.random() < 0.6:
                    invest = random.randint(5,20)
                    progress = invest // 2 + random.randint(0,4)
                    progresses[p] += progress
                    budget -= invest
                    print(p, 'вложил', invest)
        # show totals
        total_progress = sum(progresses.values())
        print('Общий прогресс:', total_progress)
        if total_progress >= 100:
            print('Стройка завершена!')
            press_enter()
            return
        time.sleep(0.6)
    print('Время закончилось. Общий прогресс:', sum(progresses.values()))
    press_enter()

# -----------------------
# 10) Комнаты с другими игроками
# Multiplayer hide-and-seek in rooms; monsters appear and players hide/seek.
# -----------------------
def rooms_vs_players():
    clear()
    print('=== Комнаты с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 5): ', 2) or 5
    rooms_count = input_int('Сколько комнат (по умолчанию 8): ', 3) or 8
    names = names_list(n)
    player_rooms = {p: random.randrange(rooms_count) for p in names}
    hidden = {p: False for p in names}
    alive = set(names)
    rounds = input_int('Раундов (по умолчанию 10): ', 1) or 10
    for r in range(1, rounds+1):
        clear()
        print(f'Раунд {r}/{rounds}. Игроки живы: {len(alive)}')
        # for each player decide action
        for p in list(alive):
            if p == 'You':
                cmd = input('Ваше действие: move L/R / hide / search (m/h/s) (Enter skip): ').strip().lower()
                if cmd.startswith('m'):
                    dirc = input('L или R: ').strip().lower()
                    nr = player_rooms[p] - 1 if dirc == 'l' else player_rooms[p] + 1
                    if 0 <= nr < rooms_count:
                        player_rooms[p] = nr
                        hidden[p] = False
                        print('Вы вошли в комнату', nr)
                elif cmd == 'h':
                    hidden[p] = True
                    print('Вы спрятались.')
                elif cmd == 's':
                    print('Вы обыскали комнату.')
            else:
                # NPC move/hide/search probabilistically
                act = random.random()
                if act < 0.4:
                    # move
                    dirc = random.choice([-1,1])
                    nr = player_rooms[p] + dirc
                    if 0 <= nr < rooms_count:
                        player_rooms[p] = nr
                        hidden[p] = False
                elif act < 0.7:
                    hidden[p] = True
                else:
                    pass  # search
        # monsters appear randomly in rooms and eat unhidden players
        monster_room = random.randrange(rooms_count) if random.random() < 0.35 else None
        if monster_room is not None:
            victims = [p for p in alive if player_rooms[p] == monster_room and not hidden[p]]
            for v in victims:
                print('Монстр съел', v)
                alive.remove(v)
        time.sleep(0.8)
        if len(alive) <= 1:
            break
    clear()
    print('Игра окончена. Выжившие:', ', '.join(sorted(alive)))
    press_enter()

# -----------------------
# 11) Проклятие с другими игроками
# House roaming where each round an effect appears; players experience it; last alive wins.
# -----------------------
def curse_vs_players():
    clear()
    print('=== Проклятие с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 5): ', 2) or 5
    rooms_count = input_int('Комнат в доме (по умолчанию 6): ', 2) or 6
    names = names_list(n)
    healths = {p: 10 for p in names}
    positions = {p: random.randrange(rooms_count) for p in names}
    rounds = input_int('Раундов (по умолчанию 12): ', 1) or 12
    effects = [
        ('shadow','-2'), ('blessing','+2'), ('freeze','-1'),
        ('feast','+1'), ('curse_sleep','-1'), ('mana','+1')
    ]
    for r in range(1, rounds+1):
        clear()
        print(f'Раунд {r}/{rounds}')
        print('Позиции игроков:', positions)
        # each player chooses move or stay
        for p in names:
            if p == 'You':
                cmd = input('move L/R or stay (m/s) (Enter stay): ').strip().lower()
                if cmd.startswith('m'):
                    dirc = input('L или R: ').strip().lower()
                    nr = positions[p] - 1 if dirc == 'l' else positions[p] + 1
                    if 0 <= nr < rooms_count:
                        positions[p] = nr
            else:
                if random.random() < 0.6:
                    positions[p] = max(0, min(rooms_count-1, positions[p] + random.choice([-1,0,1])))
        # effect appears in random room
        effect = random.choice(effects)
        room = random.randrange(rooms_count)
        print(f'В комнате {room} проявилось: {effect[0]} ({effect[1]})')
        # apply effect to players in that room
        for p in names:
            if positions[p] == room:
                if effect[1].startswith('-'):
                    delta = int(effect[1])
                    healths[p] += delta
                else:
                    delta = int(effect[1].replace('+',''))
                    healths[p] += delta
                print(p, '-> здоровье', healths[p])
        # remove dead
        for p in list(names):
            if healths[p] <= 0:
                print(p, 'умер от эффекта.')
                names.remove(p)
        time.sleep(0.8)
        if len(names) <= 1:
            break
    clear()
    print('Итог здоровья игроков:')
    for p, h in healths.items():
        print(p, h)
    press_enter()

# -----------------------
# 12) Живой автомобиль с глазами и ртом с другими игроками
# Cute multiplayer pet car interactions: players can feed, polish, drive; car responds.
# -----------------------
def living_car_vs_players():
    clear()
    print('=== Живой автомобиль с глазами и ртом с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ', 1) or 4
    names = names_list(n)
    car = {'mood':5, 'fuel':5, 'dirt':3}
    rounds = input_int('Раундов взаимодействия (по умолчанию 8): ', 1) or 8
    for r in range(1, rounds+1):
        clear()
        print(f'Раунд {r}/{rounds}. Машина — настроение {car["mood"]}, топливо {car["fuel"]}, грязь {car["dirt"]}')
        for p in names:
            if p == 'You':
                action = choose_option('Действие для машины:', ['feed (заправить)','clean (почистить)','talk','drive','skip'])
                if action is None:
                    print('Пропуск.')
                elif action == 0:
                    car['fuel'] = min(10, car['fuel'] + 3); car['mood'] = min(10, car['mood']+1)
                    print('Вы заправили машину.')
                elif action == 1:
                    car['dirt'] = max(0, car['dirt'] - 2); car['mood'] = min(10, car['mood']+1)
                    print('Вы почистили машину.')
                elif action == 2:
                    car['mood'] = min(10, car['mood']+1); print('Вы поговорили с машиной.')
                elif action == 3:
                    if car['fuel'] > 0:
                        car['fuel'] -= 1; car['mood'] = min(10, car['mood']+1)
                        print('Вы покатались — машина довольна.')
                    else:
                        print('Нет топлива.')
            else:
                # NPC action probabilistic
                act = random.random()
                if act < 0.25:
                    car['fuel'] = min(10, car['fuel'] + 2); car['mood'] += 1
                elif act < 0.5:
                    car['dirt'] = max(0, car['dirt'] - 1); car['mood'] += 1
                elif act < 0.8:
                    if car['fuel'] > 0:
                        car['fuel'] -= 1; car['mood'] += 1
                # else skip
        # small decay
        car['mood'] = max(0, car['mood'] - 1)
        car['dirt'] = min(10, car['dirt'] + 1)
        time.sleep(0.6)
    clear()
    print('Финальное состояние машины:', car)
    press_enter()
# -----------------------
# Singleplayer games
# -----------------------

def revenge_game():
    clear()
    print('=== Месть ===')
    story = ['You were betrayed','You lost something','You were humiliated']
    reason = random.choice(story)
    print('Сюжет:', reason)
    choice = input_choice('Как мстить?', ['Confront','Sabotage','Forgive'])
    if choice == 'Forgive':
        print('Месть отменена. Вы чувствуете облегчение.')
    else:
        outcome = random.choice(['Success','Backfire','Unclear'])
        print('Исход:', outcome)
    press_enter()

def happy_car():
    clear()
    print('=== Довольная машина ===')
    mood = 5
    fuel = 3
    for i in range(5):
        clear()
        print(f'Настроение: {mood}, Топливо: {fuel}')
        action = choose_option('Действие:', ['Почистить','Заменить масло','Покататься','Покормить топливом','Поговорить'])
        if action == 0:
            mood = min(10, mood+1)
            safe_print('Машина сияет и улыбается.')
        elif action == 1:
            mood = min(10, mood+2); fuel = max(0, fuel-1)
            safe_print('Машина мурлычет.')
        elif action == 2:
            if fuel > 0:
                fuel -= 1; mood = min(10, mood+2)
                safe_print('Весёлая поездка!')
            else:
                safe_print('Нет топлива.')
        elif action == 3:
            fuel += 2
            safe_print('Топливо добавлено.')
        elif action == 4:
            mood = min(10, mood+1)
            safe_print('Машина отвечает "Бип-бип!"')
        else:
            safe_print('Вы ничего не сделали.')
    print('Итог — машина довольна на', mood)
    press_enter()

def the_path():
    clear()
    print('=== Путь ===')
    steps = input_int('Сколько шагов пройти (по умолчанию 12): ', 1) or 12
    encounters = ['старый мост','дерево с запиской','пустая колодец','сторожевой камень','мираж']
    mood = 0
    for s in range(steps):
        item = random.choice(encounters)
        print(f'Шаг {s+1}: вы встретили {item}')
        cmd = input('Взаимодействовать? (y/n): ').strip().lower()
        if cmd == 'y':
            outcome = random.choice(['+','-','neutral'])
            if outcome == '+':
                mood += 1; print('Это принесло утешение.')
            elif outcome == '-':
                mood -= 1; print('Это было опасно.')
            else:
                print('Ничего не произошло.')
        time.sleep(0.4)
    print('Итоговое состояние:', mood)
    press_enter()

def lights_out():
    clear()
    print('=== Свет выключен ===')
    print('Вы в доме, свет гаснет. Нужно добраться до двери на ощупь.')
    pos = 0
    target = 6
    while pos < target:
        step = input_choice('Куда двигаться?', ['Left','Right','Forward','Listen'])
        if step == 'Forward':
            pos += 1
            print('Вы продвинулись вперёд.')
        elif step == 'Listen':
            hint = random.choice(['шаги справа','вода слева','тишина'])
            print('Вы слышите:', hint)
        else:
            print('Вы двинулись в сторону и потеряли время.')
            pos += 0
        if random.random() < 0.12:
            print('Что-то зашевелилось в темноте...')
        time.sleep(0.5)
    print('Вы нашли дверь и вышли на свет.')
    press_enter()

def scareman():
    clear()
    print('=== Страхолюдина ===')
    fear = 0
    for i in range(5):
        event = random.choice(['шепот','тень','вопль','шелест'])
        print('Событие:', event)
        resp = input('Спрятаться или бежать? (h/run): ').strip().lower()
        if resp == 'h':
            fear += random.randint(0,1)
            safe_print('Вы затаились...')
        else:
            fear += random.randint(1,3)
            safe_print('Вы бежите — сердце колотится!')
    print('Уровень страха:', fear)
    press_enter()

def clown_game():
    clear()
    print('=== Клоун ===')
    mood = 0
    for i in range(4):
        action = choose_option('Что делать?', ['Смеяться','Подходить ближе','Убежать','Остаться'])
        if action == 0:
            mood += 1; safe_print('Клоун улыбается. Вы чувствуете лёгкое облегчение.')
        elif action == 1:
            mood += random.choice([-2,2]); safe_print('Клоун реагирует непредсказуемо.')
        elif action == 2:
            mood += -1; safe_print('Вы убежали — но клоун догнал вас в кошмаре.')
        else:
            safe_print('Ничего не происходит.')
    print('Итог:', mood)
    press_enter()

def spirits_months():
    clear()
    print('=== Духи месяцев года ===')
    months = ['январь','февраль','март','апрель','май','июнь','июль','август','сентябрь','октябрь','ноябрь','декабрь']
    print('Вы вызываете духа месяца...')
    chosen = random.choice(months)
    print('Дух', chosen, 'рассказывает пророчество:', random.choice(['жаркое лето','холодная зима','урожай','буря']))
    press_enter()

def spirits_seasons():
    clear()
    print('=== Духи времён года ===')
    seasons = ['весна','лето','осень','зима']
    for s in seasons:
        print(s, '->', random.choice(['торжествует','спит','плачет','поёт']))
    press_enter()

def spirits_weekdays():
    clear()
    print('=== Духи дней недели ===')
    days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
    for d in days:
        print(d, '-', random.choice(['энергия','покой','тоска','веселье','хандра','радость','сонливость']))
    press_enter()

def abandoned_place():
    clear()
    print('=== Заброшка ===')
    rooms = ['кухня','подвал','чердак','зал','веранда']
    pos = random.choice(rooms)
    print('Вы в', pos)
    for i in range(5):
        obj = random.choice(['старый диван','разбитое окно','письмо','кровавая метка','детская игрушка'])
        print('Найдено:', obj)
        ans = input('Забрать / Уйти? (take/leave): ').strip().lower()
        if ans == 'take' and random.random() < 0.2:
            print('Вы получили таинственный предмет...')
        time.sleep(0.6)
    press_enter()

def zombie_apocalypse():
    clear()
    print('=== Зомби апокалипсис ===')
    survivors = 3
    supplies = 5
    days = input_int('Сколько дней вы хотите выживать? (по умолчанию 5): ', 1) or 5
    for d in range(days):
        print(f'День {d+1}: supplies {supplies}, survivors {survivors}')
        event = random.choice(['raid','quiet','zombie_horde'])
        if event == 'raid':
            lost = random.randint(0,1)
            survivors -= lost
            supplies -= random.randint(0,2)
            print('Налёт мародёров!')
        elif event == 'zombie_horde':
            lost = random.randint(0,2)
            survivors -= lost
            print('Наши потеряли', lost)
        else:
            supplies += random.randint(0,2)
            print('Тихий день — пополнили запасы.')
        if survivors <= 0 or supplies < 0:
            print('Все пали.')
            press_enter()
            return
        time.sleep(0.6)
    print('Вы выжили! Осталось людей:', survivors)
    press_enter()

def dont_eat_cake():
    clear()
    print('=== Не ешь кекс ===')
    print('Перед вами кекс. Не ешьте его.')
    for i in range(3):
        ans = input('Сдержитесь? (y/n): ').strip().lower()
        if ans == 'y':
            print('Вы сильны!')
        else:
            print('Вы съели кекс и случилось странное...')
            break
        time.sleep(0.5)
    press_enter()

def five_nights_freddy():
    clear()
    print('=== 5 ночей с Freddy (упрощено) ===')
    nights = input_int('Ночей (по умолчанию 3): ', 1) or 3
    sanity = 10
    for n in range(nights):
        print('Ночь', n+1)
        checks = random.randint(1,3)
        for c in range(checks):
            if random.random() < 0.25:
                sanity -= random.randint(1,3)
                print('Аниматроник рядом! Потеря рассудка.')
            else:
                print('Тишина...')
            time.sleep(0.6)
        if sanity <= 0:
            print('Вы потеряли рассудок.')
            press_enter()
            return
    print('Вы пережили ночи! Рассудок:', sanity)
    press_enter()

def run_run_run():
    clear()
    print('=== БЕГИ ===')
    distance = 0
    while distance < 20:
        cmd = input('Бежать быстро или медленно? (fast/slow): ').strip().lower()
        if cmd == 'fast':
            distance += random.randint(2,5)
            print('Вы ускорились.')
        else:
            distance += random.randint(0,2)
            print('Вы медленно бежите.')
        if random.random() < 0.1:
            print('Что-то догоняет вас!')
        time.sleep(0.4)
    print('Вы убежали на безопасное расстояние.')
    press_enter()

def be_quieter():
    clear()
    print('=== Будь тише! ===')
    noise = 0
    for i in range(6):
        action = input('Сделать тихо или шумно? (quiet/noisy): ').strip().lower()
        if action == 'quiet':
            noise += 0
            print('Тихо...')
        else:
            noise += random.randint(1,3)
            print('Шум!')
        if noise >= 6 and random.random() < 0.5:
            print('Вы привлекли внимание.')
            press_enter()
            return
        time.sleep(0.4)
    print('Вы прошли незамеченным.')
    press_enter()

def oddities():
    clear()
    print('=== Странности ===')
    for i in range(5):
        event = random.choice(['зеркало показывает не тебя','часы идут назад','дерево шепчет','тень улыбается'])
        print('Странность:', event)
        input('Нажмите Enter, чтобы продолжить...')
    press_enter()

def talk_planets():
    clear()
    print('=== Говори с планетами ===')
    planets = ['Mercury','Venus','Earth','Mars','Jupiter','Saturn']
    for _ in range(4):
        p = random.choice(planets)
        print(p, 'говорит:', random.choice(['Помоги мне','Я одинок','Спасибо','Я в порядке']))
        input('Ответить (Enter): ')
    press_enter()

def apocalypse():
    clear()
    print('=== Конец света ===')
    scenario = random.choice(['метеориты','ядерная война','паника','климатическая катастрофа'])
    print('Сценарий:', scenario)
    choice = input_choice('Что делать?', ['Hide','Flee','Join others','Record'])
    print('Исход вашего выбора:', random.choice(['Выживете','Погибнете','Останетесь в подвешенном состоянии']))
    press_enter()

def revive_ability():
    clear()
    print('=== Способность оживлять ===')
    tries = input_int('Сколько раз применить способность? (по умолчанию 3): ', 1) or 3
    for i in range(tries):
        target = input_choice('Кого оживить?', ['Растение','Животное','Покинутый предмет','Камень'])
        success = random.random() < 0.5
        if success:
            print('Оживление успешно —', target, 'ожило!')
        else:
            print('Не удалось. Цена: вы чувствуете слабость.')
        time.sleep(0.6)
    press_enter()

# -----------------------
# Multiplayer variants (simulated NPCs)
# -----------------------

def revenge_vs_players():
    clear()
    print('=== Месть с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ', 2) or 4
    names = names_list(n)
    scores = {p:0 for p in names}
    for r in range(4):
        victim = random.choice(names)
        print('Раунд', r+1, 'жертва:', victim)
        for p in names:
            if p == 'You':
                action = choose_option('Что вы делаете?', ['Саботаж','Публичная порка','Прощение','Игнорировать'])
                if action in (0,1):
                    scores[p] += random.randint(0,2)
            else:
                if random.random() < 0.6:
                    scores[p] += random.randint(0,2)
        time.sleep(0.6)
    clear()
    print('Результаты мстителей:')
    for p in names:
        print(p, scores[p])
    press_enter()

def apocalypse_vs_players():
    clear()
    print('=== Конец света с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 5): ', 2) or 5
    names = names_list(n)
    resources = {p: random.randint(1,5) for p in names}
    rounds = input_int('Раундов выживания (по умолчанию 6): ', 1) or 6
    for r in range(rounds):
        print('Раунд', r+1)
        event = random.choice(['radiation','storm','panic','calm'])
        if event == 'storm':
            loser = random.choice(names)
            resources[loser] = max(0, resources[loser]-2)
            print(loser, 'потерял ресурсы.')
        elif event == 'panic':
            giver = random.choice(names)
            taker = random.choice([x for x in names if x!=giver])
            transfer = min(2, resources[giver])
            resources[giver] -= transfer
            resources[taker] += transfer
            print(giver, 'поделился с', taker)
        else:
            print('Стабильно.')
        time.sleep(0.6)
    print('Итоги ресурсов:')
    for p in names:
        print(p, resources[p])
    press_enter()

def five_nights_vs_players():
    clear()
    print('=== 5 ночей с Freddy с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 3): ', 1) or 3
    names = names_list(n)
    sanity = {p:10 for p in names}
    nights = input_int('Ночей (по умолчанию 3): ',1) or 3
    for night in range(nights):
        print('Ночь', night+1)
        for p in names:
            loss = random.randint(0,3)
            sanity[p] -= loss
            print(p, 'потерял', loss)
        time.sleep(0.6)
    print('Остатки разума:')
    for p in names:
        print(p, sanity[p])
    press_enter()

def abandoned_vs_players():
    clear()
    print('=== Заброшка с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ', 1) or 4
    names = names_list(n)
    health = {p:10 for p in names}
    rooms = ['кухня','чердак','подвал','зал']
    for r in range(5):
        room = random.choice(rooms)
        print('Комната:', room)
        for p in names:
            if p == 'You':
                cmd = input('Кирпич/искать/уйти (brick/search/leave): ').strip().lower()
                if cmd == 'search' and random.random() < 0.3:
                    health[p] += 1; print('Вы нашли аптечку.')
            else:
                if random.random() < 0.2:
                    health[p] -= 1
        time.sleep(0.6)
    print('Здоровье игроков:')
    for p in names:
        print(p, health[p])
    press_enter()

def oddities_vs_players():
    clear()
    print('=== Странности с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 5): ', 1) or 5
    names = names_list(n)
    weird = {p:0 for p in names}
    for i in range(6):
        effect = random.choice(['mirror','voices','timewarp','shadows'])
        print('Эффект:', effect)
        for p in names:
            if random.random() < 0.3:
                weird[p] += 1
        time.sleep(0.5)
    print('Показатели странностей:')
    for p in names:
        print(p, weird[p])
    press_enter()

def revive_vs_players():
    clear()
    print('=== Способность оживлять с другими игроками ===')
    n = input_int('Игроков (включая вас) (по умолчанию 4): ',1) or 4
    names = names_list(n)
    alive = {p: random.choice([True, True, False]) for p in names}
    print('Исходное состояние (alive):', alive)
    for p in names:
        if p == 'You':
            target = input('Кого вы оживите? (имя) или Enter случайно: ').strip()
            if target not in names:
                target = random.choice(names)
            success = random.random() < 0.6
            alive[target] = success
            print('Вы пытались оживить', target, 'успех=', success)
        else:
            if random.random() < 0.4:
                t = random.choice(names)
                alive[t] = random.random() < 0.5
    print('Финальное состояние alive:', alive)
    press_enter()
# -------------------------
# Collect games into menu
# -------------------------
GAMES = [
    ('Math Quiz', math_quiz),
    ('Guess the Number', guess_number),
    ('Minesweeper (Сапёр)', minesweeper),
    ('Dogonalki (Догонялки)', dogonalki),
    ('Hide & Seek (Прятки)', hide_and_seek),
    ('Snakes and Ladders (Змеи и Лестницы)', snakes_and_ladders),
    ('Прятки-догонялки ВИРУС', hide_chase_virus),
    ('Бункер', bunker),
    ('Догонялки с мячом', chase_with_ball),
    ('Выживание', survival_game),
    ('Рельсы', rails_game),
    ('Гонки', racing_game),
    ('Вышибалы', dodgeball),
    ('Туман', fog_game),
    ('Рейд', raid_game),
    ('Термометр', thermometer_game),
    ('Змейка', snake_game),
    ('Решение поезда', trolley_game),
    ('Живой автомобиль', living_car),
    ('Живой автомобиль с глазами и ртом', living_car_with_face),
    ('Красный свет - зелёный свет', red_green_light),
    ('Третий лишний', odd_one_out),
    ('Сахарные соты', sugar_hives),
    ('Последний выживший', last_survivor),
    ('Стеклянный мост', glass_bridge),
    ('Драка', fight_game),
    ('Сумо', sumo),
    ('Карате', karate),
    ('Всё оживает!', everything_alive),
    ('Болтай с ожившими предметами', chat_with_items),
    ('Комнаты', rooms_game),
    ('Монстр', monster_game),
    ('Катастрофа', catastrophe),
    ('Преследование (ты — преследователь)', pursuit_player_chaser),
    ('Преследование с мячом (ты — преследователь)', pursuit_with_ball_player_chaser),
    ('Сказка', fairy_tale),
    ('Проклятие', curse_game),
    ('Настолка "Бункер"', bunker_boardgame),
    ('Предатель', traitor_game),
    ('Страх', fear_game),
    ('Паук', spider_game),
    ('День рождение', birthday_game),
    ('Стоматолог', dentist_game),
    ('Аквафобия', aquaphobia),
    ('Арахнофобия', arachnophobia),
    ('Клаустрофобия', claustrophobia),
    ('Lumber Jack', lumber_jack),
    ('Pizza Memory', pizza_memory),
    ('Food Memory', food_memory),
    ('Sound Memory', sound_memory),
    ('Memory (Pairs)', memory_classic),
    ("Liar's Bar", liars_bar),
    ('Hitman', hitman),
    ('True or False', true_or_false),
    ('Death Columns', death_columns),
    ('Guess the Word', guess_the_word),
    ("Who's SUS?", whos_sus),
    ('Мафия', mafia_game),
    ('Оживший мир', living_world),
    ('Русская рулетка', russian_roulette),
    ('Интерпретация', interpretation_game),
    ('Репутация', reputation),
    ('Танки', tanks_game),
    ('Симулятор компьютерного вируса', virus_simulator),
    ('Симулятор стройки', construction_simulator),
    ('Школа', school_simulator),
    ('Сложный Math Quiz', hard_math_quiz),
    ('Кликер', clicker),
    ('Math Quiz на время', timed_math_quiz),
    ('Очень сложный Math Quiz', very_hard_math_quiz),
    ('Math Quiz но с другими игроками', math_quiz_vs_players),
    ('Планетарий', planetarium),
    ('Ожившие планеты', living_planets),
    ('Звёзды', stars_game),
    ('Блеск', shine_game),
    ('Quiz (basic)', quiz_easy),
    ('Сложный Quiz', quiz_hard),
    ('Quiz на время', quiz_timed),
    ('Очень сложный Quiz', quiz_very_hard),
    ('Quiz но с другими игроками', quiz_vs_players),
    ('Сапёр с другими игроками', minesweeper_vs_players),
    ('Догонялки с другими игроками', chase_vs_players),
    ('Догонялки с мячом с другими игроками', chase_ball_vs_players),
    ('Кликер с другими игроками', clicker_vs_players),
    ('Memory с другими игроками', memory_vs_players),
    ('Pizza Memory с другими игроками', pizza_memory_vs_players),
    ('Food Memory с другими игроками', food_memory_vs_players),
    ('Sound Memory с другими игроками', sound_memory_vs_players),
    ('Симулятор стройки с другими игроками', construction_vs_players),
    ('Комнаты с другими игроками', rooms_vs_players),
    ('Проклятие с другими игроками', curse_vs_players),
    ('Живой автомобиль с глазами и ртом с другими игроками', living_car_vs_players),
    ('Месть', revenge_game),
    ('Довольная машина', happy_car),
    ('Путь', the_path),
    ('Свет выключен', lights_out),
    ('Страхолюдина', scareman),
    ('Клоун', clown_game),
    ('Духи месяцев года', spirits_months),
    ('Духи времён года', spirits_seasons),
    ('Духи дней недели', spirits_weekdays),
    ('Заброшка', abandoned_place),
    ('Зомби апокалипсис', zombie_apocalypse),
    ('Не ешь кекс', dont_eat_cake),
    ('5 ночей с Freddy', five_nights_freddy),
    ('БЕГИ', run_run_run),
    ('Будь тише!', be_quieter),
    ('Странности', oddities),
    ('Говори с планетами', talk_planets),
    ('Конец света', apocalypse),
    ('Способность оживлять', revive_ability),
    ('Месть с другими игроками', revenge_vs_players),
    ('Конец света с другими игроками', apocalypse_vs_players),
    ('5 ночей с Freddy с другими игроками', five_nights_vs_players),
    ('Заброшка с другими игроками', abandoned_vs_players),
    ('Странности с другими игроками', oddities_vs_players),
    ('Способность оживлять с другими игроками', revive_vs_players),
]

# -------------------------
# Main menu & launcher
# -------------------------
def main_menu():
    while True:
        clear()
        print('=== Minigames Hub (Python, no external modules) ===\n')
        for idx, (title, _) in enumerate(GAMES, start=1):
            print(f'{idx}. {title}')
        print('0. Выход')
        choice = input_int('\nВыберите игру (номер): ', 0, len(GAMES))
        if choice is None:
            continue
        if choice == 0:
            print('Пока! Спасибо за игру.')
            time.sleep(0.3)
            break
        game = GAMES[choice-1][1]
        try:
            game()
        except Exception as e:
            print('Произошла ошибка в игре:', e)
            import traceback
            traceback.print_exc()
            press_enter()

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print('\nВыход. До свидания.')
        sys.exit(0)
