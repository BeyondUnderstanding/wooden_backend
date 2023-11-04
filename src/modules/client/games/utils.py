from src.models import Game


def populate_adapter(obj: Game, start_date, end_date):
    return {
        'id': obj.id,
        'title': obj.title,
        'price': obj.price,
        'is_available': obj.check_available(start_date, end_date),
        'images': obj.images
    }

def populate_adapter_full(obj: Game, start_date, end_date):
    return {
        'id': obj.id,
        'title': obj.title,
        'description': obj.description,
        'price': obj.price,
        'attributes': obj.attributes,
        'is_available': obj.check_available(start_date, end_date),
        'images': obj.images
    }
