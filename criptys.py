import pygame
import sys
import random
import threading
import time
import numpy as np

pygame.init()

# Configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FRAME_HEIGHT = 630
PLAYER_PART_WIDTH = 500
BACKGROUND_COLOR = (255, 255, 255)  
COLOR_POSITIVE = (30, 132, 127)     
COLOR_NEGATIVE = (236, 193, 156)    

class GameView:
    def __init__(self, screen, x, y, width, height, num_columns):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.num_columns = num_columns
        self.surface = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.label_top_rect = pygame.Rect(x, y - 30, width, 30) 
        self.label_bottom_rect = pygame.Rect(x, y + height, width, 30)
        
    def draw_rectangles(self, data_top, msg_crypte):
        # Remplir le fond
        self.surface.fill(BACKGROUND_COLOR)
        
        # Calculer la valeur maximale
        max_value = max(abs(max(data_top, key=abs, default=0)), 
                        abs(max(msg_crypte, key=abs, default=0)))
        
        # Espacement et dimensions
        column_spacing = 10
        total_spacing = column_spacing * (self.num_columns + 1)
        column_width = (self.width - total_spacing) // self.num_columns
        
        # Espace central
        central_gap = 30
        available_height = (self.height - central_gap) // 2
        
        # Hauteur d'un rectangle unitaire
        if max_value > 0:
            rect_height = available_height // max_value
        else:
            rect_height = 10
        
        rect_spacing = 2
        
        # Dessiner les rectangles
        for i in range(self.num_columns):
            x = column_spacing + i * (column_width + column_spacing)
            
            # Rectangles du haut
            value_top = data_top[i]
            if value_top != 0:
                color_top = COLOR_POSITIVE if value_top > 0 else COLOR_NEGATIVE
                num_rects = abs(value_top)
                
                for j in range(num_rects):
                    y = j * (rect_height + rect_spacing)
                    pygame.draw.rect(self.surface, color_top, 
                                    (x, y, column_width, rect_height))
            
            # Rectangles du bas
            value_bottom = msg_crypte[i]
            if value_bottom != 0:
                color_bottom = COLOR_POSITIVE if value_bottom > 0 else COLOR_NEGATIVE
                num_rects = abs(value_bottom)
                
                for j in range(num_rects):
                    y = self.height - (j + 1) * (rect_height + rect_spacing)
                    pygame.draw.rect(self.surface, color_bottom, 
                                    (x, y, column_width, rect_height))
        
        # Dessiner la bordure
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, self.width, self.height), 2)
        
        # Blitter sur l'écran
        self.screen.blit(self.surface, (self.x, self.y))
    
    def draw_labels(self,  top_label, msg_crypte):
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, self.label_top_rect)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, self.label_bottom_rect)
        # Label du haut
        label_surface = self.font.render(top_label, True, (0, 0, 0))
        label_rect = label_surface.get_rect(center=(self.x + self.width // 2, self.y - 15))
        self.screen.blit(label_surface, label_rect)
        
        
        # Afficher les valeurs sous les colonnes
        column_spacing = 2
        total_spacing = column_spacing * (self.num_columns + 1)
        column_width = (self.width - total_spacing) // self.num_columns
        
        for i in range(self.num_columns):
            x = self.x + column_spacing + i * (column_width + column_spacing) + column_width // 2
            value_text = self.font.render(str(msg_crypte[i]), True, (0, 0, 0))
            value_rect = value_text.get_rect(center=(x, self.y + self.height + 15))
            self.screen.blit(value_text, value_rect)
            
            
    def fillscreen(self):
        self.surface.fill(BACKGROUND_COLOR)
        #self.screen.blit(self.surface, (self.x, self.y))
        
class PlayerModel:
    def __init__(self, nb_col,key_type, key_value, msg_crypte):
        self.num_columns = nb_col
        self.key_type=key_type
        self.key_value=key_value
        self.msg_crypte=msg_crypte
        
        if len(self.key_value) < self.num_columns:
            self.key_value.extend([0] * (self.num_columns - len(self.key_value)))
        if len(self.msg_crypte) < self.num_columns:
            self.msg_crypte.extend([0] * (self.num_columns - len(self.msg_crypte)))
    
    def add_key_to_crypted(self):
        self.msg_crypte = [a + b for a, b in zip(self.key_value, self.msg_crypte)]
    def inverse_key(self):
        self.key_value = [-a for a in self.key_value]
    def decal_droite(self):
        self.key_value = [self.key_value[-1]] + self.key_value[:-1]
    def decal_gauche(self):
        self.key_value = self.key_value[1:] + [self.key_value[0]]
    
    def verif_win(self):
        return  not(all(abs(x) in (0, 1) for x in self.msg_crypte))

    
class AiModel:
    def __init__(self, nb_col,key_type, key_value, msg_crypte):
        self.num_columns = nb_col
        self.key_type=key_type
        self.key_value=key_value
        self.msg_crypte=msg_crypte
        self.lock = threading.Lock()  
        
        if len(self.key_value) < self.num_columns:
            self.key_value.extend([0] * (self.num_columns - len(self.key_value)))
        if len(self.msg_crypte) < self.num_columns:
            self.msg_crypte.extend([0] * (self.num_columns - len(self.msg_crypte)))
    
    
    
    # les 4 actiosn qui correspondent aux fleches du joueur
    def add_key_to_crypted(self):
        with self.lock:
            self.msg_crypte = [a + b for a, b in zip(self.key_value, self.msg_crypte)]
    def inverse_key(self):
        with self.lock:
            self.key_value = [-a for a in self.key_value]
    def decal_droite(self):
        with self.lock:
            self.key_value = [self.key_value[-1]] + self.key_value[:-1]
    def decal_gauche(self):
        with self.lock:
            self.key_value = self.key_value[1:] + [self.key_value[0]]
            
    # vérification de la victoire    
    def verif_win(self):
        with self.lock:
            return  not(all(abs(x) in (0, 1) for x in self.msg_crypte))
        
    # calcule de la valeur de la combinaison actuelle pour trouver la meilleur actions possible
    def cal_val_som(self):
        with self.lock:
            return sum(abs(x+y)  for x,y in zip(self.msg_crypte,self.key_value )) 

    def cal_val_val(self):
        with self.lock:
            return [abs(x+y)  for x,y in zip(self.msg_crypte,self.key_value )]  
    
    # obtenir une copie de l'état actuel (clé et message crypté)
    def get_state_copy(self):      
        with self.lock:             
            return self.key_value.copy(), self.msg_crypte.copy()
    
    
class GameController:
    def __init__(self,view,model):
        self.game_view=view
        self.game_model=model

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.game_model.add_key_to_crypted()
                elif event.key == pygame.K_UP:
                    self.game_model.inverse_key()
                elif event.key == pygame.K_LEFT:
                    self.game_model.decal_gauche()
                elif event.key == pygame.K_RIGHT:
                    self.game_model.decal_droite()
                elif event.type == pygame.QUIT:  # Clic sur la croix
                    return False
        return True

    

    def render(self):
        self.game_view.fillscreen()
        #Pour jouer en static avec la clé public
        self.game_view.draw_rectangles(self.game_model.key_value,self.game_model.msg_crypte)
        self.game_view.draw_labels(self.game_model.key_type, self.game_model.msg_crypte )
        return self.game_model.verif_win()

class AiController:
    def __init__(self,view,model,ai_speed=0.5):
        self.ia_view=view
        self.ia_model=model
        self.nb_iter=0
        self.ai_speed = ai_speed  #Difficulté lié à la vitesse de l'ia
        self.running = False      
        self.thread = None  
        self.game_finished = False
    
    def ai_thread_loop(self):
        while self.running and not self.game_finished:
            if not self.ia_model.verif_win():
                self.game_finished = True
                break
            self.glouton_Action()


    def glouton_findbest(self):
        best_pos=0
        #best_combi=self.ia_model.key_value
        current_pos=0
        min_val=self.ia_model.cal_val_som()
        for _ in range(self.ia_model.num_columns):
            current_val=self.ia_model.cal_val_som()
            #pour test
            #print(self.ia_model.cal_val_som(), ' pos=',current_pos,' best_combi=',best_combi)
            if current_val < min_val:
                min_val = current_val
                #best_combi=self.ia_model.key_value
                best_pos=current_pos
            self.ia_model.inverse_key()
            self.actualiser()
            
            current_pos += 1
            
            current_val=self.ia_model.cal_val_som()
            #pour test
            #print(self.ia_model.cal_val_som(), ' pos=',current_pos,' best_combi=',best_combi)
            if current_val < min_val:
                min_val = current_val
                #best_combi=self.ia_model.key_value
                best_pos=current_pos
            self.ia_model.decal_droite()
            self.actualiser()
            
            current_pos += 1    
        return best_pos
    
    def start_ai(self):
        if self.thread is None or not self.thread.is_alive():
            self.running = True
            self.game_finished = False
            self.thread = threading.Thread(target=self.ai_thread_loop, daemon=True)
            self.thread.start()
        

    def stop_ai(self):
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=2.0)


    def glouton_Action(self):
        pos_cible=self.glouton_findbest()
        
        _=0
        #print('add  valcalc =',self.ia_model.cal_val_som(),'\n',self.ia_model.key_value,'\n', self.ia_model.msg_crypte )
        for _ in range(pos_cible):
            
            if _ % 2:
                self.ia_model.decal_droite()
                self.render()
                
            if not( _ % 2):
                self.ia_model.inverse_key()
                self.render()
                
                
        
        self.nb_iter+=1
        self.ia_model.add_key_to_crypted()   
        print(self.nb_iter)

    def random_action(self):
        action = random.randint(1, 4)
        match action:
            case 1:
                self.ia_model.add_key_to_crypted()
            case 2:
                self.ia_model.inverse_key()
            case 3:
                self.ia_model.decal_droite()
            case 4:
                self.ia_model.decal_gauche()

    def actualiser(self):
        self.ia_view.fillscreen()
        key_value, msg_crypte = self.ia_model.get_state_copy()
        self.ia_view.draw_rectangles(key_value,msg_crypte)
        self.ia_view.draw_labels(self.ia_model.key_type, msg_crypte )
        time.sleep(self.ai_speed)
        #self.random_action()
        return self.ia_model.verif_win()

    def render(self):
        self.ia_view.fillscreen()
        key_value, msg_crypte = self.ia_model.get_state_copy()
        self.ia_view.draw_rectangles(key_value,msg_crypte)
        self.ia_view.draw_labels(self.ia_model.key_type, msg_crypte )
        
        #self.random_action()
        return self.ia_model.verif_win()


####################################################
#### gestion du chiffrement du message et des clés 

#Convertit un entier non-négatif avec de s-1 0 et 1  sur 4 bits
def decimal_vers_ternaire_balance(n, width=4):
   
    if width <= 0:
        return []
    trits = [0] * width #allocation d'espace
    temp = n
    for i in range(width):
        reste = temp % 3 #le modulo 3 pour savoir si il rest 0 1 ou 2 
        temp = temp // 3
        # On interprète 0=0,1=1,2=-1
        if reste == 0:
            trits[i] = 0
        elif reste == 1:
            trits[i] = 1
        else:
            trits[i] = -1
    return trits

#Transormations d'un char e ndecimal puis ver des trits
def char_vers_ternaire(char, width=4):
    if char == ' ':
        index = 0
    elif char.isdigit():
        index = int(char) + 1        
    elif char.isalpha():
        index = ord(char.upper()) - ord('A') + 11  # 11 après les chiffres
    else:
        raise ValueError(f"Caractère non supporté: {char!r}")
    return decimal_vers_ternaire_balance(index, width)

def message_vers_trits(message, width=4):
    trits = []
    for char in message:
        trits.extend(char_vers_ternaire(char, width))
    return trits

#Les fonctions oppérateurs pour créer les clées 

def rotation_vecteur(vecteur, k):
    n = len(vecteur)
    if n == 0:
        return []
    k = k % n
    return vecteur[-k:] + vecteur[:-k] if k != 0 else vecteur.copy()

def multiplication_scalaire(coef, vecteur):
    return [coef * x for x in vecteur]

def addition_vecteurs(a, b):
    n = max(len(a), len(b))
    a2 = a + [0] * (n - len(a))
    b2 = b + [0] * (n - len(b))
    return [x + y for x, y in zip(a2, b2)]

#1 on cré la clé public avec 1 grande colonne et des petites
def generer_cle_privee(taille):
    if taille <= 0:
        return []
    # Rancome ^pour moettre la position de la grand colonne 
    position_grande = random.randint(0, taille - 1)
    cle = []
    for i in range(taille):
        if i == position_grande:
            cle.append(random.randint(8, 15))
        else:
            cle.append(random.randint(-2, 2))
    return cle

#2 clé privé --> combinaison de la clé privé 
def generer_cle_publique(cle_privee, nb_melanges=3):
    #on utilise la clé privé pour créer la clé publique en ajoutant aléatoirement et en tournant de vasosn aléatoire la clé pricé puis on l'ajoute
    taille = len(cle_privee)
    if taille == 0:
        return []
    cle_pub = [0] * taille
    for _ in range(nb_melanges):
        coef = random.randint(-2, 2)
        if coef == 0:
            coef = 1
        #randome du nombre de rotation
        rotation = random.randint(0, taille - 1)
        s_rotated = rotation_vecteur(cle_privee, rotation)
        terme = multiplication_scalaire(coef, s_rotated)
        cle_pub = addition_vecteurs(cle_pub, terme)
    return cle_pub


# --- Chiffrement ---------------------------------------------------------
# on chiffre le message avec la clé publique
def chiffrer_message(message_trits, cle_publique, nb_termes=None):
    taille = len(message_trits)
    if taille == 0:
        return []
            
    if nb_termes is None:
        nb_termes = random.randint(2, 3)
        
    #on utilise la clé public en ajoutant aléatoirement et en tournant de vasosn aléatoire la clé pricé puis on l'ajoute    
    # même principe que la clé publique
    ap = [0] * taille
    for _ in range(nb_termes):
        coef = random.randint(-1, 1)
        if coef == 0:
            coef = 1
        rotation = random.randint(0, taille - 1)
        p_rotated = rotation_vecteur(cle_publique, rotation)
        terme = multiplication_scalaire(coef, p_rotated)
        ap = addition_vecteurs(ap, terme)
        
        c = addition_vecteurs(ap, message_trits)
    #s'assurer de la bonne taille du mot
    return c[:taille]


#fonction qui traite toute les génarations de clé et de chiffrements  pour les renvoyer puis lancer le jeu
def generer_et_chiffrer(message, trit_width=4, nb_melanges=8, nb_termes_chiff=5):
    #On traduit le message ent trits
    message_trits = message_vers_trits(message, width=trit_width)
    taille = len(message_trits)
    # on génère les clés et on chiffre le message
    cle_privee = generer_cle_privee(taille)
    cle_publique = generer_cle_publique(cle_privee, nb_melanges=nb_melanges)
    chiffre = chiffrer_message(message_trits, cle_publique, nb_termes=nb_termes_chiff)
    return taille,cle_privee, cle_publique, chiffre




if __name__ == "__main__":
    #ON demande le message à chiffer puis à déchiffrer
    msg = input('Saisir le message à chiffrer : ').strip()
    num_columns,cle_prive,cle_public,msg_crypte=generer_et_chiffrer(msg, trit_width=4, nb_melanges=15, nb_termes_chiff=6)
    msg_crypte_joueur=msg_crypte
    msg_crypte_ia=msg_crypte
    #générer ailleur 
    #num_columns = 8
    #cle_prive = [-1, 1, 0, -1, 7, 0, 0, 0]
    #cle_public = [-1, 8, -1, 1, 0, -8, 2, -7]
    #msg_crypte_joueur = [-4,-9,8,12,-1,16,-10,7 ]
    #msg_crypte_ia = [-4,-9,8,12,-1,16,-10,7 ]
    
 
    #num_columns = 12 # --> 5 itérations
    #cle_prive =         [0,1,0,-1,0,0,-1,-1,15,2,1,-2]
    #cle_public =        [-6, 1, 16, -2, 13, 15,1,-4,26,34,7,-3]
    #msg_crypte_joueur = [-68,-20,-19,-51,-21,-42,-1,-54,-77,-33,-36,-68]
    #msg_crypte_ia =     [-68,-20,-19,-51,-21,-42,-1,-54,-77,-33,-36,-68]
     
    #création de la fenêtre
    global_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Projet Cryptis")
    global_screen.fill(BACKGROUND_COLOR)
    running = True
    clock = pygame.time.Clock()

    #On initialise nos vues models et controlleurs 
    #player_model=PlayerModel(num_columns,"Clé public", cle_public, msg_crypte_joueur)
    player_model=PlayerModel(num_columns,"Clé privé", cle_prive, msg_crypte_joueur)
    
    ai_model=AiModel(num_columns,"Clé publique", cle_public, msg_crypte_joueur)
    #ai_model=AiModel(num_columns,"Clé privé", cle_prive, msg_crypte_joueur)
    usr_part = GameView(global_screen, 20, 30, PLAYER_PART_WIDTH, FRAME_HEIGHT, num_columns)
    ai_part = GameView(global_screen, WINDOW_WIDTH - PLAYER_PART_WIDTH - 20, 30, 
                                PLAYER_PART_WIDTH, FRAME_HEIGHT, num_columns)
    player_ctrl = GameController(usr_part,player_model)    
    ai_ctrl =AiController(ai_part,ai_model)
    
    
    #on initialise une première fois les deux éléments (joueurs et IA) 
    player_ctrl.render()
    ai_ctrl.render()
    
    ai_ctrl.start_ai()
    
    #Boucle qui gère les actions du joueur et les éléments de l'ia 
    while running:
        #gérer les actions
        running = player_ctrl.handle_events()
        #ai_ctrl.glouton_Action()
        
        #vérifier les condirions de victoire
        ia_win=ai_ctrl.render()
        player_win=player_ctrl.render()
        
        running = ia_win and player_win and running
        clock.tick(60)
        pygame.display.flip()
    ai_ctrl.stop_ai()
    
    #pour que le joueru puisse finir aussi si l'ia à été trop rapide
    running = True    
    while running:
        running = player_ctrl.handle_events()
        player_win=player_ctrl.render()
        running =  player_win and running
        clock.tick(60)
        pygame.display.flip()    
    pygame.quit()
    sys.exit()
    
    #game = GameManager(8)
    #game.run()