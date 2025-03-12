
class language:
    #========================================================================================#
    LOAD = 1 # Instruction de chagement.
    '''Help: Charge une valeur dans l'accumulateur '''
    ADD = 2 # Instruction d'addition.
    '''Help: '''
    STORE = 3 # Instruction 
    '''Help: '''
    READ = 4 # Lire dans la Memoire de de traille.
    '''Help: Recharge l'accumulateur avec la valeur stocker à l'adresse memory[addr] de la memoire.'''
    WRITE = 5 # Ecrire dans la Memoire de travail.
    '''Help: Ecrit la valeur charger dans l'accumulateur à une adresse de la memoire.'''
    PUSH = 6
    '''Help: Ajoute une valeur a backup'''
    POP = 7
    '''Help: Recupere la valeur enregistré dans backup'''

    
    #==================================================================================================#
    
    SUBB = 3 # Instruction de subtraction.
    '''Help: '''
    DIV = 4 # Instruction de division.
    '''Help: '''
    MULTIP = 5 # Instruction de multiplication.
    '''Help: '''
    #===========================================================================================#
    

    END = 99 # Instruction d'arrrete du cpu.   
    #==========================================================================================#
    

class cpuConcept:

    def __init__(self):
        self.accumulator = 0 # registre de travail pour stocker les calculs intermediaire.
        '''Gestion du registre backup:'''
        self.backup_start = 0 # Debut du backup dans memoryData
        self.backup_end = 1048576 # Réservation de 1048576 (1Mo) octets soit pour le backup dans memoryData. 
        self.backup_pointer = self.backup_start # Pointeur vers la prochaines case libre.

        self.memoryProgram = [0]*5242880 # Memoire de 5242880 cases soit 5242880 octets (5Mo) pour stocker le programme.
        self.memoryData = [0]* 2097152 # Memoire de 2097152 cases soit 2097152 octets (2Mo) pour stocker les données.
        self.cp = 0 # Compteur de programme, qui pointe l'instructio en cours.
        self.running = False # Satus/ Etat du cpu(faux).
        print("============================================================")
        print("             EXECUTION            ")
    
    def load_program(self, program): #  
        """charge un programme en memoire en reservant les 200 premieres cases pour les instructions"""
        if len(program) > len(self.memoryProgram):
            raise ValueError("Error(54): La tailles du program est superieure à l'espaces réservé.")
        self.memoryProgram[:len(program)] = program # Charger dans dans la memoire de programme, le programme.
        self.cp = 0 # Reinitialiser le compteur de programme.
    

    def run(self):
         """"Execute le programme dans la memoire memoryProgram"""
         self.running = True # Etat du cpu(vrai).
         while self.running:
            opcode = self.memoryProgram[self.cp] # Recuperation d'instruction du programme / Lire le programme actuelle.(op= operation code, nombre qui represente une instructiion du cpu et indique qu'elle operation effectuer par le cpu).

            if opcode == 1: # LOAD, valuer intermediaire.
                self.cp += 1
                self.accumulator = self.memoryProgram[self.cp]
                print(f"Chargement de la valeur {self.accumulator} à l'adresse {self.cp}.")
                

            elif opcode == 2: # ADD, valuer intermediaire.
                self.cp +=1 
                value = self.memoryProgram[self.cp]
                self.accumulator += value
                print(f"Ajout de la valeur {value} à la valeur {self.accumulator} de l'accumulator")
                
            
            elif opcode == 3: # STORE, adresse memoire memoryData
                self.cp +=1 
                address=self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(82): Adresse memoire invalide {address}.")
                self.memoryData[address] = self.accumulator
                print(f"Store")
                
            
            elif opcode == 4: # READ, adresse memoire memoryData
                self.cp +=1
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(90): Adresse memoire invalide {address}.")
                self.accumulator = self.memoryData[address]
                print(f"Recharge l'accumulateur avec la valeur charger à l'adresse {address}.")
                 

            elif opcode == 5: # WRITE, adresse memoryData
                self.cp +=1
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(98): Address memoire invalide {address}.")
                self.memoryData[address] = self.accumulator
                print(f"Ecriture de la valeur chargée dans l'accumulator à l'adresse {address}.")
                
            elif opcode == 6: # PUSH, (Ajouter une valeur à backup)
                self.push_to_backup(self.accumulator)
                print(f"Ajout de la valeur: {self.accumulator} aux backup.")

            elif opcode == 7: # POP, (Recuperer la plus ancienne valuer de backup)
                self.accumulator = self.pop_from_backup()
                print(f"Recuperation du backup: {self.accumulator}.")
                
            elif opcode == 99: # END, arrêt du  programme
                self.running = False
                print(f"Mise en arrêt du cpu: {self.running}")

            else:
                raise ValueError(f"Error(111): Opcode inconnu {opcode} à l'adresse {self.cp}.")
                self.running = False
            self.cp+=1 # Passe à l'instruction suivante.
            self.display_state() # Afficher l'état final.

    def push_to_backup(self, value):
        """Ajoute une valeur au FIFO (backup)"""
        if self.backup_pointer < self.backup_end:
            self.memoryData[self.backup_pointer] = value
            self.backup_pointer += 1
        else:
            print(f"Error(122): Backup plien, impossible d'y ajouter une valeur de plus")
    
    def pop_from_backup(self):
        """Recupere la premiere valeur enregistre das le backup (FIFO)"""
        if self.backup_pointer > self.backup_start:
            value = self.memoryData[self.backup_start]
            self.memoryData[self.backup_start: self.backup_pointer - 1] = self.memoryData[self.backup_start + 1: self.backup_pointer]
            self.memoryData[self.backup_pointer - 1] = 0 # Efface la derniere case.
            self.backup_pointer -=1
            return value
        else:
            print(f"Error(133): Backupt vide, impossible d'y recuperer une valeur.")
            return 0 

    def display_state(self):
         """affiche lles informations apres execution"""
         print("============================================================")
         print("\n=== ETAT FINAL DU CPU ===")
         print(f"Compteur de program (cp): {self.cp}")
         print(f"Accumulateur: {self.accumulator}")
         print(f"Memoire Programme: {self.memoryProgram[:10]}")
         print(f"MEmoire Données: {self.memoryData[:10]}")
         print(f"Contenu du backup: {self.memoryData[self.backup_start:self.backup_start+min(10, self.backup_pointer)]}")
         print("============================================================")
         

