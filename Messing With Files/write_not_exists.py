# files/write_not_exists.py
with open('write_x.txt', 'w') as fw:  # this succeeds
    # for line in fw:
        print('Test1\nTest2',file=fw)
        fw.write('Test3')

with open('write_x.txt', 'rt') as fw:  # this succeeds
    # fw.write('Writing line 1')
    for line in fw:
        print(line.strip())

    # fw.close()
# with open('write_x.txt', 'x') as fw:  # this fails
#     fw.write('Writing line 2')