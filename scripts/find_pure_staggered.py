import unicodedata
from collections import defaultdict
import time
import json
import random

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

dict_words = set()
dict_display = {}
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        raw = line.strip()
        w = strip_accents(raw)
        if w.isalpha():
            dict_words.add(w)
            if w not in dict_display:
                dict_display[w] = raw.upper()

freq = {}
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        p = line.strip().split()
        if len(p) >= 3 and not p[1][0].isupper():
            w = strip_accents(p[0])
            freq[w] = max(freq.get(w, 0), int(p[2]))

w50 = set()
with open("scripts/pt_br_50k.txt", "r", encoding="utf-8") as f:
    for line in f:
        p = line.strip().split()
        if p and p[0].isalpha():
            w50.add(strip_accents(p[0]))

# Strict blacklist: English, slang, weird words, archaisms, initials, abbreviations, vulgarities
blacklist = {
    # English / Foreign
    'ART', 'ALIENS', 'DORIAN', 'ACE', 'ST', 'EST', 'AM', 'HOME', 'CHAD', 'HORACE',
    'CHET', 'STAN', 'CORNO', 'BITCH', 'COCK', 'PENIS', 'VAGINA', 'SHIT', 'FUCK',
    'DICK', 'DIE', 'MIN', 'DOC', 'TOP', 'DNA', 'DVD', 'CDS', 'CSI', 'HIV', 'GPS',
    'FBI', 'KGB', 'CIA', 'BBC', 'BMW', 'BIG', 'BOX', 'GAY', 'SEX', 'HOT', 'RED',
    'BUS', 'MEN', 'BOY', 'GIRL', 'MAN', 'WAR', 'END', 'CAR', 'CAT', 'DOG', 'SUN',
    'BAD', 'GET', 'RUN', 'LET', 'SAY', 'PUT', 'NEW', 'OLD', 'ONE', 'TWO', 'TEN',
    'FAR', 'HER', 'HIS', 'HIM', 'SHE', 'WHO', 'WHY', 'HOW', 'ALL', 'ANY', 'MAY',
    'WAY', 'DAY', 'OUR', 'NOW', 'OUT', 'OFF', 'PER', 'VINTAGE', 'HALL', 'ISLAND',
    'ICE', 'POP', 'RAM', 'PAT', 'BANG', 'BEST', 'HEM', 'HAN', 'HONG', 'ROBE',
    'SECTOR', 'VECTOR', 'BAR', 'PUB', 'SHOW', 'SITE', 'WEB', 'APP', 'LINK',
    'POST', 'FEED', 'CHAT', 'EMAIL', 'MAIL', 'BYTE', 'BIT', 'PIXEL', 'CHIP',
    # Weird / Archaic / Obscure / Slang / Proper names
    'SA', 'ADA', 'ARI', 'ME', 'BELMAZ', 'ZORAIA', 'RUEIRO', 'LOROSA', 'ARATUS',
    'ICAPUI', 'TA', 'SI', 'TI', 'DUMA', 'LIONEL', 'DALE', 'ESTEREIS', 'ALOMORFO',
    'BENJAMIN', 'CAMARA', 'OURESCER', 'IGDLOITA', 'ARARAI', 'MATESE', 'AMICAL',
    'MADRIA', 'ERGUER', 'SOIOTO', 'MAMILO', 'ANAS', 'JIRO', 'OTAN', 'RAMONA',
    'ARGO', 'TOTO', 'ASIM', 'NAOS', 'LOIRAS', 'LOIROS', 'ZELOSO', 'ARSENICO',
    'UNOS', 'MICADO', 'AMADAS', 'CAMADA', 'TAMA', 'AMAL', 'MEBOSA', 'OLOFRO',
    'MARIACHI', 'MARISA', 'ELISSA', 'LAOS', 'IVES', 'ALAN', 'DAMIEN', 'ERIC',
    'NERO', 'MARI', 'ARIA', 'ALF', 'ABI', 'ABU', 'AHN', 'ARE', 'DEA', 'DUM',
    'ECA', 'ELI', 'GIL', 'GOA', 'LEO', 'PAU', 'PUS', 'RAI', 'RUM', 'SOS', 'UNA',
    'VAL', 'VOS', 'CAM', 'CLA', 'SACANA', 'ERECAO', 'PEITOS', 'MANE', 'MORE',
    'MOLE', 'CACADA', 'CIGANA', 'REATOR', 'REITOR', 'EUROPA', 'ELAINE', 'ROUPAO',
    'APACHE', 'ATO', 'UTA', 'APU', 'ETA', 'OTO', 'UFO', 'AXE', 'BAU', 'BIA',
    'BOA', 'BOI', 'BUA', 'CEU', 'CIA', 'DOM', 'DON', 'DUO', 'EIA', 'ELO', 'EMA',
    'EPA', 'ERA', 'ETA', 'EVA', 'FIM', 'GEO', 'GOL', 'GIA', 'GUA', 'HEI', 'IAO',
    'IDA', 'IMO', 'INA', 'IRA', 'ITA', 'ITU', 'IUA', 'IVA', 'IZA', 'JUS', 'LAO',
    'LIA', 'LUA', 'MAO', 'MEO', 'MIA', 'MIO', 'MOA', 'MOI', 'MUA', 'NEO', 'NIA',
    'NOA', 'NOI', 'NUA', 'OBA', 'OCA', 'ODA', 'ODE', 'OIA', 'OLA', 'OLE', 'OPA',
    'ORA', 'ORO', 'OSA', 'OTO', 'OVA', 'OVO', 'PAI', 'PAN', 'PAO', 'PIA', 'PIO',
    'POA', 'POI', 'PUM', 'QUA', 'RAD', 'RAI', 'RAO', 'REI', 'RIA', 'RIO', 'ROA',
    'ROU', 'RUA', 'RUI', 'SAO', 'SED', 'SEI', 'SEN', 'SEU', 'SIA', 'SIM', 'SIO',
    'SOA', 'SOB', 'SOI', 'SOL', 'SOM', 'SUA', 'SUL', 'TAI', 'TAO', 'TEO', 'TEU',
    'TIA', 'TIO', 'TOA', 'TRI', 'TUA', 'TUI', 'UBA', 'UFO', 'UIA', 'UIS', 'UJA',
    'UMA', 'UNI', 'URA', 'URI', 'USA', 'USO', 'UVA', 'VAI', 'VAL', 'VAO', 'VEE',
    'VEM', 'VEO', 'VER', 'VIA', 'VIM', 'VIN', 'VIO', 'VIR', 'VIS', 'VIU', 'VOO',
    'VOZ', 'ZUM'
}
# Notice above we accidentally blacklisted some valid 3-letter words like PAI, PAO, CEU, LUA, SOL, SOM, RUA, RIO, REI, VER, VOZ.
# Let's clean up the 3-letter words explicitly!
