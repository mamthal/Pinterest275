class Pin:
    def __init__(self, pin_id, pin_name, pin_url):
        self.pin_id = pin_id
        self.pin_name = pin_name
        self.pin_url = pin_url

def retreive_all_pins():
    pinslist = []
    pinslist = retreiveallpinsdb()
    return pinslist

def retreive_pin():
    pin = []
    pin = retreivepindb()
    return pin
    
