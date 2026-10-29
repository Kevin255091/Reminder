#在Python Prompt之下，用from TaiwanButterflyAnalysis import *
#之後就可以直接分析各個書本提到的蝴蝶種類差異

def get_rid_of_parentheses_comment(string):
    if string == '':
        return ''

    if string[-1] == ')':
        i = len(string)-2
        while i >= 0:
            if string[i] == '(':
                break
            i -= 1
        
        if i == 0:
            print('全沒了')
            return '?'

        return string[:i]

    return string

def is_butterfly_name_line(line):
    L = line.strip().rstrip('\r\n')
    ws = L.split(' ')
    if 2 <= len(ws):
        name1 = get_rid_of_parentheses_comment(ws[0])
        name2 = get_rid_of_parentheses_comment(ws[1])
        if name1[-1] == '蝶' and name2[-1] == '蝶':
            return True

    return False

books_dict = {}
books_dict['台灣常見的蝴蝶'] = []
books_dict['蝶影尋蹤123'] = []
books_dict['蝴蝶100'] = []
books_dict['近郊蝴蝶'] = []
books_dict['蝴蝶生活史圖鑑'] = []

台灣常見的蝴蝶 = books_dict['台灣常見的蝴蝶']
蝶影尋蹤 = books_dict['蝶影尋蹤123']
蝴蝶一百 = books_dict['蝴蝶100']
近郊蝴蝶 = books_dict['近郊蝴蝶']
蝴蝶生活史圖鑑 = books_dict['蝴蝶生活史圖鑑']


with open('台灣的蝴蝶.txt', 'r', encoding='utf-8') as fin:
    while True:
        line = fin.readline()

        if line == '':
            break

        L = line.strip().rstrip('\r\n')

        if is_butterfly_name_line(L):
            butterfly_name = L
            while True:
                last_pos = fin.tell()
                line = fin.readline()

                if line == '':
                    break

                if is_butterfly_name_line(line):
                    fin.seek(last_pos)
                    break

                L = line.strip().rstrip('\r\n')

                if L == '':
                    break

                if L.startswith('《'):
                    L1 = L.split('》')[0]
                    bookname = L1[1:]
                    
                    if butterfly_name in books_dict[bookname]:
                        print(f'{butterfly_name} 已經在 {bookname} 了!')
                        continue

                    books_dict[bookname].append(butterfly_name)

                continue


A = set(台灣常見的蝴蝶)
B = set(蝶影尋蹤)
C = set(蝴蝶一百)
D = set(近郊蝴蝶)
E = set(蝴蝶生活史圖鑑)


def print_sets_names():
    print('A = set(台灣常見的蝴蝶)')
    print('B = set(蝶影尋蹤)')
    print('C = set(蝴蝶一百)')
    print('D = set(近郊蝴蝶)')
    print('E = set(蝴蝶生活史圖鑑)')

print_sets_names()
