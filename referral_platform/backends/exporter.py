

def export_full_data(params):
    import tasks

    report = params['report']
    method_to_call = getattr(tasks, report)
    method_to_call.delay(params)
    return True
