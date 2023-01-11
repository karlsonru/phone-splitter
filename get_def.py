import csv
import io

def get_number_in_range(code, n):
    number = -1
    _n = n
    for i in range(len(n), 7):
        _n = '0' + _n
    number = int(code + _n)
    return number

def load_def(defs_filename):
    defs = []
    with open(defs_filename, 'r', errors='ignore', encoding='utf8') as f:
        next(f)
        lines = f.readlines()
    
    for line in lines:
        _line = line.split(';')
        code = _line[0]
        n1 = get_number_in_range(code, _line[1])
        n2 = get_number_in_range(code, _line[2])
        region = _line[5].rstrip()
        district = 'undefined' #_line[10].rstrip()
        provider =_line[4].rstrip()
        defs.append({'region': region, 'district': district, 'provider': provider,'n1': n1, 'n2': n2})
    return defs

def get_provider(phone, defs):
    provider = 'NA'
    district = 'NA'
    region = 'NA'
    for p in defs:
        if phone >= p['n1'] and phone <= p['n2']:
            provider = p['provider']
            region = p['region']
            district = p['district']
            break
    return provider, district, region

def split_phones(file) -> io.BytesIO:
    defs = load_def('DEF-9xx.csv')

    proxy = io.StringIO()
    writer = csv.writer(proxy, delimiter=';')

    lines = file.readlines()
    for _line in lines:
        line = int(_line.strip()[-10:])
        provider = get_provider(line, defs)
        print([line, provider[0], provider[1], provider[2]])
        writer.writerow([line, provider[0], provider[1], provider[2]])

    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('utf8', 'replace'))
    mem.seek(0)

    proxy.close()

    return mem

if __name__ == '__main__':
    split_phones()
