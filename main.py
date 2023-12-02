#Password manager
#by: Polizeli

import os
from random import randint
from socket import gethostname

def databasecharacters():
    dbc = ['-','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '@', '$', '%', '&', '*']
    return dbc

def passwordgenerator(n1):
    #return a random srt passaword 

    dbc = databasecharacters()
    password = ''

    for i in range(0, n1):
        password += dbc[randint(0, len(dbc)-1)]

    return password

def keyprocessing(key):
    #trasnform a str key(ex: 'key123' ) into a list of int's
    #that list is necessary to encrepypt and decrypt the passwords
    #return a list of int's

    dbc = databasecharacters()
    finalkey = []
    partialVALUE = 0
    c = 0

    for l in key:
        pos = dbc.index(l)
        partialVALUE += pos

    for i in range(0, len(key)):
        atual = key[i]
        passada = key[i-1]

        x = dbc.index(atual)
        y = dbc.index(passada)
        
        finalkey.append(partialVALUE * (x * y))

    return finalkey

def encrypt(password, key):

    dbc = databasecharacters()
    keyint = keyprocessing(key)
    ecp = ''    # encrypted password
    psi = []    # the password, but now in int's
    con = 0     # its just a counter 
    pv  = 0     # partial value

    for i in password:
        psi.append(dbc.index(i))
    
    for i in range(0, len(password)):
        pv = (keyint[con] % len(dbc)) + psi[i]

        if pv >= len(dbc):
            pv -= len(dbc)

        if con < (len(key) - 1):
            con += 1
        else:
            con = 0
        
        ecp += dbc[pv]  

    return ecp
            
def decrypt(password, key):

    dbc = databasecharacters()
    keyint = keyprocessing(key)
    dcp = ''    # decrypt password
    psi = []    # the encrypt passaword, but now in it's
    con = 0     # it's just a counter
    pv  = 0     # partial value

    for i in password:
        psi.append(dbc.index(i))

    for i in range(0, len(password)):
        pv = (psi[i] + len(dbc)) - (keyint[con] % len(dbc))
        
        if pv >= len(dbc):
            pv -= len(dbc)

        if con < len(key) - 1:
            con += 1
        else:
            con = 0

        dcp += dbc[pv]

    return dcp

def append(plataform, login, password):
    with open("codes/a.txt", "a") as file:
        file.write("\nplataform = {} login = {} password = {}\n".format(plataform, login, password))

def search(term): 
    lstterm = 0         # last term 
    qterms  = 0         # quantity of terms
    fileterms = []      # list of the found terms

    with open("codes/a.txt", "r") as file:
        file = file.read()

    size = len(file)

    while True:
        s = file.find(term, lstterm, size)
        ac = ''

        if s == -1:
            break

        else:
            qterms += 1
            lstterm = file.find("\n", s)

            for i in range (s, lstterm):
                ac = ac + file[i]
            fileterms.append(ac)

    return fileterms

def interface():
    line = '-=' * 22 + '-'

    print(line)
    print("Welcome {}".format(gethostname()))
    print("You are using my password manager")
    print("Developed by: Polizeli")
    print(line)

    while True:
        print("Your options")
        print("0 - Exit\n1 - Generate password\n2 - Search")
        print(line)

        choice = int(input("Your choice: "))
        print(line)
        if choice == 0: 
            break
        
        elif choice == 1:

            platform = input("Platform: ")
            login = input("Login: ")
            password = passwordgenerator(int(input("Number of characters for the password: ")))
            key = input("Encryption key: ")
            print(line)
            print("Data confirmation:")
            print("Platform: {}\nLogin: {}\nPassword: {}\nEncryption key: {}".format(platform, login, password, key))
            print(line)
            confirmation = input("Do you want to confirm (y/n): ")
            if confirmation == 'n':
                break
            elif confirmation == 'y':
                encrypted_password = encrypt(password, key)
                append(platform, login, encrypted_password)
                print(line)
            else:
                print("It's either 'y' or 'n'!")
                print(line)

        elif choice == 2:
            term = input("Platform to be searched: ")
            search_result = search(term)
            print(line)
            if len(search_result) == 0:
                print("No term found")
                print(line)
                option = input("Do you want to continue (y/n): ")
                if option == 'y':
                    pass
                elif option == 'n':
                    break
            
            if len(search_result) >= 1:
                a = ''
                print("Found {} occurrence(s) of the term {}".format(len(search_result), term))
                for i in range(0, len(search_result)):
                    print("{} - {}".format(i+1, search_result[i]))
                print(line)
                n1 = int(input("Make your decision: ")) - 1 
                choice = input("Do you want to decrypt this password (y/n): ")
                if choice == 'y':
                    key = input("Encryption key: ")
                    v = search_result[n1].find("password = ") + len("password = ")
                    w = search_result[n1]
                    print(line)
                    for i in range(v, len(w)):
                        a += w[i]
                    decrypted_password = decrypt(a, key)
                    print("Your password is \n{}".format(decrypted_password))
                    print(line)
                elif choice == 'n':
                    pass

interface()
