# SCREEN RESOLUTION: 1600 x 900
import math
import tkinter
import invader
import invaderBullet
import player
import playerBullet
import json
import platform


# Create a class with the window as methods so we can add our own methods
class myGUI:
    def __init__(self, master):
        self.master = master
        self.windowWidth = master.winfo_width()
        self.windowHeight = master.winfo_height()
        #print(self.windowHeight, self.windowWidth)
        self.player = None
        self.screen = "main_menu"
        self.entities = []
        self.canvas = None
        self.paused = False
        self.tickCount = 0
        # Represents how many characters of the cheat code pattern we have entered
        self.cheatCodeChars = 0
        self.cheatCodes = []
        self.boss = False
        # Image to display on the window
        self.bossImage = tkinter.PhotoImage(file="bossImage.png")

    # Method which renders the main menu screen
    def mainMenuScreen(self):
        self.master.unbind("<KeyPress>")
        self.master.unbind("<KeyRelease>")
        # Delete all widgets
        self.deleteAllWidgets()
        self.screen = "main_menu"
        self.entities = []
        # if we have come from som other screen delete the canvas
        if self.canvas is not None:
            self.canvas.destroy()
        self.buttonW = 50
        self.buttonH = 5
        self.newGameBtn = tkinter.Button(self.master, command=self.newGamePress, text="New Game", width=self.buttonW, height=self.buttonH, bg="Gray")
        self.loadGameBtn = tkinter.Button(self.master, command=self.loadGameScreen, text="Load Game", width=self.buttonW, height=self.buttonH, bg="Gray")
        self.keybindBtn = tkinter.Button(self.master, command=self.keybindPress, text="Keybindings", width=self.buttonW, height=self.buttonH, bg="Gray")
        self.newGameBtn.place(x=self.windowWidth/5 - 180, y=self.windowHeight/2 - 43)
        self.loadGameBtn.place(x=self.windowWidth*.8 - 180, y=self.windowHeight/2 - 43)
        self.keybindBtn.place(x=self.windowWidth/2 - 180, y=self.windowHeight/2 - 43)
        self.leaderBdFrame = tkinter.Frame(self.master, width=400, height=300, bg="light blue")
        self.leaderBdFrame.place(x=self.windowWidth/2, y=200, anchor="center")
        # Render the headings for the leaderboard
        posLabel = tkinter.Label(self.leaderBdFrame, text="Position", background="light blue", font=("Helvetica", 16))
        posLabel.grid(row=0, column=0)
        nameLabel = tkinter.Label(self.leaderBdFrame, text="Name", background="light blue", font=("Helvetica", 16))
        nameLabel.grid(row=0, column=1)
        scoreLabel = tkinter.Label(self.leaderBdFrame, text="Score", background="light blue", font=("Helvetica", 16))
        scoreLabel.grid(row=0, column=2)

        try:
            with open("leaderboard.json") as scoreFile:
                ldrBrdDict = json.load(scoreFile)
                # Only render 10 entries
                for key in ldrBrdDict:
                    if 1 <= ldrBrdDict[key][1] <= 10:
                        positionLabel = tkinter.Label(self.leaderBdFrame, text=ldrBrdDict[key][1], background="light blue", font=("Helvetica", 16))
                        positionLabel.grid(row=ldrBrdDict[key][1], column=0)
                        nameLabel = tkinter.Label(self.leaderBdFrame, text=key, background="light blue", font=("Helvetica", 16))
                        nameLabel.grid(row=ldrBrdDict[key][1], column=1)
                        scoreLabel = tkinter.Label(self.leaderBdFrame, text=ldrBrdDict[key][0], background="light blue", font=("Helvetica", 16))
                        scoreLabel.grid(row=ldrBrdDict[key][1], column=2)

                scoreFile.close()
        except IOError as e:
            print("Leaderboard file not found, displaying leaderboard as empty")
        self.master.bind("<KeyPress>", lambda event: self.handleMainMenuPress(event))
        # bind the boss key
        self.master.bind("`", lambda event: self.handleBossKey(event))

    def newGamePress(self):
        self.loadLevel()

    def loadGamePress(self):
        pass

    def keybindPress(self):
        self.keybindingsScreen()

    def loadLevel(self, level=1, lives=3):
        self.master.unbind("<KeyPress>")
        self.deleteAllWidgets()
        # As the levels increase so should the invader bullet's speed and their frequency, but the score should increase as well
        self.screen = "game_screen"
        self.paused = False

        # Delete any entities and start from scratch
        self.entities = []
        # Create a canvas to draw images on
        if self.canvas is not None:
            self.canvas.destroy()
        self.canvas = tkinter.Canvas(self.master, bg="black", width=self.windowWidth, height=self.windowHeight)
        self.canvas.pack()
        # Create and add the background image
        self.bgImage = tkinter.PhotoImage(file="Background.png")
        self.canvas.create_image(self.windowWidth/2, self.windowHeight/2, image=self.bgImage)
        #Create and add the player sprite
        self.plImage = tkinter.PhotoImage(file="Player.png")
        self.plImage = self.plImage.zoom(20, 20)
        self.playerIm = self.canvas.create_image(self.windowWidth/2, self.windowHeight - 200, image=self.plImage)

        #Create the player
        playerSpeed = 2
        if self.player is None:
            self.player = player.Player(self.windowWidth/2, self.windowHeight - 200, playerSpeed, 620, self.windowWidth, self.windowHeight, self.plImage, self.cheatCodes)
            # Bind key up and key down events to their respective player methods
            self.screen = "game_screen"
        self.master.bind("<KeyPress>", lambda event: self.player.keyDown(event))
        self.master.bind("<KeyRelease>", lambda event: self.player.keyUp(event))
        # Resetting various player attributes
        self.player.x = self.windowWidth/2
        self.player.y = self.windowHeight - 200
        self.player.paused = False
        self.player.isAlive = True
        if lives != 3:
            self.player.lives = lives
        if level==1:
            self.player.score = 0
            self.player.level = 1
        elif level > 1:
            self.player.level = level
            # if we have loaded from a save update the score
            self.player.score = 0
            if level >= 2:
                self.player.score += 21
            if level >= 3:
                self.player.score += 21 * 2
            if level >= 4:
                self.player.score += 28 * 3
            if level >= 5:
                self.player.score += 28 * 4
            if level >= 6:
                self.player.score += 35 * 5
            if level >= 7:
                self.player.score += 35 * 6
            if level >= 8:
                self.player.score += 42 * 7
            if level >= 9:
                self.player.score += 42 * 8
            if level >= 10:
                self.player.score += 49 * 9
        # Now create all the enemies (invaders)
        self.invImage = tkinter.PhotoImage(file="invader.png")
        self.invImage = self.invImage.zoom(7, 7)

        # Create 21 enemies
        # define the bounds for which the invaders may move in
        minX, maxX = 80, self.windowWidth - 80
        # Represents the number of enemies per row and column
        rowLength = 7
        # Choosing the number of rows based on the level
        columnLength = 3
        if level in [1, 2]:
            columnLength = 3
        elif level in [3, 4]:
            columnLength = 4
        elif level in [5, 6]:
            columnLength = 5
        elif level in [7, 8]:
            columnLength = 6
        elif level in [9, 10]:
            columnLength = 7
        elif level > 10:
            columnLength = 7

        invaderSpeed = 2
        # keep a list of all invaders
        self.invaders = [[0 for i in range(rowLength)] for j in range(columnLength)]
        for i in range(columnLength):
            # Generate invaders on the right of the centre
            for j in range(0, math.ceil(rowLength/2)):
                x = self.windowWidth/2 + (j * 200)
                y = i * 80 + 20
                invIm = self.canvas.create_image(x, y, image=self.invImage)
                theInvader = invader.Invader(x, y, invaderSpeed if i % 2 == 0 else -1*invaderSpeed, minX, maxX, self.invImage, i, self.player.level)
                self.entities.append([theInvader, invIm])
                self.invaders[i][j] = theInvader
            # Generate invaders on the left of the centre
            for j in range(math.floor(rowLength/2), 0, -1):
                x = self.windowWidth / 2 - (j * 200)
                y = i * 80 + 20
                invIm = self.canvas.create_image(x, y, image=self.invImage)
                theInvader = invader.Invader(x, y, invaderSpeed if i % 2 == 0 else -1*invaderSpeed, minX, maxX, self.invImage, i, self.player.level)
                self.entities.append([theInvader, invIm])
                self.invaders[i][j + math.floor(rowLength / 2)] = theInvader
        # Create a scoreboard to show the player their score
        self.scoreTextItem = self.canvas.create_text(20, 20, text="SCORE: " + str(self.player.score), font=("Helvetica", 16), anchor="nw")
        self.invadersLeft = rowLength * columnLength
        # Create a piece of text to show the level the player is on
        self.levelTextItem = self.canvas.create_text(self.windowWidth-20, 20, text="LEVEL: " + str(self.player.level), font=("Helvetica", 16), anchor="ne")
        # Create some text to show the number of lives left
        self.livesTextItem = self.canvas.create_text(self.windowWidth/2, 20, text="LIVES: " + str(self.player.lives), font=("Helvetica", 16), anchor="n")
        # Make our own ad hoc main loop by repeatedly calling a tick function
        self.tick()

    # Function switches to the main screen and destroys whatever is passed to it e.g. a frame or button
    def switchMainScreenAndDestroy(self, toDestroy=None):
        self.player = None
        if toDestroy is not None:
            toDestroy.destroy()
        # switch to main menu
        self.mainMenuScreen()

    # Method called every 0.01s
    def tick(self):
        if self.screen == "game_screen":
            if not self.player.isAlive:
                pass
            # If we have just paused
            elif self.player.paused and self.paused is False:
                self.paused = True
                menuWidth = 600
                menuHeight = 400
                # Create a frame to contain all the buttons on the pause screen
                self.pauseFrame = tkinter.Frame(self.master, bg="white", width=menuWidth, height=menuHeight)
                self.pauseFrame.place(x=self.windowWidth/2 - menuWidth/2, y=self.windowHeight/2 - menuHeight)
                # Create some text to indicate the game is paused
                pauseLabel = tkinter.Label(self.pauseFrame, text="Game Paused", font=("Helvetica", 16))
                pauseLabel.place(x=menuWidth / 2, y=16, anchor="center")
                # Create a button to return to the main menu
                mainMenuBtn = tkinter.Button(self.pauseFrame, command=lambda: self.switchMainScreenAndDestroy(self.pauseFrame), text="Return to main menu", width=self.buttonW, height=self.buttonH, bg="Gray")
                mainMenuBtn.place(x=menuWidth/2 - 180, y=menuHeight-90)
                # Create a button to resume the game
                resumeBtn = tkinter.Button(self.pauseFrame, command=lambda: self.player.setPaused(False), text="Resume game", width=self.buttonW, height=self.buttonH, bg="Gray")
                resumeBtn.place(x=menuWidth/2 - 180, y=menuHeight-180)

                # Create some widgets to let the user save their game
                saveLabel = tkinter.Label(self.pauseFrame, text="Save game", font=("Helvetica", 16))
                saveLabel.place(x=menuWidth / 2, y=60, anchor="center")
                save1Btn = tkinter.Button(self.pauseFrame, command=lambda: self.saveGame("1"), text="Save 1", width=int(self.buttonW/3), height=self.buttonH, bg="Gray")
                save2Btn = tkinter.Button(self.pauseFrame, command=lambda: self.saveGame("2"), text="Save 2",
                                          width=int(self.buttonW / 3), height=self.buttonH, bg="Gray")
                save3Btn = tkinter.Button(self.pauseFrame, command=lambda: self.saveGame("3"), text="Save 3",
                                          width=int(self.buttonW / 3), height=self.buttonH, bg="Gray")
                save1Btn.place(x=menuWidth*.3, y=130, anchor="center")
                save2Btn.place(x=menuWidth * .5, y=130, anchor="center")
                save3Btn.place(x=menuWidth * .7, y=130, anchor="center")

            # If we have just unpaused
            elif self.player.paused is False and self.paused is True:
                self.paused = False
                # Destroy the pause menu
                self.pauseFrame.destroy()

            # If we are currently paused
            elif self.paused:
                pass
            else:

                # Tick the player
                result = self.player.tickPlayer(self.entities)
                self.canvas.move(self.playerIm, self.player.x - self.player.lastX, self.player.y - self.player.lastY)
                if result is not None:
                    # Unpack all the messages
                    for msg in result:
                        if msg[0] == "shoot":
                            bulletW = 7 * 10 if "wide_load" in self.cheatCodes else 5
                            bulletH = 7 * 5 if "wide_load" in self.cheatCodes else 5
                            moveSpeed = 10
                            bObj = playerBullet.PlayerBullet(self.player.x, self.player.y, bulletW, bulletH, moveSpeed, self.cheatCodes)
                            bImg = self.canvas.create_rectangle(self.player.x - bulletW/2, self.player.y - 1.5*bulletH, self.player.x + bulletW/2, self.player.y + 1.5*bulletH, fill="red")
                            self.entities.append([bObj, bImg])
                        # if the player has been hit by a bullet    
                        if msg[0] == "destroy":
                            if self.player.lives <= 0:
                                # Display all the death widgets
                                self.player.isAlive = False
                                self.deathFrame = tkinter.Frame(self.master, width=self.windowWidth, height=self.windowHeight, background="")
                                self.canvas.create_text(self.windowWidth/2, self.windowHeight/2 - 100, text="Game Over", fill="red", font=("Helvetica", 32))
                                self.canvas.create_text(self.windowWidth/2, self.windowHeight/2 - 60, text="Enter name to save score", font=("Helvetica", 16))
                                self.nameEntry = tkinter.Entry(self.deathFrame, bg="Gray", font=("Helvetica", 16), justify=tkinter.CENTER)
                                self.nameEntry.place(x=self.windowWidth/2 - 120, y=self.windowHeight/2 -40)
                                saveScoreBtn = tkinter.Button(self.deathFrame, command=lambda: self.saveScoreExit(), text="Save score", bg="gray", width=self.buttonW, height=self.buttonH,)
                                saveScoreBtn.place(x=self.windowWidth/2 - 180, y=self.windowHeight*0.5)
                                self.returnBtn = tkinter.Button(self.deathFrame, command=lambda: self.switchMainScreenAndDestroy(self.deathFrame), text="Return to main menu", width=self.buttonW, height=self.buttonH, bg="Gray")
                                self.returnBtn.place(x=self.windowWidth/2 - 180, y=self.windowHeight*0.6)
                                self.deathFrame.place(x=0, y=0)
                            else:
                                # Otherwise remove the offending bullet
                                self.canvas.delete(msg[1][1])
                                # Remove the entry from the entity array
                                self.entities.remove(msg[1])
                                # Decrement the players lives on the screen
                                self.canvas.itemconfig(self.livesTextItem, text="LIVES: " + str(self.player.lives))

                # Tick all the entities, bullets & enemies
                for ent in self.entities:
                    # Ensuring none of the invaders have reached the road
                    if isinstance(ent[0], invader.Invader):
                        if ent[0].y >= 620:
                            # If an invader reaches the road, end the game
                            self.player.isAlive = False
                            self.deathFrame = tkinter.Frame(self.master, width=self.windowWidth,height=self.windowHeight, background="")
                            self.canvas.create_text(self.windowWidth / 2, self.windowHeight / 2 - 100, text="Game Over",fill="red", font=("Helvetica", 32))
                            self.canvas.create_text(self.windowWidth / 2, self.windowHeight / 2 - 60,text="Enter name to save score", font=("Helvetica", 16))
                            self.nameEntry = tkinter.Entry(self.deathFrame, bg="Gray", font=("Helvetica", 16), justify=tkinter.CENTER)
                            self.nameEntry.place(x=self.windowWidth / 2 - 120, y=self.windowHeight / 2 - 40)
                            saveScoreBtn = tkinter.Button(self.deathFrame, command=lambda: self.saveScoreExit(), text="Save score", bg="gray", width=self.buttonW, height=self.buttonH, )
                            saveScoreBtn.place(x=self.windowWidth / 2 - 180, y=self.windowHeight * 0.5)
                            self.returnBtn = tkinter.Button(self.deathFrame,
                                                            command=lambda: self.switchMainScreenAndDestroy(
                                                                self.deathFrame), text="Return to main menu",
                                                            width=self.buttonW, height=self.buttonH, bg="Gray")
                            self.returnBtn.place(x=self.windowWidth / 2 - 180, y=self.windowHeight * 0.6)
                            self.deathFrame.place(x=0, y=0)
                    result = ent[0].tick(self.entities)
                    # The result from ticking entities is a 2d array with separate messages which are contained within the sub arrays
                    # We unpack the messages
                    if result is not None:
                        for msg in result:
                            if msg[0] == "destroy":
                                # Delete the image from a canvas
                                self.canvas.delete(ent[1])
                                # Remove the entry from the entity array
                                if ent in self.entities:
                                    self.entities.remove(ent)
                                # If the invader has been destroyed by the player
                                if isinstance(ent[0], invader.Invader):
                                    # increment the player's score
                                    self.player.incrementScore()
                                    # And update the scoreboard
                                    self.canvas.itemconfig(self.scoreTextItem, text="SCORE: " + str(self.player.score))
                                    self.invadersLeft -= 1
                                    if self.invadersLeft <= 0:
                                        #print("here")
                                        self.player.level += 1
                                        self.loadLevel(self.player.level)
                                        return

                            # If shoot is returned and it is an invader
                            elif msg[0] == "shoot" and isinstance(ent[0], invader.Invader):
                                invBulletSpeed = 3 * (1.2 ** (self.player.level - 1))
                                bulletW = 7
                                bulletH = 7
                                invBullet = invaderBullet.InvaderBullet(ent[0].x, ent[0].y, bulletW, bulletH, ent[0].moveSpeed, invBulletSpeed, self.windowHeight)
                                invBulletImg = self.canvas.create_rectangle(ent[0].x - bulletW/2, ent[0].y - 1.5*bulletH, ent[0].x + bulletW/2, ent[0].y + 1.5*bulletH, fill="gray")
                                self.entities.append([invBullet, invBulletImg])
                            # If a row has indicated they should change direction
                            elif msg[0] == "chgDir" and isinstance(ent[0], invader.Invader):
                                # msg[1] contains the row of the invader changing direction
                                for enemy in self.invaders[msg[1]]:
                                    enemy.changeDir()
                                    #self.canvas.move(ent[1], ent[0].x - ent[0].lastX, ent[0].y - ent[0].lastY)
                    self.canvas.move(ent[1], ent[0].x - ent[0].lastX, ent[0].y - ent[0].lastY)
        self.tickCount += 1
        if self.screen == "game_screen":
            self.master.after(10, self.tick)

    def saveScoreExit(self):
        if self.nameEntry.get() == "":
            self.nameEntry.config(bg="red")
        else:
            # Dictionary storing the leader board with names as keys
            ldrBrdDict ={}
            name = self.nameEntry.get()
            try:
                with open("leaderboard.json") as scoreFile:
                    ldrBrdDict = json.load(scoreFile)
                    scoreFile.close()
            except IOError as e:
                print("Leaderboard file not found, creating it instead")
            # Leaderboard should be of the format "name": [highScore, leaderboardPosition]
            # If the user already has an entry in the scoreboard
            if name in ldrBrdDict:
                # If they have got a better score, replace it
                if ldrBrdDict[name][0] < self.player.score:
                    ldrBrdDict[name][0] = self.player.score
            # Otherwise create a new entry with their name and score
            else:
                ldrBrdDict[name] = [self.player.score, 0]
            # Now sort the dictionary by score and assign the leaderboard positions
            scoreArr = sorted(ldrBrdDict.items(), key=lambda j:j[1][0], reverse=True)
            for i in range(len(scoreArr)):
                tup = scoreArr[i]
                ldrBrdDict[tup[0]][1] = i + 1
            with open("leaderboard.json", "w") as scoreFile:
                json.dump(ldrBrdDict, scoreFile)
                scoreFile.close()

        #return to the main menu
        self.switchMainScreenAndDestroy(self.deathFrame)

    def keybindingsScreen(self):
        self.master.unbind("<KeyPress>")
        self.deleteAllWidgets()
        # Create a frame to put all the keybinding things in
        self.keybindingsFrame = tkinter.Frame(self.master)

        #Open or create the file storing the keybindings
        try:
            with open("keybinds.json") as keybindFile:
                self.keybindings = json.load(keybindFile)
                keybindFile.close()
        except IOError as e:
            print("Keybindings file not found, creating it instead")
            # Keybindings follows the scheme "keybindings": [keycode, keysym]
            if platform.system().lower() == "linux":
                self.keybindings = {
                    "forward": [25, "w"],
                    "backward": [39, "s"],
                    "left": [38, "a"],
                    "right": [40, "d"],
                    "shoot": [65, "space"],
                    "pause": [9, "Escape"]
                }   
            else:
                self.keybindings = {
                    "forward": [87, "w"],
                    "backward": [83, "s"],
                    "left": [65, "a"],
                    "right": [68, "d"],
                    "shoot": [32, "space"],
                    "pause": [27, "Escape"]
                }
            
        with open("keybinds.json", "w") as keybindFile:
            json.dump(self.keybindings, keybindFile)
            keybindFile.close()
        counter = 1
        self.keyBindingWidgets = {}
        for key in self.keybindings:
            nameLabel = tkinter.Label(self.keybindingsFrame, text=key + " Key:", font=("Helvetica", 16))
            keyLabel = tkinter.Label(self.keybindingsFrame, text=self.keybindings[key][1], font=("Helvetica", 16))
            keyEntry = tkinter.Button(self.keybindingsFrame, font=("Helvetica", 16), text="Click to rebind")
            keyEntry.config(command=lambda key=key: self.handleEntryClick(key))
            nameLabel.grid(row=counter, column=0)
            keyLabel.grid(row=counter, column=1)
            keyEntry.grid(row=counter, column=2)
            self.keyBindingWidgets[key] = [nameLabel, keyLabel, keyEntry]
            counter += 1

        # forwardLabel = tkinter.Label(self.keybindingsFrame, text="Forward Key:")
        # forwardKey = tkinter.Label(self.keybindingsFrame, text=)
        # self.forwardEntry = tkinter.Button(self.keybindingsFrame, font=("Helvetica", 16), command=lambda: self.handleEntryClick("forward"), text="Click to rebind")
        self.keybindingsFrame.pack()
        # Add a button to return to the main menu
        returnBtn = tkinter.Button(self.master, command=lambda: self.switchMainScreenAndDestroy(self.keybindingsFrame),text="Return to main menu", width=self.buttonW, height=self.buttonH, bg="Gray")
        returnBtn.place(x=self.windowWidth/2, y=self.windowHeight/2, anchor="center")

    # Method handles when a player presses on a keybinding entry to change the keybinding
    def handleEntryClick(self, keyName):
        self.master.bind("<KeyPress>", lambda event: self.handleKeyPress(event, keyName))
        self.master.bind("<Button-1>", lambda event: self.handleLMBClick())
        self.master.config(background="black")
        self.messageLabel = tkinter.Label(self.master, text="PRESS A KEY TO BIND OR LEFT MOUSE BUTTON TO CANCEL", font=("Helvetica", 25), fg="red")
        self.messageLabel.place(x=self.windowWidth/2, y=self.windowHeight/2, anchor="center")

    # Method called when the player presses a key and they have pressed on a keybinding entry
    def handleKeyPress(self, event, keyName):
        # Change the key to whatever they pressed
        self.keybindings[keyName] = [event.keycode, event.keysym]
        self.keyBindingWidgets[keyName][1].config(text=self.keybindings[keyName][1])
        # Save the keybindings
        with open("keybinds.json", "w") as keybindFile:
            json.dump(self.keybindings, keybindFile)
            keybindFile.close()
        self.handleLMBClick()

    # Method called when player presses left mouse button (cancel) when keybinding entry has been pressed
    def handleLMBClick(self):
        self.master.unbind("<KeyPress>")
        self.master.unbind("<Button-1>")
        self.master.config(background="white")
        self.messageLabel.destroy()

    def deleteAllWidgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()
    
    def loadGameScreen(self):
        self.master.unbind("<KeyPress>")
        self.deleteAllWidgets()
        if self.canvas is not None:
            self.canvas.destroy()
        self.screen = "load_game_screen"
        # open/create the file containing the saves
        saves = {}
        try:
            with open("saves.json") as saveFile:
                saves = json.load(saveFile)
                saveFile.close()
        except IOError as e:
            print("Saves file not found, creating it instead")
            # Create a save file they are all level 1
            saves = {"1": [1, 3], "2": [1, 3], "3": [1, 3]}
        with open("saves.json", "w") as saveFile:
            json.dump(saves, saveFile)
            saveFile.close()
        game1 = tkinter.Button(self.master, command=lambda : self.loadSave("1"), text="Load Game 1 | Level: " + str(saves["1"][0]) + " | Lives: " + str(saves["1"][1]), width=self.buttonW,
                                         height=self.buttonH, bg="Gray")
        game2 = tkinter.Button(self.master, command=lambda : self.loadSave("2"), text="Load Game 2 | Level: " + str(saves["2"][0]) + " | Lives: " + str(saves["2"][1]), width=self.buttonW,
                                         height=self.buttonH, bg="Gray")
        game3 = tkinter.Button(self.master, command=lambda : self.loadSave("3"), text="Load Game 3 | Level: " + str(saves["3"][0]) + " | Lives: " + str(saves["3"][1]), width=self.buttonW,
                                         height=self.buttonH, bg="Gray")
        game1.place(x=self.windowWidth * 0.2, y=self.windowHeight/2, anchor="center")
        game2.place(x=self.windowWidth * 0.5, y=self.windowHeight/2, anchor="center")
        game3.place(x=self.windowWidth * 0.8, y=self.windowHeight/2, anchor="center")
        # Add a button to return to main menu
        returnBtn = tkinter.Button(self.master, command=lambda: self.switchMainScreenAndDestroy(), text="Return to main menu", width=self.buttonW, height=self.buttonH, bg="Gray")
        returnBtn.place(x=self.windowWidth / 2, y=self.windowHeight * .7, anchor="center")

    def loadSave(self, saveNum):
        saves = {}
        with open("saves.json", "r") as saveFile:
            saves = json.load(saveFile)
            saveFile.close()
        save = saves[saveNum]
        # Reset the save so the user can't keep reloading it
        level, lives = save[0], save[1]
        saves[saveNum] = [1, 3]
        # Save the saves file
        with open("saves.json", "w") as saveFile:
            json.dump(saves, saveFile)
            saveFile.close()

        self.loadLevel(level, lives)

    def saveGame(self, saveNum):
        # get the saves
        saves = {}
        try:
            with open("saves.json") as saveFile:
                saves = json.load(saveFile)
                saveFile.close()
        except IOError as e:
            print("Saves file not found, creating it instead")
            # Create a save file they are all level 1
            saves = {"1": [1, 3], "2": [1, 3], "3": [1, 3]}
        saves[saveNum][0] = self.player.level
        saves[saveNum][1] = self.player.lives
        with open("saves.json", "w") as saveFile:
            json.dump(saves, saveFile)
            saveFile.close()
        # save the new save
        self.switchMainScreenAndDestroy()

    # method called on the main menu screen to see if the user has got to the cheat code screen
    def handleMainMenuPress(self, event):
        keys = []
        if platform.system().lower() == "linux":
            keys = [111, 116, 113, 114]
        else:
            keys = [38, 40, 37, 39]
        # Up down left right must be pressed in that order to unlock the cheat code screen
        if event.keycode == keys[self.cheatCodeChars]:
            self.cheatCodeChars += 1
        else:
            self.cheatCodeChars = 0
        if self.cheatCodeChars >= 4:
            self.cheatCodeScreen()
            self.cheatCodeChars = 0

    def cheatCodeScreen(self):
        self.deleteAllWidgets()
        self.master.unbind("<KeyPress>")
        self.screen = "cheat_code_screen"
        # button to return to main menu
        mainMenuBtn = tkinter.Button(self.master, command=lambda: self.switchMainScreenAndDestroy(), text="Return to main menu", width=self.buttonW, height=self.buttonH, bg="Gray")
        mainMenuBtn.place(x=self.windowWidth / 2, y=self.windowHeight - 200, anchor="center")
        # Create a cheat code entry
        self.cheatCodeEntry = tkinter.Entry(self.master, bg="Gray", font=("Helvetica", 16), justify=tkinter.CENTER)
        self.cheatCodeEntry.place(x=self.windowWidth/2, y=self.windowHeight/2, anchor="center")
        self.enterCodeBtn = tkinter.Button(self.master, command=lambda: self.checkCheatCode(self.cheatCodeEntry.get()), text="Enter code", width=self.buttonW, height=self.buttonH, bg="Gray")
        self.enterCodeBtn.place(x=self.windowWidth/2, y=self.windowHeight/2 + 100, anchor="center")
        self.cheatCodeLabel = tkinter.Label(self.master, text="Cheat codes:", font=("Helvetica", 16))
        for code in self.cheatCodes:
            self.cheatCodeLabel["text"] += "\n" + code
        self.cheatCodeLabel.place(x=self.windowWidth * 0.8, y=0, anchor="n")
        self.resetCodesBtn = tkinter.Button(self.master, command=lambda: self.resetCheatCodes(), text="Reset cheat codes", width=self.buttonW, height=self.buttonH, bg="Gray")
        self.resetCodesBtn.place(x=self.windowWidth / 2, y=self.windowHeight / 2 - 100, anchor="center")

    def checkCheatCode(self, cheatCode):
        cheatCodes = ["rapid_fire", "super_speed", "no_death", "free_move", "wide_load"]
        if cheatCode in cheatCodes and cheatCode not in self.cheatCodes:
            self.cheatCodeLabel["text"] += "\n" + cheatCode
            self.cheatCodes.append(cheatCode)

    def resetCheatCodes(self):
        self.cheatCodes = []
        self.cheatCodeLabel["text"] = "Cheat codes:"

    def handleBossKey(self, event):
        self.boss = not self.boss
        # If the boss is looking
        if self.boss:
            # Pause the game if the player is playing
            if self.screen == "game_screen":
                self.player.paused = True
                self.paused = True
            self.bossLabel = tkinter.Label(self.master, image=self.bossImage)
            self.bossLabel.place(x=0, y=0, anchor="nw")
            self.master.title("Excel")
        else:
            # Reset everything we changed
            if self.screen == "game_screen":
                self.player.paused = False
                self.paused = False
            self.bossLabel.place_forget()
            self.master.title("Invaders!")

root = tkinter.Tk()
root.geometry("1600x900")
root.title("Invaders!")
root.update()
window = myGUI(root)
window.mainMenuScreen()
root.mainloop()
