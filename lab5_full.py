
import time
import turtle
#from lab5_full import node, binary_search_tree


class node:
    def __init__(self, value=None):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.parent = None  # pointer to parent node in tree

    def show_ch(self):
        print(
            f"value{self.value} \t left_child {self.left_child} \t right_child {self.right_child}")


class binary_search_tree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root == None:
            self.root = node(value)
        else:
            self._insert(value, self.root)

    def _insert(self, value, cur_node):
        if value <= cur_node.value:
            if cur_node.left_child == None:
                cur_node.left_child = node(value)
                cur_node.left_child.parent = cur_node  # set parent
            else:
                self._insert(value, cur_node.left_child)
        else:
            if cur_node.right_child == None:
                cur_node.right_child = node(value)
                cur_node.right_child.parent = cur_node  # set parent
            else:
                self._insert(value, cur_node.right_child)

    def build_from_line(self, line):
        for word in line:
            self.insert(word)

    def min_value_node(self, n):
        current = n
        while current.left_child != None:
            current = current.left_child
        return current

    def inOrderSuccessor(self, n):

        # Step 1 of the above algorithm
        if n.right_child is not None:
            return self.min_value_node(n.right_child)

        # Step 2 of the above algorithm
        p = n.parent
        while(p is not None):
            if n != p.right_child:
                break
            n = p
            p = p.parent
        return p

    def delete_value(self, value):
        return self.delete_node(self.find(value))

    def delete_node(self, node):

        # Protect against deleting a node not found in the tree
        if node == None or self.find(node.value) == None:
            print("Node to be deleted not found in the tree!")
            return None

            # returns the number of children for the specified node
        def num_children(n):
            num_children = 0
            if n.left_child != None:
                num_children += 1
            if n.right_child != None:
                num_children += 1
            return num_children

        # get the parent of the node to be deleted
        node_parent = node.parent

        # get the number of children of the node to be deleted
        node_children = num_children(node)

        # CASE 1 (node has no children)
        if node_children == 0:

            if node_parent != None:
                # remove reference to the node from the parent
                if node_parent.left_child == node:
                    node_parent.left_child = None
                else:
                    node_parent.right_child = None

            else:
                self.root = None

        # CASE 2 (node has a single child)
        if node_children == 1:

            # get the single child node
            if node.left_child != None:
                child = node.left_child
            else:
                child = node.right_child

            if node_parent != None:
                # replace the node to be deleted with its child
                if node_parent.left_child == node:
                    node_parent.left_child = child
                else:
                    node_parent.right_child = child
            else:
                self.root = child

            # correct the parent pointer in node
            child.parent = node_parent

        # CASE 3 (node has two children)
        if node_children == 2:

            # find inorder sucessor of cur node
            #successor = min_value_node(node.right_child)
            successor = self.inOrderSuccessor(node)
            # copy the inorder successor's value to the node formerly
            # holding the value we wished to delete
            node.value = successor.value

            # delete the inorder successor now that it's value was
            # copied into the other node
            self.delete_node(successor)

    def find(self, value):
        if self.root != None:
            return self._find(value, self.root)
        else:
            return None

    def _find(self, value, cur_node):
        if value == cur_node.value:
            return cur_node
        elif value < cur_node.value and cur_node.left_child != None:
            return self._find(value, cur_node.left_child)

        elif value > cur_node.value and cur_node.right_child != None:
            return self._find(value, cur_node.right_child)

    def postorder(self):
        a = self._postorder()
        result = []
        for mem in a:
            result.append(mem.value)
        return result

    def _node_dict(self):
        # create a dict with a node.nvalue as a key and node memory containier as a value
        node_dict = {}
        line = self._postorder()
        for kernel in line:
            if kernel.value in node_dict:
                node_dict[kernel.value].append(kernel)
            else:
                node_dict[kernel.value] = [kernel]

        return node_dict

    def unique(self):
        a_dict = self._node_dict()
        for key in a_dict:
            if len(a_dict[key]) > 1:
                for i in a_dict[key]:
                    self.delete_node(i)
                a_dict[key] = []
            else:
                continue

    def unique1(self):
        a_dict = self._node_dict()
        for key in a_dict:
            if len(a_dict[key]) > 1:
                for i in a_dict[key][::-1]:
                    self.delete_node(i)
                a_dict[key] = []
            else:
                continue

    def _postorder(self):
        """Return the nodes in the binary tree using post-order_ traversal.
            A post-order_ traversal visits left subtree, right_child subtree, then root.

            """
        node_stack = []
        result = []
        node = self.root

        while True:
            while node is not None:
                if node.right_child is not None:
                    node_stack.append(node.right_child)
                node_stack.append(node)
                node = node.left_child

            node = node_stack.pop()
            if (node.right_child is not None and
                    len(node_stack) > 0 and
                    node_stack[-1] is node.right_child):
                node_stack.pop()
                node_stack.append(node)
                node = node.right_child
            else:
                result.append(node)
                node = None

            if len(node_stack) == 0:
                break

        return result

    def drawtree(self, flag=False):

        import turtle

        def height(node):
            return 1 + max(height(node.left_child), height(node.right_child)) if node else -1

        def jumpto(x, y):
            t.penup()
            t.goto(x, y)
            t.pendown()

        def draw(node, x, y, dx):
            if node:
                t.goto(x, y)
                jumpto(x, y-20)
                t.write(str(node.value), align='center',
                        font=('Arial', 12, 'normal'))

                draw(node.left_child, x-dx, y-60, dx/2)
                jumpto(x, y-20)

                draw(node.right_child, x+dx, y-60, dx/2)
        if flag:
            turtle.Screen().clear()
        t = turtle.Turtle()
        t.speed(0)
        turtle.Screen().delay(0)
        h = height(self.root)
        print(h)  # height(self.root) #
        jumpto(0, 30*h)
        draw(self.root, 0, 30*h, 40*h)
        t.hideturtle()
        turtle.Screen().mainloop()
        time.sleep(5)
        turtle.done()


