from flask import request


class Utils() :

    @staticmethod
    def getRequestValue(key):
        return request.values.get(key, None)

    @staticmethod
    def getRequestJSON():
        return request.json
