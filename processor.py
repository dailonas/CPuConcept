import json
import time

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
        print("============             EXECUTION            ==============\n")
    
    def load_program(self, program): #  
        """charge un programme en memoire en reservant les 200 premieres cases pour les instructions"""
        if len(program) > len(self.memoryProgram):
            raise ValueError("Error(54): La tailles du program est superieure à l'espaces réservé.")
        self.memoryProgram[:len(program)] = program # Charger dans dans la memoire de programme, le programme.
        self.cp = 0 # Reinitialiser le compteur de programme.
    
    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = [int(x) for x in f.read().split()]
            self.load_program(data)

    def run(self):
         """"Execute le programme dans la memoire memoryProgram"""
         self.running = True # Etat du cpu(vrai).
         while self.running:
            opcode = self.memoryProgram[self.cp] # Recuperation d'instruction du programme / Lire le programme actuelle.(op= operation code, nombre qui represente une instructiion du cpu et indique qu'elle operation effectuer par le cpu).

            if opcode == 1: # LOAD, valuer intermediaire.
                self.cp += 1
                self.accumulator = self.memoryProgram[self.cp]
                print(f"=> Chargement de la valeur {self.accumulator} à l'adresse {self.cp}.")
                

            elif opcode == 2: # ADD, valuer intermediaire.
                self.cp +=1 
                value = self.memoryProgram[self.cp]
                self.accumulator += value
                print(f"=> Ajout de la valeur {value} à la valeur {self.accumulator - value} de l'accumulator")
                
            
            elif opcode == 3: # STORE, adresse memoire memoryData
                self.cp +=1 
                address=self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(82): Adresse memoire invalide {address}.")
                self.memoryData[address] = self.accumulator
                print(f"=> Store")
                
            
            elif opcode == 4: # READ, adresse memoire memoryData
                self.cp +=1
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(90): Adresse memoire invalide {address}.")
                self.accumulator = self.memoryData[address]
                print(f"=> Recharge l'accumulateur avec la valeur charger à l'adresse {address}.")
                 

            elif opcode == 5: # WRITE, adresse memoryData
                self.cp +=1
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(98): Address memoire invalide {address}.")
                self.memoryData[address] = self.accumulator
                print(f"=> Ecriture de la valeur chargée dans l'accumulator à l'adresse {address}.")
                
            elif opcode == 6: # PUSH, (Ajouter une valeur à backup)
                self.push_to_backup(self.accumulator)
                print(f"=> Ajout de la valeur: {self.accumulator} aux backup.")

            elif opcode == 7: # POP, (Recuperer la plus ancienne valuer de backup)
                self.accumulator = self.pop_from_backup()
                print(f"=> Recuperation du backup: {self.accumulator}.")

            elif opcode == 8: # SUB, valuer intermediaire.
                self.cp +=1 
                value = self.memoryProgram[self.cp]
                self.accumulator -= value
                print(f"=> Soustraction de la valeur {value} à la valeur {self.accumulator + value} de l'accumulator")

            elif opcode == 9: # DIV, valuer intermediaire.
                self.cp +=1 
                value = self.memoryProgram[self.cp]
                if value == 0:
                    raise ValueError(f"Error(127): Division par {value} imposible.")
                    self.running = False
                self.accumulator /= value
                print(f"=> Division par {value} de la valeur {self.accumulator * value} de l'accumulator")

            elif opcode == 10: # MULT, valuer intermediaire.
                self.cp +=1 
                value = self.memoryProgram[self.cp]
                self.accumulator *= value
                print(f"=> Multiplication par {value} de la valeur {self.accumulator / value} de l'accumulator")

            elif opcode == 11: # ABS, valuer intermediaire.
                self.cp +=1 
                value = self.memoryProgram[self.cp]
                self.accumulator = abs(value)
                print(f"=> Calcule de la valeur absolue de la valeur {value} avant chargement.")
            
            elif opcode == 12: # AABS, valuer intermediaire.
                self.accumulator = abs(self.accumulator)
                print(f"=> Suppression de la negativité de la valeur de l'accumulateur.")
            
            elif opcode == 13: # SIG, (Inverse le signe de l'accumulateur).
                self.accumulator = -self.accumulator
                print(f"=> Innverse du signe de l'accumulateur de {-self.accumulator} à {self.accumulator}.")

            elif opcode == 14: # JUMP, (Saut inconditionnel).
                self.pc = self.memoryProgram[self.cp + 1]-1
                # -1, pour compenser l'incrementation.
                print(f"=> Saut inconditionnel à l'adresse {self.cp}.")

            elif opcode == 15: # JUMPZ, (Saut conditionnel).
                addr = self.memoryProgram[self.cp+1]
                if self.accumulator == 0:
                    self.cp= addr - 1
                    print(f"=> Saut conditionnel(=0) à l'adresse {self.cp}.")

            elif opcode == 16: # JUMPD, (Saut conditionnel).
                addr = self.memoryProgram[self.cp+1]
                if self.accumulator != 0:
                    self.cp= addr - 1
                    print(f"=> Saut conditionnel(!0) à l'adresse {self.cp}.")
                else:
                    print(f"=> Saut conditionnel(!0) vérifié!")
                    continue
                    
                
            elif opcode == 17: # STOP, (Pause inconditionnel).
                self.cp +=1
                value = self.memoryProgram[self.cp]
                time.sleep(value)

            elif opcode == 99: # END, arrêt du  programme
                self.running = False
                print(f"=> Mise en arrêt du cpu: {self.running}")

            else:
                raise ValueError(f"Error(154): Opcode inconnu {opcode} à l'adresse {self.cp}.")
                self.running = False
            self.cp+=1 # Passe à l'instruction suivante.
            self.display_state() # Afficher l'état final.

    def push_to_backup(self, value):
        """Ajoute une valeur au FIFO (backup)"""
        if self.backup_pointer < self.backup_end:
            self.memoryData[self.backup_pointer] = value
            self.backup_pointer += 1
        else:
            print(f"Error(165): Backup plien, impossible d'y ajouter une valeur de plus")
    
    def pop_from_backup(self):
        """Recupere la premiere valeur enregistre das le backup (FIFO)"""
        if self.backup_pointer > self.backup_start:
            value = self.memoryData[self.backup_start]
            self.memoryData[self.backup_start: self.backup_pointer - 1] = self.memoryData[self.backup_start + 1: self.backup_pointer]
            self.memoryData[self.backup_pointer - 1] = 0 # Efface la derniere case.
            self.backup_pointer -=1
            return value
        else:
            print(f"Error(176): Backupt vide, impossible d'y recuperer une valeur.")
            return 0 
        
    def save_to_file(self, filename1, filename2):
        with open(filename1, 'w') as f:
            json.dump(self.memoryData[:50], f)
        with open(filename2, 'w') as f:
            json.dump(self.memoryProgram[:50], f)


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
         
#============#
class address:
    #==============#
    addr = [0] * 999
    addr[0] = 1001 
    addr[1] = 1002
    addr[2] = 1003
    addr[3] = 1004
    addr[4] = 1005
    addr[5] = 1006
    addr[6] = 1007
    addr[7] = 1008
    addr[8] = 1009
    addr[9] = 1010
    addr[10] = 1011
    addr[11] = 1012
    addr[12] = 1013
    addr[13] = 1014
    addr[14] = 1015
    addr[15] = 1016
#==================#
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
    '''Help: Ajoute une valeur a backup.'''
    POP = 7
    '''Help: Recupere la valeur enregistré dans backup.'''
    SUB = 8 # Instruction de subtraction.
    '''Help: '''
    DIV = 9 # Instruction de division.
    '''Help: '''
    MULT = 10 # Instruction de multiplication.
    '''Help: '''
    ABS = 11 # Instruction, valeur absolu.
    '''Help: Charger la valeur absolu de cette valuer (value).'''
    AABS = 12 # Instruction
    '''Help: Supprimer la negativité de l'accumulateur.'''
    SIG = 13 # Instruction
    '''Help: Changer le signe de la valeur dans l'accumulateur.'''
    JUMP = 14 #Saut conditionel
    '''Help: Aller à addr.'''
    JUMPZ = 15 #Saut conditionel
    '''Help: Aller à addr si accumulator = 0.'''
    JUMPD = 16 #Saut conditionel
    '''Help: Aller à addr si accumulator != 0'''
    STOP = 17 #Pause inconditionel
    '''Help: Faire une du programme.'''
    #==================================================================================================#
    test=1000
    CMP=test # Comparaison
    '''Help: '''
    CEQ= test# Comparaison
    '''Help: '''
    CNEQ=test # Comparaison
    '''Help: '''
    CLT=test # Comparaison
    '''Help: '''
    CGT= test# Comparaison
    '''Help: '''
    #===========================================================================================#
    END = 99 # Instruction d'arrrete du cpu.   
    #==========================================================================================#  