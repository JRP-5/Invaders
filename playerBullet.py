class PlayerBullet:
    def __init__(self, x, y, bW, bH, moveSpeed, cheatCodes=[]):
        self.x = x
        self.y = y
        self.lastX = x 
        self.lastY = y
        self.bulletWidth = bW
        self.bulletHeight = bH
        self.moveSpeed = moveSpeed

    def tick(self, entities=[]):
        result = []
        self.lastX = self.x
        self.lastY = self.y
        self.y -= self.moveSpeed
        # If the bullet has gone off the screen
        if self.y < 0:
            # Destroy the bullet
            result.append(["destroy", None])
        return result