import fileinput
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('My_App')


#log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

#logging.basicConfig(filename="logdata.log", level=logging.DEBUG, format=log_format,filemode='w')

def main():
    logger.info('Start application')
    my_list = []
    folder_path = ""
    max_req_time = 0
    max_resource = 0
    number_of_failed_req = 0
    total_number_of_bytes = 0
    total_req_time = 0

    logger.debug('Logging enabled')
    for line in fileinput.input(files="log.txt"):
        new_list = [elem for elem in line.split(" ")]
        my_list.append(new_list)

    logger.debug('Processing log data')

    for list in my_list:

        path = list[0]
        result_code = list[1]
        number_of_bytes = int(list[2])
        request_time = int(list[3])

        if number_of_bytes > max_resource:
            logging.warning('Request available!')
            folder_path = path
            max_req_time = request_time

        if result_code == "404":
            logging.error('404 source not found!')
            number_of_failed_req += 1

        total_number_of_bytes += number_of_bytes

        total_req_time += request_time

    logger.info('Finished processing data.')

    logger.info('Printing data.')

    logger.info('Values: {0}, {1}, {2}, {3}, {4}, {5}'.format(folder_path, str(max_req_time), str(number_of_failed_req),
                                                              str(total_number_of_bytes),
                                                              str(total_number_of_bytes / 1000),
                                                              str(total_req_time / len(my_list))))

    print("Largest resources path : " + folder_path + " processing time: " + str(max_req_time))

    print("Failed " + str(number_of_failed_req) + " times")
    print("Total " + str(total_number_of_bytes) + "bytes")
    print("Total " + str(total_number_of_bytes / 1000) + "kilobytes")
    print("Mean time: " + str(total_req_time / len(my_list)))
    logger.critical('This application is about to finish!')
    logger.info('Application finished')


if __name__ == '__main__':
    main()
