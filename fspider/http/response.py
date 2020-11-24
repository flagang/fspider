from parsel import Selector, SelectorList


class Response:
    def __init__(self, url, status: int, body: bytes, encoding: str = 'utf8', meta: dict = None):
        self.url = url
        self._encoding = encoding
        self._body = body
        self.status = status
        self._selector: Selector = None
        self.meta = meta

    @property
    def body(self) -> bytes:
        return self._body

    @property
    def text(self) -> str:
        return self._body.decode(self._encoding)

    def xpath(self, rule: str) -> SelectorList:
        if self._selector is None:
            self._selector = Selector(text=self.text)
        return self._selector.xpath(rule)

    def __repr__(self):
        return f'<{self.status} {self.url}>'
