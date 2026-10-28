import os

def is_butterfly_name_line(line):
    L = line.strip().rstrip('\r\n')
    ws = L.split(' ')
    if len(ws) == 2 and ws[0][-1] == '蝶' and ws[1][-1] == '蝶':
        return True
    return False

books_dict = {}
books_dict['台灣常見的蝴蝶'] = set()
books_dict['蝶影尋蹤123'] = set()
books_dict['蝴蝶100'] = set()
books_dict['近郊蝴蝶'] = set()
books_dict['蝴蝶生活史圖鑑'] = set()

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
                    books_dict[bookname].add(butterfly_name)

                continue


