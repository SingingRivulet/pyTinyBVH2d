import math


# 向量
class vec:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y


# AABB包围盒，同时也是节点
class AABBNode:
    def __init__(self) -> None:

        # print("createNode")

        self.left = None
        self.right = None
        self.parent = None
        self.next = None

        self.min = vec()
        self.max = vec()

        self.isDataNode = False

    def dump(self, spaceNum=-1):
        if spaceNum < 0:
            spaceNum = 0
            print("root:")
        spre = "  "
        for i in range(spaceNum):
            spre += "  "
        s = f"{spre}node:({self.min.x},{self.min.y})->({self.max.x},{self.max.y})"
        if not self.isDataNode:
            s += " ↓"
        print(s)
        if self.left != None:
            print(spre+" left:")
            self.left.dump(spaceNum+1)
        if self.right != None:
            print(spre+" right:")
            self.right.dump(spaceNum+1)

    def setLeft(self, inNode) -> None:
        self.left = inNode
        inNode.parent = self

    def setRight(self, inNode) -> None:
        self.right = inNode
        inNode.parent = self

    def getMergeSizeSq(self, other) -> float:
        tf = vec()
        tt = vec()
        tf.x = min(self.min.x, other.min.x)
        tf.y = min(self.min.y, other.min.y)
        tt.x = max(self.max.x, other.max.x)
        tt.y = max(self.max.y, other.max.y)

        lx = tt.x-tf.x
        ly = tt.y-tf.y
        return (lx*lx + ly*ly)

    def merge(self, other):
        out = AABBNode()
        out.min.x = min(self.min.x, other.min.x)
        out.min.y = min(self.min.y, other.min.y)
        out.max.x = max(self.max.x, other.max.x)
        out.max.y = max(self.max.y, other.max.y)
        return out

    def isEmpty(self) -> bool:
        return self.min.x > self.max.x or self.min.y > self.max.y

    def inBox(self, point) -> bool:
        return (
            (point.x >= self.min.x and point.x <= self.max.x) and
            (point.y >= self.min.y and point.y <= self.max.y))

    def onStep(self, p: float) -> bool:
        return (p >= self.min.x) and (p <= self.max.x)

    def intersects(self, inNode) -> bool:
        return (
            (self.min.x >= inNode.min.x and self.min.x <= inNode.max.x) or
            (inNode.min.x >= self.min.x and inNode.min.x <= self.max.x)
        ) and (
            (self.min.y >= inNode.min.y and self.min.y <= inNode.max.y) or
            (inNode.min.y >= self.min.y and inNode.min.y <= self.max.y)
        )

    def inBox_AABB(self, inNode) -> bool:
        return (
            ((inNode.min.x >= self.min.x) and (inNode.max.x <= self.max.x)) and
            ((inNode.min.y >= self.min.y) and (inNode.max.y <= self.max.y))
        )

    def getSizeSq(self) -> float:
        lx = self.max.x-self.min.x
        ly = self.max.y-self.min.y
        return (lx*lx + ly*ly)

    def getCenter(self):
        lx = (self.max.x+self.min.x)/2
        ly = (self.max.y+self.min.y)/2
        return vec(lx, ly)

    def getExtent(self):
        lx = self.max.x-self.min.x
        ly = self.max.y-self.min.y
        return vec(lx, ly)

    def collisionTest(self, inNode, callback):
        if self.left != None and self.left.intersects(inNode):
            if(self.left.isDataNode):
                callback(self.left)
            else:
                self.left.collisionTest(inNode, callback)

        if self.right != None and self.right.intersects(inNode):
            if(self.right.isDataNode):
                callback(self.right)
            else:
                self.right.collisionTest(inNode, callback)

    def fetchByArea(self, area_min, area_max, callback):
        tmp = AABBNode()
        tmp.max = area_max
        tmp.min = area_min
        self.collisionTest(tmp, callback)

    def fetchByPoint(self, point, callback):
        if self.left != None and self.left.inBox(point):
            if(self.left.isDataNode):
                callback(self.left)
            else:
                self.left.fetchByPoint(point, callback)
        if self.right != None and self.right.inBox(point):
            if(self.right.isDataNode):
                callback(self.right)
            else:
                self.right.fetchByPoint(point, callback)

    def fetchByStep(self, step: float, callback):
        if self.left != None and self.left.onStep(step):
            if(self.left.isDataNode):
                callback(self.left)
            else:
                self.left.fetchByStep(step, callback)
        if self.right != None and self.right.onStep(step):
            if(self.right.isDataNode):
                callback(self.right)
            else:
                self.right.fetchByStep(step, callback)

    def autoclean(self):
        if self.left == None and self.right == None and (not self.isDataNode):
            if self.parent != None:
                if(self.parent.left == self):
                    self.parent.left = None

                if(self.parent.right == self):
                    self.parent.right = None

                self.parent.autoclean()

        elif self.parent != None and self.parent.parent != None:
            if self.parent.left != None and self.parent.right == None:
                self.parent.left = None
            elif self.parent.left == None and self.parent.right != None:
                self.parent.right = None
            else:
                return

            if self.parent.parent.left == self.parent:
                self.parent.parent.left = self
            else:
                self.parent.parent.right = self

            self.parent = self.parent.parent
            self.parent.autoclean()

    def add(self, inNode):
        if(self.left != None):
            if((not self.left.isDataNode) and inNode.inBox_AABB(self.left)):
                self.left.add(inNode)
                return
            elif(self.right == None):
                self.setRight(inNode)
                return

        if(self.right != None):
            if(not self.right.isDataNode) and inNode.inBox_AABB(self.right):
                self.right.add(inNode)
                return
            elif(self.left == None):
                self.setLeft(inNode)
                return

        if(self.right == None and self.left == None):
            self.setLeft(inNode)
            return

        ls = self.left.getMergeSizeSq(inNode)
        rs = self.right.getMergeSizeSq(inNode)

        # nnode.parent=self

        if(ls < rs):
            nnode = inNode.merge(self.left)
            nnode.setLeft(self.left)
            nnode.setRight(inNode)
            self.setLeft(nnode)
        else:
            nnode = inNode.merge(self.right)
            nnode.setLeft(self.right)
            nnode.setRight(inNode)
            self.setRight(nnode)

    def remove(self):
        if(self.parent != None):
            if(self.parent.left == self):
                self.parent.left = None

            if(self.parent.right == self):
                self.parent.right = None

            self.parent.autoclean()
            self.parent = None

    def drop(self):
        if(self.left != None):
            self.left.drop()
            self.left = None

        if(self.right != None):
            self.right.drop()
            self.right = None

        if(self.parent != None):
            if(self.parent.left == self):
                self.parent.left = None

            if(self.parent.right == self):
                self.parent.right = None

            self.parent = None

    def autodrop(self):
        p = self.parent
        self.drop()
        if(p != None):
            p.autoclean()


class dataNode(AABBNode):
    def __init__(self) -> None:
        super().__init__()
        self.isDataNode = True
