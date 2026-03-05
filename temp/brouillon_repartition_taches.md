
#===================================================================
#=============== Binôme entrées, sorties et interface ==============
(manips strings, ggestion fichiers, création interfaces visuelles et
blinder le programme contre les erreurs humaines)

#--------------------------------------------------
#----- Parsing (Lecture fichier `config.txt`) -----
Ouvrir et lire le fichier de config passé en argument (`config.txt`)
Ignorer proprement les lignes de commentaire (qui commencent par un `#`)
Extraire les valeurs associées aux clés obligatoires (`WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`)
Convertir ces données brutes vers les bons types Python (ex: "WIDTH=20":str -> 20:int; "ENTRY=0,0" -> tuple(0, 0))

#-------------------------------
#----- Gestion des erreurs -----
Garantir que le programme ne plante JAMAIS
Créer des `try-except` pour attraper toutes les erreurs :
	fichier de config introuvable
	erreur de syntaxe
	largeur négative, coordonnées de sortie en dehors de la grille, etc.
Afficher des messages d'erreur clairs pour l'utilisateur dans la console

#-----------------------------------------------
#----- Interface Visuelle et interactivité -----
Affichage du labyrinthe (en ASCII dans le terminal / dans une fenêtre graphique avec MiniLibX)
Montrer clairement les murs, l'entrée, la sortie et le chemin résolu
Créer le menu interactif permettant à l'utilisateur de :
	regénérer un nouveau labyrinthe
	afficher/masquer la solution
	changer les couleurs des murs.

#-------------------------------------------
#----- exportation (fichier de sortie) -----
Prendre la grille générée par l'autre binôme et écrire le fichier de sortie (`OUTPUT_FILE`)
	convertir chaque case en hexadécimal (Bit 0: Nord + Bit 1: Est + Bit 2: Sud + Bit 3: Ouest)
	écrire les données ligne par ligne
	insérer une ligne vide
	ajouter les coordonnées d'entrée, de sortie, et le texte du chemin le plus court



#===================================================================
#================ Binôme algos, logique et packaging ===============

#----------------------------------
#----- Class `MazeGenerator` -----
Créer une classe pour encapsuler toute la logique de génération
Concevoir la structure de données interne (par ex class `Cell`) pour stocker les murs, cases...

#----------------------------------------------------
#----- Moteur pour générer le labyrinthe (algo) -----
Implémenter l'algo de génération (? backtracking recursif)
	y compris une graine (seed) pour que le résultat soit reproductible
Gérer les contraintes du terrain :
	cohérence des murs mitoyens
	murs sur les bordures extérieures
	empêcher la formation de couloirs plus larges que 2 cases
Si PERFECT=True, garantir 1 unique chemin entre l'entrée et la sortie

#----------------------
#----- motif "42" -----
Calculer les coordonnées des cases entièrement fermées pour dessiner le "42"

/!\ si la taille du labyrinthe est trop petite pour y mettre "42",
	lever une erreur spécifique pour affichage dans la console par l'autre binome
	omettre le motif et poursuivre

#---------------------------------
#----- Pathfinding (solveur) -----
Quand le labyrinthe est généré, écrire un second algo (par ex BFS Breadth-First Search)
	pour trouver le chemin le plus court entre l'entrée et la sortie
Traduire ce chemin en une suite de lettres `N`, `E`, `S`, `W`
	à fournir au binôme pour son fichier de sortie

#----------------------------
#----- Packaging Python -----
Isoler le module de génération pour qu'il soit installable via `pip`
Configurer les fichiers de build pour générer les archives `.tar.gz` et `.whl` nommées `mazegen-*`
Rédiger la mini-documentation expliquant comment importer et utiliser la classe `MazeGenerator`


#===========================
#----- Tâches communes -----
#===========================

Type Hints et Docstrings 
README.md (choix d'algos, planning, répartition rôles...)
