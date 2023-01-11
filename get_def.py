import csv

def get_number_in_range(code, n):
    number = -1
    _n = n
    for i in range(len(n), 7):
        _n = '0' + _n
    number = int(code + _n)
    return number

def load_def(defs_filename):
    defs = []
    with open(defs_filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        _line = line.split(';')
        code = _line[1]
        n1 = get_number_in_range(code, _line[2])
        n2 = get_number_in_range(code, _line[3])
        region = _line[8].rstrip()
        district = _line[10].rstrip()
        provider =_line[6].rstrip()
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

def main():
    defs = load_def('DEF_original.csv')
    result = []
    with open('1.csv', 'r') as f:
        lines = f.readlines()
        for _line in lines:
            line = int(_line.strip()[-10:])
            provider = get_provider(line, defs)
            result.append([line, provider[0], provider[1], provider[2]])
    with open('1_result.csv', 'w') as f:
        csv_writer = csv.writer(f, delimiter = ';')
        csv_writer.writerows(result)
    return None

if __name__ == '__main__':
    main()
