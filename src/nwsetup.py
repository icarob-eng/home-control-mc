''' Notas importantes:
    Apesar de serem mal documentados, os padrões de conexão do ESP-8266,
sabe-se que ele pode lembrar de até 6 redes. Embora que, após testes,
observou-se que ele só se conecte automáticamente na última rede conectada,
assim, não se precisa preocupar com conexão com redes conhecidas em locais
estranhos.

Problemas:
    -AP do ESP instável, deixando de aparecer em questão de poucos segundos.
    -Incapaz de conectar com o microcontrolador usando AP do celular, mesmo
por Java ou Python. Não sei se o problema é no microcontrolador ou no AP. Mais
testes são necessários, incluindo outros outros clientes além do celular.
'''

import network
import ubinascii
import json
from mac import *
import random

MAC_ADDR = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
WAIT_TIME = 5  # tempo de espera de conexão a redes
FILE = 'networks.json'  # arquivo com todas as redes salvas
# esturura do arquivo: [[essid, senha], [essid, senha]]


def get_nws():
    '''retorna lista de redes salvas'''
    try:
        with open(FILE, 'r') as f:
            nws = list(json.load(f))
        return nws
    except ValueError:
        return []


def del_nw(essid):
    '''esquece rede selecionada'''
    nws = get_nws()
    for n in nws:
            if n[0] == essid:
                nws.remove(n)
                break
    with open(FILE, 'w') as f:
        json.dump(nws, f)


def add_nw(essid, password, ordem=-1):
    '''adiciona uma rede na posição selecionada, padrão como final'''
    nws = get_nws()
    nws.insert(ordem, [essid, password])
    with open(FILE, 'w') as f:
        json.dump(nws, f)


def conn_attempt(wlan):
    '''espera um tempo para tentar uma conexão e retorna se conseguiu'''
    tries = 0
    while not wlan.isconnected():
        time.sleep(0.1)
        tries += 1
        if tries > WAIT_TIME * 10:
            return False
    return True


def scan_and_connect(wlan):
    '''retorna verdadeiro es conseguiu conectar, senão retorna falso'''
    scan = wlan.scan()
    ssids = [i[0].decode() for i in scan]
    # separa os ssids do scan e decodifica
    for nw in [nw for nw in get_nws() if nw[0] in ssids]:
    # 'adicione nw para cada nw em get_nws() se nw[0] estivier em ssids'
        wlan.connect(nw[0], nw[1])
        if(conn_attempt(wlan)):
            return True
    return False


def setup_wlan():
    # checa se o pino d0 está ligado ao positivo, se estiver roteia wi-fi,
    #  senão, connecta na rede pré-configurada
    print('\n\nStarting network configurations.')
    if Pin(pn['d0'][0], Pin.IN)():
        wlan = network.WLAN(network.AP_IF)
        wlan.active(True)  # ativa o ponto de acesso wi-fi
        network.WLAN(network.STA_IF).active(False)  # desativa estação wi-fi
        print('\nAP connection setted up.')
    else:
        network.WLAN(network.AP_IF).active(False)  # desativa o ponto de acesso wi-fi
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)  #  ativa wi-fi
        
        if(not conn_attempt(wlan)):
            # primeiro tenta conectar com redes já salvas
            while(not scan_and_connect(wlan)):
                time.sleep(1)
                # se não conseguiu conectar em nada, continua tentando até que consiga
        
        print('\nSTA connection setted up at "{}" network.'.format(wlan.config('essid')))
        blink()  # se for uma conexão de estação wi-fi, pisca antes de desligar
        time.sleep(0.1)  # espera um pouco antes de desligar o led
    return wlan

if __name__ == '__main__':
    setup_wlan()
