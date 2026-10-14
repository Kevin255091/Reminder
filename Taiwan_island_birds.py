#會在台灣本島出現的鳥種數，但不包含迷鳥


def Taiwan_island_bird(bird_info):
    Tib = False
    for info in bird_info:
        if '/' not in info:
            continue

        habitats = info.split('，')

        for h in habitats:
            if '/' not in h:
                continue

            stat = h.split('/')[0]

            Tib = True
            for p in ['金', '馬', '澎', '蘭', '綠島', '海']:
                if p in stat:
                    Tib = False
                    break

            if Tib:
                break
        
        if Tib:
            break

    return Tib

def write_bird_info(bird_info, fout):
    for info in bird_info:
        fout.write(info + '\n')

    fout.write('\n')

bird_count = 0
bird_info = []

with open('台灣野鳥名錄與觀察.txt', 'r', encoding='utf-8') as fin, \
        open('台灣本島野鳥_除了迷鳥.txt', 'w', encoding='utf-8') as fout:
    for line in fin:
        if line == '':
            if bird_info != []:
                if Taiwan_island_bird(bird_info):
                    bird_count += 1
                    write_bird_info(bird_info, fout)
            break

        L = line.strip().rstrip('\r\n')

        if L == '':
            if Taiwan_island_bird(bird_info):
                bird_count += 1
                write_bird_info(bird_info, fout)
            bird_info.clear()
            continue

        if L.startswith('#'):
            continue

        bird_info.append(L)

print(f'除了迷鳥，台灣本島會出現的野鳥有{bird_count}種，詳細種類已寫到檔案')
