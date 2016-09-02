#!/usr/bin/env python3
# coding:utf-8

# pac-maker
#
# Author: lintmx
# Version: 1.1.0

import argparse
import os

from urllib import request

proxy = 'SOCKS5 127.0.0.1:1080'
special_rule = '''
    if (specialList.hasOwnProperty(host)) {
        if (specialList[host] == 1) {
            return direct;
        } else {
            return proxy;
        }
    }'''

class IpList(list):
    def insert_ip(self, ip, mask):
        ip_int = to_int(ip)
        ip_count = str((2 ** (32 - mask)) // 256)

        for i in range(len(self)):
            if float(self[i]) > float(ip_int):
                self.insert(i, ip_int + '.' + ip_count)

                break
        else:
            self.append(ip_int + '.' + ip_count)

def insert_special(site):
    special_list = []

    with open('special', 'r') as special_file:
        for line in special_file:
            special_list.append(line)

    if str(site + '\n') not in special_list:
        special_list.append(site + '\n')

        with open('special', 'w') as special_file:
            for line in special_list:
                special_file.write(line)
    else:
        print('This site already exists.')

def insert_white(site):
    white_list = []

    with open('white', 'r') as white_file:
        for line in white_file:
            white_list.append(line)

    if str(site + '\n') not in white_list:
        white_list.append(site + '\n')

        with open('white', 'w') as white_file:
            for line in white_list:
                white_file.write(line)
    else:
        print('This site already exists.')


def insert_black(site):
    black_list = []

    with open('black', 'r') as black_file:
        for line in black_file:
            black_list.append(line)

    if str(site + '\n') not in black_list:
        black_list.append(site + '\n')

        with open('black', 'w') as black_file:
            for line in black_list:
                black_file.write(line)
    else:
        print('This site already existe.')


def read_white_file():
    str_white = "    var whiteList = {"

    with open('white', 'r') as white_file:
        for line in white_file:
            if (line == '\n' or line[:1] == '#'):
                continue

            str_white += "\n        '" + line.strip('\n') + "' : 1,"

    str_white = str_white[:-1]
    str_white += "\n    };\n"

    return str_white


def read_black_file():
    str_black = "    var blackList = {"

    with open('black', 'r') as black_file:
        for line in black_file:
            if (line == '\n' or line[:1] == '#'):
                continue

            str_black += "\n        '" + line.strip('\n') + "' : 1,"

    str_black = str_black[:-1]
    str_black += "\n    };\n"

    return str_black


def read_special_file():
    str_special = "    var specialList = {"

    with open('special', 'r') as special_file:
        for line in special_file:
            if (line == '\n' or line[:1] == '#'):
                continue

            line = line.split('@')
            str_special += "\n        '" + line[0] + "' : " + line[1].strip('\n') + ","

    str_special = str_special[:-1]
    str_special += "\n    };\n"

    return str_special


def read_ip_file():
    str_iplist = "    var chinaIP = ["

    with open('iplist', 'r') as iplist_file:
        for line in iplist_file:
            line = line.split('.')
            str_iplist += "\n        [" + line[0] + ", " + line[1].strip('\n') + "],"

    str_iplist = str_iplist[:-1]
    str_iplist += "\n    ];\n"

    return str_iplist


def to_int(ipv4):
    ipv4 = ipv4.split('.')
    ipv4_int = str(int(ipv4[0]) * 65536 + int(ipv4[1]) * 256 + int(ipv4[2]) * 1)

    return ipv4_int


def update_ip_list():
    apnic_url = 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    ip_list = IpList()

    request.urlretrieve(apnic_url, 'apnic')

    with open('apnic', 'r') as apnic_file:
        for line in apnic_file:
            if (line[:1] == '#' or line == '\n'):
                continue

            line = line.split('|')

            if line[1] == 'CN' and line[2] == 'ipv4':
                ip_list.append(to_int(line[3]) + '.' + str(int(line[4]) // 256))

    ip_list.insert_ip('0.0.0.0', 8)
    ip_list.insert_ip('10.0.0.0', 8)
    ip_list.insert_ip('127.0.0.0', 8)
    ip_list.insert_ip('169.254.0.0', 16)
    ip_list.insert_ip('172.16.0.0', 12)
    ip_list.insert_ip('192.0.0.0', 24)
    ip_list.insert_ip('192.0.2.0', 24)
    ip_list.insert_ip('192.88.99.0', 24)
    ip_list.insert_ip('192.168.0.0', 16)
    ip_list.insert_ip('198.18.0.0', 15)
    ip_list.insert_ip('198.51.100.0', 24)
    ip_list.insert_ip('203.0.113.0', 24)
    ip_list.insert_ip('224.0.0.0', 4)
    ip_list.insert_ip('240.0.0.0', 4)

    new_list = IpList()
    i = 0

    while (i < len(ip_list) - 1):
        start_ip = int(ip_list[i].split('.')[0])
        ip_count = int(ip_list[i].split('.')[1])
        k = 0

        while ((i + k + 1) < len(ip_list) and int(ip_list[i + k].split('.')[0]) + int(ip_list[i + k].split('.')[1]) ==
            int(ip_list[i + k + 1].split('.')[0])):
            ip_count += int(ip_list[i + k + 1].split('.')[1])
            k += 1

        new_list.append(str(start_ip) + '.' + str(ip_count))
        i += k + 1

    with open('iplist', 'w') as ip_file:
        for line in new_list:
            ip_file.write(line + '\n')


def generate_pac_file():
    with open('proxy.js', 'r') as base_pac:
        pac = base_pac.read()

    # Replace rule list
    rule = ""

    if (os.path.isfile(os.getcwd() + "/special")):
        rule += read_special_file()
        pac = pac.replace('__SPECIAL_RULE__',special_rule)
    else:
        pac = pac.replace('__SPECIAL_RULE__', '')

    if (os.path.isfile(os.getcwd() + "/black")):
        rule += read_black_file()

    if (os.path.isfile(os.getcwd() + "/white")):
        rule += read_white_file()

    if (os.path.isfile(os.getcwd() + "/iplist")):
        rule += read_ip_file()

    pac = pac.replace('__PROXY_ADDRESS__', proxy)
    pac = pac.replace('__INSERT_CONTAINER__', rule)

    with open('proxy.pac', 'w') as pac_file:
        pac_file.write(pac)


def main():
    parser = argparse.ArgumentParser(description='A tool to quickly generate proxy auto-config files.')

    parser.add_argument('-s', '--special', help='Add a site to special list.')
    parser.add_argument('-w', '--white', help='Add a site to white list.')
    parser.add_argument('-b', '--black', help='Add a site to black list.')
    parser.add_argument('-u', '--update', help='Update ip list from apnic.', required=False, action='store_true')

    args = parser.parse_args()

    # Update IP list.
    if args.update == True:
        update_ip_list()

    # Add rule to special list.
    if args.special is not None:
        insert_special(args.special)

    # Add rule to white list.
    if args.white is not None:
        insert_white(args.white)

    # Add rule to black list.
    if args.black is not None:
        insert_black(args.black)

    # Generate a pac file.
    generate_pac_file()


if __name__ == '__main__':
    main()
