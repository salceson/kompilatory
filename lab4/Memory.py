class Memory:
    def __init__(self, name):
        self.name = name
        self.memory = {}

    def has_key(self, name):
        return self.memory.has_key(name)

    def get(self, name):
        return self.memory.get(name)

    def put(self, name, value):
        self.memory[name] = value


class NoMemoryError(RuntimeError):
    pass


class MemoryStack:

    def __init__(self, memory=None):
        self.memory = memory
        self.stack = []
        if memory:
            self.stack.append(memory)

    def get(self, name):
        if self.memory is None:
            raise NoMemoryError()
        return self.memory.get(name)

    def insert(self, name, value):
        if self.memory is not None:
            self.memory.put(name, value)

    def set(self, name, value):
        if self.memory is None:
            raise NoMemoryError()
        self.memory.memory[name] = value

    def push(self, memory):
        self.memory = memory
        self.stack.append(memory)

    def pop(self):
        return self.stack.pop()


if __name__ == "__main__":
    memstack = MemoryStack()
    memory = Memory("test")
    memstack.push(memory)
    memstack.set("troll", 10.0)
    print memstack.get("troll")
    try:
        memstack.get("d")
    except KeyError:
        print "OK (no key)"
    mem = memstack.pop()
    if mem == memory:
        print "OK (mem)"
    print memstack.stack