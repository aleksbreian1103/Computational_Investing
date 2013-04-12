i = 0
while i < 10:
    numbers = raw_input('Enter 10 integers: ')
    i += 1
for n in numbers:
    if int(n) % 2 != 0:
        print 'odd'
    else:
        continue