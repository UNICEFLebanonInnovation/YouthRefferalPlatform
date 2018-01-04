
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

    try:
        for row in ws.rows:
            if row[0].value == 'start':
                continue
            data = {}
            # not for use 1, 2, 3, 4
            data['youth_nationality'] = row[5].value
            data['governorate'] = row[6].value
            data['partner_organisation'] = row[7].value
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
                data['youth_nationality'] = row[16].value

            data['id_number'] = row[17].value  # UNHCR ID
            data['id_number'] = row[18].value  # Jordanian ID
            data['bayanati_id'] = row[19].value  # Bayanati_ID
            # training date 20
            # training end date 21
            data['youth_sex'] = row[22].value
            data['youth_marital_status'] = row[23].value if row[23].value else 'single'
            birthday = row[24].value.split('-')
            data['youth_birthday_year'] = birthday[0]
            data['youth_birthday_month'] = birthday[1]
            data['youth_birthday_day'] = birthday[2]

            result = post_data(protocol=protocol, url=base_url, apifunc='/api/registrations/', token=token, data=data)
            registry = json.loads(result)

            assessment = {}
            assessment['registration_id'] = registry['id']
            assessment['youth_id'] = registry['youth_id']
            assessment['assessment_id'] = 1
            assessment['data'] = row
            post_data(protocol=protocol, url=base_url, apifunc='/api/assessment-submission/', token=token, data=assessment)

    except Exception as ex:
        print("---------------")
        print("error: ", ex.message)
        print(json.dumps(data, cls=DjangoJSONEncoder))
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
