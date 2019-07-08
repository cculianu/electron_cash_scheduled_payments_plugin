import datetime

DISPLAY_AS_AMOUNT = 1
DISPLAY_AS_AMOUNT_FIAT = 5
DISPLAY_AS_ADDRESS = 2
DISPLAY_AS_DATETIME = 3
DISPLAY_AS_AMOUNT_NO_UNITS = 4


from electroncash.address import Address
from electroncash.util import PrintError

class ValueFormatter(PrintError):
    def __init__(self, window):
        self.window = window
        self.wallet = window.wallet

    def format_contact(self, address):
        if isinstance(self.wallet.contacts, dict):
            # old contacts API
            if address in self.wallet.contacts.keys():
                contact_type, contact_name = self.wallet.contacts[address]
                return contact_name +" <"+ address +">"
        else:
           # new contacts API
            try:
                for contact in self.wallet.contacts.get_all():
                    if address == contact.address:
                        return contact.name + " <" + contact.address + ">"
            except Exception as e:
                self.print_error("WARNING: Could not detecmine contacts API, giving up:", repr(e))

    def format_value(self, value, display_type=0):
        if display_type in (DISPLAY_AS_AMOUNT, DISPLAY_AS_AMOUNT_NO_UNITS):
            return self.window.format_amount(value, whitespaces = False) + ((' '+ self.window.base_unit()) if display_type == DISPLAY_AS_AMOUNT else '')
        elif display_type == DISPLAY_AS_AMOUNT_FIAT:
            fx = self.window.fx
            units = fx.get_currency() if fx else '(FIAT)'
            return '%0.2f %s' % (float(value), units)
        elif display_type == DISPLAY_AS_ADDRESS:
            contact_name = self.format_contact(value)
            if contact_name is None:
                if Address.is_valid(value):
                    contact_name = Address.from_string(value).to_ui_string()
                else:
                    contact_name = value
            return contact_name
        elif display_type == DISPLAY_AS_DATETIME:
            if value is None:
                return "-"
            return datetime.datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M")
        return str(value)

