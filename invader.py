import random
import math
import playerBullet


class Invader:
    def __init__(self, x, y, moveSpeed, minX, maxX, invaderImage, row, level):
        self.x = x
        self.y = y
        self.lastX = x
        self.lastY = y
        self.minX = minX
        self.maxX = maxX
        self.moveSpeed = moveSpeed
        self.invaderImage = invaderImage
        self.row = row
        self.level = level
        self.down =False

    def tick(self, entities=[]):
        result = []
        self.lastX = self.x
        self.lastY = self.y
        self.x += self.moveSpeed
        # Checking if the invader should change direction
        if self.x > self.maxX or self.x < self.minX:
            result.append(["chgDir", self.row])
        # Check if the invader has been hit by one of the player's bullets
        for ent in entities:
            if isinstance(ent[0], playerBullet.PlayerBullet):
                # Compare the player's bullet and the invader to see if they're colliding
                if ent[0].x - ent[0].bulletWidth/2 <= self.x + self.invaderImage.width()/2 and ent[0].x + ent[0].bulletWidth/2 >= self.x - self.invaderImage.width()/2 and ent[0].y - ent[0].bulletHeight/2 <= self.y + self.invaderImage.height()/2 and ent[0].y + ent[0].bulletHeight/2 >= self.y - self.invaderImage.height()/2:
                    result.append(["destroy", None])
        # Move down if reached end of row and changed direction
        if self.down:
            self.y += 20
            self.down = False

        # The invader should shoot
        if random.randint(0, math.floor(1200 * (0.8 ** (self.level-1)))) == 0:
            # Tell the main function to shoot
            result.append(["shoot", None])

        return result

    def changeDir(self):
        self.moveSpeed = -1*self.moveSpeed
        self.down = True

