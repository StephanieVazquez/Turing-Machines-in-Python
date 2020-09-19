"""
Created on Tue Nov 04 20:30:13 2016

@author: Stephanie Vázquez
"""

import sys

pr = sys.stdout.write

class MachineTapeException(Exception):
    """ Turing Exception Exception """
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        return self.value

class TuringErrorException(Exception):
    """ Turing Exception Exception """
    def __str__(self):
        return "Sintaxis no válida"

class TuringAcceptException(Exception):
    """ Turing Accept Exception """
    def __str__(self):
        return "Cadena aceptada"

class MachineTape:
    def __init__(self, initialString=[], initialPos=0, blank="_"):
        """ Cinta implementada con una lista """
        self.tape = []
        self.pos = initialPos
        self.blank = blank
        self.initialString = initialString
        if len(initialString) > 0:
            for ch in initialString:
                self.tape.append(ch)
        else:
            self.tape.append(blank)

    def reinit(self):
        self.__init__(self.initialString)

    def move(self, check_char, changeto_char, direction):
        """ Solo puede haber movimientos R, L"""
        # validación
        if check_char != self.tape[self.pos]:
            raise MachineTapeException ("Error en el caracter")
        
        # cambio de caracter
        self.tape[self.pos] = changeto_char
        
        if direction == "L":
            self.move_left()
        elif direction == "R":
            self.move_right()
        else: raise MachineTapeException ("Dirección no válida")
    
    def read(self):
        """ Regresa el caracter en la cabeza lectora"""
        return self.tape[self.pos]
    
    def move_left(self):
        if self.pos <= 0: 
            self.tape.insert(-1, self.blank)
            self.pos = 0
        else:
            self.pos += -1

    def move_right(self):
        self.pos += 1
        if self.pos >= len(self.tape): self.tape.append(self.blank)
    
    def show(self):
        """ Imprimir la cinta """
        for ch in self.tape:
            pr(ch)
        pr("\n"); pr(" "*self.pos + "^"); pr("\n")

"""
Se crea la estructura de la máquina a partir de un diccionario.
    Con los sig pasos:
	1. Revisar si longitud de cadena es 0 y si se encuentra la MT en un edo final
	2. Si edo actual está en edos finales mostrar Aceptado
	3. Si edo actual no está definido en el programa mostrar Error
	4. Revisar el caracter en la cabeza
	5. Si caracter en la cabeza  no está en el programa marcar Error
	6. Sacar dest_state, char_out, y movimiento de diccionario
	7. Hacer nuevo estado, edo actual
	8. Escribir en la cinta, moverla cabeza

Program Layout:
    [state][char_in] --> [(dest_state, char_out, movement)]
"""

class TuringMachine:
    def __init__(self, initialString, initialStringTape2, finalStates=[], blank="_"):
        self.blank = blank
        self.tape = MachineTape(initialString)
        self.tape2 = MachineTape(initialStringTape2)
        self.fstates = finalStates
        self.program = {}
        self.initState = 0
        self.state = self.initState
        self.lenStr = len(initialString)
        self.lenStrTape2 = len(initialStringTape2)
    
    def reinit(self):
        self.state = self.initState
        self.tape.reinit()
    
    def addTransition(self, state, char_inT1, char_inT2, dest_state, char_outT1, char_outT2, movementT1, movementT2):
        if not self.program.has_key(state):
            self.program[state] = {}
            
        if not self.program[state].has_key(char_inT1):
            self.program[state][char_inT1]={}

        tup = (dest_state, char_outT1, char_outT2, movementT1, movementT2)
        self.program[state][char_inT1][char_inT2] = tup

    def step(self):
        """ Pasos 1 - 3 """
        if self.lenStr == 0 and self.state in self.fstates: raise TuringAcceptException
        if self.state in self.fstates: raise TuringAcceptException 
        if self.state not in self.program.keys(): raise TuringErrorException
        
        """ Pasos 4 y 5 """
        head = self.tape.read()
        head2 = self.tape2.read()
        if head not in self.program[self.state].keys(): raise TuringErrorException
        if head2 not in self.program[self.state].keys(): raise TuringErrorException
            
        """ Pasos 6 y 7 """
        # execute transition
        (dest_state, char_outT1, char_outT2, movementT1, movementT2) = self.program[self.state][head][head2]
        
        self.state = dest_state
        try:
            """ Paso 8 """
            self.tape.move(head, char_outT1, movementT1)
            self.tape.move(head2, char_outT2, movementT2)
        except MachineTapeException, s:
            print s

    def execute(self):
        """La máquina de Turing se queda en ciclo hasta llegar a un estado de aceptación o rechazo """
        try:
            while 1:
                m.tape.show()
                m.step()
        except (TuringErrorException, TuringAcceptException), s:
            print s

if __name__ == "__main__":
    #
    m = TuringMachine("1001101100101", [1])
    m.addTransition(0,'1','_',0,'1','0','R','R')
    m.addTransition(0,'0','_',0,'0','1','R','R')
    m.addTransition(0,'_','_',1,'_','_','L','L')
     
    # 
    m.execute()
