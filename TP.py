from  time import time, sleep

# décorateur Python qui enregistre le temps d'exécution d'une fonction
# def timer(function):
#     def wrapper(*args, **kwargs):
#         debut = time()  # Temps de début de l'exécution de la fonction
#         resultat = function(*args, **kwargs)  # Appel de la fonction
#         fin = time()
#         temps = debut - fin
#         sl = temps
#         print(f"le temps d'éxecution de la fonction {function.__name__}: {sl} secondes")
#         return resultat
#     return wrapper


# fonction Python qui prend une liste d'entiers et renvoie une nouvelle liste contenant uniquement les nombres pairs
def list_of_even_number(choice):
    choice = "o"
    my_list = []
    even_number_list = []

    def even_number(number: int):
        return (int(number) % 2)

    while choice == "o":

        nbr = input("Entrer un nombre ")
        my_list.append(nbr)
        verify = even_number(nbr)
        if verify == 0:
            even_number_list.append(nbr)
        choice = input("voulez vous continuer ? o/n ")

        
    print("votre liste de chiffre paire est {0}".format(even_number_list))
    print("Fin merci d'avoir participer :)")
    return even_number_list  
    
list_of_even_number("o")

# def compter_caracteres(chaine):
#     compteurs = {}
    
#     for caractere in chaine:
#         if caractere in compteurs:
#             compteurs[caractere] += 1
#         else:
#             compteurs[caractere] = 1

#     return compteurs
# dictionnaire = {}
# # Exemple d'utilisation de la fonction
# ma_chaine = "Bonjour le monde"
# resultat = compter_caracteres(ma_chaine)

# print("Nombre d'occurrences de chaque caractère :")
# for caractere, occurences in resultat.items():
#     dictionnaire = {caractere:occurences}
#     print(dictionnaire)
    
    
    
# def compteur_element():
#     compteur = {}
#     chaine = input("entrez une chaine :")
#     for element in chaine:
#         if element in compteur:
#             compteur[element] += 1
#         else:
#             compteur[element] = 1
#     return compteur
            
# a = compteur_element()
# print(a)



# list_1 = []
# list_2 = []

# lenght = 0

# print("Liste 1")
# while lenght < 5:
#     a = input("Entrer un nombre: ")
#     list_1.append(a)
#     lenght = len(list_1)
    
# print("Liste 1: ",list_1)
# lenght = 0

# print("Liste 2")
# while lenght < 5:
#     a = input("Entrer un nombre: ")
#     list_2.append(a)
#     lenght = len(list_2)
# print("Liste 2: ",list_2)

# final_list = []

# for val in list_1:
#     if val in list_2:
#         final_list.append(val)
# print(final_list) 

