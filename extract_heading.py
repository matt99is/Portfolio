with open('page.html', 'r', encoding='utf-8') as f:
    for line in f:
        if 'id="1qo7e6n"' in line:
            idx = line.find('id="1qo7e6n"')
            section = line[idx:idx+2500]
            print(section)
            break
