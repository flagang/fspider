from collections import UserDict


class Headers(UserDict):
    """ 忽略key大小写的字典   """

    def __getitem__(self, item):
        return super(Headers, self).__getitem__(item.lower())

    def __setitem__(self, key, value):
        return super(Headers, self).__setitem__(key.lower(), value)
