import itertools
import random

try:
    xrange is None
except NameError:
    xrange = range


class AvlNode(object):
    """docstring for AvlNode"""
    Track = False
    RotationCount = 0
    TraversalCount = 0

    def __init__(self, key, value):
        super(AvlNode, self).__init__()
        self.key = key
        self.value = value
        self.height = 1
        self.right = None
        self.left = None

    @staticmethod
    def RightRotation(node):
        assert node.left is not None
        going_up = node.left
        new_left_node = going_up.right
        node.left = new_left_node
        going_up.right = node

        node.set_height()
        going_up.set_height()

        assert abs(AvlNode.BalanceFactor(going_up)) < 2

        return going_up

    @staticmethod
    def LeftRotation(node):
        assert node.right is not None
        going_up = node.right
        new_right_node = going_up.left
        node.right = new_right_node
        going_up.left = node

        node.set_height()
        going_up.set_height()

        assert abs(AvlNode.BalanceFactor(going_up)) < 2

        return going_up

    @staticmethod
    def UnlinkNodes(p, c):
        if p.right is c:
            p.right = None
        if p.left is c:
            p.left = None
        p.set_height()

    @staticmethod
    def LinkNodes(p, c):
        if c.key < p.key:
            assert p.left is None
            p.left = c
        if c.key > p.key:
            assert p.right is None
            p.right = c
        p.set_height()

    @staticmethod
    def ReBalance(node):
        bf = AvlNode.BalanceFactor(node)

        if abs(bf) > 1:
            if AvlNode.Track:
                AvlNode.RotationCount += 1
            if bf > 0:
                if AvlNode.BalanceFactor(node.right) < 0:
                    # double rotation
                    # right rotation node.right
                    node.right = AvlNode.RightRotation(node.right)
                # left rotation
                return AvlNode.LeftRotation(node)
            else:
                if AvlNode.BalanceFactor(node.left) > 0:
                    # double rotation
                    # left rotation node.left
                    node.left = AvlNode.LeftRotation(node.left)
                # right rotaion
                return AvlNode.RightRotation(node)
        return node

    @staticmethod
    def ReBalanceLeftist(parent, node):
        assert parent is not None
        while node is not None:
            if AvlNode.Track:
                AvlNode.TraversalCount += 1
            AvlNode.UnlinkNodes(parent, node)
            node = AvlNode.ReBalance(node)
            AvlNode.LinkNodes(parent, node)
            parent = node
            node = node.left

    @staticmethod
    def ReBalanceRightist(parent, node):
        assert parent is not None
        while node is not None:
            if AvlNode.Track:
                AvlNode.TraversalCount += 1
            AvlNode.UnlinkNodes(parent, node)
            node = AvlNode.ReBalance(node)
            AvlNode.LinkNodes(parent, node)
            parent = node
            node = node.right

    @staticmethod
    def BalanceFactor(node):
        if node is None:
            return 0
        left = 0
        right = 0
        if node.left is not None:
            left = node.left.height
        if node.right is not None:
            right = node.right.height
        return right - left

    def set_height(self):
        left = 0
        right = 0
        if self.left is not None:
            left = self.left.height
        if self.right is not None:
            right = self.right.height
        self.height = max(left, right) + 1

    def path_to_key(self, key):
        """
        Generates the path from self to the node
        with node.key == key or its parent if
        the node is not in the tree
        """
        path = []
        parent = None
        next_node = self
        while next_node is not None:
            parent = next_node
            path.append(parent)
            if key < next_node.key:
                next_node = next_node.left
            elif key > next_node.key:
                next_node = next_node.right
            else:
                break
        return path

    @staticmethod
    def ReBalancePath(path):
        while len(path) > 1:
            to_rebalance = path.pop()
            parent = path[-1]
            to_rebalance.set_height()

            if parent.right is to_rebalance:
                parent.right = AvlNode.ReBalance(to_rebalance)
            if parent.left is to_rebalance:
                parent.left = AvlNode.ReBalance(to_rebalance)

        return AvlNode.ReBalance(path.pop())

    def insert(self, key, value):
        path = self.path_to_key(key)
        node = path[-1]

        if node.key == key:
            node.value = value
            return node

        # we know now that the key is not in the tree
        parent = path[-1]

        node = AvlNode(key, value)
        if parent.key < key:
            assert parent.right is None
            parent.right = node
        else:
            assert parent.left is None
            parent.left = node

        # now we have to rebalance
        return AvlNode.ReBalancePath(path)

    def search(self, key):
        to_check = self

        while to_check is not None and to_check.key != key:
            to_check = to_check.left if key < to_check.key else to_check.right

        return to_check

    def min(self):
        current = self
        while current.left is not None:
            current = current.left
        return current

    def max(self):
        current = self
        while current.right is not None:
            current = current.right
        return current

    def successor(self, key):
        node = self.search(key)

        if node is not None and node.right is not None:
            return node.right.min()

        root = self
        successor = None
        while root is not None:
            if key < root.key:
                successor = root
                root = root.left
            elif key > root.key:
                root = root.right
            else:
                break
        return successor

    def predecessor(self, key):
        node = self.search(key)

        if node is not None and node.left is not None:
            return node.left.max()

        root = self
        predecessor = None
        while root is not None:
            if key > root.key:
                predecessor = root
                root = root.right
            elif key < root.key:
                root = root.left
            else:
                break
        return predecessor

    @staticmethod
    def DeleteNode(root, key):
        path = root.path_to_key(key)

        to_delete = path.pop()
        if to_delete.key != key:
            return root

        # 2 children
        if to_delete.left is not None and to_delete.right is not None:
            successor = to_delete.successor(to_delete.key)

            path = root.path_to_key(successor.key)
            assert path[-1] is successor
            path.pop()
            to_delete.key = successor.key
            to_delete.value = successor.value
            to_delete = successor

        # One or zero children
        next_node = None
        if to_delete.left is not None and to_delete.right is None:
            next_node = to_delete.left
        else:
            next_node = to_delete.right

        if next_node is not None:
            AvlNode.UnlinkNodes(to_delete, next_node)

        if len(path) == 0:
            return next_node

        parent = path[-1]
        AvlNode.UnlinkNodes(parent, to_delete)

        if next_node is not None:
            AvlNode.LinkNodes(parent, next_node)
            path.append(next_node)

        return AvlNode.ReBalancePath(path)

    def is_balanced(self):
        children = [self.left, self.right]
        for c in children:
            if c is not None and not c.is_balanced():
                return False

        bfo = AvlNode.BalanceFactor(self)

        self.set_height()

        bf = AvlNode.BalanceFactor(self)

        assert bf == bfo, "Bad update at: %d" % self.key

        if abs(bf) > 1:
            print("Failed at: %d" % self.key)
            print("BF: {0}".format([bf]))
            print("Left: {0}\t Right: {1}".format(*children))
            return False
        return True

    def __repr__(self):
        return "K: {0} V: {1} H:{2}".format(*[self.key, self.value, self.height])

    def copy(self):
        node = AvlNode(self.key, self.value)

        node.height = self.height
        if self.left is not None:
            node.left = self.left.copy()

        if self.right is not None:
            node.right = self.right.copy()

        return node


class AvlTree(object):
    """docstring for AvlTree"""

    def __init__(self):
        super(AvlTree, self).__init__()
        self.root = None  # AvlNode

    def copy(self):
        new = AvlTree()
        new.root = self.root.copy()
        return new

    def search(self, value):
        return self.root.search(value)

    def insert(self, key, value):
        if self.root is None:
            self.root = AvlNode(key, value)
        else:
            self.root = self.root.insert(key, value)

    def delete(self, key):
        self.root = AvlNode.DeleteNode(self.root, key)

    def remove_range(self, lower, upper):
        self.remove_below(lower)
        self.remove_above(upper)

    def remove_above(self, x):
        """
        self: avl tree
        x: upper limit
        """
        node = self.root.search(x)

        if node is None:
            x = self.root.predecessor(x).key

        path = self.root.path_to_key(x)  # root -> ... -> x

        for i in xrange(len(path) - 1):
            AvlNode.UnlinkNodes(path[i], path[i + 1])
        # si fuera c++ habria que borrar explicitamente los nodos aca
        path = list(filter(lambda e: e.key <= x, path))

        for i in xrange(len(path) - 1, 0, -1):
            AvlNode.LinkNodes(path[i - 1], path[i])

        # the path only contains nodes whose keys are <= x
        # we know x is in the path
        assert path[-1].key == x
        to_rebalance = path[-1]

        if to_rebalance.right is not None:
            # all bigger than x must go
            to_rebalance.right = None
            to_rebalance.set_height()

        root = AvlNode(float("-inf"), None)

        AvlNode.ReBalanceRightist(root, path[0])
        self.root = root.right
        AvlNode.UnlinkNodes(root, self.root)
        assert abs(AvlNode.BalanceFactor(self.root)) < 2

    def remove_below(self, x):
        """
        self: avl tree
        x: lower limit
        """
        node = self.root.search(x)

        if node is None:
            x = self.root.successor(x).key

        path = self.root.path_to_key(x)  # root -> ... -> x

        for i in xrange(len(path) - 1):
            AvlNode.UnlinkNodes(path[i], path[i + 1])
        # si fuera c++ habria que borrar explicitamente los nodos aca
        path = list(filter(lambda e: e.key >= x, path))

        for i in xrange(len(path) - 1, 0, -1):
            AvlNode.LinkNodes(path[i - 1], path[i])

        # the path only contains nodes whose keys are >= x
        # we know x is in the path
        assert path[-1].key == x
        to_rebalance = path[-1]

        if to_rebalance.left is not None:
            # all lesser than x must go
            to_rebalance.left = None
            to_rebalance.set_height()

        root = AvlNode(float("-inf"), None)

        AvlNode.ReBalanceLeftist(root, path[0])
        self.root = root.right
        AvlNode.UnlinkNodes(root, self.root)
        assert abs(AvlNode.BalanceFactor(self.root)) < 2

    def is_balanced(self):
        if self.root is not None:
            return self.root.is_balanced()
        return True


if __name__ == '__main__':
    original_tree = AvlTree()

    size = 1000

    for i in xrange(size):
        original_tree.insert(i, i)

    assert original_tree.is_balanced(), "There is problem rebalancing during insert!"
    print(original_tree.root.height)

    # new_tree = original_tree.copy()
    # for i in xrange(size):
    #     try:
    #         new_tree.delete(i)
    #     except Exception:
    #         print("Failed at iteration: %d" % i)
    #         raise
    #     assert new_tree.is_balanced(), "Fallo delete"

    # random deletion
    # numbers = itertools.permutations(range(size))
    numbers = list(range(size))
    # for i, p in enumerate(numbers):
    while True:
        new_tree = original_tree.copy()
        p = numbers
        random.shuffle(p)
        for x in xrange(len(p) - 1, -1, -1):
            try:
                new_tree.delete(x)
            except Exception:
                print("Failed when deleting random")
                print(p)
                raise
            assert new_tree.is_balanced(), "Fallo delete random"

    # for i in xrange(size):
    #     new_tree = original_tree.copy()

    #     AvlNode.Track = True
    #     AvlNode.RotationCount = 0
    #     AvlNode.TraversalCount = 0
    #     try:
    #         new_tree.remove_above(i)
    #     except Exception:
    #         print("Failed at iteration: %d" % i)
    #         raise

    #     assert new_tree.is_balanced(), "Failed at iteration: %d" % i

    #     for x in xrange(i + 1, size):
    #         assert new_tree.search(x) is None

    #     print("#####################################################")
    #     print("Upper bound: %d" % i)
    #     print("Height: %d" % new_tree.root.height)
    #     print("Rotations: %d" % AvlNode.RotationCount)
    #     print("Traversal count: %d" % AvlNode.TraversalCount)

    # for i in xrange(size):
    #     new_tree = original_tree.copy()

    #     AvlNode.Track = True
    #     AvlNode.RotationCount = 0
    #     AvlNode.TraversalCount = 0
    #     try:
    #         new_tree.remove_below(i)
    #     except Exception:
    #         print("Failed at iteration: %d" % i)
    #         raise

    #     assert new_tree.is_balanced(), "Failed at iteration: %d" % i

    #     for x in xrange(i):
    #         assert new_tree.search(x) is None

    #     print("#####################################################")
    #     print("Lower bound: %d" % i)
    #     print("Height: %d" % new_tree.root.height)
    #     print("Rotations: %d" % AvlNode.RotationCount)
    #     print("Traversal count: %d" % AvlNode.TraversalCount)

    # print("#####################################################")

    print("Done!")
