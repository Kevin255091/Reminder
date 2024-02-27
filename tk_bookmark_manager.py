import io
import re
from tkinter import *
from tkinter import messagebox
import random

def all_choose_btn_click():
    for i in range(bookmark_file_num):
        checkboxes[i].set(True)

def all_choose_cancel_btn_click():
    for i in range(bookmark_file_num):
        checkboxes[i].set(False)

def search_btn_click():
    bookmark_file_choose = []
    for i in range(bookmark_file_num):
        if checkboxes[i].get() == True:
            bookmark_file_choose.append(bookmark_files[i])

    if len(bookmark_file_choose) == 0:
        messagebox.showinfo('提示', '未選擇目標檔案')
        return 

    for fname in open_files_write_append:
        open_files_write_append[fname].close()
    open_files_write_append.clear()

    cursor_pos = text_widget.index(INSERT)
    line_start_pos = cursor_pos.split('.')[0] + '.0'

    buf = io.StringIO(text_widget.get(line_start_pos, END))
    for line in buf:
        no_newline = line.strip().rstrip('\r\n')
        if len(no_newline) > 0:
            #search_keywords = [ w.lower() for w in re.findall(r'[^,\s]+', no_newline) ]
            search_keywords = parse_keywords(no_newline)
            break
        else:
            hint_info_label.config(text='游標所在行沒有關鍵字可供搜尋')
            root.after(2000, hint_info_label_refresh)
            return

    keyword_num = len(search_keywords)
    text_widget.insert(INSERT, '\n==========================================================\n')
    text_widget.insert(INSERT, '關鍵字為：')
    for w in search_keywords:
        text_widget.insert(INSERT, '\"' + w + '\"  ')
    text_widget.insert(INSERT, '\n\n')

    result = False

    for fname in bookmark_file_choose:
        if fname not in open_files_read:
            try:
                f = open(fname, 'r', encoding='utf-8')
                open_files_read[fname] = f
            except IOError:
                messagebox.showinfo('提示', '無法開啟檔案 ' + fname)
                break
        else:
            f = open_files_read[fname]
            f.seek(0)

        bookmarks = []
        for line in f:
            no_newline = line.strip().rstrip('\r\n')
            if len(no_newline) > 0:
                bookmarks.append(no_newline)
                continue

            for bookmark_line in bookmarks:
                b = bookmark_line.lower()
                keyword_count = 0
                for keyword in search_keywords:
                    if keyword in b:
                        keyword_count += 1
                if keyword_count == keyword_num:
                    text_widget.insert(INSERT, fname + ' : \n')
                    for m in bookmarks:
                        restrict_m = strip_outrange_char(m)
                        text_widget.insert(INSERT, restrict_m+'\n')
                    text_widget.insert(INSERT, '\n')
                    result = True
                    break

            bookmarks.clear()

    if result == False:
        text_widget.insert(INSERT, '查無結果\n')
    text_widget.insert(INSERT, '==========================================================\n')

    text_widget.mark_set(INSERT, cursor_pos)

    hint_info_label.config(text='搜尋完成')
    root.after(2000, hint_info_label_refresh)

def strip_outrange_char(words):
    char_list = [words[j] for j in range(len(words)) if ord(words[j]) in range(65536)]
    s=''
    for c in char_list:
        s=s+c
    return s

def hint_info_label_refresh():
    hint_info_label.config(text='')

def write_append_btn_click():
    bookmark_file_choose = []
    for i in range(bookmark_file_num):
        if checkboxes[i].get() == True:
            bookmark_file_choose.append(bookmark_files[i])

    if len(bookmark_file_choose) == 0:
        messagebox.showinfo('提示', '未選擇目標檔案')
        return

    if len(bookmark_file_choose) > 1:
        messagebox.showinfo('提示', '寫入的目標檔案只能有一個')
        return

    bookmark_file = bookmark_file_choose[0]

    if bookmark_file not in open_files_write_append:
        try:
            f = open(bookmark_file, 'a', encoding='utf-8')
            open_files_write_append[bookmark_file] = f
        except IOError:
            messagebox.showinfo('提示', '無法開啟檔案 ' + bookmark_file)
            return
    else:
        f = open_files_write_append[bookmark_file]

    bookmarks = []
    buf = io.StringIO(text.get('1.0', END))
    write_count = 0
    write_fail_occur = False
    for line in buf:
        no_newline = line.strip().rstrip('\r\n')
        if len(no_newline) > 0:
            bookmarks.append(no_newline)
            continue

        if len(bookmarks) == 2:
            try:
                f.write(bookmarks[0] + '\n' + bookmarks[1] + '\n\n')
            except Exception as e:
                messagebox.showerror('錯誤', str(e))
                write_fail_occur = True
                break
            write_count += 1
            text_widget.delete('1.0', '4.0')
            bookmarks.clear()
            continue

        if len(bookmarks) == 1:
            messagebox.showinfo('提示', '僅有一行的資料不可寫入')
            write_fail_occur = True
            break

        if len(bookmarks) == 0:
            text_widget.delete('1.0', '2.0')
            continue

        if len(bookmarks) > 2:
            if messagebox.askquestion('提示', '有一筆資料超過三行，確定寫入?') == 'yes':
                s = ''
                for b in bookmarks:
                    s += b + '\n'
                s += '\n'
                f.write(strip_outrange_char(s))
                write_count += 1
                text_widget.delete('1.0', str(len(bookmarks)+2) + '.0')
                bookmarks.clear()
            else:
                write_fail_occur = True
                break

    while write_fail_occur == False and len(bookmarks) > 0:
        if len(bookmarks) == 2:
            try:
                f.write(bookmarks[0] + '\n' + bookmarks[1] + '\n\n')
            except Exception as e:
                messagebox.showerror('錯誤', str(e))
                write_fail_occur = True
                break
            write_count += 1
            text_widget.delete('1.0', '3.0')
        elif len(bookmarks) == 1:
            showinfo('提示', '僅有一行的資料不可寫入')
            write_fail_occur = True
        elif len(bookmarks) > 2:
            if messagebox.askquestion('提示', '有一筆資料超過三行，確定寫入?') == 'yes':
                s = ''
                for b in bookmarks:
                    s += b + '\n'
                s += '\n'
                f.write(strip_outrange_char(s))
                write_count += 1
                text_widget.delete('1.0', str(len(bookmarks)+1) + '.0')
            else:
                write_fail_occur = True
        break

    if write_count > 0:
        if write_fail_occur == False:
            hint_info_label.config(text='寫入緩衝區成功')
        else:
            hint_info_label.config(text='部分寫入緩衝區成功')
        root.after(2000, hint_info_label_refresh)

def show_random_bookmarks_btn_click():
    bookmark_file_choose = []
    for i in range(bookmark_file_num):
        if checkboxes[i].get() == True:
            bookmark_file_choose.append(bookmark_files[i])

    if len(bookmark_file_choose) == 0:
        messagebox.showinfo('提示', '未選擇目標檔案')
        return 

    for fname in open_files_write_append:
        open_files_write_append[fname].close()
    open_files_write_append.clear()

    cursor_pos = text_widget.index(INSERT)
    line_start_pos = cursor_pos.split('.')[0] + '.0'
    next_line_start_pos = str(int(line_start_pos.split('.')[0]) + 1) + '.0'
    line = text.get(line_start_pos, next_line_start_pos).strip().rstrip('\r\n')

    max_gen_num = 20
    try:
        gen_bookmark_num = int(line)
        if gen_bookmark_num > max_gen_num:
            gen_bookmark_num = max_gen_num
    except:
        gen_bookmark_num = random.randint(3, 5)
    
    bookmark_total_num = 0
    bookmarks = []
    for fname in bookmark_file_choose:
        if fname not in open_files_read:
            try:
                f = open(fname, 'r', encoding='utf-8')
                open_files_read[fname] = f
            except IOError:
                messagebox.showinfo('提示', '無法開啟檔案 ' + fname)
                break
        else:
            f = open_files_read[fname]
            f.seek(0)

        for line in f:
            L = line.strip().rstrip('\r\n')
            if len(L) > 0:
                bookmarks.append('')
                continue

            if len(bookmarks) == 2:
                bookmark_total_num += 1
            
            bookmarks.clear()

    bookmark_index_choose = set()
    i = 0
    while i < gen_bookmark_num:
        n = random.randint(1, bookmark_total_num)
        if n not in bookmark_index_choose:
            bookmark_index_choose.add(n)
            i += 1

    text_widget.insert(INSERT, '\nRandomly choosing ' + str(gen_bookmark_num) + ' bookmarks as follows:\n')
    text_widget.insert(INSERT, '==========================================================\n')

    bookmark_count = 0
    bookmarks = []
    for fname in bookmark_file_choose:
        f = open_files_read[fname]
        f.seek(0)

        for line in f:
            L = line.strip().rstrip('\r\n')
            if len(L) > 0:
                bookmarks.append(L)
                continue

            if len(bookmarks) == 2:
                bookmark_count += 1
                if bookmark_count in bookmark_index_choose:
                    text_widget.insert(INSERT, bookmarks[0] + '\n' + bookmarks[1] + '\n\n')
            
            bookmarks.clear()

    text_widget.mark_set(INSERT, cursor_pos)

def delete_window_check():
    for fname in open_files_write_append:
        open_files_write_append[fname].close()
    for fname in open_files_read:
        open_files_read[fname].close()
    root.destroy()

def select_all(event):
    text_widget.tag_add(SEL, '1.0', 'end-1c')
    return 'break'

def scroll_down_one_page(event):
    text_widget.yview_scroll(1, PAGES)
    return 'break'

def scroll_up_one_page(event):
    text_widget.yview_scroll(-1, PAGES)
    return 'break'

def parse_keywords(line):
    delim = ' ,'
    line = line.strip().rstrip('\r\n')
    line_len = len(line)
    keywords = []
    i = 0
    while i < line_len:
        c = line[i]
        if c not in delim:
            if c != '\"':
                j = i+1
                while j < line_len:
                    c = line[j]
                    if c in delim or c == '\"':
                        break
                    else:
                        j += 1
                keywords.append( line[i:j].lower() )
                i = j
                continue
            else:
                j = i+1
                while j < line_len:
                    if line[j] == '\"':
                        break
                    j += 1
                if j > i+1:
                    keywords.append( line[i+1:j].lower() )
                i = j+1
                continue
        else:
            i += 1
    return keywords


root = Tk()
root.title('書籤搜尋與新增小程式')

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
w = int(screenWidth * 0.9)
h = int(screenHeight * 0.8)
x = int((screenWidth - w) / 2)
y = int((screenHeight - h) / 5)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

font_size = 14

files_select_toolbar = Frame(root)
files_select_toolbar.pack(side=TOP, fill=X, padx=2, pady=(15, 0))

files_select_label = Label(files_select_toolbar, text='書籤檔案（可複選）', font=(None, font_size))
files_select_label.pack(side=LEFT, padx=2, pady=3)

bookmark_files = ['地圖集.txt', 
             '音樂.txt', 
             '圖書與光碟.txt', 
             '維基百科詞條.txt', 
             '影片集.txt', 
             'PTT.txt', 
             '電腦.txt',
             '網站集.txt'
            ]
checkboxes = {}
bookmark_file_num = len(bookmark_files)
for i in range(bookmark_file_num):
    checkboxes[i] = BooleanVar()
    checkboxes[i].set(True)
    cbtn = Checkbutton(files_select_toolbar, text=bookmark_files[i], font=(None, font_size), variable=checkboxes[i])
    cbtn.pack(side=LEFT, padx=(20, 0), pady=3)

button_toolbar = Frame(root)
button_toolbar.pack(side=TOP, fill=X, padx=2, pady=(15, 0))

show_random_btn = Button(button_toolbar, text='show random', font=(None, font_size), command=show_random_bookmarks_btn_click)
show_random_btn.pack(side=LEFT, padx=(5, 1), pady=3)

search_btn = Button(button_toolbar, text='search', font=(None, font_size), command=search_btn_click)
search_btn.pack(side=LEFT, padx=(490, 1), pady=3)

write_append_btn = Button(button_toolbar, text='write append', font=(None, font_size), command=write_append_btn_click)
write_append_btn.pack(side=LEFT, padx=(20, 1), pady=3)

all_choose_cancel_btn = Button(button_toolbar, text='取消全選', font=(None, font_size), command=all_choose_cancel_btn_click)
all_choose_cancel_btn.pack(side=LEFT, padx=(60, 0), pady=3)
all_choose_btn = Button(button_toolbar, text='全選', font=(None, font_size), command=all_choose_btn_click)
all_choose_btn.pack(side=LEFT, padx=(20, 0), pady=3)

hint_info_label = Label(button_toolbar, text='      ', font=(None, 12))
hint_info_label.pack(side=RIGHT, padx=2, pady=1)

instruct_info_toolbar = Frame(root)
instruct_info_toolbar.pack(side=TOP, fill=X, padx=2, pady=(15, 0))

instruct_info = '請在下面的 text area 輸入要 search 的關鍵字\
或是要 write append 的網頁書籤（名稱和網址分兩行），並按下 search 或是 write append 按鈕'
instruct_info_label = Label(instruct_info_toolbar, text=instruct_info, font=(None, font_size))
instruct_info_label.pack(side=LEFT, padx=2, pady=3)

xscrollbar = Scrollbar(root, orient=HORIZONTAL)
yscrollbar = Scrollbar(root)
text_widget = Text(root, wrap='none', bg='lightgreen', font='Consolas 16', undo=True, blockcursor=True)

xscrollbar.pack(side=BOTTOM, fill=X)
yscrollbar.pack(side=RIGHT, fill=Y)
text_widget.pack(fill=BOTH, expand=True, padx=(5, 0))

xscrollbar.config(command=text_widget.xview)
yscrollbar.config(command=text_widget.yview)
text_widget.config(xscrollcommand=xscrollbar.set)
text_widget.config(yscrollcommand=yscrollbar.set)
text_widget.bind("<Control-Key-a>", select_all)
text_widget.bind("<Control-Key-A>", select_all)
text_widget.bind("<Control-Key-l>", scroll_down_one_page)
text_widget.bind("<Control-Key-L>", scroll_up_one_page)
text_widget.focus_set()

open_files_read = {}
open_files_write_append = {}

root.protocol('WM_DELETE_WINDOW', delete_window_check)

root.mainloop()
