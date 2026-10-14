import os

watched_count = 0

with open('台灣野鳥名錄與觀察.txt', 'r', encoding='utf-8') as fin:
    for line in fin:
        if line.startswith('已看過'):
            watched_count += 1
            continue

print(f'已看過 {watched_count} 種鳥類')
