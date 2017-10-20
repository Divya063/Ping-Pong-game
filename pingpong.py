import simplegui
import random
import math

#pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
PAD_WIDTH = 8
PAD_HEIGHT = 80
paddle1_pos = paddle2_pos = HEIGHT/2
paddle_vel = 6 # this is the speed that the paddles move at
paddle1_vel = paddle2_vel = 0
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
DIFFICULTY = 1.1
rally=0
score = [0,0]

#settings
p1_up = simplegui.KEY_MAP['w']
p1_down = simplegui.KEY_MAP['s']
p2_up = simplegui.KEY_MAP['up']
p2_down = simplegui.KEY_MAP['down']

#computer player on or not
computer_on = False
class ball:
    # the ball class needs the initial position to initialise
    def __init__(self,x_pos,y_pos, l_r):
        self.pos = [x_pos, y_pos]
        self.vel = [0,0]
        if l_r == 'RIGHT':
            self.vel[0] = random.randrange(2,4)
        elif l_r == 'LEFT':
            self.vel[0] = -random.randrange(2,4)
        else:
            self.vel [0] = random.choice([-1,1]) * random.randrange(2,4)
        self.vel[1] = -random.randrange(1,3)
        self.colour = 'White'
        self.radius = 20
        print 'Used'
    
    def __init__(self,x_pos,y_pos):
        self.pos = [x_pos, y_pos]
        self.vel = [0,0]
        self.vel [0] = random.choice([-1,1]) * random.randrange(2,4)
        self.vel[1] = -random.randrange(1,3)
        self.colour = 'White'
        self.radius = 20
    
    def reset(self,l_r):
        global rally
        self.pos = [WIDTH/2,HEIGHT/2]
        if l_r == 'RIGHT':
            self.vel[0] = random.randrange(2,4)
        elif l_r == 'LEFT':
            self.vel[0] = -random.randrange(2,4)
        else:
            self.vel [0] = random.choice([-1,1]) * random.randrange(2,4)
        self.vel[1] = -random.randrange(1,3)
        self.colour = 'White'
        rally = 0
        
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.colour = 'White'
    
    def get_pos(self):
        return self.pos
        
    def set_pos(self,a):
        self.pos = a
        
    def get_vel(self):
        return self.vel
            
    def set_vel(self,a):
        self.vel = a
            
    def get_colour(self):
        return self.colour
        
    def set_colour(self,colour):
        self.colour = colour
        
    def draw(self,canvas):
        canvas.draw_circle(self.pos,self.radius,1,self.colour,self.colour)
     
    def bounce_wall(self):
        self.vel[0] = -self.vel[0]*DIFFICULTY
        self.colour = 'Red'
    
    def bounce_vert(self):
        self.vel[1] = -self.vel[1]
        self.colour='Red'
    
    def check_collision(self):
        global rally, score
        
        #which side the ball is on
        player_side = int(self.pos[0]//(WIDTH/2))
        if player_side:
            paddle_pos = paddle2_pos
            side = 'LEFT'
            other_player = 0
        else:
            paddle_pos = paddle1_pos
            side = 'RIGHT'
            other_player =1
            
        if not((self.pos[0] > PAD_WIDTH + self.radius) and (self.pos[0]< WIDTH - PAD_WIDTH - self.radius)):
            #ball not in play area, has hit a side
            if (self.pos[1] >= paddle_pos - HALF_PAD_HEIGHT) and (self.pos[1] <= paddle_pos + HALF_PAD_HEIGHT):
                #hit the paddle
                self.bounce_wall()
                rally +=1
            else:
                self.reset(side)
                score[other_player] += 1
                
        if (self.pos[1] <= self.radius or self.pos[1] >= HEIGHT - self.radius):
            #collision with floor/ceiling
            self.bounce_vert()
    
    def get_speed(self):
        return int(math.sqrt(self.vel[0]**2 + self.vel[1]**2))
            
def paddle_maker(paddle_pos,left_right):
    #left_right is either 0 or 1
    return [[left_right * (WIDTH - PAD_WIDTH),paddle_pos - HALF_PAD_HEIGHT],[PAD_WIDTH+ left_right * (WIDTH - PAD_WIDTH),paddle_pos - HALF_PAD_HEIGHT],[PAD_WIDTH+ left_right * (WIDTH - PAD_WIDTH),paddle_pos + HALF_PAD_HEIGHT],[left_right * (WIDTH - PAD_WIDTH),paddle_pos + HALF_PAD_HEIGHT]]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, DIFFICULTY  # these are numbers
    global score, ball1  # these are ints
    ball1 = ball(WIDTH/2,HEIGHT/2)
    score = [0,0]
    DIFFICULTY = 1.1
    label_difficulty.set_text('Difficulty: '+str(int(DIFFICULTY*10 - 10)))

def draw(canvas):
    global score, paddle1_pos, paddle2_pos, rally, paddle1_vel, paddle2_vel, ball_pos, ball_vel, ball_colour
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball1.update()
    
    ball1.check_collision()
        
    # draw ball
    ball1.draw(canvas)
   
    #check if computer is playing
    if computer_on:
        computer_p1()
        canvas.draw_text('Computer',[WIDTH/7, 100],40,'Grey')
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos <= HALF_PAD_HEIGHT and paddle1_vel <0:
        paddle1_vel = 0
    elif paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT and paddle1_vel>0:
        paddle1_vel = 0
    if paddle2_pos <= HALF_PAD_HEIGHT and paddle2_vel <0:
        paddle2_vel = 0
    elif paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT and paddle2_vel>0:
        paddle2_vel = 0
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_polygon(paddle_maker(paddle1_pos,0),1,'White','White')
    canvas.draw_polygon(paddle_maker(paddle2_pos,1),1,'White','White')
    
    # draw scores
    canvas.draw_text(str(score[0]),[WIDTH/3 - 30, 50],60,'White')
    canvas.draw_text(str(score[1]),[WIDTH *2 /3, 50],60,'White')
    label_rally.set_text('Rally length: '+str(rally))
    label_speed.set_text('Ball speed:'+str(ball1.get_speed()))
                         
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == p1_up:
        #left player & up
        paddle1_vel = -paddle_vel
    elif key == p2_up:
        #right player & up
        paddle2_vel = -paddle_vel
    elif key == p1_down:
        #left player & down
        paddle1_vel = paddle_vel
    elif key ==p2_down:
        #right player & down
        paddle2_vel = paddle_vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if (key == p1_up ) and paddle1_vel < 0:
        paddle1_vel =0
    if (key == p1_down) and paddle1_vel > 0:
        paddle1_vel =0
    if (key == p2_up ) and paddle2_vel < 0:
        paddle2_vel =0
    if (key == p2_down) and paddle2_vel > 0:
        paddle2_vel =0

def harder_game():
    global DIFFICULTY
    DIFFICULTY += 0.1
    label_difficulty.set_text('Difficulty: '+str(int(DIFFICULTY*10 - 10)))

def easier_game():
    global DIFFICULTY
    if DIFFICULTY >= 1.1:
        DIFFICULTY -=0.1
    label_difficulty.set_text('Difficulty: '+str(int(DIFFICULTY*10 - 10)))

def computer_p1():
    #helper function to run player 1
    global paddle1_vel 	#only has control of the [paddle velocity]
    
    #check to see paddle position relative to ball position    
    if not((ball1.get_pos()[1] >= paddle1_pos - HALF_PAD_HEIGHT) and (ball1.get_pos()[1] <= paddle1_pos + HALF_PAD_HEIGHT)) and (int(ball1.get_pos()[0]//(WIDTH/2)) == 0):
        if (paddle1_pos < ball1.get_pos()[1]):
            #paddle is higher than the ball position, move down
            paddle1_vel = paddle_vel
        elif paddle1_pos > ball1.get_pos()[1]:
            #paddle is lower than the ball position, move up
            paddle1_vel = -paddle_vel
        else:
                paddle1_vel = 0

def set_computer():
    global computer_on, score
    computer_on = not(computer_on)
    score = [0,0]

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset',new_game)
frame.add_button('Harder level',harder_game)
frame.add_button('Easier level',easier_game)
frame.add_button('Toggle auto Player',set_computer)
label_difficulty = frame.add_label('Difficulty: 1')
label_rally = frame.add_label('Rally length: 0')
label_speed = frame.add_label('Ball speed: 0')

# start frame
new_game()
frame.start()
