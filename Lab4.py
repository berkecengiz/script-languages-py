import sys
import logging
import re
import argparse
import json

# https://www.tutorialspoint.com/python/assertions_in_python.htm

from itertools import islice

#lab5 task1
def read_config(config):
    regex = '^.*\.(json)$'
    r_compile = re.compile(regex)
    if r_compile.match(config):
        try:
            with open(config) as file:
                data = json.load(file)
                for info in data['config']:
                    if check_json(info['request'], info['logger'], info['lines'], info['order']):
                        return info['server'], info['request'], info['logger'], info['lines'], info['order']
                    else:
                        return None
        except FileNotFoundError:
            print("File does not exist")
            return None
    else:
        print("File is not of type .json")
        return None

#modified for lab5 task2
#assertions can be used here?
def check_json(request, logger, lines, order):
    if request.upper() not in ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT', 'PATCH']:
        print("HTTP Request error")
        return False
    elif logger.upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        print("Logger Level error")
        return False
    elif int(lines) <= 0:
        print("Number of Lines error")
        return False
    elif order.upper() not in ['ASC', 'DESC']:
        print("Improper Order Choice")
        return False
    else:
        print("Acceptable Config.")
        return True


#modified for lab5 task4

#def read_log(file_name):
#   dictionary = {}
#   file = open(file_name, 'r')
#    for line in file():
#        split_line = line.split(" ")
#        key = split_line[0] + " " + split_line[3]    
#        dictionary[key] = line
#    return dictionary
    
def read_log(file_name):
    regex = '([(\d\.)]+) (.+) (.+) \[(.*?)\] "(.*?)" (.+) (.+) "(.*?)" "(.*?)"' 
    d_d = dict()
    file = open(file_name, 'r')
    for line in file:
        d_t = re.match(regex, line).groups()
        if d_t[0] in d_d.keys():
            d_d[d_t[0]].append(d_t[3:])
        else:
            d_d.update({d_t[0]: [d_t[3:]]})
    return d_d

#tas4/5
def ip_requests(data):
    r_d = dict()
    for x in data.keys():
        r_d.update({x: len(data[x])})
    return r_d

#task4/6
def ip_find(data, most_active=True):
    if most_active:
        max_r = [k for k, v in data.items() if v == max(data.values())]
        return max_r
    else:
        min_r = [k for k, v in data.items() if v == min(data.values())]
        return min_r

#task4/7
def longest_request(data):
    longest = max(
        [(key, max(value, key=lambda ip_l: len(ip_l[1]))[1]) for key, value in data.items()],
        key=lambda m_l: len(m_l[1]))
    return longest

#404 failed error
def non_existent(data):
    non_data = []
    for k, v in data.items():
        for x in v:
            if x[2] == "404":
                if x[1] not in non_data:
                    non_data.append(x[1])
    return non_data

#task5/4-5
def get_request_containing(search, data):
    METHOD = 0
    found_data = []
    for k, v in data.items():
        for x in v:
            request = x[1].split(" ", 1)
            if request[METHOD] in ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT', 'PATCH']:
                if search in request[1]:
                    found_data.append(request)
    return found_data

#task5/4-5
def get_config_requests(data, config):
    METHOD = 0
    found_data = []
    for k, v in data.items():
        for x in v:
            request = x[1].split(" ", 1)
            if request[METHOD] == config[1].upper():
                found_data.append(x)
    return found_data

#task5/4-5
def print_config_requests(data, config):
    num_lines = config[3]
    while True:
        if input("Press ENTER to continue. Or 'q+ENTER' to Quit: ").upper() == 'Q':
            break
        print("-------------------------------------------------------------------")
        for x in range(int(num_lines)):
            try:
                print(data[x])
                data.pop(x)
            except IndexError:
                break

#run function which calls remanings
def run():
    parser = argparse.ArgumentParser(description='Parser to retrieve log file and config file.')
    parser.add_argument("--file", required=True, help="Access Log File")
    parser.add_argument("--config", help="Optional Config File")
    args = parser.parse_args()
    all_data = []
    config = []

    try:
        config = read_config(args.config)
    except AttributeError:
        print("No Config Provided")

    try:
        all_data = read_log(args.file)
    except FileNotFoundError:
        print("Log file not found.")
        exit()

    #lab5 task3 (set config levels)
    if config is not None:
        my_logger = logging.getLogger()
        if config[2].upper() == 'DEBUG':
            my_logger.setLevel(10)
        if config[2].upper() == 'INFO':
            my_logger.setLevel(20)
        if config[2].upper() == 'WARNING':
            my_logger.setLevel(30)
        if config[2].upper() == 'ERROR':
            my_logger.setLevel(40)
        if config[2].upper() == 'CRITICAL':
            my_logger.setLevel(50)
        config_data = get_config_requests(all_data, config)
        print_config_requests(config_data, config)

    # print(get_request_containing('robots', all_data))
    # print(all_data["5.188.62.214"])
    # r_data = ip_requests(all_data)
    # print(r_data)
    # print(ip_find(r_data))
    # print(ip_find(r_data, most_active=False))
    # print(non_existent(all_data))
    # print(longest_request(all_data))


if __name__ == '__main__':
    run()
