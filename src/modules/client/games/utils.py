from src.modules.client.basket.utils import calculate_delta
from src.models import Game


def populate_adapter(obj: Game, start_date, end_date):
    delta = calculate_delta(start_date, end_date)
    a =  {
        **obj.__dict__,
        'is_available': obj.check_available(delta),
        'images': obj.images
    }
    return a

def populate_adapter_full(obj: Game, start_date, end_date):
    delta = calculate_delta(start_date, end_date)
    a = {
        **obj.__dict__,
        'is_available': obj.check_available(delta),
        'images': obj.images
    }
    return a
