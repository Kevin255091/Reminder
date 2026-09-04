import datetime
from time import sleep
import re
from Lunar_to_2099 import get_lunar_date
from Lunar_to_2099 import lunar_date_str
from Lunar_to_2099 import get_jie

def str_to_date(date_str):
    try:
        date = [int(d) for d in date_str.split('-')]
        D = datetime.date(date[0], date[1], date[2])
    except:
        D = datetime.date(2000, 1, 1)

    return D

def print_lunar_festival(lunar_date, lunar_festival_filename):
    month = lunar_date[1]
    day   = lunar_date[2]

    lm = '正二三四五六七八九十冬臘'

    found = False
    with open(lunar_festival_filename, 'r', encoding='utf-8') as fin:
        for line in fin:
            L = line.rstrip('\r\n')

            if L[0] in lm:
                month_read = lm.index(L[0]) + 1
                day_read   = int(L[2:4])
                
                if month_read == month and day_read == day:
                    print(L[6:])
                    found = True

            elif L[0] == ' ':
                if month_read == month and day_read == day:
                    print(L.strip())
                    found = True
            else:
                print(f'Cannot recognize {L}')
                print('Program terminated.')
                input('按Enter鍵結束程式...')
                sys.exit()
    
    if found == False:
        print()

def get_weekday_number_str(date):
    s = ['一', '二', '三', '四', '五', '六', '日']
    return s[date.weekday()]

def check_weekly_routines(today, weekly_routines):
    something_mentioned = False
    weekday = today.weekday()
    if weekly_routines[weekday] != '':
        routine_list = [e for e in re.split(r'\s*,\s*', weekly_routines[weekday]) if e]
        for routine in routine_list:
            print('今天 ' + routine)
        something_mentioned = True
    tomorrow = today + datetime.timedelta(days=1)
    weekday = tomorrow.weekday()
    if weekly_routines[weekday] != '':
        routine_list = [e for e in re.split(r'\s*,\s*', weekly_routines[weekday]) if e]
        for routine in routine_list:
            print('明天 ' + routine)
        something_mentioned = True

    if something_mentioned:
        print('=================================================================')

    return something_mentioned

def check_future_plans(date, future_plans):
    something_mentioned = False

    today = datetime.date.today()
    extra_info = '       '
    if date == today:
        extra_info = '(今天)  '
    elif date == today + datetime.timedelta(days=1):
        extra_info = '(明天)  '
    elif date == today + datetime.timedelta(days=2):
        extra_info = '(後天)  '
    elif date == today + datetime.timedelta(days=3):
        extra_info = '(大後天)'
    else:
        extra_info = '(' + get_weekday_number_str(date) + ')    '

    for fp in future_plans:
        if date == fp[0]:
            print(str(fp[0]) + extra_info + ' ' + fp[1])
            something_mentioned = True

    if something_mentioned:
        print('=================================================================')

    return something_mentioned

weekly_routines_filename = 'weekly_routines.txt'
future_plans_filename = '記事本.txt'
memos_filename = 'memos.txt'
lunar_festival_filename = '農曆節慶.txt'

weekly_routines = ['', '', '', '', '', '', '']
future_plans = []

with open(weekly_routines_filename, 'r', encoding='utf-8') as f:
    for line in f:
        L = line.strip().rstrip('\r\n')
        if L != '':
            space_index = L.find(' ')
            weekday = L[:space_index]
            routines = L[space_index+1:]
            if weekday == '星期一':
                weekly_routines[0] += routines
            elif weekday == '星期二':
                weekly_routines[1] += routines
            elif weekday == '星期三':
                weekly_routines[2] += routines
            elif weekday == '星期四':
                weekly_routines[3] += routines
            elif weekday == '星期五':
                weekly_routines[4] += routines
            elif weekday == '星期六':
                weekly_routines[5] += routines
            elif weekday == '星期日':
                weekly_routines[6] += routines
            else:
                print('無法辨識星期幾')


today = datetime.date.today()
print('今天是 ' + str(today) + ' 星期' + get_weekday_number_str(today), end=', ')

lunar_date = get_lunar_date(datetime.datetime(today.year, today.month, today.day))
print(lunar_date_str(lunar_date[1], lunar_date[2]), end=' ')
print_lunar_festival(lunar_date, lunar_festival_filename)
jie = get_jie(today)
if jie == '':
    print('=================================================================')
else:
    print(jie)
    print('=================================================================')

with open(future_plans_filename, 'r', encoding='utf-8') as f:
    for line in f:
        L = line.strip().rstrip('\r\n')
        if L != '':
            space_index = L.find(' ')
            future_date = L[:space_index]
            plans = L[space_index+1:]
            
            if '~' in future_date:
                start_date, end_date = [str_to_date(dt) for dt in future_date.split('~')]
                
                if today < start_date and today + datetime.timedelta(days=2) >= start_date:
                    future_plans.append((start_date, plans))
                elif start_date <= today <= end_date:
                    future_plans.append((today, plans))

                continue

            if future_date == '':
                continue

            future_plans.append((str_to_date(future_date), plans))


magic_line_number = 34

something_mentioned = check_weekly_routines(today, weekly_routines)

d = today
for i in range(5):
    r = check_future_plans(d, future_plans)
    if r :
        something_mentioned = r
    d += datetime.timedelta(days=1)

print('備忘錄:')
with open(memos_filename, 'r', encoding='utf-8') as f:
    memo = False
    for line in f:
        L = line.strip().rstrip('\r\n')
        if L != '':
            print(L)
            memo = True

    if memo:
        print('=================================================================')
        something_mentioned = True
    else:
        print('無')


print()
    
if something_mentioned:
    input('按Enter鍵結束程式...')

if not something_mentioned:
    print('沒有特別事情要提醒。\n程式將在2秒後結束...\n')
    sleep(2)

