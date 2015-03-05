#!/usr/bin/python
#Ecrit par Charles Le Reun, Jason Ngosso et Cyril Segretain
#Projet QuotientGraph - 2014
#INSA Centre Val de Loire


#Fonction Centre : demande le centre a l'utilisateur et verifie que ce centre est un noeud
def centre(matrice):
	find=0
	while (find == 0):				#boucle tant que le centre n'est pas trouve valide
		try:								#permet de ne pas interrompre le programme en cas d'erreur, gestion d'erreur ensuite
			center=input("Choisissez le centre : ")
			recherche(matrice, center)				#le centre est compare a la premiere colonne de la matrice
			print "le centre choisi est", center, ". Nous generons le fichier de sortie, veuillez patienter."
			find=1
		except NameError:				#gestion d'erreur si le nom est mal ecrit
			print 'Erreur de nom, entrez le centre entre quote !'
		except IndexError:			#gestion d'erreur si le centre est inconnu
			print 'Centre inconnu.'
	return center

#Fonction recherche (qui recherche uniquement les noeuds donc en premiere colonne de la matrice)
def recherche(matrice, point):
	trouve=0
	i=0
	while trouve==0:
		if i > len(matrice):
			return -1
			break
		if matrice[i][0]==point:
			trouve=1
		i=i+1
	return (i-1)

#Fonction recherche_index qui permet de chercher un point dans toute la matrice
def recherche_index(matrice, point):
	i=0	
	while i < len(matrice):
		try:
			trouve=matrice[i].index(point)		#index renvoie la position de la valeur trouvee
		except ValueError:
			i=i+1
		else:
			return i										#renvoie le numero de ligne ou a ete trouve le point
			break
	return -1

#Fonction classe qui permet de creer les premiers tas en fonction du centre
def classe(matrice, centre):
	i=1
	j=0
	tas_adjacent=[]
	position_centre=recherche(matrice, centre)
	matrice_centre=matrice.pop(position_centre)  		#le centre est pop pour etre ecarte du traitement ensuite
	longueur=len(matrice_centre)
	while (longueur != 1):										#boucle autant de fois que le centre a d'adjacent
		search=recherche(matrice, matrice_centre[i])		#on recherche la ligne correspondant a l'adjacent
		ligne=matrice.pop(search)								#on pop la ligne
		tas_adjacent.append(ligne)								#on ajoute la ligne dans tas_adjacent
		matrice.append(ligne)									#on replace la ligne a la fin de la matrice
		longueur=longueur-1
		i=i+1
	return tas_adjacent, matrice_centre

#Fonction creation_matrice qui cree la matrice principale avec le fichier d'entree
def creation_matrice():
	from string import rstrip, lstrip
	#from numpy import *
	i=0
	error=1
	empty_line='\n'
	matrice=[[]]									#creation de la matrice
	while error==1:
		try:											#fichier source, gestion d'erreur, puis ouverture
			fichier=input('Entrez le nom du fichier d\'entree entre quote : ')
			f=open(fichier,'r')
			error=0
		except NameError:				#gestion d'erreur si le nom est mal ecrit
			print 'Erreur de nom, entrez le centre entre quote !'
		except SyntaxError:
			print 'Erreur de nom, entrez le centre entre quote !'
		except TypeError:
			print 'Erreur de nom, entrez le centre entre quote !'
		except IOError:
			print 'Fichier non trouve.'
	with f:
		while True:							#boucle infinie
			line=f.readline()				#lecture du fichier ligne par ligne
			if not line: break			#si fin du fichier, on sort de la boucle
			while line==empty_line:		#ligne vide, on lit la ligne suivante
				line=f.readline()
			matrice.append(list())		#on cree une liste d'adjacence dans la matrice (deuxieme dimension)
			matrice[i].append(line.lstrip("\t").rstrip("\n"))		#on ajoute le contenu de la ligne sans les tab et les sauts de ligne
			line=f.readline()				#on lit la ligne suivante qui doit etre un adjacent
			while line!=empty_line:		#tant qu'on ne tombe pas sur une ligne vide qui separe deux noeuds
				if not line.startswith("\t\t\t"): 	#si la ligne n'est pas un attribut commencant par 3 tabulations
					matrice[i].append(line.lstrip("\t").rstrip("\n"))	#on ajoute la ligne dans la liste
				line=f.readline()
			i=i+1								#on change de ligne dans la matrice donc changement de noeud
	tmp=matrice.pop(i)					#suppression de la derniere liste car vide
	f.close()
	return matrice

#Fonction creation_table_tas qui permet de creer la matrice de sortie avec juste les modules
def creation_table_tas(matrice, tas_adjacent, centre):
	table_tas=[[]]
	table_tas[0].append(centre)				#on ajoute le centre en premiere ligne pour le differencier
	table_tas.append(list())
	for element in tas_adjacent:				#on ajoute les adjacents au centre dans la deuxieme ligne
		table_tas[1].append(element[0])
	table_tas.append(list())
	for element in matrice:						#on ajoute les non-adjacents au centre dans la troisieme ligne
		ok=1
		for connu in tas_adjacent:
			if element[0]==connu[0]:			#on verifie que le noeud n'est pas dans la liste des adjacents
				ok=0
		if ok!=0:		
			table_tas[2].append(element[0])
	return table_tas

#Fonction pivot qui applique la regle du pivot
def pivot(matrice, tas):
	i=1
	tab_prov = []
	while i < len(tas):			#la boucle qui va parcourir toute la matrice tas
		j=0
		while j < len(tas[i]):		#la boucle qui va parcourir chaque noeud contenue dans la matrice tas
			pivot=tas[i][j]
			ligne = recherche(matrice, pivot)
			for adjacent in matrice[ligne]:				#recherche des adjacents au noeud 
				if adjacent not in tas[i]:			#si un adjacent ne se trouve pas sur la meme ligne du noeud dans la matrice tas
					valeur = recherche_index(tas, adjacent)
					if valeur == -1:
						break
					c=0
					d=-1
					while c < len(tas[valeur]):			#parcours la ligne de tas contenant un adjacent au noeud qui n'est pas sur la meme ligne que le noeud
						if tas[valeur][c] in matrice[ligne]:	#lorsque l'on trouve un adjacent sur cette ligne on incremente un compteur
							d=d+1
							tab_prov.append(tas[valeur][c])		#et on le stock dans un tableau provisoire
						c=c+1
					if c-1 != d:					#si le nombre de cases du tableau provisoire = le nombre de cases de la ligne prise
						e=0
						f=0
						e=len(tas)
						tas.append(list())
						while tab_prov:				#on deplace les valeurs stockees dans le tableau provisoire dans une nouvelle ligne de tas
							tas[e].append(tab_prov.pop(0))
						while f<len(tas[e]):
							g=0
							for val in tas[valeur]:
								print "val :", val
								if tas[valeur][g] == tas[e][f]:		#on supprime les adjacents qui etaient contenus sur l ancienne ligne de tas
									tas[valeur].remove(val)
								g=g+1
							f=f+1
					else:
						while tab_prov:				#sinon on reinitialise le tableau provisoire
							tab_prov.pop()
			j=j+1
		i=i+1
	print matrice
	print tas
	return tas

#Fonction ecrire qui ecrit la matrice table_tas dans un fichier de sortie
def ecrire(table_tas):
	fic=open('fichier_sortie.txt', 'w')
	i=0
	with fic:
		while i < len(table_tas):				#parcours de toutes les lignes de table_tas
			j=0
			while j < len(table_tas[i]):		#parcours d une ligne
				fic.write(table_tas[i][j])		#ecriture du noeud
				fic.write(' ')					#separation des noeuds par un espace
				j=j+1
			fic.write('\n')						#separation des tas par un saut de ligne
			i=i+1
	fic.close()

#On cree la matrice principale
matrice=creation_matrice()
#On choisit le centre
centre=centre(matrice)
#On applique la regle du centre
tas_adjacent, matrice_centre=classe(matrice, centre)
#On cree la table de sortie
table_tas=creation_table_tas(matrice, tas_adjacent, centre)
#On applique la regle du pivot
tas=pivot(matrice, table_tas)
#Une seconde fois pour verifier que les modules sont minimises
tas=pivot(matrice, tas)
#On ecrit la table de sortie dans un fichier
ecrire(tas)
