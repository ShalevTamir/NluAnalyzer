# TODO: change to out if possible
def is_castable(item_to_cast: any, type_to_cast: type):
    try:
        type_to_cast(item_to_cast)
        return True
    except:
        return False
