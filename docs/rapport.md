# Rapport de projet

## Groupe

* Bensadok Yanis 28708067
* Hami Islam 21208634

## Description des choix importants d'implémentation

Notre code est divisé en trois parties :

* ### **Les méthodes utiles** :

> * `wallStates(walls)` : donne la liste des coordonnees des murs.
> * `playerStates(players)`: donne la liste des coordonnees des joueurs.
> * `legal_wall_position(pos)`: retourne True si un mur est valable.
> * `draw_random_wall_location()`:tire au hasard un couple de position permettant de placer un mur.
> * `remaining_walls(player)`: retourne le nombre de mur restants.
> * `eval(player)`: retourne le score.
> * `calculPath(player)`: calcul le path du joueur.
> * `finDePartieSiGagne(player)`: arrete la partie si un joueur atteint la ligne adverse.

* ### **Les stratégies** :

Pour implementer les strategies on a decide de creer une fonction par strategie, qui retourne a chaque tour du joueur le coup a jouer.

Puis on boucle sur les 2 strategies jusqu'a ce que un joueur gagne.

* ### **Le menu (choix de la stratégie des joueurs)** :

Au lancement du code un menu s'affiche en presentant les strategies disponible et demande d'abord  au joueur 0 de choisir sa strategie puis au joueur 1.

## Description des stratégies proposées

### ***Stratégie Aléatoire***

La stratégie aléatoire du jeu Corridor consiste à avancer dans un labyrinthe en choisissant des directions de manière aléatoire jusqu'à atteindre la sortie. Cette stratégie peut sembler simpliste, mais elle peut s'avérer efficace dans certains contextes. En effet, elle permet de visiter plusieurs zones du labyrinthe et de découvrir des chemins qui peuvent mener à la sortie plus rapidement que si l'on avait suivi un parcours prédéfini. Toutefois, cette stratégie n'assure pas la réussite à tous les coups, car il est possible de se retrouver bloqué dans une impasse ou de tourner en rond.

Pour implementer cette strategie, on a cree plusieurs fonctions, parmis elle:

* >`remaining_walls(player)`: retourne le nombre de murs restants pour un joueur.

* >`wall_notblock(x1,y1,x2,y2)`: verifie si un mur donnee bloque l'acces a l'objectif.

Pour creer une fonction `StrategieAlea(player)` qui en utilisant un facteur de hasard, un joueur va soit avancer vers une position aleatoire, soit appeler la fonction `draw_random_wall_location()`, si il a des murs restant, pour tirer au hasard 1 mur valide et verifier apres si le mur ne bloque pas avant de le placer sur la map.

### ***Strategie Walls First***

La stratégie "walls first" est une technique où deux joueurs doivent atteindre leur objectif tout en bloquant l'autre joueur. Cette stratégie consiste à placer tous les murs sur le chemin optimal de l'adversaire avant de commencer à avancer soi-même. En d'autres termes, le joueur qui utilise cette stratégie va construire une barrière de murs sur le trajet le plus court entre la position de départ de son adversaire et l'objectif de celui-ci. Cette barrière empêchera l'adversaire de progresser et le contraindra à chercher un autre chemin, lui faisant perdre du temps et de l'énergie. Une fois les murs placés, le joueur peut alors se déplacer vers son propre objectif en évitant les murs qu'il a lui-même construits. Cette stratégie est particulièrement efficace si l'on connaît bien le terrain de jeu et les habitudes de son adversaire, car elle permet de prévoir les déplacements de l'adversaire et d'anticiper ses mouvements.

Pour implementer cette strategie on a creer une fonction:

* > `StrategieWallsFirst(player)`: recupere une position du chemin de l'adversaire et verifie pour chaque configuration des murs qui ne bloque pas a cette position lequel augmente le plus la taille du path de l'adversaire, puis le joueur commence a avancer sur son chemin optimal vers la ligne d'arrivee.

### ***Strategie Murs Intelligents***

La stratégie des "Murs Intelligents" dans le jeu quorridor consiste a poser un mur sur le chemin de l'adversaire si il est plus proche que le joueur de sa ligne d'arrivee de tel sorte a augmenter la distance de l'adversaire de son objectif sinon il avance sur son chemin optimal.

* > `StrategieMursIntelligent(player)`: stocke dans 2 variables les distances des 2 joueurs par rapport a l'objectif, puis verifie si la distance du joueur est superieur a celle de l'adversaire donc on joue le mur le plus efficace pour bloquer l'adversaire, sinon on avance sur le chemin.

### ***Strategie Mini-Max elagage alpha-beta***

La stratégie Minimax Alpha-Beta est une technique de recherche de décision utilisée dans le jeu Quoridor pour aider les joueurs à prendre des décisions éclairées en fonction des mouvements possibles de leur adversaire. La stratégie repose sur le principe de minimisation des pertes potentielles et de maximisation des gains possibles. Les joueurs commencent par évaluer la situation actuelle du plateau de jeu en attribuant des valeurs numériques à chaque position, en fonction de son avantage ou de son désavantage. Ensuite, le joueur simule les mouvements possibles de l'adversaire et utilise l'algorithme Minimax Alpha-Beta pour déterminer le mouvement optimal qui maximisera leurs gains tout en minimisant les pertes potentielles. L'algorithme Minimax Alpha-Beta utilise une méthode de coupure de branche pour éviter de parcourir toutes les combinaisons possibles de mouvements, en éliminant les mouvements qui ne sont pas pertinents. Cette stratégie permet aux joueurs de prendre des décisions plus éclairées et plus efficaces pour maximiser leurs chances de gagner la partie.

Pour implementer cette strategie on a creer des fonctions :

* > `get_possible_moves(player)`:retourne la liste des murs qu'un joueur peut poser a un instant donnee.

* > `minimax_ab(player,state, depth, alpha, beta, maximizing_player)`: prend en entrée les paramètres suivants: le joueur actuel, l'état actuel du jeu (position des joueurs et des murs), la profondeur de l'arbre de recherche, les valeurs alpha et beta pour l'élagage de l'arbre, et un booléen indiquant si le joueur actuel est en train de maximiser ou minimiser son score.
La fonction commence par vérifier si la profondeur de recherche est atteinte ou si l'un des joueurs a atteint son objectif (dans ce cas, la fonction renvoie une évaluation du score actuel). Si le joueur actuel est en train de maximiser son score, la fonction recherche le mouvement qui maximise le score en calculant d'abord le chemin le plus court à l'objectif à l'aide de l'algorithme A* et en évaluant ensuite chaque mouvement possible, soit en déplaçant le joueur, soit en plaçant un mur. L'algorithme alpha-beta est utilisé pour élaguer les branches de l'arbre qui ne contribuent pas à la recherche. Si le joueur actuel est en train de minimiser son score, le processus est similaire, sauf qu'il cherche le mouvement qui minimise le score. Le meilleur mouvement trouvé est renvoyé avec l'évaluation correspondante.

* > `minimax_strategy(player)`:appelle la fonction minimax_ab pour recuperer le meilleur coup et l'execute.

## Description des résultats

Comparaison entre les stratégies. Bien indiquer les cartes utilisées.

### **Stratégie Walls First**

|  | Aléatoire | Murs Intelligents | MiniMax Alpha Beta | 
|----------|:-------------:|:------:|:-----: |
| Pourcentage de victoire| 84% | 37% | 50%|

### **Stratégie Murs Intelligents**

|  | Aléatoire | Walls First | MiniMax Alpha Beta | 
|----------|:-------------:|:------:|:-----: |
| Pourcentage de victoire| 97% | 63% | 50% |


### **Stratégie MiniMax élagage Alpha Beta à Horizon 3**

|  | Aléatoire | Walls First | Murs Intelligents | 
|----------|:-------------:|:------:|:-----: |
| Pourcentage de victoire| 100% | 50% | 50%|

On remarque que les 3 stratégies gagnent avec une écrasante probabilité contre Aléatoire.

On peut aussi voir que MiniMax et Murs Intelligents dominent faiblement Walls First, Murs Intelligents gagne plus souvent face à Walls First principalement car puisque Walls First utilise tout ses murs au début de la partie elle n'en a plus pour bloquer Murs Intelligents durant le reste de la partie alors que Murs Intelligents utilise seulement ses murs quand la distance de son path est plus longue que son adversaire .

Sinon pour le pourcentage de victoire de MiniMax Alpha Beta face au deux autres s'explique par son horizon (profondeur) initialisé à 3 pour question d'optimisation de temps CPU . Puisque MiniMax AlphaBeta est une stratégie qui parcourt l'ensemble des coups possibles limités par l'horizon . Il existe donc un seuil d'horizon k où MiniMax Alpha Beta voit assez de coups en avance pour ne pas se faire piéger par l'adversaire . Donc MiniMax Alpha Beta à une horizon k domine fortement les deux autres adversaires .