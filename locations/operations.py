import re
from locations.opening_hours import regex, REPLACE

def extract_phone(phone: str) -> str:
    '''
    Input examples:
    +7 (495) 787-7-787
    8 (800) 100-0-100

    Output example:
    74957877787
    88001000100
    '''

    return "".join(re.findall(r'\d', phone))

def extract_email(email: str) -> str:
    '''
    Input examples:
    sd hellowoeld@mail.com asdfsadfasd
    [sadasd] hellowoeld@mail.com,sas

    Output example:
    hellowoeld@mail.com
    hellowoeld@mail.com
    '''

    return re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+', email)


def parse_hours(opening_hours):
    if type(opening_hours) is str:
        re_hours = regex.findall(opening_hours.lower())
        hours_string = ' '.join(re_hours)
        
        for key, value in REPLACE.items():
            hours_string = hours_string.replace(key, value)

        return hours_string
    else:
        return opening_hours