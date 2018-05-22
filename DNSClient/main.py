import argparse
import socket

from data_DNS_package import MessageFormat


QUERY_TYPES = {
    'A': 1,
    'NS': 2,
    'CNAME': 5,
    'SOA': 6,
    'MB': 7,
    'PTR': 12,
    'MX': 15,
    'AAAA': 28
}


class DNSClient:
    def __init__(self, server, q_type, is_TCP, is_debug, is_recursion):
        self.q_type = QUERY_TYPES[q_type]
        self.is_TCP = is_TCP
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM if is_TCP else socket.SOCK_DGRAM
        )  # TCP, UDP
        self.sock.settimeout(30)
        self.server = server
        self.is_debug = is_debug
        self.is_recursion = is_recursion
        self.try_connect()

    def try_connect(self):
        try:
            self.sock.connect((self.server, 53))
            return True
        except:
            print('Cannot connect to server' + str(self.server))
            return False

    def client_disconnect(self):
        self.sock.close()

    def send_query(self, host_name):
        message = MessageFormat(q_type=self.q_type, host_name=host_name, is_recursion=self.is_recursion)
        query = message.encode_message(is_TCP=self.is_TCP)
        self.sock.send(query)
        try:
            response = self.sock.recv(1024)
            if self.is_TCP:
                response = response[2:]
            message.decode_message(response)

            if self.is_debug:  # debug mode!
                print('DNS PACKAGE!\n')
                message.print_result()

        except UnicodeDecodeError:
            print('Time out: {0}'.format(self.server))
            exit(0)


def __create_parser():
    parser = argparse.ArgumentParser(
        usage='-s <server name> -hn <host name> [[-qt <query type>] [-tp <udp or tcp>] [-d] [-r]]'
    )
    parser.add_argument(
        '-s',
        '--server',
        required=True,
        help='Enter server number'
    )
    parser.add_argument(
        '-hn',
        '--hostname',
        required=True,
        help='Enter host name'
    )
    parser.add_argument(
        '-qt',
        '--query_type',
        required=False,
        default='A',
        help='Enter IP version. Default: A'
    )
    parser.add_argument(
        '-tp',
        '--transportProtocol',
        required=False,
        help='Enter transport protocol (tcp or udp). Default: udp'
    )
    parser.add_argument(
        '-d',
        '--debug',
        required=False,
        default=True,
        nargs='?',
        help='Debug mode'
    )
    parser.add_argument(
        '-r',
        '--recursion',
        required=False,
        nargs='?',
        help='Recursion'
    )

    return parser


if __name__ == '__main__':
    parser = __create_parser()
    args = parser.parse_args()

    client = DNSClient(server=args.server, q_type=args.query_type, is_TCP=args.transportProtocol,
                       is_debug=args.debug, is_recursion=args.recursion)
    client.send_query(host_name=args.hostname)
    client.client_disconnect()
