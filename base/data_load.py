import xml.etree.ElementTree as ET
import datetime
from . models import High_level_tests

def load_file(filename, file, pk):
    tree = ET.parse(file)
    value = filename.split('/')[-1]
    file_name = value.split('.')[0]
    root = tree.getroot()
    test_case = root[1]
    head = root[0]
    dictionary_of_values = head[0].attrib
    name = dictionary_of_values['name']
    sf_code = dictionary_of_values['sf-code']
    family = dictionary_of_values['family']
    try:
        sf_sn = dictionary_of_values['sf-sn']
    except:
        sf_sn = ''
    try:
        si_id_string = dictionary_of_values['sf-id-string']
    except:
        si_id_string = ''
    result_dict = head[1].attrib
    result = result_dict['value']
    try:
        fail_test_name = result_dict['fail-test-name']
    except:
        fail_test_name = ''
    try:
        fail_group_name = result_dict['fail-group-name']
    except:
        fail_group_name = ''
    test_total_time = head[3].attrib['value']
    try:
        tester_info = head[5].attrib['value']
    except:
        tester_info = ''
    try:
        user_name = head[6].attrib['value']
    except:
        user_name = ''
    
    timestamp = head[8].attrib['value']
    try:
        ini_security = head[9].attrib['value']
    except:
        ini_security = ''
    #print(timestamp)
    #timestamp=parse_date(timestamp)
    date_time_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    #print(date_time_obj)
    #print(name)
    count = 0
    for child in test_case:
        for item in child:
            count += 1
    number_of_test = count
    record = High_level_tests.objects.create(project=pk, unique_id=file_name, name=name, sf_code=sf_code,family=family, sf_sn=sf_sn, si_id_string=si_id_string, result=result, 
    fail_test_name=fail_test_name, fail_group_name=fail_group_name,test_total_time=float(test_total_time),  tester_info=tester_info,
    user_name=user_name,timestamp=date_time_obj, ini_security = ini_security, number_of_test = number_of_test)