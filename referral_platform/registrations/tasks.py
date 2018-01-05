
from referral_platform.taskapp.celery import app

import json
import httplib
import datetime
from time import mktime
from django.core.serializers.json import DjangoJSONEncoder
from openpyxl import load_workbook


@app.task
def import_registrations(filename, base_url, token, protocol='HTTPS'):

    wb = load_workbook(filename=filename, read_only=True)
    ws = wb['Sheet2']
    data = {}
    header = []
    index = 0
    for row in ws.iter_rows(min_row=1, max_row=1):
        for cell in row:
            header.append((index, cell.value))
            index += 1

    for row in ws.rows:
        try:
            if row[0].value == 'start':
                continue
            data = {}
            # not for use 1, 2, 3, 4
            data['youth_nationality'] = int(row[5].value) if row[5].value else None
            data['governorate'] = int(row[6].value) if row[6].value else None
            data['partner_organisation'] = int(row[7].value) if row[7].value else None
            # training type 8
            # center type 9
            if row[10].value or not row[10].value == 'na':
                data['center_id'] = row[10].value

            # concent paper 11
            # If_you_answered_Othe_the_name_of_the_NGO 12

            data['youth_first_name'] = row[13].value
            data['youth_last_name'] = row[14].value
            data['youth_father_name'] = row[15].value
            # nationality 1 instead of 16
            if row[16].value:
                data['youth_nationality'] = int(row[16].value)

            data['id_number'] = row[17].value  # UNHCR ID
            if not row[17].value:
                data['id_number'] = row[18].value  # Jordanian ID
            data['bayanati_id'] = row[19].value  # Bayanati_ID
            # training date 20
            # training end date 21
            data['youth_sex'] = row[22].value
            if not row[23].value or row[23].value == 'na':
                data['youth_marital_status'] = 'single'
            else:
                data['youth_marital_status'] = row[23].value

            data['youth_birthday_year'] = ''
            data['youth_birthday_month'] = ''
            data['youth_birthday_day'] = ''
            if row[24].value:
                birthday = row[24].value.split('-')
                data['youth_birthday_year'] = int(birthday[0])
                data['youth_birthday_month'] = int(birthday[1])
                data['youth_birthday_day'] = int(birthday[2])

            result = post_data(protocol=protocol, url=base_url, apifunc='/api/registration/', token=token, data=data)
            registry = json.loads(result)

            submit_assessment(header, row, registry, base_url, token, protocol)

        except Exception as ex:
            print("---------------")
            print("error: ", ex.message)
            print(json.dumps(data, cls=DjangoJSONEncoder))
            print("---------------")
            pass


def submit_assessment(header, row, registry, base_url, token, protocol='HTTPS'):
    try:
        assessment_data = {}
        for key, value in header:
            assessment_data[value] = row[key].value

        assessment = {}
        assessment['registration'] = registry['id']
        assessment['youth'] = registry['youth_id']
        assessment['assessment'] = 1
        assessment['data'] = assessment_data
        post_data(protocol=protocol, url=base_url, apifunc='/api/assessment-submission/', token=token, data=assessment)

    except Exception as ex:
        print("---------------")
        print("error: ", ex.message)
        print(json.dumps(assessment, cls=DjangoJSONEncoder))
        print("---------------")
        pass


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)

    def decode(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)


def post_data(protocol, url, apifunc, token, data):

    params = json.dumps(data, cls=MyEncoder)

    headers = {"Content-type": "application/json", "Authorization": token, "HTTP_REFERER": url, "Cookie": "token="+token}

    if protocol == 'HTTPS':
        conn = httplib.HTTPSConnection(url)
    else:
        conn = httplib.HTTPConnection(url)
    conn.request('POST', apifunc, params, headers)
    response = conn.getresponse()
    result = response.read()

    if not response.status == 201:
        if response.status == 400:
            raise Exception(str(response.status) + response.reason + response.read())
        else:
            raise Exception(str(response.status) + response.reason)

    conn.close()

    return result
