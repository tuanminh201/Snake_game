class CoordinateDLL:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None
        self.prev = None

    def getxy(self):
        return self.x, self.y

    def getnext(self):
        return self.next

    def getprev(self):
        return self.prev

    def setnext(self, nextnode):
        self.next = nextnode

    def setprev(self, prevnode):
        self.prev = prevnode

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"


class Snake:
    def __init__(self, start: CoordinateDLL):
        self.fruitseaten = 0
        self.head = start
        self.last = start

    def ate(self, location: CoordinateDLL):
        """
        call this when the snake ate something. snake's tail will remain unchanged
        """
        self.fruitseaten += 1
        location.setnext(self.head)
        self.head.setprev(location)
        self.head = location

    def move(self, location: CoordinateDLL):
        """
        call this when the snake did NOT eat something. snake's tail will be moved
        """
        # insert new location at the start of the snake:
        location.setnext(self.head)
        self.head.setprev(location)
        self.head = location

        # remove the last element from the snake and set the current second last element as the new last element
        # also change the next element to None to signal the new end of the snake
        self.last = self.last.getprev()
        self.last.setnext(None)

    def __str__(self):
        result = "["
        curr = self.head
        while curr.getnext() is not None:
            result += str(curr)+", "
            curr = curr.getnext()
        return result+str(curr)+"]"
