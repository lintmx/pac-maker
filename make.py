#!/usr/bin/env python3
#coding:utf-8

# pac-maker
#
# Author: lintmx
# Version: 1.1.0

import os
import argparse

from urllib import request

proxy = 'SOCKS5 127.0.0.1:1080'

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

def insert_white(site):
    white_list = []

    with open('white', 'r') as white_file:
        for line in white_file:
            white_list.append(line)
    
    if site not in white_list:
        white_list.append(site)

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

    if site not in black_list:
        black_list.append(site)

        with open('black', 'w') as black_file:
            for line in black_list:
                black_file.write(line)
    else:
        print('This site already existe.')

def read_white_file():
    str_white = "{"

    with open('white', 'r') as white_file:
        for line in white_file:
            if (line == '\n' or line[:1] == '#'):
                continue

            str_white += "\n        '" + line.strip('\n') + "' : 1,"

    str_white = str_white[:-1]
    str_white += "\n    }"

    return str_white

def read_black_file():
    str_black = "{"

    with open('black', 'r') as black_file:
        for line in black_file:
            if (line == '\n' or line[:1] == '#'):
                continue

            str_black += "\n        '" + line.strip('\n') + "' : 1," 

    str_black = str_black[:-1]
    str_black += "\n    }"

    return str_black

def read_special_file():
    str_special = "{"

    with open('special', 'r') as special_file:
        for line in special_file:
            continue

        line = line.split('@')
        str_special += "\n        '" + line[0] + "' : " + line[1].strip('\n') + ","

    str_special = str_special[:-1]
    str_special += "\n    }"

    return str_special

def read_ip_file():
    str_iplist = "["

    with open('iplist', 'r') as iplist_file:
        for line in iplist_file:
            line = line.split('.')
            str_iplist += "\n        [" + line[0] + ", " + line[1].strip('\n') + "],"

    str_iplist = str_iplist[:-1]
    str_iplist += "\n    ]"

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

    pac = pac.replace('__PROXY_ADDRESS__', proxy)
    pac = pac.replace('__SPECIALLIST__', read_special_file())
    pac = pac.replace('__WHITELIST__', read_white_file())
    pac = pac.replace('__BLACKLIST__', read_black_file())
    pac = pac.replace('__CHINAIP__', read_ip_file())

    with open('proxy.pac', 'w') as pac_file:
        pac_file.write(pac)

def main():
    parser = argparse.ArgumentParser(description='A tool to quickly generate proxy auto-config files.')
    parser.add_argument('-w', '--white', help='Add a site to white list.')
    parser.add_argument('-b', '--black', help='Add a site to black list.')
    parser.add_argument('-u', '--update', help='Update ip list from apnic.', required=False, action='store_true')
    
    args = parser.parse_args()
    
    if args.update == True:
        update_ip_list()
    
    if args.white is not None:
        insert_white(args.white)

    if args.black is Not None:
        insert_black(args.black)

    generate_pac_file()

if __name__ == '__main__':
    main()
