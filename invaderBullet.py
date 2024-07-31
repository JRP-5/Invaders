# class reprsents a bullet from an invader
class InvaderBullet:
    def __init__(self, x, y, bW, bH, xVel, yVel, screenHeight):
        self.x = x
        self.y = y
        self.lastX = x
        self.lastY = y
        self.bulletWidth = bW
        self.bulletHeight = bH
        self.xVel = xVel
        self.yVel = yVel
        self.screenHeight = screenHeight

    def tick(self, entities=[]):
        result = []
        self.lastX = self.x
        self.lastY = self.y
        self.y += self.yVel
        # If the bullet has gone off the screen
        if self.y > self.screenHeight:
            # Destroy the bullet
            result.append(["destroy", None])

        return result