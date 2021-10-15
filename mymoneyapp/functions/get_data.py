from ..models import Record
    
def recent(user):
    records = Record.objects.filter(username = user)
    last_index = len(records) - 1

    if len(records) == 0 or last_index == 0:
        return records

    else:
        recent_records = []
        i = last_index
        counter = 0

        while counter < 6 and i >= 0:
            recent_records.append(records[i])
            i = i - 1
            counter = counter + 1
        return recent_records
