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

class SingletonDatas(BaseClass, SingletonInstance):
    clients = {}

    def clientAdd(self, client, name):
        self.clients[client] = name

    def clientOut(self, client):
        del self.clients[client]
