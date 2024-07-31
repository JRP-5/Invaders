import invaderBullet
import json
import platform

class Player:

    def __init__(self, x, y, moveSpeed, minY, screenWidth, screenHeight, playerIm, cheatCodes=[]):
        self.x = x
        self.y = y
        self.minY = 0 if "free_move" in cheatCodes else minY
        self.maxY = screenHeight
        self.minX = 0
        self.maxX = screenWidth
        # velocity x and y represent how fast the player should move when pressing the movement keys
        self.velX = moveSpeed * 5 if "super_speed" in cheatCodes else moveSpeed
        self.velY = moveSpeed * 5 if "super_speed" in cheatCodes else moveSpeed
        self.lastX = 0
        self.lastY = 0
        self.lives = 3
        # Read in the keybindings from a file
        try:
            with open("keybinds.json") as keybindFile:
                self.keybindings = json.load(keybindFile)
                keybindFile.close()
        except IOError as e:
            print("Keybindings file not found, using defaults instead")
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
        # Use a dictionary to store keys and their state
        self.forwardKey = self.keybindings["forward"][0]
        self.backwardKey = self.keybindings["backward"][0]
        self.leftKey = self.keybindings["left"][0]
        self.rightKey = self.keybindings["right"][0]
        self.shootKey = self.keybindings["shoot"][0]
        # The pause Key is set as the escape key
        self.pauseKey = self.keybindings["pause"][0]
        self.keys = {self.forwardKey: False, self.backwardKey: False, self.leftKey: False, self.rightKey: False, self.shootKey: False, self.pauseKey: False}
        self.shootCooldown = 0
        self.isAlive = True
        # Indicates whether the player has the game paused or not
        self.paused = False
        self.playerImage = playerIm
        self.score = 0
        self.level = 1
        self.cheatCodes = cheatCodes

    def keyUp(self, event):
        if event.keycode in self.keys:
            self.keys[event.keycode] = False

    def keyDown(self, event):
        if event.keycode in self.keys:
            self.keys[event.keycode] = True
        # Because pausing is slightly different to movement we process it here
        if event.keycode == self.pauseKey:
            self.paused = not self.paused

    def tickPlayer(self, entities=[]):
        result = []
        self.lastX = self.x
        self.lastY = self.y
        if self.keys[self.forwardKey]:
            self.y -= self.velY
        if self.keys[self.backwardKey]:
            self.y += self.velY
        if self.keys[self.leftKey]:
            self.x -= self.velX
        if self.keys[self.rightKey]:
            self.x += self.velX

        # Ensuring the player hasn't moved out of their area
        if self.y < self.minY:
            self.y += self.velY
        if self.y > self.maxY:
            self.y -= self.velY
        if self.x < self.minX:
            self.x += self.velX
        if self.x > self.maxX:
            self.x -= self.velX

        # Decrease the shoot cooldown
        self.shootCooldown -= 1
        # Detect and process the player shooting
        if self.keys[self.shootKey] and self.shootCooldown <= 0:
            # Add a cooldown so the player cannot constantly shoot
            self.shootCooldown = 4 if "rapid_fire" in self.cheatCodes else 60
            result.append(["shoot", None])

        if "no_death" not in self.cheatCodes:
            # Check against every invader bullet to see if the player has been hit
            for ent in entities:
                # If the entity is an invader bullet
                if isinstance(ent[0], invaderBullet.InvaderBullet):
                    if ent[0].x - ent[0].bulletWidth/2 <= self.x + self.playerImage.width()/2 and ent[0].x + ent[0].bulletWidth/2 >= self.x - self.playerImage.width()/2 and ent[0].y - ent[0].bulletHeight/2 <= self.y + self.playerImage.height()/2 and ent[0].y + ent[0].bulletHeight/2 >= self.y - self.playerImage.height()/2:
                        # Decrease the player's lives and destroy the bullet that hit them
                        self.lives -= 1
                        result.append(["destroy", ent])

        return result

    def setPaused(self, bool):
        self.paused = bool

    # Method increases the player's score when they kill an invader
    def incrementScore(self):
        self.score += self.level
