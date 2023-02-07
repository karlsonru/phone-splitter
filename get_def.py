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
        region = _line[5].rstrip()
        provider =_line[4].rstrip()
        defs.append({ 'region': region, 'provider': provider,'n1': n1, 'n2': n2 })
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
    logger.debug(f'Количество строк: {len(lines)}')
    errors = 0

    for _line in lines:
        try:
            line = int(_line.strip()[-10:])
            provider, region = get_provider(line, defs)
            
            if len(_line.strip()) == 11:
                phone = '7' + str(line)
            else:
                phone = line

            writer.writerow([phone, provider, region])
        except:
            writer.writerow([str(_line, 'utf-8', 'ignore'), 'ERROR', 'ERROR'])
            errors += 1
            pass

    logger.debug(f'Строк с ошибками: {errors}')

    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('cp1251', 'replace'))
    mem.seek(0)

    proxy.close()

    return mem
