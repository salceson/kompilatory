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

    def __str__(self):
        return self.name


class MemoryStack:
    def __init__(self, memory=None):
        self.stack = []
        self.stack.append(memory if memory else Memory("TopLevelMemory"))

    def get(self, name):
        for i in xrange(1, len(self.stack)+1):
            if self.stack[len(self.stack)-i].has_key(name):
                return self.stack[i].get(name)
        return None

    def insert(self, name, value):
        self.stack[-1].put(name, value)

    def set(self, name, value):
        for i in xrange(1, len(self.stack)+1):
            if self.stack[len(self.stack)-i].has_key(name):
                self.stack[i].put(name, value)
                break

    def push(self, memory):
        self.stack.append(memory)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]


if __name__ == "__main__":
    memstack = MemoryStack()
    memory = Memory("test")
    memstack.push(memory)
    print [str(x) for x in memstack.stack]
    memstack.insert("troll", 2.0)
    print memstack.get("troll")
    memstack.set("troll", 10.0)
    print memstack.get("troll")
    d = memstack.get("d")
    if d is None:
        print "OK (no key)"
    mem = memstack.pop()
    if mem == memory:
        print "OK (mem)"
    print [str(x) for x in memstack.stack]