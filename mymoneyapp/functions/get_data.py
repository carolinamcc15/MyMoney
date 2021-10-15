from ..models import Record
    
def recent(user):
    records = Record.objects.filter(username = user).order_by('-update_datetime')
    recent_records = []
    counter = 0

    for record in records:
        recent_records.append(record)
        counter = counter + 1

        if len(recent_records) == 6:
            break
        
    return recent_records
