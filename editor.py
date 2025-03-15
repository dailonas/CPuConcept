from processor import cpuConcept
from processor import language
from processor import address
#===============================#
cpu = cpuConcept()
f = language 
w = address
#===============================#
program = [
    
    f.LOAD, 8,
    f.STOP, 1,
    f.SUB, 2,
    f.PUSH,
    f.JUMPD, f.ADD,
    f.END
  
]
#======================================================#
cpu.load_program(program)
cpu.run()