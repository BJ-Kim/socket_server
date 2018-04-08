# -*- coding: utf-8 -*-

class BaseClass:
    pass

class SingletonInstance:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class ConnectionDatas(BaseClass, SingletonInstance):
    connection_list = {}

    # def __init__(*args, **kwargs):
    #     print "init call"

    def clientAdd(self, client, name):
        self.connection_list[client] = name

    def clientOut(self, client):
        print(self.connection_list[client])
        del self.connection_list[client]
