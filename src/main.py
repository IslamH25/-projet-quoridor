# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
from itertools import chain
import math

#petit message

import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme








# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'mini-quoridorMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 60  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    # #for arg in sys.argv:
    # iterations = 100 # default
    # if len(sys.argv) == 2:
    #     iterations = int(sys.argv[1])
    # print ("Iterations: ")
    # print (iterations)

    init()
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize
    assert nbLignes == nbCols # a priori on souhaite un plateau carre
    lMin=2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les murs)
    lMax=nbLignes-2 
    cMin=2
    cMax=nbCols-2
    g =np.ones((nbLignes,nbCols),dtype=bool)  # une matrice remplie par defaut a True  
   
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
       
           
    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players]
    ligneObjectif = (initStates[1][0],initStates[0][0]) # chaque joueur cherche a atteindre la ligne ou est place l'autre 
    print(ligneObjectif)
    
    
    # on localise tous les murs
    # sur le layer ramassable    
    walls = [[],[]]
    walls[0] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == 0 or o.get_rowcol()[0] == 1)]  
    walls[1] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == nbLignes-2 or o.get_rowcol()[0] == nbLignes-1)]  
    allWalls = walls[0]+walls[1]
    nbWalls = len(walls[0])
    assert len(walls[0])==len(walls[1]) # les 2 joueurs doivent avoir le mm nombre de murs
    
    #-------------------------------
    # Fonctions permettant de récupérer les listes des coordonnées
    # d'un ensemble d'objets murs ou joueurs
    #-------------------------------
    
    def wallStates(walls): 
        # donne la liste des coordonnees dez murs
        return [w.get_rowcol() for w in walls]
    
    def playerStates(players):
        # donne la liste des coordonnees dez joueurs
        return [p.get_rowcol() for p in players]
    
   
    #-------------------------------
    # Rapport de ce qui est trouve sut la carte
    #-------------------------------
    print("lecture carte")
    print("-------------------------------------------")
    print("lignes", nbLignes)
    print("colonnes", nbCols)
    print("Trouvé ", nbPlayers, " joueurs avec ", int(nbWalls/2), " murs chacun" )
    print ("Init states:", initStates)
    print("-------------------------------------------")

    #-------------------------------
    # Carte demo 
    # 2 joueurs 
    # Joueur 0: place au hasard
    # Joueur 1: A*
    #-------------------------------
    
        
    #-------------------------------
    # On choisit une case objectif au hasard pour chaque joueur
    #-------------------------------
    
    allObjectifs = ([(ligneObjectif[0],i) for i in range(cMin,cMax)],[(ligneObjectif[1],i) for i in range(cMin,cMax)])
    print("Tous les objectifs joueur 0", allObjectifs[0])
    print("Tous les objectifs joueur 1", allObjectifs[1])
    objectifs =  (allObjectifs[0][random.randint(cMin,cMax-3)], allObjectifs[1][random.randint(cMin,cMax-3)])
    print("Objectif joueur 0 choisi au hasard", objectifs[0])
    print("Objectif joueur 1 choisi au hasard", objectifs[1])

    #-------------------------------
    # Fonctions definissant les positions legales et placement de mur aléatoire
    #-------------------------------
    
    def legal_wall_position(pos):
        row,col = pos
        # une position legale est dans la carte et pas sur un mur deja pose ni sur un joueur
        # attention: pas de test ici qu'il reste un chemin vers l'objectif
        return ((pos not in wallStates(allWalls)) and (pos not in playerStates(players)) and row>lMin and row<lMax-1 and col>=cMin and col<cMax)
    
    def draw_random_wall_location():
        # tire au hasard un couple de position permettant de placer un mur
        while True:
            random_loc = (random.randint(lMin,lMax),random.randint(cMin,cMax))
            if legal_wall_position(random_loc):  
                inc_pos =[(0,1),(0,-1),(1,0),(-1,0)] 
                random.shuffle(inc_pos)
                for w in inc_pos:
                    random_loc_bis = (random_loc[0] + w[0],random_loc[1]+w[1])
                    if legal_wall_position(random_loc_bis):
                        return(random_loc,random_loc_bis)

    def remaining_walls(player):
        if(player==0):
            return len(walls[player])-murs[0]
        else:
            return len(walls[player])-murs[1]
        
    def wall_notblock(x1,y1,x2,y2):
        if(legal_wall_position((x1,y1)) and legal_wall_position((x2,y2))):
            g[x1][y1] = False
            g[x2][y2] = False
            #calcule A* de nouveau pour les 2 joueurs
            path[0] = calculPath(0)
            path[1] = calculPath(1)
            if path[0][len(path[0])-1] != objectifs[0] or path[1][len(path[1])-1] != objectifs[1] :
                g[x1][y1] = True
                g[x2][y2] = True
                return False
            else:
                g[x1][y1] = True
                g[x2][y2] = True
                return True
        return False

    def eval(player):
        p[0] = ProblemeGrid2D(players[0].get_rowcol(),objectifs[0],g,'manhattan')
        p[1] = ProblemeGrid2D(players[1].get_rowcol(),objectifs[1],g,'manhattan')
        path[0] = probleme.astar(p[0],verbose=False)
        path[1] = probleme.astar(p[1],verbose=False)
        distance = []
        distance.append(len(path[0]))
        distance.append(len(path[1]))
        return distance[player] - distance[abs(player-1)]

    def h(player):
        return eval(player)

    def get_possible_moves(player):
        moves={}
        # l=[]
        j=0
        if(player==players[0]):
            i=0
        else:
            i=1
        if(remaining_walls(i)>0):
            for x in range(lMin,lMax):
                for y in range(cMin,cMax):
                    if legal_wall_position((x,y)):  
                        inc_pos =[(0,1),(-1,0)] 
                        for w in inc_pos:
                            x1,y1 = (x + w[0],y+w[1])
                            if legal_wall_position((x1,y1)):
                                if(wall_notblock(x,y,x1,y1)):
                                    moves['W'+str(j)]=(x,y),(x1,y1)
                                    j+=1
        return moves

    def calculPath(player):
        
        p[player] = ProblemeGrid2D(players[player].get_rowcol(),objectifs[player],g,'manhattan')
        return probleme.astar(p[player],verbose=False)

    def finDePartieSiGagne(player):
        row,_ = players[player].get_rowcol()
        if row == ligneObjectif[player]:
            print("le joueur ",player," a atteint son but!")
            pygame.quit()
            exit(player)





        

    #-------------------------------
    # Mettre les bordures du plateaux à False 
    #------------------------------- 

    for i in range(nbLignes):                 # on exclut aussi les bordures du plateau
        g[0][i]=False
        g[1][i]=False
        g[nbLignes-1][i]=False
        g[nbLignes-2][i]=False
        g[i][0]=False
        g[i][1]=False
        g[i][nbLignes-1]=False
        g[i][nbLignes-2]=False

    ################################
    # Les Stratégies 
    ################################

    #-------------------------------
    # Stratégie - Aleatoire
    #-------------------------------

    def StrategieAlea(player):
        tours[player] += 1
        
        hasard = random.randint(0,1)

        if(hasard==0 and remaining_walls(player)):
            
            while True :
                ((x1,y1),(x2,y2)) = draw_random_wall_location()

                if(wall_notblock(x1,y1,x2,y2)):
                    g[x1][y1] = False
                    g[x2][y2] = False
                    walls[player][murs[player]].set_rowcol(x1,y1)
                    walls[player][murs[player]+1].set_rowcol(x2,y2)
                    # incrémente nb murs utilis
                    murs[player] += 2
                    print(player," ",murs[player])
                    game.mainiteration()
                    
                    path[0] = calculPath(0)
                    path[1] = calculPath(1)
                    break
                else:
                    continue
        else :
            print(path)
            path[player].pop(0)
            row, col = path[player][0]
            posPlayers[player]=(row, col)
            players[player].set_rowcol(row,col)
            print ("pos joueur ",player,":", row,col)
            finDePartieSiGagne(player)
            # mise à jour du pleateau de jeu
            game.mainiteration()

    #-------------------------------
    # Stratégie - Murs d'abord
    #-------------------------------

    def StrategieWallsFirst(player):

        if(remaining_walls(player)):
            chemin_adverse = path[abs(player-1)]
            d = []
            for x,y in chemin_adverse:
                for dx,dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                    if(wall_notblock(x,y,x+dx,y+dy)):
                        g[x][y] = False
                        g[x+dx][y+dy] = False

                        path[0] = calculPath(0)
                        path[1] = calculPath(1)

                        d.append( [((x,y),(x+dx,y+dy)) , len(path[abs(player-1)]) - len(path[player])])

                        g[x][y] = True
                        g[x+dx][y+dy] = True

                    else:
                        continue
            
            if len(d) == 0 :
                while(True):
                    print("bug ici?")
                    (x1,y1),(x2,y2)=draw_random_wall_location()
                    if(wall_notblock(x1,y1,x1,y2)):
                        break
                g[x1][y1] = False
                g[x2][y2] = False
                walls[player][murs[player]].set_rowcol(x1,y1)
                walls[player][murs[player]+1].set_rowcol(x2,y2)
                path[0] = calculPath(0)
                path[1] = calculPath(1)
                # incrémente nb murs utilis
                murs[player] += 2
                print(player," ",murs[player])
                game.mainiteration()
            else :
                max = -10
                m = []
                m.append(d[0][0])
                for move, dist in d :
                    if dist > max :
                        m = []
                        m.append(move)
                        max = dist 
                    if dist == max :
                        m.append(move)

                mu = m[random.randint(0,len(m)-1)]
                     
                
                ((x1,y1),(x2,y2)) = mu
                g[x1][y1] = False
                g[x2][y2] = False
                walls[player][murs[player]].set_rowcol(x1,y1)
                walls[player][murs[player]+1].set_rowcol(x2,y2)
                path[0] = calculPath(0)
                path[1] = calculPath(1)
                # incrémente nb murs utilis
                murs[player] += 2
                print(player," ",murs[player])
                game.mainiteration()
        
        else : 
            path[player] = calculPath(player)
            path[player].pop(0)
            row, col = path[player][0]
            posPlayers[player]=(row, col)
            players[player].set_rowcol(row,col)
            print ("pos joueur ",player,":", row,col)
            finDePartieSiGagne(player)
            # mise à jour du pleateau de jeu
            game.mainiteration()


    #-------------------------------
    # Stratégie - Murs Intelligents 
    #-------------------------------

    def StrategieMursIntelligent(player):

        distance = len(path[player])
        distance_adverse = len(path[abs(player-1)])

        if(distance_adverse <= distance and remaining_walls(player)):
            chemin_adverse = path[abs(player-1)]
            d = []
            for x,y in chemin_adverse:
                for dx,dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                    if(wall_notblock(x,y,x+dx,y+dy)):
                        g[x][y] = False
                        g[x+dx][y+dy] = False

                        path[0] = calculPath(0)
                        path[1] = calculPath(1)

                        d.append( [((x,y),(x+dx,y+dy)) , len(path[abs(player-1)]) - len(path[player])])

                        g[x][y] = True
                        g[x+dx][y+dy] = True

                    else:
                        continue
            
            if len(d) == 0 :
                path[player] = calculPath(player)
                path[player].pop(0)
                row, col = path[player][0]
                posPlayers[player]=(row, col)
                players[player].set_rowcol(row,col)
                print ("pos joueur ",player,":", row,col)
                finDePartieSiGagne(player)
                # mise à jour du pleateau de jeu
                game.mainiteration()
            else :
                max = -10
                m = []
                m.append(d[0][0])
                for move, dist in d :
                    if dist > max :
                        m = []
                        m.append(move)
                        max = dist 
                    if dist == max :
                        m.append(move)

                mu = m[random.randint(0,len(m)-1)]
                     
                
                ((x1,y1),(x2,y2)) = mu
                g[x1][y1] = False
                g[x2][y2] = False
                walls[player][murs[player]].set_rowcol(x1,y1)
                walls[player][murs[player]+1].set_rowcol(x2,y2)
                
                
                path[0] = calculPath(0)
                path[1] = calculPath(1)
                # incrémente nb murs utilis
                murs[player] += 2
                print(player," ",murs[player])
                game.mainiteration()
        
        else : 
            path[player] = calculPath(player)
            path[player].pop(0)
            row, col = path[player][0]
            posPlayers[player]=(row, col)
            players[player].set_rowcol(row,col)
            print ("pos joueur ",player,":", row,col)
            finDePartieSiGagne(player)
            # mise à jour du pleateau de jeu
            game.mainiteration()

    #-------------------------------
    # MinMax 
    #-------------------------------

    def minimax_strategy(player):
        _, move = minimax_ab(player, players[player].get_rowcol(), 3, -math.inf, math.inf, True)
        print(move,"le mouvement choisi")
        if move[0] == "depl":
            posPlayers[player]= move[1]
            (row, col) = move[1]
            players[player].set_rowcol(row,col)
            print ("pos joueur ",player,":", row,col)
            finDePartieSiGagne(player)
            print ("pos joueur ",player,":", move[1])
        else : 
            ((x1,y1),(x2,y2)) = move[1] 
            walls[player][murs[player]].set_rowcol(x1,y1)
            walls[player][murs[player]+1].set_rowcol(x2,y2)
            # incrémente nb murs utilisés 
            g[x1][y1] = False
            g[x2][y2] = False
            murs[player] += 2
            
            path[0] = calculPath(0)
            path[1] = calculPath(1)
        
        game.mainiteration()



    def minimax_ab(player,state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state == objectifs[player]:
            return h(player) , None
        if maximizing_player:
            max_eval = -math.inf
            best_move = None

            ### Path A* 
            p[player] = ProblemeGrid2D(state,objectifs[player],g,'manhattan')
            path[player] = probleme.astar(p[player],verbose=False)
            row,col=path[player][1]
            players[player].set_rowcol(row,col)
            score, _=minimax_ab(abs(player-1), players[abs(player-1)].get_rowcol() , depth-1, alpha, beta , False)
            row_initial,col_initial= state 
            players[player].set_rowcol(row_initial,col_initial)
            if max_eval < score:
                max_eval = score
                best_move = ["depl", (row,col)]
            ### Murs
            for move in get_possible_moves(player).values():

                ((x1,y1),(x2,y2)) = move 
                g[x1][y1] = False
                g[x2][y2] = False

                # incrémente nb murs utilisés 
                murs[player] += 2

                eval, _ = minimax_ab(abs(player-1),players[abs(player-1)].get_rowcol(), depth-1, alpha, beta, False)

                g[x1][y1] = True
                g[x2][y2] = True

                # incrémente nb murs utilisés 
                murs[player] -= 2
                
                if eval > max_eval:
                    print(best_move," MAX")
                    max_eval = eval
                    best_move = ["mur", ((x1,y1),(x2,y2))]
                alpha = max(alpha, eval)
                if beta <= alpha:
                    print("ALPHA MAX ###############################")
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None

            p[player] = ProblemeGrid2D(state,objectifs[player],g,'manhattan')
            path[player] = probleme.astar(p[player],verbose=False)
            row,col=path[player][1]
            players[player].set_rowcol(row,col)
            score,_=minimax_ab(abs(player-1), players[abs(player-1)].get_rowcol() , depth-1, alpha, beta , True)
            row_initial,col_initial= state 
            players[player].set_rowcol(row_initial,col_initial)
            if min_eval > score:
                min_eval = score
                best_move = ["depl", (row,col)]

            for move in get_possible_moves(player).values():
                
                ((x1,y1),(x2,y2)) = move 
                g[x1][y1] = False
                g[x2][y2] = False

                # incrémente nb murs utilisés 
                murs[player] += 2

                eval, _ = minimax_ab(abs(player-1),players[abs(player-1)].get_rowcol(), depth-1, alpha, beta, True)

                g[x1][y1] = True
                g[x2][y2] = True

                # incrémente nb murs utilisés 
                murs[player] -= 2

                if eval < min_eval:
                    print(best_move," MIN")
                    min_eval = eval
                    best_move = ["mur", ((x1,y1),(x2,y2))]
                beta = min(beta, eval)
                if beta <= alpha:
                    print("BETA MIN #########################")
                    break
            return min_eval, best_move
    
    
    #-------------------------------
    # Menu
    #-------------------------------
    # Initialisation des variables 
    #nombre de murs utilisés par les joueurs
    murs = [0, 0]

    posPlayers = initStates

    #calcule A* de nouveau pour les 2 joueurs
    p = []
    p.append(ProblemeGrid2D(players[0].get_rowcol(),objectifs[0],g,'manhattan'))
    p.append(ProblemeGrid2D(players[1].get_rowcol(),objectifs[1],g,'manhattan'))
    path = []
    path.append(probleme.astar(p[0],verbose=False))
    path.append(probleme.astar(p[1],verbose=False))

    tours = [0, 0]

    print("Stratégies : ")
    print("0 : Aléatoire ")
    print("1 : Alterner")
    print("2 : Bloquer le chemin ")
    print("3 : MiniMax alpha beta a*")


    stratj0 = (int)(sys.argv[1])
    stratj1 = (int)(sys.argv[2])
    
    # stratj0 = (int)(input("Choississez la stratégie du joueur 0\n"))
    # stratj1 = (int)(input("Choississez la stratégie du joueur 1\n"))
    while(True):
        match stratj0 :
            case 0:
                print("joueur 0 Alea")
                StrategieAlea(0)
            case 1:
                print("joueur 0 Walls First")
                StrategieWallsFirst(0)
            case 2:
                print("joueur 0 Murs Intelligent")
                StrategieMursIntelligent(0)
            case 3:
                print("joueur 0 MiniMax Alpha Beta")
                minimax_strategy(0)
        match stratj1 :
            case 0:
                print("joueur 1 Alea")
                StrategieAlea(1)
            case 1:
                print("joueur 1 Walls First")
                StrategieWallsFirst(1)
            case 2:
                print("joueur 1 Murs Intelligent")
                StrategieMursIntelligent(1)
            case 3:
                print("joueur 1 MiniMax Alpha Beta")
                minimax_strategy(1)

    

if __name__ == '__main__':
    main()
    


