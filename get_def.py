from cgi import FieldStorage
import csv
import io

def load_def(defs_filename: str) -> list[dict]:
    defs = []
    with open(defs_filename, 'r', errors='ignore', encoding='utf8') as f:
        next(f)
        lines = f.readlines()
    
    for line in lines:
        _line = line.split(';')
        code = _line[0]
        n1 = int(code + _line[1].zfill(7))
        n2 = int(code + _line[2].zfill(7))
        region = _line[5].rstrip()
        provider =_line[4].rstrip()
        defs.append({'region': region, 'provider': provider,'n1': n1, 'n2': n2})
    return defs

def get_provider(phone: int, defs: list[dict]) -> tuple[str]:
    provider = 'NA'
    region = 'NA'
    for p in defs:
        if phone >= p['n1'] and phone <= p['n2']:
            provider = p['provider']
            region = p['region']
            break
    return provider, region

def split_phones(file: FieldStorage) -> io.BytesIO:
    defs = load_def('DEF-9xx_latest.csv')

    proxy = io.StringIO()
    writer = csv.writer(proxy, delimiter=';')

    lines = file.readlines()
    for _line in lines:
        line = int(_line.strip()[-10:])
        provider = get_provider(line, defs)
        writer.writerow([line, provider[0], provider[1]])

    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('cp1251', 'replace'))
    mem.seek(0)

    proxy.close()

    return mem

if __name__ == '__main__':
    split_phones()
