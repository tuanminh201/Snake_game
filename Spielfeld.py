from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from LinkedList import Snake, CoordinateDLL
import random


class SnakeSpielFeld(qtw.QLabel):
    """
    self.timer:
    self.image:
    self.direction:
    self.gamerunning:
    self.snake:
    """
    def __init__(self, scoreLabel: qtw.QLabel, length=10):
        self.SPIELFELDFARBE = qtg.QColor(66, 66, 66)
        self.SNAKEFARBE = qtg.QColor(61, 235, 52)
        self.FRUCHTFARBE = qtg.QColor(101, 52, 235)
        super().__init__()
        # self.setFixedSize(500, 500)
        self.image = qtg.QImage(length, length, qtg.QImage.Format_RGBA8888)
        self.image.fill(self.SPIELFELDFARBE)
        # refresh pixels
        self.refresh()

        self.timer = qtc.QTimer()
        # Manipulate snake function below
        self.timer.timeout.connect(self.tick)

        self.highscore = 0
        self.scoreLabel = scoreLabel
        self.timerspeed = 250
        self.solidWalls = False
        self.changeddirection = False
        self.fruitsspawned = 0
        self.length = length
        self.direction = 0
        self.gamerunning = False
        self.gameended = False
        # spawn initial snake
        self.spawnnewsnake()
    def spawnnewsnake(self):
        """
        spawns a snake into the game.
        """
        startx = self.length // 2
        starty = self.length // 2
        self.snake = Snake(CoordinateDLL(startx, starty))
        self.image.setPixelColor(startx, starty, self.SNAKEFARBE)

    def refresh(self):
        """
        refreshes the diplayed pixels!
        """
        self.setPixmap(qtg.QPixmap.fromImage(self.image).scaled(self.size(), qtc.Qt.KeepAspectRatio))

    def stoptimer(self):
        self.timer.stop()
        self.gamerunning = False

    def starttimer(self, initial_interval= 250):
        # Call snakespeed to check for amount of fruitseaten to increase snake speed and difficulty
        initial_interval = self.snakespeed(self.snake.fruitseaten)
        self.timer.start(initial_interval)
        self.timerspeed = initial_interval
        self.gamerunning = True
        print(self.snakespeed(self.snake.fruitseaten))


    def snakespeed(self, fruitseaten):
        if int(fruitseaten) < 1:
            return 250
        elif int(fruitseaten) < 2:
            return 230
        elif int(fruitseaten) < 4:
            return 200
        elif int(fruitseaten) < 6:
            return 180
        elif int(fruitseaten) < 8:
            return 150
        elif int(fruitseaten) < 10:
            return 100
        elif int(fruitseaten) < 12:
            return 50
        else:
            return 40


    def reset(self):
        """
        setzt spielfeld zurueck
        """
        self.image = qtg.QImage(self.length, self.length, qtg.QImage.Format_RGBA8888)
        self.image.fill(self.SPIELFELDFARBE)
        self.spawnnewsnake()
        self.gameended = False
        self.refresh()
        self.direction = 0

    def changesize(self, length):
        """
        aendert spielfeldgroeße
        """
        self.length = length
        self.reset()

    def movesnake(self):
        currheadpos = self.snake.head
        currlastpos = self.snake.last
        if self.direction == 0:
            nextpos = CoordinateDLL(currheadpos.x, currheadpos.y - 1)
        elif self.direction == 1:
            nextpos = CoordinateDLL(currheadpos.x + 1, currheadpos.y)
        elif self.direction == 2:
            nextpos = CoordinateDLL(currheadpos.x, currheadpos.y + 1)
        else:
            nextpos = CoordinateDLL(currheadpos.x - 1, currheadpos.y)
        nextposcolor = self.getpixRGB(nextpos.x, nextpos.y)

        maxx = self.length - 1
        if 0 <= nextpos.x <= maxx and 0 <= nextpos.y <= maxx:
            # nextpos gueltig
            if nextposcolor == self.SPIELFELDFARBE:
                self.snake.move(nextpos)
            elif nextposcolor == self.FRUCHTFARBE:
                self.snake.ate(nextpos)
                self.stoptimer()
                self.starttimer()
            elif nextposcolor == self.SNAKEFARBE:
                self.gameover()
        else:
            if self.solidWalls:
                self.gameover()
            else:
                newnextpos = CoordinateDLL(nextpos.x % self.length, nextpos.y % self.length)
                self.snake.move(newnextpos)
        self.image.setPixelColor(currlastpos.x, currlastpos.y, self.SPIELFELDFARBE)
        self.image.setPixelColor(self.snake.head.x, self.snake.head.y, self.SNAKEFARBE)

    def gameover(self):
        if self.snake.fruitseaten > self.highscore:
            self.highscore = self.snake.fruitseaten
        self.stoptimer()
        self.gamerunning = False
        self.gameended = True
        messagebox = qtw.QMessageBox()
        messagebox.setWindowTitle("Game Over!")
        messagebox.setText("Dein Score: " + str(self.snake.fruitseaten))
        executable = messagebox.exec_()
        self.gameover.has_been_called = True

    def getpixRGB(self, x, y):
        qcolortemp = self.image.pixel(x, y)
        red = qtg.qRed(qcolortemp)
        green = qtg.qGreen(qcolortemp)
        blue = qtg.qBlue(qcolortemp)
        return qtg.QColor(red, green, blue)

    def tick(self):
        """
        manipulates the self.image variable in a way that the snake does a single move.
        """
        self.movesnake()
        self.spawnFood()
        self.scoreLabel.setText("Score: " + str(self.snake.fruitseaten) + "\n"
                                "\n"
                                "Mit 'ESC' kann man das Spiel\n"
                                "Pausieren oder Verlassen wenn\n"
                                "es vorbei ist.")
        self.refresh()
        self.changeddirection = False

    def spawnFood(self):
        zahl = random.randint(1, 15)
        if zahl == 1 and (self.fruitsspawned - self.snake.fruitseaten) < 10:
            while True:  # fruitx in Snake and fruity in Snake
                # Potentielle Endlosschleife? oder sehr langsam wenn Snake sehr lang?
                fruitx = random.randint(0, self.length - 1)
                fruity = random.randint(0, self.length - 1)
                rgb = self.getpixRGB(fruitx, fruity)
                if rgb == self.SPIELFELDFARBE:
                    break
            self.image.setPixelColor(fruitx, fruity, self.FRUCHTFARBE)
            self.fruitsspawned += 1
