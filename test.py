from tinyBVH2d import *
import json

# 使用方法：
# 创建根节点
root = AABBNode()
#
# 创建第一个数据节点
node1 = dataNode()
node1.min = vec(0, 0)
node1.max = vec(10, 10)
node1.value = "node1"
root.add(node1)
#
# 创建第二个数据节点
node2 = dataNode()
node2.min = vec(50, 50)
node2.max = vec(100, 100)
node2.value = "node2"
root.add(node2)
#
# 创建第三个数据节点
node3 = dataNode()
node3.min = vec(150, 150)
node3.max = vec(200, 200)
node3.value = "node3"
root.add(node3)
#
# 删除第二个数据节点
# node2.autodrop()

root.dump()
node1.parent.dump()
node2.parent.dump()

print(" ")


def callback(node):
    print(node.value)


print("find:(75,75)")
root.fetchByPoint(vec(75, 75), callback)
print("find:(25,25)")
root.fetchByPoint(vec(25, 25), callback)
print("find:(5,5)")
root.fetchByPoint(vec(5, 5), callback)
print("find:(5,5)->(75,75)")
root.fetchByArea(vec(5, 5), vec(75, 75), callback)
print("find:(75,75)->(200,200)")
root.fetchByArea(vec(75, 75), vec(200, 200), callback)
