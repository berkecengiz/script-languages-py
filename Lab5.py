import json

def main():
    make_config()

#task5/1
def make_config():
    
    data = {'config': []}
    web_log = input("Webserver Log:")
    http_request = input("HTTP Request:")
    log_level = input("Logging Level:")
    num_lines = input("# of Output Lines:")
    list_order = input("Order by Date(ASC or DESC):")
    data['config'].append({'server': web_log,
                           'request': http_request,
                           'logger': log_level,
                           'lines': num_lines,
                           'order': list_order})
    with open('config.json', 'w') as file:
        json.dump(data, file)
    file.close()


if __name__ == '__main__':
    main()