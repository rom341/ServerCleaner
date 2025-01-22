class ClientServerPathPair:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

class Template:
    def __init__(self, owner, description, clientServerPaths, ttlDefault, keepAlive, keepAliveTimer, keepAliveIncrement):
        self.owner = owner
        self.description = description
        self.clientServerPaths = clientServerPaths
        self.ttlDefault = ttlDefault #default time, that file can exist on server in seconds
        self.keepAlive = keepAlive #if true, it will expand ttl every {keepAliveTimer} seconds
        self.keepAliveTimer = keepAliveTimer
        self.keepAliveIncrement = keepAliveIncrement #if client is online, it will expand it`s ttl by this time in seconds