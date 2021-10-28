import sys
import logging
import re

#2
def run():
    my_logger = logging.getLogger()
    my_logger.setLevel(10)
    logging.info('Start Application')
    data = read_log()
    
    print("\nSuccessful Reads: ")
    print_html_data(successful_reads(data))
    print("\nFailed Reads: ")
    print_html_data(failed_reads(data))
    print("\nHTML Reads: ")
    print_html_data(html_entries(data))

#3
if __name__ == '__main__':
    if not sys.stdin.isatty(): #returns true if file is connected
        run()
    else:
        print("The is no data was provided.")

#4
def read_log():
    data = []
   # d_types = (str, int, int, int)
    count = 0
    logging.info('Reading Log')
    for line in data:
        new_list = [elem for elem in line.split()]
        if len(new_list) == 4:
            new_list[0] = str(new_list[0])
            new_list[1] = int(new_list[1])
            new_list[2] = int(new_list[2])
            new_list[3] = int(new_list[3])
            data.append(tuple(new_list))
        count += 1
    logging.debug('Total list entries: %d' % len(data))
    return data

#5
def successful_reads(data):
    s_list = []
   # s_read = re.compile("2[0-9]{2}")
    logging.info('Checking successful reads')
    for line_tuple in data:
        if line_tuple[1] //100 == 2:
            s_list.append(line_tuple)
    logging.info('Successful reads: %d' % len(s_list))
    return s_list

#6
def failed_reads(data):
    #fourxx = re.compile("4[0-9]{2}")
    #fivexx = re.compile("5[0-9]{2}")
    list4 = []
    list5 = []
    logging.info('Checking failed reads')
    for list_tuple in data:
        if (list_tuple[1]//100) == 4:
            list4.append(list_tuple)
        if (list_tuple[1]//100) == 5:
            list5.append(list_tuple)
    logging.info('4xx reads: %d' % len(list4))
    logging.info('5xx reads: %d' % len(list5))
    merged_list = list4 + list5
    return merged_list

#7
def html_entries(data):
    html_list = []
    #html_re = re.compile("\w+.html")
    logging.info('Checking html entries')
    for elem in data:
        elem1 = elem[0].rsplit('.')
        if len(elem1) == 2 and elem1[1] == 'html':
            html_list.append(elem)
    return html_list
    logging.info('Html reads: %d' % len(html_list))
    return html_list

#8
def print_html_data(data):
    for x in data:
        print('\nFile Path: %s\tHTTP Code: %d\tBytes: %d\tTime: %d' % (x[0], x[1], x[2], x[3]))
