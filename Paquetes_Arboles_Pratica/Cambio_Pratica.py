from datetime import datetime

class Paquete:
    def _init_(self, id, prioridad, peso, tamaño, destino, fecha_entrega):
        self.id = id
        self.prioridad = prioridad
        self.peso = peso
        self.tamaño = tamaño
        self.destino = destino
        self.fecha_entrega = fecha_entrega

    def _str_(self):
        return f"ID: {self.id}"

class BinaryTree:
    def _init_(self, data):
        self.data = data
        self.leftchild = None
        self.rightchild = None

    def _str_(self, level=0):
        ret = "  " * level + str(self.data) + "\n"
        if self.leftchild:
            ret += self.leftchild._str_(level + 1)
        if self.rightchild:
            ret += self.rightchild._str_(level + 1)
        return ret
### agrefamos la funcion priTree


#### agregar printree:

def printTree(node, prefix="", is_left=True):
    if not node:
        return
    if node.rightchild:
        printTree(node.rightchild, prefix + ("│    " if is_left else "    "), False)
    print(prefix + ("└── " if is_left else "┌── ") + str(node.data))
    if node.leftchild:
        printTree(node.leftchild, prefix + ("     " if is_left else "│   "), True)

## esto es para verificar el orde de prioridad de cada paquete a la hora de insertarse en el arbol heap min

#modificar la prioridad se deben despachar primero los paquetes con menor peso, adcionalmente si se tiene n paquetes con 
# el mismo peso, el siguiente orden de prioridad dede ser la fecha de entrega mas proxima,por ultimo si se tiene varios 
# paquetes con el mismo peso y fehca de entrega, se priorizalos paquetes con mayor volumen (tamaño), es decir primero se envia
# los grandes luego los medianos y por ultimo los pequeños 

def esNuevaRaiz(paquete_nuevo, paquete_nodo_actual):
    if paquete_nuevo.peso < paquete_nodo_actual.peso:             # pregunta la prioridad para saber 
        return True                                                         # i este debe ser la raiz del arbol
    if paquete_nuevo.peso == paquete_nodo_actual.peso:
        if paquete_nuevo.fecha_entrega < paquete_nodo_actual.fecha_entrega:
            return True
        if paquete_nuevo.fecha_entrega == paquete_nodo_actual.fecha_entrega:
            if  paquete_nuevo.tamaño > paquete_nodo_actual.tamaño:
                return True
    return False                                     




# encuentra el padre de un hijo o hoja para hacer el intercambio de prioridad si es necesario 

def encontrarPadre(root, child):
    if root is None or (root.leftchild == child or root.rightchild == child):       
        return root
    return encontrarPadre(root.leftchild, child) or encontrarPadre(root.rightchild, child)



# esto es para contar los nodos en el arbol recusrivamente 
# cuenta 1 si la raiz tiene hijos y se llama recurivamente,
#y retonra 1 si llega una hoja es decir una raiz sin hijos 

def contarNodos(node):
    if node is None:
        return 0
    return 1 + contarNodos(node.leftchild) + contarNodos(node.rightchild)



# mantener el arbol lleno de izquierda a derecha 
def encontrarPosicion(node):
    if node is None:
        return None, None           # para que nos arroje dos valores 
    
    izquierda = contarNodos(node.leftchild)
    derecha = contarNodos(node.rightchild)
    if izquierda <= derecha:
        if node.leftchild is None:
            return node, 'left'         # None, None == node, left
        return encontrarPosicion(node.leftchild)
    else:
        if node.rightchild is None:
            return node, 'right'
        return encontrarPosicion(node.rightchild)
    

def insertarMinHeap(root, paquete): # esta fucion inserta los nodos en base a los criterio de prioridad 
                                    # de las funciones anteriores esNuevaRaiz
    if root.data is None:
        root.data = paquete
        return root
    
    if esNuevaRaiz(paquete, root.data): # si esto se cunmple hace el intercambio de valores 
        root.data, paquete = paquete, root.data
    nodo_padre, lado = encontrarPosicion(root)  # nodo_padre ase referencia al padre y lado a laposicion donde este deva ir insertado
    nuevo_nodo = BinaryTree(paquete)
    if lado == 'left':
        nodo_padre.leftchild = nuevo_nodo
    else:
        nodo_padre.rightchild = nuevo_nodo
    nodo_actual = nuevo_nodo
    while nodo_actual != root:
        nodo_padre = encontrarPadre(root, nodo_actual)
        if nodo_padre and esNuevaRaiz(nodo_actual.data, nodo_padre.data):
            nodo_actual.data, nodo_padre.data = nodo_padre.data, nodo_actual.data
            nodo_actual = nodo_padre
        else:
            break
    return root


# funcion consultar proximo paquete a enviar:

def proximo_en_enviar(rootNode):
    if rootNode is None:
        return "No hay paquetes por enviar"
    
    # Asegúrate de que los hijos existen antes de acceder a ellos
    if rootNode.leftchild is None and rootNode.rightchild is None:
        return "No hay paquetes por enviar"
    
    if rootNode.leftchild is None:
        return f"El próximo paquete a enviar es: {rootNode.rightchild.data.id}"
    
    if rootNode.rightchild is None:
        return f"El próximo paquete a enviar es: {rootNode.leftchild.data.id}"
    
    # Comparar las prioridades
    if rootNode.leftchild.data.prioridad < rootNode.rightchild.data.prioridad:
        return f"El próximo paquete a enviar es: {rootNode.leftchild.data.id}"
    elif rootNode.rightchild.data.prioridad < rootNode.leftchild.data.prioridad:
        return f"El próximo paquete a enviar es: {rootNode.rightchild.data.id}"
    else:
        # Si las prioridades son iguales, comparar las fechas de entrega
        if rootNode.leftchild.data.fecha_entrega < rootNode.rightchild.data.fecha_entrega:
            return f"El próximo paquete a enviar es: {rootNode.leftchild.idata.idd}"
        elif rootNode.leftchild.data.fecha_entrega > rootNode.rightchild.data.fecha_entrega:
            return f"El próximo paquete a enviar es: {rootNode.rightchild.data.id}"
        else:
            # Si las fechas son iguales, comparar el peso
            if rootNode.leftchild.data.peso > rootNode.rightchild.data.peso:
                return f"El próximo paquete a enviar es: {rootNode.leftchild.data.id}"
            elif rootNode.leftchild.data.peso < rootNode.rightchild.data.peso:
                return f"El próximo paquete a enviar es: {rootNode.rightchild.data.id}"
            else:
                # Si el peso también es igual, comparar el tamaño
                if rootNode.leftchild.data.tamaño > rootNode.rightchild.data.tamaño:
                    return f"El próximo paquete a enviar es: {rootNode.leftchild.data.id}"
                else:
                    return f"El próximo paquete a enviar es: {rootNode.rightchild.data.id}"




## recorre todo el arbol buscado y comparando que paquete tiene el id a encontrar
def Buscar_paquete_id(rootNode, id): ##metodo inOrden
    
    if not rootNode:
        return False, "No se encontró el paquete"
    
    # Recorremos el subárbol izquierdo
    encontrado, mensaje = Buscar_paquete_id(rootNode.leftchild, id)
    
    # Si ya se encontró en el subárbol izquierdo, retornamos el resultado
    if encontrado:
        return True, mensaje
    
    # Verificamos el nodo actual
    if rootNode.data and rootNode.data.id == id:
        mensaje = f"Paquete encontrado: {rootNode.data}"
        return True, mensaje
    
    # Si no lo encontramos, continuamos con el subárbol derecho
    return Buscar_paquete_id(rootNode.rightchild, id)


# nos retorna el ultimo nodo de el minimo subarbol 
# para retornarlo en eliminar paquete y hace eliminar una raiz pasadola a ser una hoja

def minimoArbol(node):
    if node is None:
        return None
    min_node = node
    left_min = minimoArbol(node.leftchild)
    right_min = minimoArbol(node.rightchild)
    if left_min and left_min.data < min_node.data:
        min_node = left_min
    if right_min and right_min.data < min_node.data:
        min_node = right_min
    return min_node

# encunetra el paquete a eliminar y llama a miniArbol para saber por cual nodo cambiarlo

def Eliminar_paquete_id(rootNode, id):
    if rootNode is None:
        return f"No se encontró ningún paquete con ID {id}."

    # Si el nodo raíz tiene el ID buscado
    if rootNode.data.id == id:
        mensaje = f"El paquete con ID {id} fue eliminado exitosamente."
        # Caso 1: Nodo sin hijos
        if rootNode.leftchild is None and rootNode.rightchild is None:
            return mensaje  # Eliminar el nodo

        # Caso 2: Nodo con un hijo
        if rootNode.leftchild is None:
            return mensaje  # Retornar el hijo derecho
        if rootNode.rightchild is None:
            return mensaje  # Retornar el hijo izquierdo

        # Caso 3: Nodo con dos hijos
        # Encontrar el mínimo en el subárbol derecho
        min_larger_node = minimoArbol(rootNode.rightchild)
        # Reemplazar el nodo a eliminar con el nodo mínimo
        rootNode.data = min_larger_node.data
        # Eliminar el nodo mínimo del subárbol derecho
        rootNode.rightchild = Eliminar_paquete_id(rootNode.rightchild, min_larger_node.data.id)
        return mensaje

    # Recorrer el subárbol izquierdo y derecho para buscar el ID
    mensaje_izq = Eliminar_paquete_id(rootNode.leftchild, id)
    if "exitosamente" in mensaje_izq:
        return mensaje_izq
        
    mensaje_der = Eliminar_paquete_id(rootNode.rightchild, id)
    if "exitosamente" in mensaje_der:
        return mensaje_der
    
    return f"No se encontró ningún paquete con ID {id}."


# Extrae el paquete más prioritario (la raíz)
def Enviar_siguiente(rootNode):
    if rootNode is None:
        return None
        
    # Si el árbol solo tiene la raíz
    if rootNode.leftchild is None and rootNode.rightchild is None:
        valor_eliminado = rootNode.data
        rootNode.data = None
        return valor_eliminado
    #Esta función recursiva calcula la altura del árbol, que es la longitud del camino más largo desde la raíz hasta una hoja.
    #  es Necesaria para saber dónde está el último nivel del árbol
    def altura_arbol(node):  # Sin ella, no podríamos ubicar el último nodo para reemplazar la raíz
        if node is None:
            return 0
        return 1 + max(altura_arbol(node.leftchild), altura_arbol(node.rightchild))
    
    #cuenta cuántos nodos hay en un nivel específico del árbol. Esto se usa para determinar si el último nivel está lleno.
    # Esencial para encontrar el último nodo que reemplazará la raíz
    def contar_nodos_nivel(node, nivel):
        if node is None or nivel < 0:
            return 0
        if nivel == 0:
            return 1
        return contar_nodos_nivel(node.leftchild, nivel - 1) + contar_nodos_nivel(node.rightchild, nivel - 1)

    # Esta función localiza y elimina el último nodo del árbol, que es el nodo más a la derecha en el nivel más bajo.
    # Usa las dos funciones anteriores para localizar el último nodo (altura_arbol,contar_nodos_nivel)
    # Este nodo reemplazará la raíz que se está eliminando
    def encontrar_y_eliminar_ultimo_nodo(node, parent=None):
        altura = altura_arbol(rootNode)
        # Encontrar el último nivel con nodos
        ultimo_nivel = altura - 1
        nodos_ultimo_nivel = contar_nodos_nivel(rootNode, ultimo_nivel)
        
        # Si el último nivel está lleno, buscar en el penúltimo nivel
        if nodos_ultimo_nivel == 0:
            ultimo_nivel -= 1
            nodos_ultimo_nivel = contar_nodos_nivel(rootNode, ultimo_nivel)

        def encontrar_ultimo(node, nivel_actual, pos_objetivo): # POS_OBJETIVO ES PARA  rastraer el nodo del ultimo nivel
                                                                # para eliminar la raiz deseada 
            if node is None:
                return None, None

            if nivel_actual == 0:
                return node, parent

            nodos_izq = contar_nodos_nivel(node.leftchild, nivel_actual - 1)
            
            if pos_objetivo <= nodos_izq:
                return encontrar_ultimo(node.leftchild, nivel_actual - 1, pos_objetivo)
            else:
                return encontrar_ultimo(node.rightchild, nivel_actual - 1, pos_objetivo - nodos_izq)

        ultimo_nodo, padre = encontrar_ultimo(rootNode, ultimo_nivel, nodos_ultimo_nivel)
        
        # Eliminar el último nodo
        if padre:
            if padre.rightchild == ultimo_nodo:
                padre.rightchild = None
            else:
                padre.leftchild = None
                
        return ultimo_nodo

    # se crea el cambio de variables de la raiz por el ultimo nodo y se elmina
    # Encontrar y eliminar el último nodo
    ultimo_nodo = encontrar_y_eliminar_ultimo_nodo(rootNode)
    
    # Guardar el valor de la raíz para retornarlo
    valor_eliminado = rootNode.data
    
    # Reemplazar el valor de la raíz con el del último nodo
    rootNode.data = ultimo_nodo.data
    
    # Proceso de hundimiento (heapify down) para mantener la propiedad de Heap donde la raiz es la que tiene mayor prioridad 
    def heapify_down(node):
        while node:
            smallest = node
            left_child = node.leftchild
            right_child = node.rightchild
            
            # Verificar y comparar el hijo izquierdo
            if left_child and esNuevaRaiz(left_child.data, smallest.data):
                smallest = left_child
                
            # Verificar y comparar el hijo derecho
            if right_child and esNuevaRaiz(right_child.data, smallest.data):
                smallest = right_child
                
            # Si no hay cambios, terminamos
            if smallest == node:
                break
                
            # Intercambiar valores con el hijo con mayor prioridad
            node.data, smallest.data = smallest.data, node.data
            node = smallest
    
    # Aplicar heapify down O HUNDIMOENTO     desde la raíz
    heapify_down(rootNode)
    
    return valor_eliminado

###

"""
def eliminarUltimoNodo(root):
        altura = alturaArbol(root)
        ultimo_nivel = altura - 1
        nodos_ultimo_nivel = contarNodosNivel(root, ultimo_nivel)
        if nodos_ultimo_nivel == 0:
            ultimo_nivel -= 1
        return encontrarYEliminarUltimo(root, ultimo_nivel)
"""
###
"""
def alturaArbol(node):
    if node is None:
        return 0
    return 1 + max(alturaArbol(node.leftchild), alturaArbol(node.rightchild))

"""

###
"""
def contarNodosNivel(node, nivel):
    if node is None or nivel < 0:
        return 0
    if nivel == 0:
        return 1
    return (contarNodosNivel(node.leftchild, nivel - 1) +
            contarNodosNivel(node.rightchild, nivel - 1))

"""

####
"""
def encontrarYEliminarUltimo(root, nivel):
    if root is None:
        return None
    if nivel == 0:
        return root
    nodo_izq = encontrarYEliminarUltimo(root.leftchild, nivel - 1)
    if nodo_izq:
        root.leftchild = None
        return nodo_izq
    nodo_der = encontrarYEliminarUltimo(root.rightchild, nivel - 1)
    if nodo_der:
        root.rightchild = None
        return nodo_der
"""


def Proximos_de_Envio(root, level=1):
    if not root:
        return
    print(f"Nivel {level}: {root.data}")
    if root.leftchild:
        Proximos_de_Envio(root.leftchild, level + 1)
    if root.rightchild:
        Proximos_de_Envio(root.rightchild, level + 1)


# # creamos las instancias 



A = Paquete(id=1, prioridad=1, peso=10.5, tamaño=3, destino="Destino A", fecha_entrega=datetime(2024, 11, 1).date())
B = Paquete(id=2, prioridad=2, peso=8.3, tamaño=2, destino="Destino B", fecha_entrega=datetime(2024, 10, 29).date())
C = Paquete(id=3, prioridad=3, peso=15.0, tamaño=1, destino="Destino C", fecha_entrega=datetime(2024, 11, 1).date())
D = Paquete(id=4, prioridad=1, peso=6.0, tamaño=3, destino="Destino D", fecha_entrega=datetime(2024, 10, 28).date())
E = Paquete(id=5, prioridad=5, peso=12.4, tamaño=2, destino="Destino E", fecha_entrega=datetime(2024, 11, 2).date())
F = Paquete(id=6, prioridad=4, peso=9.0, tamaño=1, destino="Destino F", fecha_entrega=datetime(2024, 11, 3).date())
G = Paquete(id=7, prioridad=3, peso=5.5, tamaño=3, destino="Destino G", fecha_entrega=datetime(2024, 11, 2).date())
H = Paquete(id=8, prioridad=2, peso=13.2, tamaño=1, destino="Destino H", fecha_entrega=datetime(2024, 10, 30).date())
I = Paquete(id=9, prioridad=1, peso=7.7, tamaño=2, destino="Destino I", fecha_entrega=datetime(2024, 11, 4).date())
J = Paquete(id=10, prioridad=3, peso=11.0, tamaño=3, destino="Destino J", fecha_entrega=datetime(2024, 10, 16).date())
K = Paquete(id=11, prioridad=2, peso=6.4, tamaño=1, destino="Destino K", fecha_entrega=datetime(2024, 11, 1).date())
L = Paquete(id=12, prioridad=4, peso=14.0, tamaño=2, destino="Destino L", fecha_entrega=datetime(2024, 10, 31).date())
M = Paquete(id=13, prioridad=1, peso=11.1, tamaño=1, destino="Destino M", fecha_entrega=datetime(2024, 10, 18).date())
N = Paquete(id=14, prioridad=3, peso=8.6, tamaño=2, destino="Destino N", fecha_entrega=datetime(2024, 11, 5).date())
O = Paquete(id=15, prioridad=2, peso=7.2, tamaño=1, destino="Destino O", fecha_entrega=datetime(2024, 11, 6).date())
P = Paquete(id=16, prioridad=5, peso=13.5, tamaño=3, destino="Destino P", fecha_entrega=datetime(2024, 10, 27).date())
Q = Paquete(id=17, prioridad=4, peso=9.8, tamaño=2, destino="Destino Q", fecha_entrega=datetime(2024, 11, 7).date())
R = Paquete(id=18, prioridad=2, peso=6.9, tamaño=1, destino="Destino R", fecha_entrega=datetime(2024, 10, 15).date())
S = Paquete(id=19, prioridad=1, peso=12.7, tamaño=2, destino="Destino S", fecha_entrega=datetime(2024, 10, 8).date())
T = Paquete(id=20, prioridad=3, peso=10.2, tamaño=3, destino="Destino T", fecha_entrega=datetime(2024, 10, 14).date())




root = BinaryTree(None)  # crear la raiz
#insertar los nodo (Paquetes)
insertarMinHeap(root,A)
insertarMinHeap(root,B) 
insertarMinHeap(root,C)
insertarMinHeap(root,D)
insertarMinHeap(root,E)
insertarMinHeap(root,F)
insertarMinHeap(root,G)
insertarMinHeap(root,H)
insertarMinHeap(root,I)
insertarMinHeap(root,J)
insertarMinHeap(root,K)
insertarMinHeap(root,L)
insertarMinHeap(root,M)
insertarMinHeap(root,N)
insertarMinHeap(root,O)
insertarMinHeap(root,P)
insertarMinHeap(root,Q)
insertarMinHeap(root,R)
insertarMinHeap(root,S)
insertarMinHeap(root,T)


print("\n")
print("\n")
printTree(root)
print("\n")
print("\n")

## eliminar paquete por id 
print(Eliminar_paquete_id(root, 12))
printTree(root)
print("\n")

## buscar paquete por id:
print(Buscar_paquete_id(root,11))
print("\n")

## opcion enviar siguiente osea la raiz y sucesivamente: 
print(Enviar_siguiente(root))
printTree(root)
print("\n")

## proximo a enviar 
print("proximo en enviar")
print(proximo_en_enviar(root))



## paquetes pendientes de envio:
Proximos_de_Envio(root)