add_library('minim')       #adding the minim library to the code to use sounds
import random       #importing the random library to generate random values
res_width = 1280    #constants for the resolution
res_height = 720
restricted_x = res_width/6    #the restricted area created to limit the space in which circles can be generated to not make the game too hard (1/6th of the resolution)
restricted_y = res_height/6
radius = 75      #constant for starting radius of all circles 
colours = [[50,230,235],[255,0,0]]  #list to hold colours to generate circles of random colour
player = Minim(this) 

class Game:
    def __init__(self):
        self.over = False        #boolean variable to help decide when the game ends
        self.started = False     #variable to see when the game has begun
        self.phase = 1           #the phase/state in which the game currently is
        self.shrink_speed = 0    #the speed at which circles shrink (only for 3rd difficulty)
        self.score = 0           #holds the user's score
        self.total_clicks = 0    #variables to hold number of clicks used to calculate accuracy
        self.accurate_clicks = 0
        self.time = 60           #time for which a game runs
        self.difficulty = 1      #vairable to change the game's difficulty
    
    def display(self):
        self.draw_crosshair()   #called at the beginning of the function to make sure the crosshair is always drawn
        if self.phase == 1:     #introduction screen 
            background(bg2)     #loads the image into the background 
            fill(0)             #changes font colour to black 
            textSize(80)        #changes text size to 80
            text("Kali Aim Trainer", 340, 144)   #displays the string at the position given
            textSize(60)
            text("Start", 570, 360)
        if self.phase == 2:     #the select difficulty screen
            background(bg2)     
            fill(0)
            textSize(60)
            text("Select your Difficulty", 350, 250)
            textSize(40)
            text("1. Beginner", 500, 360)
            text("2. Intermediate", 500, 470)
            text("3. Expert", 500, 580)
        if self.phase == 3:      #the actual game phase
            if self.over == False:   #while the game is not over
                background(bg1)
                if self.started == False:   #before the actual game starts
                    self.new_circles()   #circles are initiated for the first time
                circle1.display()    #displaying all the circles
                circle2.display()
                circle3.display()
                fill(0)
                textSize(30)
                global score     #declaring global variables for score and accuracy because these variables are going to be used in other functions
                global accuracy
                score = "Score: " + str(self.score)   #creating the string to display on the screen during the game
                text(score, 1050, 50)
                if self.total_clicks == 0:     #this code block exists to prevent the code from crashing when 0 clicks have been made (division by 0)
                    accuracy = "Accuracy: 0%"
                    text(accuracy, 1050, 100)
                else:
                    acc = int(round((float(self.accurate_clicks) / float(self.total_clicks)) * 100))   #calculates the accuracy by converting to float and back to integer  
                    accuracy = "Accuracy: " + str(acc) + "%"
                    text(accuracy, 1050, 100)
                time_left = "Time Left: " + str(self.time)   #displays the time left
                text(time_left, 580, 50)
                if (frameCount - time1)%60 == 0:   #time1 is the frameCount recorded when the game starts so the current frameCount is used to decide when one second has passed because 60 frames are drawn every second
                    self.time = self.time - 1      #reduces by one when each second passes
                    circle1.time = circle1.time - 1     #the time left for each red circle also reduces by one (difficulty 2 only)
                    circle2.time = circle2.time - 1
                    circle3.time = circle3.time - 1
                if self.time == 0:  #when the timer reaches 0 the game ends
                    self.over = True
                circle1.radius = circle1.radius - self.shrink_speed     #the circles shrink everytime the draw function is called (shrink speed is 0 in difficulties 1 and 2 so the circles do not actually shrink)
                if circle1.radius == 0:   #when the circles completely disappear a new circle is generated under the same variable name
                    self.new_circle1()
                circle2.radius = circle2.radius - self.shrink_speed
                if circle2.radius == 0:
                    self.new_circle2()
                circle3.radius = circle3.radius - self.shrink_speed
                if circle3.radius == 0:
                    self.new_circle3()
                if self.difficulty == 2:
                    if circle1.colour == 1 and circle1.time == 0:   #in difficulty 2, red circles have to be despawned after 2 seconds to prevent all 3 circles from being red
                        self.new_circle1()
                    if circle2.colour == 1 and circle2.time == 0 :
                        self.new_circle2()
                    if circle3.colour == 1 and circle3.time == 0:
                        self.new_circle3()
            else:
                self.phase = 4     #the score and play again screen
                background(bg2)
                fill(0)
                textSize(60)
                text("Game Over!", 470, 250)
                textSize(40)
                text(score, 520, 360)
                text(accuracy, 500, 400)
                textSize(50)
                text("Play Again", 510, 540)
            
    def mouse_clicked(self):
        if self.phase == 1:   #if the mouse is clicked during the starting phase of the game
            if mouseX>560 and mouseX<710 and mouseY>300 and mouseY<350:   #these 4 values form an imaginary rectangle around the letters. If clicked inside, the corresponding actions are taken
                self.phase = 2   #moves to next game phase
        elif self.phase == 2:
            global time1    #global variable for time1 to record when the game starts, to be used in other functions
            if mouseX>490 and mouseX<720 and mouseY>320 and mouseY<370:
                time1 = frameCount   #records frameCount when mouse is clicked (when game starts) to calculate time elapsed 
                self.phase = 3
                self.difficulty = 1   #sets the difficulty to 1
                self.shrink_speed = 0
            if mouseX>490 and mouseX<800 and mouseY>420 and mouseY<480:
                time1 = frameCount
                self.phase = 3
                self.difficulty = 2
                self.shrink_speed = 0
            if mouseX>490 and mouseX<690 and mouseY>530 and mouseY<590:
                time1 = frameCount
                self.phase = 3
                self.difficulty = 3
                self.shrink_speed = 0.5   #the circles in difficulty 3 will shrink all around by 0.5 pixels, 60 times per second
        elif self.phase == 3:
            shot.rewind()   #rewinds the shot time so it can be played with no errors every time the mouse is clicked
            shot.play()     #plays the shot sound effect
            hit.rewind()
            if dist(mouseX, mouseY, circle1.x, circle1.y) <= float(circle1.radius/2):    #calculates the distance from the mouse position when it is pressed to the center of the circle, if it is less than half the radius, the mouse must have been clicked inside the circle
                hit.play()  #the accurate hit sound effect is played (CS:GO headshot sound effect)
                if circle1.colour == 0:  #if a blue circle was hit
                    self.score = self.score + 100   #the score increases by 100
                    self.accurate_clicks = self.accurate_clicks + 1   #the number of accuracte clicks increases by 1 
                else:    #if the shot hit a red circle
                    self.score = self.score - 50   #the score is reduced by 50
                self.total_clicks =  self.total_clicks + 1   #total number of clicks increases by 1
                self.new_circle1()   #a new circle is generated when any circle is shot
            elif dist(mouseX, mouseY, circle2.x, circle2.y) <= float(circle2.radius/2):    #same code but for circle2
                hit.play()
                if circle2.colour == 0:
                    self.score = self.score + 100
                    self.accurate_clicks = self.accurate_clicks + 1
                else:
                    self.score = self.score - 50
                self.total_clicks =  self.total_clicks + 1
                self.new_circle2()
            elif dist(mouseX, mouseY, circle3.x, circle3.y) <= float(circle3.radius/2):    #same code but for circle3
                hit.play()
                if circle3.colour == 0:
                    self.score = self.score + 100
                    self.accurate_clicks = self.accurate_clicks + 1
                else:
                    self.score = self.score - 50
                self.total_clicks =  self.total_clicks + 1
                self.new_circle3()
            else:   #if no circles are hit
                self.score = self.score - 50  
                self.total_clicks =  self.total_clicks + 1
        elif self.phase == 4:  
            if mouseX>500 and mouseX<760 and mouseY>500 and mouseY<550:  #if the user clicks the play again button
                self.phase = 2    #resets the game attributes to their original values so a new game can be started with new stats
                self.time = 60
                self.over = False
                self.score = 0
                self.total_clicks = 0 
                self.accurate_clicks = 0

    def new_circles(self):   #generates the first three circles for the beginning of the game
        if self.difficulty == 1:   #if the difficulty is 1, only blue variables are generated
            self.instantiate_circles(0, 0, 0)
        else: 
            c1 = random.randint(0,1)   #generates random colours for the circles
            c2 = random.randint(0,1)
            if c1 == 1 and c2 == 1:    #if the first two circles are red, the third one is made to be blue to avoid 3 red circles in difficulty 2
                c3 = 0
            else:
                c3 = random.randint(0,1) #otherwise, a random colour is generated
            self.instantiate_circles(c1, c2, c3)  #the circles of different colours are instantiated
        self.started = True   #indicates that the game has started
        
    def instantiate_circles(self, c1, c2, c3):  #instantiates the first three circles
        global circle1       #global variables for the circles because they are used in other functions
        global circle2
        global circle3
        circle1 = Circle(c1)  #instantiation of the circles
        circle2 = Circle(c2)
        circle3 = Circle(c3)
        self.new_circle1()    #calling the new circle funtions because they validate the positions of the circles to make sure they do not overlap
        self.new_circle2()
        self.new_circle3()
    
    def draw_crosshair(self):   #this function draws the crosshair where the cursor is
        crosshair = loadImage("crosshair2.png")   #loads the image to the variable
        cursor(crosshair)      #replaces the cursor with the crosshair image
    
    def new_circle1(self):   #creates a new circle1
        circle1.x = random.randint(restricted_x, 5*restricted_x)  #generates a random x coordinate for the circle within the restricted area
        circle1.y = random.randint(restricted_y, 5*restricted_y)  #does the same as the line 192 but for the y coordinate
        circle1.radius = radius   #resets the radius to its original value 
        circle1.time = 2   #resets the circle time to its original value
        if self.difficulty != 1:    #if the game is not in difficulty 1
            circle1.colour = random.randint(0,1)   #a random colour is generated 
        while dist(circle1.x, circle1.y, circle3.x, circle3.y) <= radius or dist(circle2.x, circle2.y, circle1.x, circle1.y) <= radius:   #checks if the distance from one circle to another is less than the radius, in which case the circles would be overlapping
            circle1.x = random.randint(restricted_x, 5*restricted_x)  #new x and y coordinates are generated if they are overlapping
            circle1.y = random.randint(restricted_y, 5*restricted_y)
    
    def new_circle2(self):   #repeats lines 191 - 200 but for circle2
        circle2.x = random.randint(restricted_x, 5*restricted_x)
        circle2.y = random.randint(restricted_y, 5*restricted_y)
        circle2.radius = radius
        circle2.time = 2
        if self.difficulty != 1:
            circle2.colour = random.randint(0,1)
        while dist(circle2.x, circle2.y, circle3.x, circle3.y) <= radius or dist(circle2.x, circle2.y, circle3.x, circle3.y) <= radius:
            circle2.x = random.randint(restricted_x, 5*restricted_x)
            circle2.y = random.randint(restricted_y, 5*restricted_y)
            
    def new_circle3(self):   #repeats lines 191 - 200 but for circle2=3
        circle3.x = random.randint(restricted_x, 5*restricted_x)
        circle3.y = random.randint(restricted_y, 5*restricted_y)
        circle3.radius = radius
        circle3.time = 2
        if self.difficulty != 1:
            circle3.colour = random.randint(0,1)
        while dist(circle2.x, circle2.y, circle3.x, circle3.y) <= radius or dist(circle1.x, circle1.y, circle3.x, circle3.y) <= radius:
            circle3.x = random.randint(restricted_x, 5*restricted_x)
            circle3.y = random.randint(restricted_y, 5*restricted_y)
        
class Circle: 
    def __init__(self, c):
        self.x = random.randint(restricted_x, 5*restricted_x)   #instantiation of a circle
        self.y = random.randint(restricted_y, 5*restricted_y)
        self.radius = radius
        self.colour = c
        self.time = 2

    def display(self):     #displays the circles on the screen
        fill(colours[self.colour][0], colours[self.colour][1], colours[self.colour][2])    #changes the colour using the list of colours
        ellipse(self.x, self.y, self.radius, self.radius)     #displays the circle using the ellipse function 
        
game = Game()     #instantiates the game
 
def setup():
    size(res_width, res_height)   #sets the game resolution
    global bg1   #global variables for all the images and sound effects to use in other functions
    global bg2
    global hit
    global shot
    global bg_music
    bg1 = loadImage("bg1.jpg")    #loads the background images into variables
    bg2 = loadImage("bg2.jpg")
    hit = player.loadFile("hit.wav")  #loads the sound effects into corresponding variables
    shot = player.loadFile("shot.wav")
    bg_music = player.loadFile("bg3.wav")
    bg_music.play()   #plays the background music
    
def draw():
    game.display()  #calls the game display function to start displaying the game
     
def mousePressed():     #mousePressed was used instead of mouseClicked because mouseClicked did not detect mouse clicks when the mouse was moving which caused some mouse clicks to go unregistered
    if mouseButton == LEFT:   #if the left mouse button was pressed
        game.mouse_clicked()  #the game mouse_clicked function is called
