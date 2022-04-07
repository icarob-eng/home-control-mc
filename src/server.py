import socket
# import uasyncio
import time
from mac import *
import network
import nwsetup

# todo: multiplos clientes com asyncio

wlan = nwsetup.setup_wlan()
tgl_led()  # apaga a led para indiciar que o server está inciando

SELF_IP = '10.0.0.120'
SELF_PORT = 5000

# configura o próprio IP
config = list(wlan.ifconfig())
config[0] = SELF_IP
wlan.ifconfig(config)

# dados de conexão
SELF_ADDR = (SELF_IP, SELF_PORT)
HEADER = 4
FORMAT = 'utf-8'
DISCONNECT_MSG = '!d'
TOGGLE_LED_MSG = '!l'
TOGGLE_RELAY_MSG = '!r:'  # depois colocar o número do relé
PING_MSG = '!p'
ADD_NW_MSG = '!addnw'
''' Sintaxe de adição de rede: '!addnw-Nomedarede-senhadarede '''
# provavelmente não é a ação mais segura
DEL_NW_MSG = '!delnw'
''' Sintaxe de remoção de rede: !delnw-Nomedarede '''


# únicos que serão enviados pelo servidor:
RESPONSE = 'OK'

MAX_CONN = 5

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(20)
server.bind(SELF_ADDR)


def start():
    print('\nHosting new Socket in {}.'.format(SELF_ADDR))
    server.listen(MAX_CONN)
    while True:
        try:
            conn, addr = server.accept()
            handle_client(conn, addr)
        except OSError:
            pass


def handle_client(conn, addr):
    def send(msg):
        '''manda cabeçalho e pacote, tendo conexão'''
        size = str(len(msg))
        conn.send(((HEADER-len(size))*'0' + size).encode(FORMAT))
        conn.send(msg.encode(FORMAT))
    
    blink()
    print('{} connected.'.format(addr))
    send('Hello!')  # primeira mensagem da comunicação
    
    connected = True
    try:
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)  # recebe mensagem
            if msg_length:  # se não for mensagem vazia
                msg = conn.recv(int(msg_length)).decode(FORMAT)
                
                if msg == DISCONNECT_MSG:
                    connected = False
                    
                elif msg == TOGGLE_LED_MSG:
                    tgl_led()
                    send(RESPONSE)
                    
                elif msg == TOGGLE_RELAY_MSG + '1':
                    tgl_pin('d1')
                    send(RESPONSE)
  
                elif msg == TOGGLE_RELAY_MSG + '2':
                    tgl_pin('d2')
                    send(RESPONSE)
                    
                elif msg == PING_MSG:
                    print('ping')
                    send('pong')
                    
                elif msg.split('-')[0] == ADD_NW_MSG:
                    nwsetup.add_nw(
                        msg.split('-')[1],
                        msg.split('-')[2]
                        )
                    send('Rede {} adcionada.'.format(msg.split('-')[1]))
                    
                    
                elif msg.split('-')[0] == DEL_NW_MSG:
                    nwsetup.del_nw(msg.split('-')[1])
                    send('Rede {} removida.'.format(msg.split('-')[1]))
                    
                else:
                    print('{}: {}'.format(addr, msg))
                    conn.send(RESP_HEADER)
                    conn.send(RESPONSE)
                    
    except OSError:
        print('{} time out.'.format(addr))
    finally:
        conn.close()
        print('{} disconnected.'.format(addr))
        blink()


if __name__ == '__main__':
    start()
