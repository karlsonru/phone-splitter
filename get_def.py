# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from __future__ import annotations
from cgi import FieldStorage
from logger import logger
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
        provider =_line[4].rstrip()
        region = _line[5].rstrip()
        timezone = _line[7].rstrip()
        defs.append({ 'region': region, 'provider': provider,'n1': n1, 'n2': n2, 'timezone': timezone })
    return defs

DEFs = load_def('DEF-9xx_latest.csv')

def get_provider(phone: int, defs: list[dict]) -> tuple[str]:
    provider = 'NA'
    region = 'NA'
    timezone = 'NA'
    for p in defs:
        if phone >= p['n1'] and phone <= p['n2']:
            provider = p['provider']
            region = p['region']
            timezone = int(p['timezone']) - 3
            break
    return provider, region, timezone

def split_phones(file: FieldStorage) -> io.BytesIO:
    defs = load_def('DEF-9xx_latest.csv')

    proxy = io.StringIO()
    writer = csv.writer(proxy, delimiter=';')

    lines = file.readlines()
    logger.debug(f'Количество строк: {len(lines)}')
    errors = 0

    writer.writerow(['Телефон', 'Оператор', 'Регион', 'Часовой пояс (МСК)'])
    for _line in lines:
        try:
            line = int(_line.strip()[-10:])
            provider, region, timezone = get_provider(line, defs)
            
            if len(_line.strip()) == 11:
                phone = '7' + str(line)
            else:
                phone = line

            writer.writerow([phone, provider, region, timezone])
        except:
            writer.writerow([str(_line, 'utf-8', 'ignore'), 'ERROR', 'ERROR', 'ERROR'])
            errors += 1
            pass

    logger.debug(f'Строк с ошибками: {errors}')

    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('cp1251', 'replace'))
    mem.seek(0)

    proxy.close()

    return mem
