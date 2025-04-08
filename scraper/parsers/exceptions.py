class ElementNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class PriceNotFoundException(ElementNotFoundException):
    def __init__(self, *args):
        super().__init__(*args)

class AvailabilityNotFoundException(ElementNotFoundException):
    def __init__(self, *args):
        super().__init__(*args)

class TitleNotFoundException(ElementNotFoundException):
    def __init__(self, *args):
        super().__init__(*args)

class PriceIsNotNormalizedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class UnableToSendKeysException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class UnableToPressButtonException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class UnableToOpenSearchResultsException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class UnableToGetNProductUrls(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class InvalidPageException(Exception):
    def __init__(self, *args):
        super().__init__(*args)