class WrongChatIDError(Exception):
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id
        super().__init__()

    def __str__(self) -> str:
        return f'Got an unexpected chat id: {self.chat_id}.'


class NoImageURLError(Exception):
    def __init__(self, value) -> None:
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return f'The returned value for image URL was {self.value}.'


class EmptyAPIKeyError(Exception):
    def __init__(self, site) -> None:
        self.site = site
        super().__init__()

    def __str__(self) -> str:
        return f'The API key for site {self.site} is empty.'


class EmptySiteInfoError(Exception):
    def __init__(self, request, img_field) -> None:
        self.request = request
        self.img_field = img_field
        super().__init__()

    def __str__(self) -> str:
        return ('One of the site parameters is missing.\n'
                f'Image request value: {self.request}'
                f'Image field value: {self.img_field}')


class StatusCodeNot200Error(Exception):
    def __init__(self, status_code) -> None:
        self.status_code = status_code
        super().__init__()

    def __str__(self) -> str:
        return (f'Got status code {self.status_code} '
                'trying to reach an endpoint.')


class EmptyBooruResultError(Exception):
    def __init__(self, booru, tags) -> None:
        self.booru = booru
        self.tags = tags
        super().__init__()

    def __str__(self) -> str:
        return (f'Got an empty result list from {self.booru} '
                f'with following tags: {self.tags}')


class NonResolvableResponseError(Exception):
    def __init__(self, booru, tags, response) -> None:
        self.booru = booru
        self.tags = tags
        self.response = response
        super().__init__()

    def __str__(self) -> str:
        msg = (f'Can\'t resolve response from {self.booru}.\n'
               f'Tags used: {self.tags}\n'
               f'Response: {self.response}')
        return msg
