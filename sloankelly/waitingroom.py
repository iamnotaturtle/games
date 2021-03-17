#!/usr/bin/python3

names = []
cmd = ''

while cmd != '4':
    print('1. List names')
    print('2. Add name')
    print('3. Call next patient')
    print('4. Quit')

    cmd = input('\rCommand: ')
    if cmd == '1':
        print('\n'.join(names))
    elif cmd == '2':
        name = input('\rAdd a name: ')
        names.append(name)
    elif cmd == '3':
        if not names:
            print('No patients left!')
        else:
            name = names.pop(0)
            print(f'Calling {name} next!')
    if cmd == '4':
        break