#!/usr/bin/env python
# coding: utf-8

# # Modélisation d'un vote implémenté sur blockchain

# In[ ]:





# In[1]:


import hashlib
class Block:  #block dont les instances vont composer ma Blockchain
    
    def __init__(self, previous_block_hash, transaction_list):

        self.previous_block_hash = previous_block_hash #hash du bloc précédent
        self.transaction_list = transaction_list #liste des transactions effectuées dans le bloc

        self.block_data = f"{' - '.join(transaction_list)} - {previous_block_hash}" #dans les données du bloc on insère les transactions ET le hash du block précédent (liaison des blocs)
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest() #calcul du hash du bloc


# In[ ]:





# In[2]:


class Blockchain:  #class Blockchain composée d'une liste de Block
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()

    def generate_genesis_block(self): #création du 1er Block -> Initialisation de ma blockchain 
        self.chain.append(Block("0", ['Genesis Block']))
    
    def create_block_from_transaction(self, transaction_list): #ajout d'un block à ma blockchain 
        previous_block_hash = self.last_block.block_hash
        self.chain.append(Block(previous_block_hash, transaction_list))

    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")

    @property #pour rendre le dernier bloc variable
    def last_block(self):
        return self.chain[-1]


# In[3]:


"""Je souhaite modéliser un vote entre un choix A et B au sein d'une ville. Et le sécuriser via ma Blockchain
n=nombre de citoyen de la ville
3n=Nombre de bulletin de vote 
n=Nb de bulletin A=Nb de bulletin B 
Pc=Pool de dépouillement 
Pe=Pool de distribution des bulletins
"""
import math
import random as rd 
import numpy as np
import matplotlib.pyplot as plt
import time 
n=rd.randint(1,100)
print(n) 
Blockchain=Blockchain() 


# In[4]:


messageclair="leo"
message=hashlib.sha256(messageclair.encode()).hexdigest()
print(message)  # exemple de hash du mot "leo" = sha256("leo")


# In[5]:


def consensus(vote,empreinte,d:int): #modélise le consensus au sein d'une blockchain 
    if mineur1(vote,empreinte,d,True) and mineur2(vote,empreinte,d,True) and mineur3(vote,empreinte,d,True): #si la majorité du réseau de validateur(=mineur) est d'accord: on ajoute le block
        print("mineur_proposition:"+vote) 
        print("mineur_hash:"+hashlib.sha256(vote.encode()).hexdigest())
        return True
    return False


# In[6]:


def mineur1(vote,empreinte,d:int,mode:bool): #mineur qui adapte sa complexité en fonction de la difficulté d compléxité en O(129^d)
    
    if mode: #le mode true est le mode "consensus" c'est à dire que le mineur vote pour l'ajout(=la validité) d'un bloc à la blockchain 
        for i in range(d+1): #d est la difficulté du minage du bloc: d étant le nombre de caractère à inverser de la fonction de hashage
            if hashlib.sha256(vote.encode()).hexdigest()[i]!=empreinte[i]:
                return False
        return True
        
    elif d==0: #le validateur cherche à inverser partielement la fonction de hashage par force brute pour valider le bloc
        for i in range(129):
            if hashlib.sha256(chr(i).encode()).hexdigest()[0]==empreinte[0]:
                return consensus(chr(i),empreinte,d)
        return False
    elif d==1:
        for i in range(129):
            for j in range(129):
                val=True
                for k in range(d+1):
                    if hashlib.sha256((chr(i)+chr(j)).encode()).hexdigest()[k]!=empreinte[k]:
                        val=False
                if val:
                    return consensus((chr(i)+chr(j)),empreinte,d)   
        return False
    elif d==2:
        for i in range(129):
            for j in range(129):
                val=True
                for k in range(d+1):
                    if hashlib.sha256((chr(i)+chr(j)).encode()).hexdigest()[k]!=empreinte[k]:
                        val=False
                if val:
                    return consensus((chr(i)+chr(j)),empreinte,d)
        return False
    elif d==3:
        for i in range(129):
            for j in range(129):
                for t in range(129): #plus la difficulté est grande plus on teste d'entrée 
                    
                    val=True
                    for k in range(d+1):
                        if hashlib.sha256((chr(i)+chr(j)+chr(t)).encode()).hexdigest()[k]!=empreinte[k]:
                            val=False
                    if val:
                        return consensus((chr(i)+chr(j)+chr(t)),empreinte,d)
        return False
    else:
        return False
    


# In[7]:


def mineur2(vote,empreinte,d:int,mode:bool): #mineur avec une compléxité constante O(129^3)
    
    if mode:
        for i in range(d+1):
            if hashlib.sha256(vote.encode()).hexdigest()[i]!=empreinte[i]:
                return False
        return True
        
    else:
        for i in range(129):
            for j in range(129):
                for t in range(129): #il faut assez de boucle pour espérer avoir une sortie correcte
                    val=True
                    for k in range(d+1):
                        if hashlib.sha256((chr(i)+chr(j)+chr(t)).encode()).hexdigest()[k]!=empreinte[k]:
                            val=False
                    if val:
                        return consensus((chr(i)+chr(j)+chr(t)),empreinte,d) #si on a trouvé un antécédent on le propose
        return False


# In[8]:


def mineur3(vote,empreinte,d:int,mode:bool): #mineur avec une compléxité constante O(129^4)
    
    if mode:
        for i in range(d+1):
            if hashlib.sha256(vote.encode()).hexdigest()[i]!=empreinte[i]:
                return False
        return True
        
    else:
        for i in range(129):
            for j in range(129):
                for t in range(129):
                    for a in range(129):#il faut assez de boucle pour espérer avoir une sortie correcte
                        val=True
                        for k in range(d+1):
                            if hashlib.sha256((chr(i)+chr(j)+chr(t)+chr(a)).encode()).hexdigest()[k]!=empreinte[k]:
                                val=False
                        if val:
                            return consensus((chr(i)+chr(j)+chr(t)+chr(a)),empreinte,d) #si on a trouvé un antécédent on le propose
        return False


# In[9]:


def mineur4(vote,empreinte,d:int,mode:bool): #mineur avec une compléxité constante O(129^4)
    
    if mode:
        for i in range(d+1):
            if hashlib.sha256(vote.encode()).hexdigest()[i]!=empreinte[i]:
                return False
        return True
        
    else:
        for i in range(129,0,-1):
            for j in range(129,0,-1):
                for t in range(129,0,-1):
                    for a in range(129,0,-1):#il faut assez de boucle pour espérer avoir une sortie correcte
                        val=True
                        for k in range(d+1):
                            if hashlib.sha256((chr(i)+chr(j)+chr(t)+chr(a)).encode()).hexdigest()[k]!=empreinte[k]:
                                val=False
                        if val:
                            return consensus((chr(i)+chr(j)+chr(t)+chr(a)),empreinte,d) #si on a trouvé un antécédent on le propose
        return False


# In[10]:


def mineur5(vote,empreinte,d:int,mode:bool): #mineur avec une compléxité constante O(129^4)
    
    if mode:
        for i in range(d+1):
            if hashlib.sha256(vote.encode()).hexdigest()[i]!=empreinte[i]:
                return False
        return True
        
    else:
        for i in range(20000000):
            val=True
            for k in range(d+1):
                if hashlib.sha256(str(i).encode()).hexdigest()[k]!=empreinte[k]: 
                    val=False
            if val:
                return consensus(str(i),empreinte,d) #si on a trouvé un antécédent on le propose
        return False


# In[11]:


def launcher(empreinte): #lanceur de la validation de block, empreinte est le hash du block en cours de validation
    d=rd.randint(0,3) #on tire une difficultée aléatoire, pour améliorer ma simulation il faudrait avoir une difficulté qui s'adapte au nombre de mineur sur mon réseau 
    print(f"difficulté:{d}")
    if mineur1("",empreinte,d,False) or mineur2("",empreinte,d,False) or mineur3("",empreinte,d,False) or mineur4("",empreinte,d,False) or mineur5("",empreinte,d,False):
        return True #si un des validateurs inverse partiellement la fonction de hashage on renvoit true 
    else:
        return False


# In[12]:


mineur1("leo","8535e86c8118bbbb0a18ac72d15d3a2b37b18d1bce1611fc60165f322cf57386",0,True)


# In[13]:


consensus("leo","8535e86c8118bbbb0a18ac72d15d3a2b37b18d1bce1611fc60165f322cf57386",0)


# In[14]:


mineur2("","07032003",3,False)


# In[15]:


mineur2("","07032003",4,False) # 4 est le max pour 3 boucle 


# In[16]:


mineur3("","07032003",5,False) #à partir de 6 (la difficultée d) on ne parvient plus à trouver le message clair(=l'antécédent=l'inversion partielle de la fonction de hashage), 5 est le max pour 4boucles


# In[17]:


mineur5("","07032003",2,False)#une nouvelle fois blocage à partir de 6 (remplacer la difficultée par 6 pour voir le blocage)


# In[18]:


launcher("07032003") #exemple de validation d'un bloc donc le hash(=l'empreinte) est: "07032003" si le launcher renvoit true alors les d premiers caractères de la proposition du mineur seront égaux aux d premiers du hash


# In[19]:


def distri(A,B,n): #création des bulletins de vote dans une pool(=smart contract)
    Pe=[["A" for i in range(n)],["B"for i in range(n)],["C" for i in range(n)]]
    empreinte=Block(Blockchain.last_block.block_hash,[f" {3*n} jetons ont été crée dans la pool Pool d'envoie"]).block_hash
    print(f"empreinte à trouver: {empreinte}")
    if launcher(empreinte): #si le réseau de validateur valide le bloc alors on ajoute le bloc à la blockchain
        Blockchain.create_block_from_transaction([f" {3*n} jetons ont été crée dans la pool Pool d'envoie"])
        print(f" {3*n} jetons ont été crée dans la pool Pool d'envoie")
        return Pe
    else:
        return "Invalidation réseau"
Pe=distri("A","B",n)
print(Pe)
Blockchain.display_chain()


# In[ ]:





# In[20]:


def distributionjeton(Pe,n): #distribution des bulletins de vote dans les portefeuilles des votants(=citoyens) de la ville
    assert len(Pe[0])==n and len(Pe[1])==n, ("Nb jeton A != Nb jeton B")
    Votants=[[] for i in range(n)]
    i=0
    for e in Votants:
        e.append("A") 
        e.append("B")
        e.append("C")
        
        Pe[0].pop()
        Pe[1].pop()
        Pe[2].pop()
        empreinte=Block(Blockchain.last_block.block_hash,[f"La pool d'envoie a envoyé 1 bulletin de vote A,B et C au votant {i}"]).block_hash
        print(f"empreinte à trouver: {empreinte}")
        if launcher(empreinte):
            Blockchain.create_block_from_transaction([f"La pool d'envoie a envoyé 1 bulletin de vote A,B et C au votant {i}"])
            print(f"La pool d'envoie a envoyé 1 bulletin de vote A,B et C au votant {i}")
        i+=1
    if Pe[0]==[] and Pe[1]==[] and Pe[2]==[]: #on vérifie que les jetons ont bien été envoyé de pool d'envoie vers le portefeuille du votant
        return Votants
    else:
        return "Problème de taille"
Votants=distributionjeton(Pe,n)  
print(Votants)
Blockchain.display_chain()


# In[21]:


def influence(t,c): #fonction permettant de régler les probabilités de vote pour simuler le choix des citoyens
    p=rd.random()
    if min(c,t)<p<max(c,t): #vote B
        return 1
    elif p<min(c,t):#vote A
        return 0
    else: #vote B
        return 2
influence(0.4, 0.8) # 40% sur A et B et 20% sur C  


# In[22]:


def vote(Votants,n): #simulation des votes des citoyens 
    assert len(Votants)==n, ("Problème nb de votants")
    Pc=[]
    i=0
    for e in Votants:
        Vote=e[influence(0.3,0.8)]
        Pc.append(Vote)
        e.remove(Vote) #on enlève le jeton du portefeuille du votant
        empreinte=Block(Blockchain.last_block.block_hash,[f"Le votant {i} a envoyé 1 bulletin de vote {Vote} à la pool de comptage"]).block_hash
        print(f"empreinte à trouver: {empreinte}")
        if launcher(empreinte):
            Blockchain.create_block_from_transaction([f"Le votant {i} a envoyé 1 bulletin de vote {Vote} à la pool de comptage"])
            print(f"Le votant {i} a envoyé 1 bulletin de vote {Vote} à la pool de comptage")
        i+=1
    return Pc
Pc=vote(Votants,n)
print(Pc)
Blockchain.display_chain()


# In[ ]:





# In[23]:


def depouillement(Pc,n):
    #assert len(Pc)==n , ("Vote corrompue")
    A=0
    B=0
    C=0
    for e in Pc:
        if e=="A":
            A+=1
        elif e=="B":
            B+=1
        else:
            C+=1
    if A>B:
        return [f"A gagnant avec {(A/n)*100}% vote A contre {(B/n)*100}% vote B et {(C/n)*100}% de vote blanc","A"]
    elif A==B:
        return [f"Egalité avec {A} vote A contre {B} vote B et {(C/n)*100}% de vote blanc","EGALITE"]
    else: 
        return [f"B gagnant avec {(A/n)*100}% vote A contre {(B/n)*100}% vote B et {(C/n)*100}% de vote blanc","B"]
depouillement(Pc,n)       
# In[ ]:





# In[24]:


def election(n,A,B):  #lancement d'une élection entre A et B de n votants avec appel de toutes les étapes 
    Pe=distri("A","B",n)
    Votants=distributionjeton(Pe,n)
    Pc=vote(Votants,n)
    #Blockchain.display_chain()
    return depouillement(Pc,n)
election(10,"A","B")


# In[195]:


#Blockchain=Blockchain()
def histo(n):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    A=0
    B=0
    C=0
    for i in range(n):
        res=election(n,A,B)
        if res[1]=='A':
            A+=1
        elif res[1]=='B':
            B+=1
        else:
            C+=1
    etiquettes = ['A', 'B', 'EGALITE']

    valeurs = [A, B, C]
    print(A,B,C)
    # Affichage des données
    ax.bar(etiquettes, valeurs, color=['red', 'blue', 'orange'], edgecolor="black")

    plt.title(f"Gagnants des votes n={n} avec facteurs d'influence")  # Titre du graphique
    plt.ylabel('Nombre occurence')  # Titre de l'axe y
    plt.xlabel('Choix')
    plt.show()  # Affichage d'une courbe
histo(n)

# In[424]:


"""Calcul des complexité"""
"""Thérorique: O(6n) car au total il y a 6parcours de liste, O(12n) avec blockchain car 1 transaction=1 envoi=1bloc"""
"""Validation patrique: """
#X=[i for i in range(1,100)]

#Y=[election(100,"A","B")[1] for i in range(1,100)]
#g=plt.plot(X,Y)
#plt.show(g)

def temps(n:int):
    ti=time.time()
    L=election(n,"A","B")
    tf=time.time()
    return [f"{tf-ti} secondes",tf-ti]

temps(100)


# In[425]:


def courbetemps(n:int):
    fig, ax = plt.subplots()
    ax.plot([i for i in range(1,n,5)], [temps(i)[1] for i in range(1,n,5)])
    
    plt.title("Temps d'execution en fonction du nombre d'habitant (avec blockchain)")
    plt.xlabel("Nombre d'habitants")
    plt.ylabel("Temps en seconde")

    plt.show() # affiche la figure à l'écran


# In[426]:


courbetemps(100)


# In[166]:


"""Pour une ville comme paris:"""
""""temps(2000000)"""


