from ..models import Record, Category
    
def recent(user):
    records = Record.objects.filter(username = user).order_by('-update_datetime')
    recent_records = []
    counter = 0

    for record in records:
        recent_records.append(record)
        counter = counter + 1

        if len(recent_records) == 4:
            break
        
    return recent_records

def top_categories(user):
    categories = Category.objects.all()
    categories_count = []

    for category in categories:
        count = Record.objects.filter(username = user).filter(category = category).count()

        category = {
            "id": category.id,
            "count": count,
        }

        if count > 0:
            categories_count.append(category)

        top_three = descendant = sorted(categories_count, key=lambda x: x['count'], reverse=True)

        if len(top_three) > 3:
            top_three = [descendant[0], descendant[1], descendant[2]]

    return top_three
