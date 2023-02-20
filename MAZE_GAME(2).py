import pygame, sys
from pygame.math import Vector2 as vec
import random, time
import time
import PySimpleGUI as sg

# Screen settings
top_bottom_buffer = 50
width = (((10 * 3) + 1) * 10) + top_bottom_buffer  # FOR BUFFER TO BE ADDED
height = (21 * 10) + top_bottom_buffer
maze_width = width - top_bottom_buffer
maze_height = height - top_bottom_buffer

maze_width, maze_height = width - top_bottom_buffer, height - top_bottom_buffer
FPS = 60

# colour settings
white = (255, 255, 255)
RED = (208, 22, 22)
GREY = (107, 107, 107)
black = (0, 0, 0)
GREEN = (0, 255, 0)
player_colour = (0, 255, 0)
# font settings
start_text_size = 13
start_font = 'arial black'

# player settings
player_start_pos = vec(1, 2)
# enemy settings

# DECK EXAMPLE ,
"""
 A USER CAN ONLY HOLD BETWEEN 1-4 CARDS PER DECK, WHEN CLICKING 1-4, SELECT CORRESPONDING CARD, IF IT HAS NOT ALREADY BEEN ANSWERED,
 DO THIS BY APPENDING TO A LIST OF USED_CARDS
 OTHERWISE, INCREMENTALLY TAKE EACH CARD OF INDEXES
 E.G. GAME STARTS, ENEMY 1 HAS DECK[0] AND USER'S SELECTED CARD WILL SELECT THE CORRESPONDING INDEX, UPDATE THE CURRENT_CARD VARIABLE
"""

# -----------------------------
pygame.init()
vec = pygame.math.Vector2
lives = 100

# enemy class
class Enemy:
    def __init__(self, app, pos, number, type):
        self.app = app  # Ref to app
        self.grid_pos = pos  # Fetch pos
        self.pix_pos = self.get_pix_pos()
        self.number = number  # Fast or slow

        self.direction = vec(1, 0)  # Not moving
        self.enemy = type  # Ref to specific enemy

        self.colour = self.set_colour()
        self.personality = self.set_personality()
        self.speed = self.set_speed()

    def recall_enemies(self):
        self.app.e_one = []  # Set values to be empty to reinstate new coordinates for each enemy
        self.app.e_one_pos = []

        self.app.e_two = []
        self.app.e_two_pos = []

        self.app.e_three = []
        self.app.e_three_pos = []

        self.app.load()  # Recall vectors
        self.app.make_enemies()  # Draw up enemies


    def set_speed(self):
        speed = random.uniform(0.1,1.1)
        return speed




    def update_enemies(self, target):
        row_count = 31  # For text data
        col_count = 21

        enemy_type = str(target)
        fullChar = False  # Open file and store it into variable of item
        with open(r'C:\Users\Eimantas\Desktop\A Level CS Stuff\Project\MazeGame\Example\test.txt', 'r') as file:
            item = file.read()
        file.close()

        complete_string = ""
        for i in range(0, row_count * col_count - 1):  # For entire file, replace enemy by zero for empty cell
            if item[i] == enemy_type:
                complete_string += "0"
            else:
                complete_string += item[i]  # Otherwise keep
        # HAD TO BUG FIX THIS SINCE WALLS WERE BEING DELETED TOWARDS END
        print(len(complete_string), row_count * col_count - 1)
        while len(complete_string) != (len(item)):  # While size is not consistent with original data
            complete_string += "1"  # Add walls

        updated_enemies = ""
        if "NULL" not in self.app.playing_cards:  # If cards available, need to generate enemies
            found = False
            while found == False:
                position = random.randint(0, len(item))  # Generate new place for enemy
                print(position)
                if complete_string[position] == "0":
                    found = True
            for i in range(0, len(item)):  # For entire file, enter new location for enemy
                if i == position:
                    updated_enemies += enemy_type
                else:
                    updated_enemies += complete_string[i]  # Otherwise keep
        else:
            updated_enemies = complete_string  # No change

        with open(r'C:\Users\Eimantas\Desktop\A Level CS Stuff\Project\MazeGame\Example\test.txt', 'w') as file:
            file.write(updated_enemies)  # Write to file back and replace it
        file.close()

    def update(self):

        global lives
        if self.app.player.grid_pos != self.grid_pos:
            print("ACCESSING ONE",self.pix_pos)# If enemy is not touching player
            self.pix_pos += self.direction * self.speed   # Update current pixel position
            if self.time_to_move():
                print('ACCESSING TWO')# If needing to move an enemy
                self.move()  # Move
        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[  # Update grid pos
                                0] - top_bottom_buffer + self.app.cell_width // 2) // self.app.cell_width + 2  # Tracking enemy pos
        self.grid_pos[1] = (self.pix_pos[
                                1] - top_bottom_buffer + self.app.cell_height // 2) // self.app.cell_height + 2  # Tracking enemy pos
        if self.app.player.grid_pos == self.grid_pos:
            if self.enemy == 1:  # IF PLAYER TOUCHES ENEMY, THEN CHECK IF SELECTED CARD IS SAME AS ENEMY CARD
                if self.app.using_card == self.app.playing_cards[0]:  # If selected card is correct
                    print('COLLISION WITH ENEMY ONE')
                    print(self.app.playing_cards)  # Checking
                    self.app.playing_cards.pop(0)  # Matches with first card so get rid of it
                    self.app.cur_cards, self.app.playing_cards = self.app.update_cards(cur_cards=self.app.cur_cards,
                                                                                       playing_cards=self.app.playing_cards)
                    # Update current cards with new set and playing cards
                    self.app.e_one = []
                    self.update_enemies(target="3")  # Update enemies
                    self.recall_enemies()  # Refresh screen
                    self.app.using_card = []  # Now gone since it has been used
                else:
                    if lives == 0:
                        pygame.quit()
                        time.sleep(1)
                    else:
                     lives -= 1
            elif self.enemy == 2:
                if self.app.using_card == self.app.playing_cards[1]:
                    # self.remove_enemy(self.grid_pos)
                    self.app.playing_cards.pop(1)
                    self.app.cur_cards, self.app.playing_cards = self.app.update_cards(cur_cards=self.app.cur_cards,
                                                                                       playing_cards=self.app.playing_cards)
                    self.app.e_two = []
                    self.update_enemies(target="2")

                    self.recall_enemies()
                    self.app.using_card = []
                else:
                    if lives == 0:
                        pygame.quit()
                        time.sleep(1)
                    else:
                     lives -= 1
            elif self.enemy == 3:
                if self.app.using_card == self.app.playing_cards[2]:
                    # self.remove_enemy(self.grid_pos)
                    self.app.playing_cards.pop(2)
                    self.app.cur_cards, self.app.playing_cards = self.app.update_cards(cur_cards=self.app.cur_cards,
                                                                                       playing_cards=self.app.playing_cards)
                    self.app.e_three = []
                    self.update_enemies(target="4")

                    self.recall_enemies()
                    self.app.using_card = []
                else:
                    if lives == 0: # All lives lost, close game
                        pygame.quit()
                        time.sleep(1)
                    else:
                     lives -= 1

    def time_to_move(self):
        # If the direction the enemy needs to move is a vector within correct direction and contained in a grid
        if int(self.pix_pos.x + top_bottom_buffer // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_pos.y + top_bottom_buffer // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):  # moving on y axis
                return True
        return False  # If not centered in a grid position not a valid move

    def move(self):
        self.direction = self.get_path_direction()  # The direction is vector,
        # Find the way in which the enemy needs to be positioned to reach player

        # self.personality = "slow"
        # if self.personality == "random":
        # self.direction = self.get_random_direction()
        # if self.personality == "slow":
        #   print('Tre')
        #   self.direction = self.get_path_direction()
        # if self.personality == "speedy":

        # if self.personality == "scared":
        #     self.direction = self.get_path_direction()

    def get_path_direction(self):
        next_cell = self.find_next_cell_in_path()
        xdir = next_cell[0] - self.grid_pos[0]  # X-direction to which player moves across a row
        ydir = next_cell[1] - self.grid_pos[1]  # Y-direction to which a player moves across columns
        return vec(xdir, ydir)

    def find_next_cell_in_path(self):
        path = self.BFS(start=[int(self.grid_pos.x), int(self.grid_pos.y)],  # Start of on grid to x with y
                        target=[int(self.app.player.grid_pos.x),
                                int(self.app.player.grid_pos.y)])  # End of player position
        return path[1]

    def BFS(self, start, target):
        print('BFS accessed')
        grid = [[0 for x in range(31)] for x in range(22)] # Width , height
        for cell in self.app.walls:  # row , col
            if cell.x < 31 and cell.y < 22:  # col , row
                grid[int(cell.y)][int(cell.x)] = 1  # Y first, X second FOR A WALL
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0] # Check first item
            queue.remove(queue[0]) # FIFO Structure
            visited.append(current) # Must have already been visited
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # UP RIGHT DOWN LEFT FOR COORDINATES
                for neighbour in neighbours: # For neighbour as index in neighbours
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]): # If valid move to be contained in grid in X
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid[1]): # If valid in Y
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited: # NOT IN WALL APPEND TO QUEUE SINCE VALID
                                if grid[next_cell[1]][next_cell[0]] != 1:  # IF NEXT MOVE NOT EQUAL TO WALL
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
                                    # CURRENT AND NEXT MOVE FOR STEP IN STEP FOR SHORTEST PATH

        # BACKTRACK
        shortest = [target]
        while target != start:
            for step in path: # LOOK THROUGH THE PATH AND MOVE ENEMY WORKING BACKWARDS
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"]) # add at start

        return shortest # found shortest

    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1

            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break

        return vec(x_dir, y_dir)

    def set_personality(self):
        return "speedy"
        # if self.number == 0:
        #     return "speedy"
        # if self.number == 1:
        #     return "slow"
        # else:
        #     return "scared"

    def remove_enemy(self, grid):
        self.grid_pos = grid
        pygame.draw.rect(
            self.app.screen,
            white,
            (self.grid_pos[0] * self.app.cell_width + top_bottom_buffer // 2,
             self.grid_pos[1] * self.app.cell_height + top_bottom_buffer // 2, self.app.cell_width,
             self.app.cell_height))

    def draw(self):
        pygame.draw.rect(
            self.app.screen,
            self.colour,
            (self.grid_pos[0] * self.app.cell_width + top_bottom_buffer // 2,
             self.grid_pos[1] * self.app.cell_height + top_bottom_buffer // 2, self.app.cell_width,
             self.app.cell_height))
        if self.enemy == 1: # If first card, draw up question for same colour and repeat
            self.app.draw_text(  # Create text to be set on the background
                'Q1: %s' % (self.app.shorten_text(self.app.playing_cards[0][0] ) ) ,
                screen=self.app.screen,
                position=[76, top_bottom_buffer // 2 + maze_height + 1 ],
                size=8, colour=self.colour, font_name=start_font, center=False)
        if self.enemy == 2:
            self.app.draw_text(  # Create text to be set on the background
                'Q2: %s' % (self.app.shorten_text(self.app.playing_cards[1][0] ) ) ,
                screen=self.app.screen,
                position=[76, top_bottom_buffer // 2 + maze_height + 1 + 11],
                size=8, colour=self.colour, font_name=start_font, center=False)
        if self.enemy == 3:
            self.app.draw_text(  # Create text to be set on the background
                'Q3: %s' % (self.app.shorten_text(self.app.playing_cards[2][0] ) ) ,
                screen=self.app.screen,
                position=[76*3, top_bottom_buffer // 2 + maze_height + 1 ],
                size=8, colour=self.colour, font_name=start_font, center=False)
        self.app.draw_text(  # Create text to be set on the background
            'LIVES: %s' % (lives),
            screen=self.app.screen,
            position=[76 * 4, 1],
            size=8, colour=self.colour, font_name=start_font, center=False)


        # pygame.draw.circle(self.app.screen,self.colour,[int(self.pix_pos.x),int(self.pix_pos.y)],4)
        # pygame.draw.rect(self.app.screen,self.colour,[int(self.pix_pos.x),int(self.pix_pos.y),self.app.cell_width,self.app.cell_height])

    def get_pix_pos(self):
        return vec(
            (self.grid_pos.x * self.app.cell_width) + top_bottom_buffer // 2 + self.app.cell_width // 2,
            (self.grid_pos.y * self.app.cell_height) + top_bottom_buffer // 2 + self.app.cell_height // 2)
        print(self.grid_pos, self.pix_pos)

    def set_colour(self):
        r = random.randint(0,255)  # GET RANDOM COLOUR TO PREVENT PATTERN REPEATING
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return (r,g,b)
        # if self.enemy == 0:
        #     return (43, 78, 203)
        # elif self.enemy == 1:
        #     return (197, 200, 27)
        # if self.enemy == 2:
        #     return (189, 29, 29)
        # if self.enemy == 3:
        #     return (215, 159, 33)


# Player Class
class Player:
    def __init__(self, app, pos):
        self.app = app  # reference to app class
        self.grid_pos = pos  # position on grid
        # fluid movement, one at a time, fixes the player to grid
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, 0)  # Not moving
        self.stored_direction = None  # Declaration  varaiable for storing direction
        self.able_to_move = True  # Boolean to check if player can move
        self.speed = 1

        self.deck = [["Q1", "A1"], ["Q2", "A2"], ["Q3", "A3"], ["Q4", "A4"], ["Q5", "A5"], ["Q6", "A6"], ["Q7", "A7"]]
        self.cur_cards = []

        # self.shoot_pix_pos = self.pix_pos
        # self.shoot_grid_pos = pos
        # self.current_card = []
        # self.enemy_card = Deck[0]
        # print('enemy card', self.enemy_card)

    def current_card(self):
        # if card in available_cards:
        self.current_card = Deck[0]
        print('SELECTED CARD', self.current_card)

    def update(self):
        if self.able_to_move:  # If true
            self.pix_pos += self.direction * 1  # Add on current vector and update pixel position

        if self.time_to_move:
            if self.stored_direction != None:  # Keep track and update of previous
                self.direction = self.stored_direction

            self.able_to_move = self.can_move()  # Check if valid move
        # setting grid position to pix pos, which is player
        self.grid_pos[0] = int((self.pix_pos[
                                    0] - top_bottom_buffer + self.app.cell_width // 2) / self.app.cell_width + 1.7)  # Tracking user pos )
        self.grid_pos[1] = int((self.pix_pos[
                                    1] - top_bottom_buffer + self.app.cell_height // 2) / self.app.cell_height + 1.7)  # Tracking user pos)

        # / self.app.cell_width + 1.7 )#Tracking user pos

        # / self.app.cell_height + 1.7 )  # Tracking user pos

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:  # if hit wall from list in app class from which user will
                # go towards, stop beforehand
                return False
        return True

    def move(self, direction):
        self.direction = direction

    def time_to_move(self):
        if int(self.pix_pos.x + top_bottom_buffer // 2) % self.app.cell_width == 0:  # If within a grid of x
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True

        if int(self.pix_pos.y + top_bottom_buffer // 2) % self.app.cell_height == 0:  # If within grid on y
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):  # moving on y axis
                return True

    def get_pix_pos(self):
        return vec(
            (self.grid_pos.x * self.app.cell_width) + top_bottom_buffer // 2 + self.app.cell_width // 2,
            (self.grid_pos.y * self.app.cell_height) + top_bottom_buffer // 2 + self.app.cell_height // 2)

    def draw(self):
        pygame.draw.rect(  # Draw the player
            self.app.screen,  # Onto screen of app
            player_colour,  # Within player colour defined as a tuple
            (self.grid_pos[0] * self.app.cell_width + top_bottom_buffer // 2,
             self.grid_pos[1] * self.app.cell_height + top_bottom_buffer // 2, self.app.cell_width,
             self.app.cell_height))
        # The start x and y with how long they are, hence needing to keep track of grid position


# App class
class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))  # Create canvas of (width,height) from maze generated
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'  # To control state of game
        self.cell_width = 10  # maze_width // 51 #10 by 10 squares
        self.cell_height = 10  # maze_height // 76

        self.player = Player(self, player_start_pos)  # self passes a copy
        self.p_pos = None

        self.e_one = []  # Each enemy is a list to keep track of where each one specifically is
        self.e_one_pos = []  # Keep tracking one enemy one
        self.e_pos_two = []  # Keep tracking of enemy two ... etc
        self.e_two = []
        self.e_two = []
        self.e_two_pos = []
        self.e_three = []
        self.e_three_pos = []
        self.walls = []

        self.cur_cards, self.playing_cards = [["Q1", "A1"], ["Q2", "A2"], ["Q3", "A3"], ["Q4", "A4"], ["Q5", "A5"],
                                              ["Q6", "A6"], ["Q7", "A7"]], []
        # Create current cards that are available for taking
        # Playing cards are the set of three available to user for usage
        self.cur_cards, self.playing_cards = self.update_cards(cur_cards=self.cur_cards,
                                                               playing_cards=self.playing_cards)
        # Update current cards and the ones that can be used by player
        self.using_card = []  # Card which user selects to use

        self.load()
        self.make_enemies()



    def run(self):  # RUNS THE GAME
        while self.running:
            if self.state == 'start':  # If at start, load start screen items
                self.start_events()
                self.start_draw()
            elif self.state == 'playing':  # If declared to play load playing items
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            else:
                self.running = False  # If exits at any stage
            self.clock.tick(FPS)  # Update screen per FPS
        pygame.quit()  # If not running, then quit
        sys.exit()  # Quit

    # ---------------------------------------------HELPER FUNCTIONS---------------------------------------------

    def draw_text(self, words, screen, position, size, colour, font_name, center=False):  # displays text
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()  # tuple of width and height
        if center:
            position[0] = position[0] - text_size[0] // 2
            position[1] = position[1] - text_size[1] // 2
        screen.blit(text, position)

    def load(self):
        self.background = pygame.image.load(
            r'C:\Users\Eimantas\Desktop\A Level CS Stuff\Project\MazeGame\Example\myMaze.png')
        self.background = pygame.transform.scale(self.background, (maze_width, maze_height))
        # opening map file and creating the walls list with coords of walls
        with open(r'C:\Users\Eimantas\Desktop\A Level CS Stuff\Project\MazeGame\Example\test.txt', 'r') as file:
            for yidx, line in enumerate(
                    file):  # line is y-index, enumerate stores account of which line is which, e.g. first line is 0
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    if char == "3":
                        self.e_one_pos.append(vec(xidx, yidx))
                    if char == "2":
                        self.e_two_pos.append(vec(xidx, yidx))
                    if char == "4":
                        self.e_three_pos.append(vec(xidx, yidx))

    def update_cards(self, cur_cards, playing_cards):
        # self.deck = [["Q1", "A1"], ["Q2", "A2"], ["Q3", "A3"], ["Q4", "A4"], ["Q5", "A5"], ["Q6", "A6"], ["Q7", "A7"]]
        i = 0  # Start at zero
        while i <= len(cur_cards) and len(playing_cards) != 3:
            # While the playing cards are not three and items to be checked is within the list of available cards
            playing_cards.append(cur_cards[i])
            i += 1
        cur_cards_copy = []  # Copy to update cards
        for x in range(i, len(cur_cards)):
            cur_cards_copy.append(cur_cards[x])  # Keep only ones not used for playing
        while len(playing_cards) < 3:  # If all used, substitute by adding in null values
            playing_cards.append(['NULL','NULL'])


        return cur_cards_copy, playing_cards

    def make_enemies(self):
        for idx, pos in enumerate(self.e_one_pos):  # For every item in list
            self.e_one.append(Enemy(self, pos, idx, type=1))  # Enemy one, so type is 1

        for idx, pos in enumerate(self.e_two_pos):
            self.e_two.append(Enemy(self, pos, idx, type=2))  # Repeat...

        for idx, pos in enumerate(self.e_three_pos):
            self.e_three.append(Enemy(self, pos, idx, type=3))

    def draw_grid(self):
        pass
        # for wall in self.walls:
        #     pygame.draw.rect(self.background,
        #                      (112,55,163),
        #                      (wall.x*self.cell_width,
        #                       wall.y*self.cell_height,
        #                       self.cell_width,
        #                       self.cell_height)
        #                      )

    # ----------------------------------------------INTRO FUNCTIONS---------------------------------
    def start_events(self):
        for event in pygame.event.get():  # Cycling to keep track of events
            if event.type == pygame.QUIT:  # If user quits
                self.running = False  # Stop game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'  # If presses spacebar start game

    def start_draw(self):
        self.screen.fill(black)  # Black background
        self.draw_text(  # Draw the text onto screen variable in centre with blue colour
            "SPACEBAR TO BEGIN", self.screen, [width // 2, height // 2], start_text_size, (0, 0, 155), start_font,
            center=True)
        self.draw_text(  # Draw text again
            "ONE PLAYER ONLY", self.screen, [width // 2, height // 2 + 25], start_text_size, (170, 132, 58), start_font,
            center=True)
        self.draw_text(
            "HIGHSCORE: ", self.screen, [2, 2], start_text_size, (170, 132, 58), start_font, center=False)
        pygame.display.update()  # Update screen so it is visible

    # ----------------------------------------------PLAYING FUNCTIONS---------------------------------
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:  # If key held down, check which key has been pressed
                if event.key == pygame.K_LEFT:  # Move the user within that direction given
                    self.player.move(vec(-1, 0))
                    # self.player.shoot_vec = vec(-1,0)
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                    # self.player.shoot_vec = vec(1, 0)
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                    # self.player.shoot_vec = vec(0, -1)
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))
                    # self.player.shoot_vec = vec(0, 1)

                if event.key == pygame.K_1:  # If user selects to pick card one
                    self.using_card = self.playing_cards[0]
                    print('selected card 1')
                if event.key == pygame.K_2:
                    self.using_card = self.playing_cards[1]
                    print('selected card 2')
                if event.key == pygame.K_3:
                    self.using_card = self.playing_cards[2]
                    print('selected card 3')

                if event.key == pygame.K_a:
                    self.e_one = []
                    self.e_one_pos = []

                    self.e_two = []
                    self.e_two_pos = []

                    self.e_three = []
                    self.e_three_pos = []
                    self.load()
                    self.make_enemies()

            # #Only move if player holds down key
            # elif event.type == pygame.KEYUP: #If key released, stop player
            #     if event.key == pygame.K_LEFT:
            #         self.player.move(vec(0,0) )
            #     if event.key == pygame.K_RIGHT:
            #         self.player.move(vec(0, 0))
            #     if event.key == pygame.K_UP:
            #         self.player.move(vec(0, 0))
            #     if event.key == pygame.K_DOWN:
            #         self.player.move(vec(0, 0))

    def playing_update(self):
        self.player.update()
        for enemy in self.e_one:
            enemy.update()
        for enemy in self.e_two:
            enemy.update()
        for enemy in self.e_three:
            enemy.update()

    def shorten_text(self,text):
        if len(text) > 25:
            copy = ""
            for i in range(0,25):
                copy += str(text)
        else:
            return  text
        return copy

    def playing_draw(self):
        self.screen.fill(GREY)  # Background of grey colour
        self.screen.blit(self.background, (top_bottom_buffer // 2, top_bottom_buffer // 2))  # Map to screen
        # # self.draw_grid()
        # self.draw_text(  # Create text to be set on the background
        #     'CURRENT SCORE:0',
        #     screen=self.screen,
        #     position=[5, 1],
        #     size=12, colour=black, font_name=start_font, center=False)
        # self.draw_text(
        #     'HIGH SCORE:0',
        #     screen=self.screen,
        #     position=[width // 2, 1],
        #     size=12, colour=black, font_name=start_font, center=False)
        self.draw_text(  # Create text to be set on the background
            'QUESTIONS:',
            screen=self.screen,
            position=[5, 1],
            size=8, colour=black, font_name=start_font, center=False)
        self.draw_text(  # Create text to be set on the background
            'CARD1: %s' % (self.shorten_text( self.playing_cards[0][1]) ),
            screen=self.screen,
            position=[76, 1],
            size=8, colour=black, font_name=start_font, center=False)
        self.draw_text(
            'CARD2: %s' % (self.shorten_text( self.playing_cards[1][1] ) ),
            screen=self.screen,
            position=[76, 11],
            size=8, colour=black, font_name=start_font, center=False)
        self.draw_text(  # Create text to be set on the background
            'CARD3: %s' % (self.shorten_text(self.playing_cards[2][1] ) ),
            screen=self.screen,
            position=[76*3, 1],
            size=8, colour=black, font_name=start_font, center=False)




        self.player.draw()

        for enemy in self.e_one:  # Re draw each enemy to grid values
            enemy.draw()
        for enemy in self.e_two:
            enemy.draw()
        for enemy in self.e_three:
            enemy.draw()
        # for shoot in self.shoot:

        pygame.display.update()


if __name__ == "__main__":
    app = App()
    app.run()

# Row count 76
# Col count 51
