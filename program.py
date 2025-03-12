from processor import cpuConcept
from processor import language

cpu = cpuConcept()
f = language

#==============================#
program = [

    f.LOAD, 42,
    f.ADD, 5,
    f.WRITE, 10,
    f.PUSH,
    f.POP,
    f.END

]
#==============================#

cpu.load_program(program)
cpu.run()