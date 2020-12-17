import socket
import selectors
import types

sel = selectors.DefaultSelector()

host = '127.0.0.1'  # Standard loopback interface address (localhost)
port = 65432        # Port to listen on (non-privileged ports are > 1023)

messages = [b'Message 1 from client.', b'Message 2 from client.']


def start_connections(i_host, i_port, num_conns):
    server_addr = (i_host, i_port)
    for i in range(0, num_conns):
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum(len(m) for m in messages),
                                     recv_total=0,
                                     messages=list(messages),
                                     outb=b'')
        sel.register(sock, events, data=data)
        

def service_connection(i_key, i_mask):
    sock = i_key.fileobj
    data = i_key.data
    if i_mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if i_mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            start_connections(host, port, num_conns=1)
        else:
            service_connection(key, mask)

