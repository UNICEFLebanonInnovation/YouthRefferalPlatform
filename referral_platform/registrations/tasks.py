
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
    ws = wb['Sheet1']

    try:
        for row in ws.rows:
            if row[0].value == 'start':
                continue
            data = {}
            data['first_name'] = row[0].value
            data['last_name'] = row[1].value if row[1].value else 'None'
            data['father_name'] = row[2].value if row[2].value else 'None'
            data['nationality'] = row[3].value if row[3].value else 'None'

            data['id_number'] = row[4].value if row[4].value else 'None'
            data['bayanati_id'] = row[5].value if row[5].value else 'None'
            data['sex'] = row[6].value if row[6].value else '000000'
            data['marital_status'] = row[7].value if row[7].value else 'None'
            data['trainer'] = row[8].value if row[8].value else 'None'
            data['center'] = row[9].value if row[9].value else 'None'

            post_data(protocol=protocol, url=base_url, apifunc='/api/young-person/', token=token, data=data)
    except Exception as ex:
        print("---------------")
        print("error: ", ex.message)
        print(json.dumps(data, cls=DjangoJSONEncoder))
        print("---------------")
        pass
