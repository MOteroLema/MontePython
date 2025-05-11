



class Metropolis():

    def __init__(self):

        #! Hay que pensar como se hace esto. Porque para Ising un paso de metropolis es invertir un espín, pero para Heisenberg y XY, el paso es girar el espín un ángulo aleatorio
        #! Igual en la clase Ising, Heisenberg, etc, se puede poner una función que se llame transform_state(), que le des un nodo y te devuelva el estado transformado (invertirlo en ising, rotarlo en el resto, etc..)