"""
File contenente la definizioni di vari funzioni di supporto che vengono
utilizzate all'interno del sistema.
"""
import re


def extract_value(description):
    match = re.search(r'(\d+(\.\d+)?)\s*(shared|half)?\s*(bath|baths)', description)
    if match:
        value = match.group(1)
        return float(value) if '.' in value else int(value)
    else:
        return None
            

def converti_in_minuscolo(valore):
    return str(valore).lower()


def converti_spazi_in_ (valore):
    return str(valore).replace(' ', '_')


"Trasformo i valori 0.5 per difetto"
def round_baths(value):
    return round(value)