class NotFoundException(Exception):
    def __init__(self , detail: str , *args):
        super().__init__(*args)
        self.detail : str = detail


class BadRequest(Exception):
    def __init__(self , detail:str, *args):
        super().__init__(*args)
        self.detail : str = detail