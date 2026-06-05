class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        node = Node(data)
        if self.rear is None:
            self.front = node
            self.rear = node
            return

        self.rear.next = node
        self.rear = node

    def dequeue(self):
        if self.front is None:
            return None

        data = self.front.data
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return data

    def get_all(self):
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result

    def remove_at(self, index):
        """Remove and return the item at `index` (0-based). Returns None if index out of range."""
        if self.front is None:
            return None

        # remove front
        if index == 0:
            return self.dequeue()

        prev = None
        current = self.front
        i = 0
        while current and i < index:
            prev = current
            current = current.next
            i += 1

        if current is None:
            return None

        # unlink current
        prev.next = current.next
        if current == self.rear:
            self.rear = prev

        return current.data
