from processor import cpuConcept
from processor import language
cpu = cpuConcept()
f = language
#===============================#
#==============================#

program = [

    # Initialisation de la variable de compteur à 1
    f.LOAD, 1,  # Charge la valeur 1 dans l'accumulateur
    f.STORE, 0,  # Stocke la valeur de l'accumulateur à l'adresse mémoire 0 (compteur)

    # Initialisation de la variable de résultat à 1
    f.LOAD, 1,  # Charge la valeur 1 dans l'accumulateur
    f.STORE, 1,  # Stocke la valeur de l'accumulateur à l'adresse mémoire 1 (résultat)

    # Début de la boucle pour calculer la factorielle
    f.LOAD, 1,  # Charge la valeur 1 dans l'accumulateur (compteur)
    f.LOAD, 2,  # Charge la valeur 2 dans l'accumulateur (constante 2)
    f.SUB, 0,    # Soustrait la valeur de la constante 2 de la valeur du compteur
    f.JUMPZ, 18,  # Saut à l'adresse 18 si le compteur est égal à 0 (fin de la boucle)

    # Multiplication du résultat par le compteur
    f.LOAD, 1,  # Charge la valeur 1 dans l'accumulateur (résultat)
    f.LOAD, 0,  # Charge la valeur 0 dans l'accumulateur (compteur)
    f.MULT, 1,    # Multiplie la valeur du résultat par la valeur du compteur
    f.STORE, 1,  # Stocke la valeur de l'accumulateur à l'adresse mémoire 1 (résultat)

    # Décrémentation du compteur
    f.LOAD, 0,  # Charge la valeur 0 dans l'accumulateur (compteur)
    f.LOAD, 1,  # Charge la valeur 1 dans l'accumulateur (constante 1)
    f.SUB, 0,    # Soustrait la valeur de la constante 1 de la valeur du compteur
    f.STORE, 0,  # Stocke la valeur de l'accumulateur à l'adresse mémoire 0 (compteur)

    # Retour au début de la boucle
    f.JUMP, -14,  # Saut à l'adresse -14 (retour au début de la boucle)

    # Fin du programme
    f.END, 0
]

#==============================#
#=========================================================#
cpu.load_program(program)
cpu.save_to_file("memoryData.json", "memoryProgram.json")
cpu.run()
print("Factorielle de 10:", cpu.memoryData[1])
print("Factorielle de 10:", cpu.memoryProgram[1])