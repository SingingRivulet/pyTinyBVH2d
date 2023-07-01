# 迷你 BVH 树，仅由一个文件构成，无任何依赖

## 使用方法：

加载库

```
from tinyBVH2d import *
```

创建根节点

```
root = AABBNode()
```

创建第一个数据节点

```
node1 = dataNode()
node1.min = vec(0, 0)
node1.max = vec(10, 10)
root.add(node1)
```

创建第二个数据节点

```
node2 = dataNode()
node2.min = vec(10, 10)
node2.max = vec(100, 100)
root.add(node2)
```

删除第二个数据节点

```
node2.autodrop()
```

显示结果

```
root.dump()
node1.dump()
node2.dump()
```
