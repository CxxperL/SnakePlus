from tkinter import *
import random
global tk
global questionList
global answerList

tk = Tk()

class falseAnswer(): #class for the false answers
    def __init__(self): #initialises the falseAnswer class and sets the variables
        self.scoreAffect = -2
        self.lifeAffect = -1

    def getFalse(self, aToUse): #gets a new false answer
        self.newA =""#creates a string
        try: #tryes to just adjust character if it is straight float answer
            self.newA = float(aToUse) #turns new answer into a float
            self.diff = random.randint(-10,10) #recieves the difference
            self.newA = str(self.newA+self.diff)#adds the difference to new number
            if self.newA[-2:] == ".0":#if float and can be integer, changes to integer
                self.newA = int(self.newA[:-2])
                
        except: #or if strings are in answer it adjusts each number individually
            count = 0
            for i in aToUse:
                if i.isdigit(): #checks if the element in aToUse is a didgit
                    self.diff = random.randint(0,10) #gets the difference to go up by
                    self.newNum = self.diff+int(i)#adds it to a new number
                    #adds the new number into where the old number was
                    aToUse = aToUse[:count]+str(self.newNum)+aToUse[count+1:]
                    if self.newNum>=10: #if the new number is bigger in length then old one then increments count
                        count = count+1
                count = count+1
            self.newA = aToUse
        return self.newA #returns new false answer



    
class question():
    def __init__(self,q, a): #initialises question class
        self.questionList = q #sets array to list of current questions
        self.answerList = a #sets array to list of current answers
        self.usedQuestion = [] #sets up array for used questions and answers
        self.usedAnswer= []

    def getQuestionNum(self): #gets the number for question and answer to be used
        self.length = len(self.questionList) #finds length of question array
        questionNumber = random.randint(0,self.length)-1 #chooses random number depending on length of array
        self.usedQuestion.append(self.questionList[questionNumber]) #adds question to the used question array
        self.questionList.pop(questionNumber) #removes question from current questions array
        return questionNumber #returns number of question

    def getQuestion(self, qNum):
        return self.usedQuestion[-1] #returns the current question

    def getAnswer(self, qNum):
        self.usedAnswer.append(self.answerList[qNum]) #adds current answer to used answer array
        self.answerList.pop(qNum)#removes answer from current answer array
        return self.usedAnswer[-1]#returns the current answer

class snakeHead():
    def __init__(self): #initialises snakeHead class
        self.bodysize = 3 #gives the snake bodysize of 3
        self.coords = [] #creates a coordinate array
        self.speed = 0.3  #sets a speed of 0.3
        self.bodies = [] #creates a bodies array
        self.direction = "right" #sets default direction of right
        for i in range(0, self.bodysize): #creates 3 coordinates so 3 bodies can be made
            self.coords.append([210,290])

        self.snakeSize() #calls snakeSize method

    def snakeSize(self):
        for x,y in self.coords: # for how long the coordinate array is
            #create a rectangle at x and y
            self.body = main.create_rectangle(x, y, x + 35, y + 35, fill="#00FF00")
            #add the body to the bodies array
            self.bodies.append(self.body)
            #update canvas
            main.update()

    def changeDirection(self, input): #changes direction of snake
        global directionChange
        directionChange = True
        #depending what the user inputed and the current direction of the snake
        #the snakes direction will change if both conditions are met
        if input == "w":
            if self.direction != "down":
                self.direction = "up"
        if input == "a":
            if self.direction != "right":
                self.direction = "left"
        if input == "d":
            if self.direction != "left":
                self.direction = "right"
        if input == "s":
            if self.direction != "up":
                self.direction = "down"
    
    def getDirection(self): #returns sh object direction
        return self.direction
    
    def getCoords(self): #returns sh object coordinates
        return self.coords

    def newCords(self, zero, newcords): #gets the new coordinates near end of while loop
        x,y = newcords #gets the new head of the snake
        self.coords.insert(zero, newcords) #places new head of snake at front of array
        body = main.create_rectangle(x, y, x + 35, y + 35, fill="#00FF00") #creates a new square for the head
        self.bodies.insert(0,body) #inserts new body into the bodies array
        main.update() #updates the canvas

    def drawSnake(self): # draws the snake
        main.delete(ALL) #deletes everything on the page to remove the old snake
        for i in range(len(self.coords)-2): #adds squares on the end of the snake for the length of the coords -2
            x,y= self.coords[i]
            main.create_rectangle(x, y, x + 35, y + 35, fill="#00FF00")
    
    def clearCoords(self): #deletes all the old coordinates
        if len(self.coords)>=len(self.bodies):
            del self.coords[self.bodysize+1:]
            del self.bodies[self.bodysize+1:]

def myround(x, base=35): #function rounds coordinates to nearest 35 so can be neatly placed on a grid
    return int(base * round(float(x)/base))

def gameEnd(gameEnding):
        #clears canvas
        main.delete(ALL)
        #creates text to alert loser of the end of the game
        main.create_text(200,200, text="Game Over", fill="#00FFFF", font=("Comic Sans MS",20, 'bold'))
        main.create_text(200,300, text="Esc to close game", fill="#000000", font=("Comic Sans MS",12))
        main.update()
        #keeps the canvas stuck on this screen until user leaves the game
        if gameEnding ==True:
            main.mainloop()
        gameEnding = True# sets the game to ending if this function has been run so mainloop can occur
        return gameEnding

def mainGame(questionList, answerList, first, difficulty): #this is the main function which runs the game
    #instances and variables set to global
    global directionChange
    global q
    global sh
    global direction
    global questionComplete
    #initialises variables
    directionChange = False
    gameEnding = False
    #sets difficulty to be in line with question and answer arrays
    difficulty = difficulty-1
    while gameEnding == False: #main game loop
        directionChange = False
        if first == True: #if statement which initialises 
            #removes the difficulty button
            dif1.place_forget()
            dif2.place_forget()
            dif3.place_forget()
            #creates instance for question class
            q = question(questionList[difficulty], answerList[difficulty])
            #creates instance for snake and false question class
            sh = snakeHead()
            fa = falseAnswer()
            #sets first to false so the if statement cant be run again
            first = False
            #sets default direction so snake can move
            direction = "right"
            #sets questionComplete to True so a question can be chosen
            questionComplete = True
            #sets score and lives variables to default values
            score = 0
            lives = 3
        #creates a line on the canvas which seperates the question space to play space
        main.create_line(-5,80,485,80, width =5)
        #removes the coords of snake that arent being used now
        if first == False:
            sh.clearCoords()
        if questionComplete == True: #if statement if a new question is needed
            if q.questionList == []: #checks to see if questionlist within q instance is empty
                difficulty = difficulty+1 #if yes then difficulty is increased
                if difficulty == 3:
                    difficulty = 0 #unless if on max difficulty it will be decreased to minium
                #sets instances arrays to new difficulty question and answers
                q.questionList = questionList[difficulty]
                q.answerList = answerList[difficulty]
                if questionList == [[],[],[]]: #checks to see if every question has been used
                    q.questionList =q.usedQuestion #reuses the old questions
                    q.answerList = q.usedAnswer #reuses the old answers
                    q.usedQuestion = []#clears used question and answer array from instance q
                    q.usedAnswer = []
            #gets the number for the question and answer
            qNum = q.getQuestionNum()
            #gets the question to be used
            qToUse = q.getQuestion(qNum)
            #gets the answer to be used
            aToUse = q.getAnswer(qNum)
            questionComplete = False
            #gets the coordinates for where the answer should appear on canvas
            ansx = random.randint(0,385)
            ansx = myround(ansx)
            ansy = random.randint(0,385)
            ansy = myround(ansy)
            #adds 80 to account for question header
            ansy= ansy+80
            #gets a false answer 1
            falseA1 = fa.getFalse(aToUse)
            while str(falseA1) == str(aToUse): #makes sure the false answer isnt the same as the correct answer
                falseA1 = fa.getFalse(aToUse)
            #gets the x coordinate for the false answer
            f1ansx = random.randint(0,385)
            f1ansx = myround(f1ansx)
            while f1ansx == ansx: #makes sure the coordinates of the false answer are the same as correct answer
                f1ansx = random.randint(0,385)
                f1ansx = myround(f1ansx)
            #gets the y coordinate for the false answer
            f1ansy = random.randint(0,385)
            f1ansy = myround(f1ansy)
            f1ansy= f1ansy+80
            while f1ansy == ansy: #makes sure the coordinates of the false answer are the same as correct answer
                f1ansy = random.randint(0,385)
                f1ansy = myround(f1ansy)
                f1ansy= f1ansy+80

            falseA2 = fa.getFalse(aToUse)
            while str(falseA2) == str(aToUse) or str(falseA2) == str(falseA1):
                falseA2 = fa.getFalse(aToUse)
            #gets the x coordinate for the false answer
            f2ansx = random.randint(0,385)
            f2ansx = myround(f2ansx)
            while f2ansx == ansx:#makes sure the coordinates of the false answer are the same as correct answer
                f2ansx = random.randint(0,385)
                f2ansx = myround(f2ansx)
            #gets the y coordinate for the false answer
            f2ansy = random.randint(0,385)
            f2ansy = myround(f2ansy)
            f2ansy= f2ansy+80
            while f2ansy == ansy:#makes sure the coordinates of the false answer are the same as correct answer
                f2ansy = random.randint(0,385)
                f2ansy = myround(f2ansy)
                f2ansy= f2ansy+80


        aToUse = str(aToUse)

        #tkinter main creations#
        questionOnScreen = main.create_text(200, 33, text="", fill="#00FF00", font=("Comic Sans MS",16, 'bold'))
        #resets the question currently on screen
        main.delete(questionOnScreen)
        #places current question on screen
        questionOnScreen = main.create_text(200, 33, text=qToUse, fill="#00FF00", font=("Comic Sans MS",16, 'bold'))
        #this places a square where the correct answer will be
        answerOnScreen = main.create_rectangle(ansx, ansy, ansx+35, ansy+35, tags=aToUse, fill="#FFFFFF" )
        #this places the correct answer as text on the square created line above
        answerText = main.create_text(ansx+15, ansy+25, text=aToUse, font=("Comic Sans MS", 12))
        #creates a square at coordinates for false answer
        f1answerOnScreen = main.create_rectangle(f1ansx, f1ansy, f1ansx+35, f1ansy+35, tags=falseA1, fill="#FFFFFF" )
        #places false answer on top of the square 
        f1answerText = main.create_text(f1ansx+15, f1ansy+25, text=falseA1, font=("Comic Sans MS", 12))
        #creates another square for false answer
        f2answerOnScreen = main.create_rectangle(f2ansx, f2ansy, f2ansx+35, f2ansy+35, tags=falseA2, fill="#FFFFFF" )
        #places text on the square for false answer
        f2answerText = main.create_text(f2ansx+15, f2ansy+25, text=falseA2, font=("Comic Sans MS", 12))
        #displays current lives and score
        showScore = main.create_text(35,15, text="Score: "+str(score), font=("Comic Sans MS", 12))
        showLives = main.create_text(35, 30, text="Lives: "+str(lives), font=("Comic Sans MS", 12))
        #updates the canvas
        main.update()
        #retrieves the coordinates stored in sh class
        coords = sh.getCoords()
        #x,y set as the coordinate of head of snake
        x,y = coords[0]
        #binds keys on keyboard to the function to allow for changing of direction of snake
        tk.bind("w", lambda event: sh.changeDirection("w"))
        tk.bind("a", lambda event: sh.changeDirection("a"))
        tk.bind("s", lambda event: sh.changeDirection("s"))
        tk.bind("d", lambda event: sh.changeDirection("d"))
        #allows esc button to quit game without saving
        tk.bind("<Escape>", lambda event: quit())
        tk.bind("<Up>", lambda event: sh.changeDirection("w"))
        tk.bind("<Left>", lambda event: sh.changeDirection("a"))
        tk.bind("<Down>", lambda event: sh.changeDirection("s"))
        tk.bind("<Right>", lambda event: sh.changeDirection("d"))
        #after the user inputs a key assigned to direction change, new direction assinged from sh class retrieved
        direction = sh.getDirection()
        #updates canvas
        main.update()
        #choses the coordinate of where the next head of the snake will be
        if direction == "up":
            y = y-35
        if direction == "down":
            y =y+35
        if direction == "right":
            x = x+35
        if direction == "left":
            x = x-35
        
        if directionChange == True and gameEnding == True:
            tk.unbind("w")
            tk.unbind("a")
            tk.unbind("s")
            tk.unbind("d")
            tk.unbind("<Up>")
            tk.unbind("<Left>")
            tk.unbind("<Right>")
            tk.unbind("<Down>")

        #if the snake hits the edge of the walls the game will end
        if x <0 or x>385 or y<80 or y>465:
            gameEnding = gameEnd(gameEnding)
        #if statement for when the snake gets the answer correct
        if x==ansx and y==ansy:
            #assingns variable to true so another question can be chosen
            questionComplete = True
            #increments score by 5
            score = score+5
            #increases the size of the snakes bodysize in sh
            sh.bodysize = sh.bodysize+1
            oldtail = coords[-1]
            #finds the end tail
            oldbodx,oldbody = oldtail
            #gets new coordinate for the extended part of snake
            if direction == "up":
                ybod = oldbody+35
                coords.append((oldbodx,ybod))
            if direction == "down":
                ybod =oldbody-35
                coords.append((oldbodx,ybod))
            if direction == "right":
                xbod = oldbodx-35
                coords.append((xbod,oldbody))
            if direction == "left":
                xbod = oldbodx+35
                coords.append((xbod,oldbody))
            #updates sh class coords to new coords
            sh.coords = coords
        #if snake is on incorrect answer
        if (x==f1ansx and y==f1ansy) or (x==f2ansx and y==f2ansy):
            #gets a new question on next run of while loop
            questionComplete = True
            #decreases score and lives by variable assigned in fa class
            score = score+ fa.scoreAffect
            lives = lives+fa.lifeAffect
        #if the user runs out of lives the game ends
        if lives ==0:
            gameEnding = gameEnd(gameEnding)
        #updates the new coordinates into sh class using newCords method
        sh.newCords(0,(x,y))
        #gets new coords
        coords = sh.getCoords()
        #detects if bodysize is greater then 3 and if snake has hit itself then the game will end
        if sh.bodysize>3:
            for i in range(1,len(sh.coords)):
                if coords[0] == coords[i]:
                    gameEnding = gameEnd(gameEnding)
        #draws snake on canvas
        sh.drawSnake()
        #tkiner wont update for another 100ms
        main.after(100)
    #updates tkinter when the game has ended
    main.update()
    #returns two variables to be used
    return score, gameEnding

def scoreUpdate(currentScore,gE):
    filename = "Score/highScore.txt"
    with open(filename) as fS:
        for line in fS:
            highScore = line
    if int(currentScore) > int(highScore):
        highScore = currentScore
        hsFile = open(filename, 'w')
        hsFile.write(str(highScore))
        hsFile.close()
    gameEnd(gE)
    main.mainloop()
    

def changeDifficulty(difficulty):
    main.config(width=420, height=500)
    #sets variables to global so can be used outside of the function
    global questionList
    global answerList
    #creates arrays for questions and answers
    questionList = []
    questionListE = []
    questionListM = []
    questionListD = []
    answerList = []
    answerListE = []
    answerListM = []
    answerListD = []
    #allows for main game function to run its initialisation
    first = True
    
    #sets filenames for easy files
    fileQ = "QuestAnsw/easyQ.txt"
    fileA = "QuestAnsw/easyA.txt"
    #reads each line of file
    with open(fileQ) as fQ:
        for line in fQ:
            #writes content of line into array
            questionListE.append(line)
    #reads each line of file
    with open(fileA) as fA:
        for line in fA:
            #writes content of line into array
            answerListE.append(line)

    #sets filenames for medium files
    fileQ = "QuestAnsw/mediumQ.txt"
    fileA = "QuestAnsw/mediumA.txt"
    with open(fileQ) as fQ:
        for line in fQ:
            #writes content of line into array
            questionListM.append(line)
    with open(fileA) as fA:
        for line in fA:
            #writes content of line into array
            answerListM.append(line)
    #sets filenames for difficult files
    fileQ = "QuestAnsw/difficultQ.txt"
    fileA = "QuestAnsw/diffiucltA.txt"
    with open(fileQ) as fQ:
        for line in fQ:
            #writes content of line into array
            questionListD.append(line)
    with open(fileA) as fA:
        for line in fA:
            #writes content of line into array
            answerListD.append(line)
    #removes the \n on the end of all the questions
    for i in range(len(questionListE)):
        temp = questionListE[i]
        if temp[:-1] == "\n":
            temp = temp[:-1]
            questionListE.pop(i)
            questionListE.insert(i,temp)
    #removes the \n on the end of all the questions        
    for i in range(len(answerListE)):
        temp = answerListE[i]
        if temp[:-1] == "\n":
            temp = temp[:-1]
            answerListE.pop(i)
            answerListE.insert(i,temp)
    #removes the \n on the end of all the questions
    for i in range(len(questionListM)):
        temp = questionListM[i]
        if temp[:-1] == "\n":
            temp = temp[:-1]
            questionListM.pop(i)
            questionListM.insert(i,temp)
    #removes the \n on the end of all the answers
    for i in range(len(answerListM)):
        temp = answerListM[i]
        if temp[:-1] == "\n":
            temp = temp[:-1]
            answerListM.pop(i)
            answerListM.insert(i,temp)
    #removes the \n on the end of all the answers
    for i in range(len(questionListD)):
        temp = questionListD[i]
        if temp[:-1] == "\n":
            temp = temp[:-1]
            questionListD.pop(i)
            questionListD.insert(i,temp)
    #removes the \n on the end of all the answers
    for i in range(len(answerListD)):
        temp = answerListD[i]
        if temp[:-1] == "\n":
            temp = temp[:-1]
            answerListD.pop(i)
            answerListD.insert(i,temp)
    #adds all sublists into their main list to be transferred to another function
    answerList.append(answerListE)
    answerList.append(answerListM)
    answerList.append(answerListD)
    questionList.append(questionListE)
    questionList.append(questionListM)
    questionList.append(questionListD)
    #deletes everything on the main canvas and clears it
    main.delete(ALL)

    #function that will cause the game to run and returns the score
    score, gE = mainGame(questionList, answerList, first, difficulty)
    #will run the function that updates score
    scoreUpdate(score, gE)

def startGame():    #this function sets the game up to allow for a difficulty to be chosen
    #sets buttons and variables to be global so can be hidden in different function
    global dif1
    global dif2
    global dif3
    global first
    #hides the previously made buttons
    first = True
    startB.place_forget()
    quitB.place_forget()
    #creates buttons for each difficulty
    dif1 = Button(tk, text="Easy Difficulty", command=lambda *args: changeDifficulty(1))
    dif2 = Button(tk, text="Medium Difficulty", command=lambda *args: changeDifficulty(2))
    dif3 = Button(tk, text="Hard Difficulty", command=lambda *args: changeDifficulty(3))
    #places the buttons on canvas
    dif1.place(x=345, y=0)
    dif2.place(x=345, y=30)
    dif3.place(x=345, y=60)
    main.update()
    #keeps code running to allow for user to choose difficulty
    main.mainloop()

def menuStart():    #this function creates menu buttons and shows highscore on a blank canvas
    #assigns variables to global so can be used in other functions
    global difficulty
    global startB
    global quitB
    global main
    global hSText
    difficulty = 0
    #creates a canvas on tkinter
    main = Canvas(width = 750, height= 500)
    tk.title("Snake+")
    #creates a button to start the game on the canvas
    startB = Button(text="Start Game", command= startGame)
    #creates a button to quit the game on the canvas
    quitB = Button(text ="Quit Game", command=quit)
    #sets the locations for the buttons on the canvas
    startB.place(x=345, y=0)
    quitB.place(x=345,y=50)
    #opens file that has current highscore
    filename = "Score/highScore.txt"
    with open(filename) as fS:
        for line in fS:
            #writes current highscore into a variable
            highScore = line
    #text created on canvas to display current high score
    main.create_text(375, 200, text="High Score: "+highScore, font=("Comic Sans MS",20, 'bold'))
    #updates the canvas
    main.pack()
    #keeps the code running for the user to click a button
    main.mainloop()

menuStart()
