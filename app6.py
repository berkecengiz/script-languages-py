import argparse
import re
import netaddr


def read_config(conf_file):
    config = dict()
    HEADER_REGEX = '\[(.+)\]'
    DATA_REGEX = '.+=.+'
    r_compile_header = re.compile(HEADER_REGEX)
    r_compile_data = re.compile(DATA_REGEX)
    key = ''
    file = open(conf_file, 'r')
    for line in file:
        if r_compile_header.match(line):
            entry = re.match(HEADER_REGEX, line).groups()
            key = entry[0]
        elif r_compile_data.match(line):
            entry = line.rstrip('\n')
            if key in config.keys():
                config[key] += " "
                config[key] += entry
            else:
                config[key] = entry
    file.close()
    return config


def check_config(config):
    filename = 'log.txt'
    loglevel = 'INFO'
    num_lines = 10
    http_req = "POST"
    sep = '-'

    if 'LogFile' in config.keys():
        filename = config['LogFile'].split("=")[1]
    else:
        print("Setting default file.")

    if 'Config' in config.keys():

        if config['Config'].split("=")[1] in \
                ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            loglevel = config['Config'].split("=")[1]
        else:
            print("Setting default log value.")
    else:
        print("Setting default log value.")

    if 'Display' in config.keys():
        display = config['Display'].split(" ")
        for x in display:
            line = x.split("=")
            if line[0] == 'lines':
                if int(line[1]) >= 1:
                    num_lines = int(line[1])
            if line[0] == "filter":
                if line[1] in \
                        ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                         'TRACE', 'OPTIONS', 'CONNECT', 'PATCH']:
                    http_req = line[1]
            if line[0] == "separator":
                sep = line[1]
    else:
        print("Setting default display values:")
    return filename, loglevel, num_lines, http_req, sep


def read_log(config):
    data = []
    regex = '([(\d\.)]+) (.+) (.+) \[(.*?)\] "(.*?)" (.+) (.+) "(.*?)" "(.*?)"'
    try:
        file = open(config[0], 'r')
        for line in file:
            line_data = re.match(regex, line).groups()
            line_tuple = (line_data[0], line_data[3],
                          line_data[4], line_data[5], line_data[6])
            data.append(line_tuple)
        file.close()
    except FileNotFoundError:
        print("Provided file does not exist. Exiting program.")
        exit()
    return data


def ip_with_subnet(ip, mask_length, data):
    my_network = ip + "/" + str(mask_length)
    subnet_list = []
    print(my_network)
    for x in data:
        if netaddr.IPAddress(x[0]) in netaddr.IPNetwork(my_network):
            subnet_list.append(x)
    return subnet_list


def print_ip_requests(data, config):
    num_lines = config[2]
    while len(data) > 0:
        if input("Press ENTER to continue. "
                 "Or 'q+ENTER' to Quit: ").upper() == 'Q':
            break
        print("--------------------------"
              "-----------------------------------------")
        for x in range(int(num_lines)):
            try:
                print(data[x])
                data.pop(x)
            except IndexError:
                break

def log_with_filter(data, config):
    the_req = config[3]
    sep = config[4]
    total_bytes = 0
    for x in data:
        http_header = x[2]
        http_req = http_header.split(" ")
        if http_req[0] == the_req:
            total_bytes += int(x[4])
    print(the_req + sep + str(total_bytes))


def run():
    parser = argparse.ArgumentParser(description='Parser to retrieve log '
                                                 'file and config file.')
    parser.add_argument("--config", help="Config File")
    args = parser.parse_args()
    if args.config is not None:
        conf_file = args.config
    else:
        print("No Conf File was Provided; Exiting Program")
        exit()
    config = read_config(conf_file)
    config_t = check_config(config)
    my_data = read_log(config_t)
    print(config_t)
    print(my_data[0])
    log_with_filter(my_data, config_t)
    ip_data = ip_with_subnet('185.191.171.2', 251579 % 16 + 8, my_data)
    print(ip_data)
    print_ip_requests(ip_data, config_t)


if __name__ == '__main__':
    run()

'''
#MacBook-Pro:LAB6 berkecengiz$ pycodestyle app6.py --config lab6.config
MacBook-Pro:LAB6 berkecengiz$ pycodestyle app6.py
app6.py:8:21: W605 invalid escape sequence '\['
app6.py:8:27: W605 invalid escape sequence '\]'
app6.py:72:17: W605 invalid escape sequence '\d'
app6.py:72:19: W605 invalid escape sequence '\.'
app6.py:72:36: W605 invalid escape sequence '\['
app6.py:72:43: W605 invalid escape sequence '\]'
app6.py:112:1: E265 block comment should start with '# '
app6.py:113:1: E302 expected 2 blank lines, found 1
app6.py:148:1: W391 blank line at end of file

#MacBook-Pro:LAB6 berkecengiz$ pycodestyle app6.py --config lab6.config
app6.py:8:21: W605 invalid escape sequence '\['
app6.py:8:27: W605 invalid escape sequence '\]'
app6.py:72:17: W605 invalid escape sequence '\d'
app6.py:72:19: W605 invalid escape sequence '\.'
app6.py:72:36: W605 invalid escape sequence '\['
app6.py:72:43: W605 invalid escape sequence '\]'
app6.py:112:1: E302 expected 2 blank lines, found 1
'''