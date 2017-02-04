#!/usr/bin/env python3
# -*- conding: utf-8 -*-

# pac-maker
#
# Author: lintmx
# Version: 2.0.0

import argparse
import json
import operator
import os
from urllib import request


class Config:
    proxy_address = ''


def read_special_list():
    special_list = {}

    with open('data.json', 'r') as data_file:
        json_data = json.load(data_file)

        for data in json_data["special_list"]:
            special_list[data[0]] = data[1]

        special_list = sorted(special_list.items(), key=operator.itemgetter(0))

    return special_list


def read_white_list():
    white_list = []

    with open('data.json', 'r') as data_file:
        json_data = json.load(data_file)

        for data in json_data["white_list"]:
            white_list.append(data)

        white_list.sort()

    return white_list


def read_black_list():
    black_list = []

    with open('data.json', 'r') as data_file:
        json_data = json.load(data_file)

        for data in json_data["black_list"]:
            black_list.append(data)

        black_list.sort()

    return black_list


def read_bypass_list():
    ip_list = {}

    with open('data.json', 'r') as data_file:
        json_data = json.load(data_file)

        for data in json_data["bypass_list"]:
            ip_list[data[0]] = data[1]

        ip_list = sorted(ip_list.items(), key=operator.itemgetter(0))

    return ip_list


def read_config():
    config = Config()

    with open('config.json', 'r') as config_file:
        json_data = json.load(config_file)
        proxy_address = ''

        for data in json_data["proxy_address"]:
            proxy_address += ('%s %s:%s; ' % (json_data["proxy_address"][data][2],
                                              json_data["proxy_address"][data][0],
                                              json_data["proxy_address"][data][1]))
        else:
            config.proxy_address = proxy_address[:-2]

    return config


def update_data_json(list_name, new_list):
    with open('data.json', 'r') as data_file:
        json_data = json.load(data_file)

        if list_name == 'ip_list':
            json_data["bypass_list"] = new_list
        if list_name == 'special_list':
            json_data["special_list"] = new_list
        if list_name == 'white_list':
            json_data["white_list"] = new_list
        if list_name == 'black_list':
            json_data["black_list"] = new_list

    with open('data.json', 'w') as data_file:
        json.dump(json_data, data_file, indent=2)


def convert_dec(ipv4_address):
    ip_split = ipv4_address.split('.')

    convert_result = int(ip_split[0]) * 65536 + int(ip_split[1]) * 256 + int(ip_split[2]) * 1

    return convert_result


def update_china_list():
    apnic_url = 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    ipv4_list = {}
    request.urlretrieve(apnic_url, 'apnic')

    with open('apnic', 'r') as apnic_file:
        for each_line in apnic_file:
            if each_line[:1] == '#' or each_line == '\n':
                continue
            each_line = each_line.split('|')

            if each_line[1] == 'CN' and each_line[2] == 'ipv4':
                ipv4_list[convert_dec(each_line[3])] = int(each_line[4]) // 256

    os.remove(os.path.join(os.getcwd(), "apnic"))

    with open('data.json', 'r') as data_file:
        json_data = json.load(data_file)

        for data in json_data["local_ip"]:
            ipv4_list[convert_dec(data[0])] = int(data[1]) // 256

    ipv4_list = sorted(ipv4_list.items(), key=operator.itemgetter(0))

    index = 0
    while index < len(ipv4_list) - 1:
        if ipv4_list[index][0] + ipv4_list[index][1] == ipv4_list[index + 1][0]:
            ipv4_list[index] = (ipv4_list[index][0], ipv4_list[index][1] + ipv4_list[index + 1][1])
            del ipv4_list[index + 1]
            index = 0
        else:
            index += 1

    update_data_json("ip_list", ipv4_list)


def modify_special_rule(address, is_proxy, delete):
    special_list = read_special_list()

    if delete:
        # TODO: del a special rule in list.
        pass
    else:
        if special_list.count((address, 1)) + special_list.count((address, 0)) > 0:
            print('The address: ' + address + ' already exists.')
        else:
            special_list.append((address, (0 if (is_proxy == 'proxy') else 1)))
            special_list.sort()
            update_data_json("special_list", special_list)
            print('success!')


def modify_white_rule(rule, delete):
    white_list = read_white_list()

    if delete:
        # TODO: del a white rule in list.
        pass
    else:
        if white_list.count(rule) > 0:
            print('The address: ' + rule + ' already exists.')
        else:
            white_list.append(rule)
            white_list.sort()
            update_data_json('white_list', white_list)
            print('success!')


def modify_black_rule(rule, delete):
    black_list = read_black_list()

    if delete:
        # TODO: del a white rule in list.
        pass
    else:
        if black_list.count(rule) > 0:
            print('The address: ' + rule + ' already exists.')
        else:
            black_list.append(rule)
            black_list.sort()
            update_data_json('black_list', black_list)
            print('success!')


def generate_special_list(compression):
    special_list = read_special_list()
    new_list = ""

    for each_line, v in special_list:
        new_list += ("\t\t'%s': %d,\n" % (each_line, v))
    else:
        new_list = new_list[:-2]

    if compression:
        new_list = new_list.replace('\t', '')
        new_list = new_list.replace('\n', '')
        new_list = new_list.replace(' ', '')

    return new_list


def generate_white_list(compression):
    white_list = read_white_list()
    new_list = ""

    for each_line in white_list:
        if compression:
            new_list += ("%s|" % each_line)
        else:
            new_list += ("\t\t'%s': 1,\n" % each_line)
    else:
        new_list = new_list[:(-1 if compression else -2)]

    return new_list


def generate_black_list(compression):
    black_list = read_black_list()
    new_list = ""

    for each_line in black_list:
        if compression:
            new_list += ("%s|" % each_line)
        else:
            new_list += ("\t\t'%s': 1,\n" % each_line)
    else:
        new_list = new_list[:(-1 if compression else -2)]

    return new_list


def generate_ip_list(compression):
    ip_list = read_bypass_list()
    new_list = ""

    for each_line, v in ip_list:
        new_list += ("\t\t[%d, %d],\n" % (each_line, v))
    else:
        new_list = new_list[:-2]

    if compression:
        new_list = new_list.replace('\t', '')
        new_list = new_list.replace('\n', '')
        new_list = new_list.replace(' ', '')

    return new_list


def generate_pac_file(compression, path):
    if compression:
        read_file = 'proxy.min.js'
    else:
        read_file = 'proxy.js'

    with open(read_file) as file:
        pac_file = file.read()

    config = read_config()

    pac_file = pac_file.replace('__PROXY_ADDRESS__', config.proxy_address)
    pac_file = pac_file.replace('__SPACIAL_LIST__', generate_special_list(compression))
    pac_file = pac_file.replace('__BLACK_LIST__', generate_black_list(compression))
    pac_file = pac_file.replace('__WHITE_LIST__', generate_white_list(compression))
    pac_file = pac_file.replace('__BYPASS_IP__', generate_ip_list(compression))

    if path is not None:
        with open(path, 'w') as file:
            file.write(pac_file)
    else:
        print(pac_file)


def main():
    parser = argparse.ArgumentParser(description='A tool to quickly generate proxy auto-config files.')

    parser.add_argument('-s', '--special', metavar='ADDRESS',
                        help='Add a rule to special list.')
    parser.add_argument('--method', metavar='METHOD', choices=('proxy', 'direct'), default='direct',
                        help='Set special rule method.')
    parser.add_argument('-w', '--white', metavar='ADDRESS',
                        help='Add a rule to white list.')
    parser.add_argument('-b', '--black', metavar='ADDRESS',
                        help='Add a rule to black list.')
    parser.add_argument('--delete', required=False, action='store_true',
                        help='Delete rule action.')
    parser.add_argument('-u', '--update', required=False, action='store_true',
                        help='Update China ip list.')
    parser.add_argument('-c', '--compression', required=False, action='store_true',
                        help='Compress the pac file.')
    parser.add_argument('-o', '--out', metavar='PATH',
                        help='Write output to file')

    parser_args = parser.parse_args()

    print(parser_args)
    if parser_args.update:
        update_china_list()

    if parser_args.special is not None:
        modify_special_rule(parser_args.special, parser_args.method, parser_args.delete)

    if parser_args.white is not None:
        modify_white_rule(parser_args.white, parser_args.delete)

    if parser_args.black is not None:
        modify_black_rule(parser_args.black, parser_args.delete)

    generate_pac_file(parser_args.compression, parser_args.out)


if __name__ == '__main__':
    main()
