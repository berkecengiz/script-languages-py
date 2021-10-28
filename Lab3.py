import sys
import logging
import re

#2 Run
def run():
    my_logger = logging.getLogger()
    my_logger.setLevel(10)
    logging.info('Start')
    data = read_log()

    print("\nSUCCESFUL READS: ")
    print_data(successful_reads(data))
    print("\nFAILED READS ")
    print_data(failed_reads(data))
    print("\nHTML READS: ")
    print_data(html_entries(data))

#4 Read Log
def read_log():
    data = []
    d_types = (str,int, int, int)
    count = 0
    logging.info('Reading Log File')
    for line in sys.stdin:
        if len(line) > 0:
            line_tuple = tuple(t(e) for t, e in zip(d_types, line.split(" ")))
            logging.debug('Lines read: %d' % count)
            data.append(line_tuple)
            count += 1
    logging.debug('Total List entries: %d' % len(data))
    return data


#5 Succesfull reads
def successful_reads(data):
    s_list = []                 #list of successful reads
    s_re = re.compile("2[0-9]{2}")
    logging.info('Checking successful reads')
    for x in data:
        if re.match(s_re, str(x[1])):
            s_list.append(x)
    logging.info('Succesful Reads: %d' % len(s_list)) 
    return s_list

#6 Failed reads
def failed_reads(data):
    four_re = re.compile("4[0-9]{2}")
    five_re = re.compile("5[0-9]{2}")
    list_4 = []
    list_5 = []
    logging.info('Checking failed reads')
    for x in data:
        if re.match(four_re, str(x[1])):
            list_4.append(x)
        elif re.match(five_re, str(x[1])):
            list_5.append(x)
    logging.info('4xx reads: %d' % len(list_4))
    logging.info('5xx reads: %d' % len(list_5))
    merged_list = list_4 + list_5      #list of failed reads
    return merged_list

#7 Html Entries
def html_entries(data):
    html_list = []
    html_re = re.compile("\w+.html")
    logging.info('Checking html entries')
    for x in data:
        end_path = x[0].split('/')[-1]
        if re.match(html_re, end_path):
            html_list.append(x)
    logging.info('Html reads: %d' % len(html_list))  #list of html reads
    return html_list

#8 Print
def print_data(data):
    for x in data:
        print('\nFile Path: %s\tHTTP Code: %d\tBytes: %d\tTime: %d' % (x[0], x[1], x[2], x[3]))

#3 Run from terminal < log.txt
if __name__ == '__main__':
    if not sys.stdin.isatty():  #returns true if file is connected
        run()
    else:
        print("There is no data provided.")
