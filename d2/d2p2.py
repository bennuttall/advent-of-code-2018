test_data = [
    'abcde',
    'fghij',
    'klmno',
    'pqrst',
    'fguij',
    'axcye',
    'wvxyz',
]

def correct_letters(data):
    ida, idb = find_close_ids(data)
    for i, (ca, cb) in enumerate(zip(ida, idb)):
        if ca != cb:
            print(ida)
            print(idb)
            return ida[:i] + ida[i+1:]

def find_close_ids(data):
    for ida in data:
        for idb in data:
            if compare(ida, idb) == 1:
                return (ida, idb)

def compare(ida, idb):
    s = 0
    for ca, cb in zip(ida, idb):
        if ca != cb:
            s += 1
    return s

assert correct_letters(test_data) == 'fgij'

if __name__ == '__main__':
    from d2p1 import data

    print(correct_letters(data))
