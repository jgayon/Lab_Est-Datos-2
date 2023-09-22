import pandas as pd
import graphviz 
import pydot
#Clase para crear nodos
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.price = data["price"]
        self.surface_total = data["surface_total"]
        self.bedrooms = data["bedrooms"]
        self.metric = self.calculate_metric()
        self.level = 1
        self.parent = None
        self.grandparent = None

    #Funcion para calcular la metrica
    def calculate_metric(self):
        return self.price / self.surface_total if self.surface_total != 0 else 0
    #Funcion para insertar un nodo, calcular el nivel, balancear y asignar nodo padre y abuelo.
    #Se utiliza el numero de cuartos como metrica secundaria para balancear el arbol
    def insert_node(self, data):
        if self.data.empty:
            self.data = data
            return

        metric = data["price"] / data["surface_total"]
        if metric < self.metric:
            if self.left:
                self.left.insert_node(data)
            else:
                self.left = TreeNode(data)
        elif metric > self.metric:
            if self.right:
                self.right.insert_node(data)
            else:
                self.right = TreeNode(data)
        else:
            if data["bedrooms"] < self.bedrooms:
                if self.left:
                    self.left.insert_node(data)
                else:
                    self.left = TreeNode(data)
            else:
                if self.right:
                    self.right.insert_node(data)
                else:
                    self.right = TreeNode(data)

        self.metric = self.calculate_metric()
        self.level = self.calculate_level()

        self.parent = self
        self.grandparent = self.parent

        balance = self.get_balance()

        if balance > 1 and metric < self.left.metric:
            return self.rotate_right()

        if balance < -1 and metric > self.right.metric:
            return self.rotate_left()

        if balance > 1 and metric > self.left.metric:
            self.left = self.left.rotate_left()
            return self.rotate_right()

        if balance < -1 and metric < self.right.metric:
            self.right = self.right.rotate_right()
            return self.rotate_left()

        return self
    #funcion para insertar un nodo y graphicar el arbol
    def insert_new(self, data):
        if self.data.empty:
            self.data = data
            return

        metric = data["price"] / data["surface_total"]
        if metric < self.metric:
            if self.left:
                self.left.insert_new(data)
            else:
                self.left = TreeNode(data)
        elif metric > self.metric:
            if self.right:
                self.right.insert_new(data)
            else:
                self.right = TreeNode(data)
        else:
            if data["bedrooms"] < self.bedrooms:
                if self.left:
                    self.left.insert_new(data)
                else:
                    self.left = TreeNode(data)
            else:
                if self.right:
                    self.right.insert_new(data)
                else:
                    self.right = TreeNode(data)
        self.metric = self.calculate_metric()
        self.level = self.calculate_level()

        self.parent = self
        self.grandparent = self.parent

        # renderiza el arbol
        self.render_tree_graph()

#Funcion para eliminar un nodo y balancear el arbol despues de eliminado.
    def delete_node(self, metric):
        if not self.data:
            return self

        if metric < self.metric:
            if self.left:
                self.left = self.left.delete_node(metric)
        elif metric > self.metric:
            if self.right:
                self.right = self.right.delete_node(metric)
        else:
            if not self.left:
                return self.right
            elif not self.right:
                return self.left
            else:
                successor = self.right.get_minimum_node()
                self.data = successor.data
                self.right = self.right.delete_node(successor.metric)

        self.metric = self.calculate_metric()
        self.level = self.calculate_level()

        balance = self.get_balance()

        if balance > 1 and self.right and metric < self.left.metric:
            return self.rotate_right()

        if balance < -1 and self.left and metric > self.right.metric:
            return self.rotate_left()

        if balance > 1 and self.right and metric > self.left.metric:
            self.left = self.left.rotate_left()
            return self.rotate_right()

        if balance < -1 and self.left and metric < self.right.metric:
            self.right = self.right.rotate_right()
            return self.rotate_left()

        return self
#Funcion para buscar un nodo
    def search_node(self, metric):
        if self.metric == metric:
            return self.data

        if metric < self.metric and self.left:
            return self.left.search_node(metric)
        elif metric > self.metric and self.right:
            return self.right.search_node(metric)

        return None
#Funcion para obtener el nodo mas bajo
    def get_minimum_node(self):
        current = self
        while current.left:
            current = current.left
        return current
#funcion para obtener el balance
    def get_balance(self):
        return self.get_height(self.left) - self.get_height(self.right)
#funcion para rotar el arbol a la izquierda
    def rotate_left(self):
        y = self.right
        T2 = y.left

        y.left = self
        self.right = T2

        self.metric = self.calculate_metric()
        y.metric = y.calculate_metric()

        self.level = self.calculate_level()
        y.level = y.calculate_level()

        return y
#funcion para rotar el arbol a la derecha
    def rotate_right(self):
        x = self.left
        T2 = x.right
    
        x.right = self
        self.left = T2
    
        self.metric = self.calculate_metric()
        x.metric = x.calculate_metric()
    
        self.level = self.calculate_level()
        x.level = x.calculate_level()
    
        return x
#funciones para obtener la altura, calcular el nivel del arbol y devolverlo
    def get_height(self, node):
        if not node:
            return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def calculate_level(self):
        return 1 + max(self.get_level(self.left), self.get_level(self.right))
    
    def get_level(self, node):
        if not node:
            return 0
        return node.level
    #Funcion para buscar nodos con metricas
    def search_nodes_with_metrics(self, metrics):
        result = []
        self._search_nodes_with_metrics(metrics, result)
        return result
#funcion recursiva para buscar nodos
    def _search_nodes_with_metrics(self, metrics, result):
        if self.metric == metrics[0]:
            if len(metrics) == 1:
                result.append(self.data)
            else:
                self._search_nodes_with_metrics(metrics[1:], result)

        if self.left and self.metric >= metrics[0]:
            self.left._search_nodes_with_metrics(metrics, result)

        if self.right and self.metric <= metrics[0]:
            self.right._search_nodes_with_metrics(metrics, result)
    #Funcion para imprimir el orden del nivel
    def print_level_order(self):
        height = self.get_height(self)
        for level in range(1, height + 1):
            self._print_current_level(self, level)
#Funcion para imprimir el nivel actual
    def _print_current_level(self, node, level):
        if node is None:
            return
        if level == 1:
            print(node.data)
        elif level > 1:
            self._print_current_level(node.left, level - 1)
            self._print_current_level(node.right, level - 1)
    #funciones para encontrar nodo padre, abuelo y tio
    def find_father(self):
        return self.parent

    def find_grandfather(self):
        return self.grandparent

    def find_uncle(self):
        if self.parent is None or self.grandparent is None:
            return None
        
        if self.parent is self.grandparent.left:
            return self.grandparent.right
        
        return self.grandparent.left
    #Funcion para renderizar el arbol
    def render_tree_graph(self):
       graph = pydot.Dot(graph_type="graph")
   
       # viajar por el arbol segun el orden y agregar nodos al nivel
       queue = [(self, 1)]
       while queue:
           node, level = queue.pop(0)
           graph_node = pydot.Node(str(node.metric), label="Metric: {}".format(node.metric))
           graph.add_node(graph_node)
           if node.left:
               left_node = pydot.Node(str(node.left.metric))
               graph.add_node(left_node)
               graph.add_edge(pydot.Edge(graph_node, left_node))
               queue.append((node.left, level + 1))
           if node.right:
               right_node = pydot.Node(str(node.right.metric))
               graph.add_node(right_node)
               graph.add_edge(pydot.Edge(graph_node, right_node))
               queue.append((node.right, level + 1))
   
       # Save the graph to a file
       graph.write_png("avl_tree_graph.png")

# Leer el dataset
data = pd.read_csv("co_properties_final.csv")

# Crear el arbol inicial
root = None
for x in range(0,len(data)):
    if root is None:
        root = TreeNode(data.loc[0])
    else:
        root.insert_node(data.loc[x])

# Renderizar el arbol inicial
root.render_tree_graph()