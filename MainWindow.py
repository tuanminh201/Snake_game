import Spielfeld as spielfeld
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc


class MainWindow(qtw.QWidget):
    """
    Stackedwidget Indices:
    0: menu
    1: game
    2: settings
    """
    def __init__(self):
        super().__init__()
        scoreLabel = qtw.QLabel("Score: 0\n"
                                "\n"
                                "Mit 'ESC' kann man das Spiel\n"
                                "Pausieren oder Verlassen wenn\n"
                                "es vorbei ist.")
        self.playerlabel = qtw.QLabel("Hallo Player 1")
        self.highscore = qtw.QPushButton("Highscore: 0")

        self.playernameinput = qtw.QLineEdit()
        self.feld = spielfeld.SnakeSpielFeld(scoreLabel, 16)
        self.gamesize = qtw.QSpinBox()

        self.playerlabel_pause = qtw.QLabel("test")
        self.scoredisplay_pause = qtw.QLabel("Dein aktueller Score: " + str(self.feld.snake.fruitseaten))

        self.timer = qtc.QTimer()
        # Initialization Process:
        self.game = qtw.QGridLayout()
        self._gameinit(scoreLabel)

        self.menu = qtw.QGridLayout()
        self._menuinit()

        self.settings = qtw.QGridLayout()
        self._settingsinit()

        self.pause = qtw.QGridLayout()
        self._pauseinit()

        # Use a QStackedWidget to switch quickly between ingame, menu and settings!
        self.stackedwidget = qtw.QStackedWidget(self)
        self.menu_layout_widget = qtw.QWidget()
        self.game_layout_widget = qtw.QWidget()
        self.settings_layout_widget = qtw.QWidget()
        self.pause_layout_widget = qtw.QWidget()

        # Since the QStackedWidget can only switch between Widgets and not layouts we are using a couple QWidgets which
        # each only contain the a layout with the needed Widgets.
        self.menu_layout_widget.setLayout(self.menu)
        self.game_layout_widget.setLayout(self.game)
        self.settings_layout_widget.setLayout(self.settings)
        self.pause_layout_widget.setLayout(self.pause)

        # Add the "Container Widgets" to the QStackedWidget
        self.stackedwidget.addWidget(self.menu_layout_widget)
        self.stackedwidget.addWidget(self.game_layout_widget)
        self.stackedwidget.addWidget(self.settings_layout_widget)
        self.stackedwidget.addWidget(self.pause_layout_widget)

        # select menu as default selectedwidget
        self.stackedwidget.setCurrentIndex(0)
        mainlayout = qtw.QGridLayout()
        mainlayout.addWidget(self.stackedwidget, 0, 0, 1, 1)
        self.setLayout(mainlayout)

    def _gameinit(self, scoreLabel: qtw.QLabel):
        """
        initializes the game widget, score, etc.
        """
        scoreLabel.setAlignment(qtc.Qt.AlignCenter)
        scoreLabel.setStyleSheet("color: 'black'; background: 'white'")
        self.game.addWidget(scoreLabel, 0, 4, 1, 1)

        feld = self.feld
        self.game.addWidget(feld, 0, 0, 1, 3)
        self.game_w = [scoreLabel, feld]

    def _menuinit(self):
        """
        initializes all menu buttons
        """
        highscorebutton = self.highscore  # qtw.QPushButton("Highscore: 0")
        newgamebutton = qtw.QPushButton("New Game")
        quitbutton = qtw.QPushButton("Quit")
        settingsbutton = qtw.QPushButton("Settings")
        highscorebutton.setDisabled(True)

        namedisplay = self.playerlabel
        namedisplay.setFixedWidth(400)
        namedisplay.setFixedHeight(40)
        namedisplay.setStyleSheet("*{background: 'white';}" + "*:hover{background: '#290000;}")
        namedisplay.setAlignment(qtc.Qt.AlignCenter)
        highscorebutton.setFixedWidth(400)
        highscorebutton.setFixedHeight(40)
        newgamebutton.setFixedHeight(40)
        quitbutton.setFixedHeight(40)
        settingsbutton.setFixedHeight(40)
        highscorebutton.setStyleSheet("color: 'black'")
        highscorebutton.setStyleSheet("*{background: 'white';}" + "*:hover{background: '#290000;}")
        newgamebutton.setFixedWidth(400)
        newgamebutton.setStyleSheet("color: 'black'")
        newgamebutton.setStyleSheet("background: 'white'")
        quitbutton.setFixedWidth(400)
        quitbutton.setStyleSheet("color: 'black'")
        quitbutton.setStyleSheet("background: 'white'")
        settingsbutton.setFixedWidth(400)
        settingsbutton.setStyleSheet("color: 'black'")
        settingsbutton.setStyleSheet("background: 'white'")

        newgamebutton.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        quitbutton.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        settingsbutton.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        newgamebutton.clicked.connect(self.gotogame)
        quitbutton.clicked.connect(qtc.QCoreApplication.instance().quit)
        settingsbutton.clicked.connect(self.gotosettings)

        self.menu.addWidget(self.playerlabel, 0, 0, 1, 1)
        self.menu.addWidget(highscorebutton, 1, 0, 1, 1)
        self.menu.addWidget(newgamebutton, 2, 0, 1, 1)
        self.menu.addWidget(settingsbutton, 3, 0, 1, 1)
        self.menu.addWidget(quitbutton, 4, 0, 1, 1)

    def _settingsinit(self):
        """
        initializes all settings buttons
        """
        settingscontainer = qtw.QWidget()
        settingscontainer.setStyleSheet("background: #290000")
        settingscontainer.setFixedWidth(400)
        settingscontainer.setFixedHeight(800)
        settingscontainer.setStyleSheet("color: 'black'")
        settingscontainergrid = qtw.QGridLayout()
        settingscontainergrid.setSpacing(10)
        settingscontainer.setLayout(settingscontainergrid)

        self.wallbutton = qtw.QPushButton()
        self.wallbutton.setFixedWidth(400)
        self.wallbutton.setFixedHeight(40)
        self.wallbutton.setCheckable(True)
        self.wallbutton.setStyleSheet("color: 'black'; background: 'white'; font-weight: bold")
        # wallbutton.setStyleSheet("background: 'white'")
        self.wallbutton.clicked.connect(self.togglesolidWalls)
        self.wallbutton.setText("Solid Walls: off")
        # wallbutton.setStyleSheet("font-weight: bold")

        playernamebutton = qtw.QPushButton("Namen aktualisieren")
        playernamebutton.setFixedWidth(400)
        playernamebutton.setFixedHeight(40)
        playernamebutton.setStyleSheet("color: 'black'")
        playernamebutton.setStyleSheet("background: 'white'")
        playernamebutton.clicked.connect(self.setplayername)

        playernameinput = self.playernameinput
        playernameinput.setText("Gebe hier deinen Namen ein! :)")
        playernameinput.setFixedWidth(400)
        playernameinput.setFixedHeight(40)
        playernameinput.setStyleSheet("color: 'black'")
        playernameinput.setStyleSheet("background: 'white'")
        playernameinput.setAlignment(qtc.Qt.AlignCenter)
        playernameinput.setToolTip("Gebe Hier Deinen Namen ein!")

        self.settings.addWidget(settingscontainer, 0, 0, 1, 1)

        backbutton = qtw.QPushButton("Back")
        backbutton.setFixedWidth(400)
        backbutton.setFixedHeight(40)
        backbutton.setStyleSheet("color: 'black'")
        backbutton.setStyleSheet("background: 'white'")
        backbutton.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        backbutton.clicked.connect(self.gotomenu)

        # gamesize is a QSpinbox
        label1= qtw.QPushButton("Spielfeldgröße")
        label1.setEnabled(False)
        label1.setStyleSheet("background-color: 'white'")
        self.gamesize.setFixedSize(400, 40)
        self.gamesize.setRange(8, 64)
        self.gamesize.setValue(self.feld.length)
        self.gamesize.valueChanged.connect(self.changegamesize)
        self.gamesize.setStyleSheet("color: 'black'; background: 'white'; font-weight: bold")
        self.gamesize.setAlignment(qtc.Qt.AlignCenter)
        self.gamesize.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        self.gamesize.setToolTip("Größe des Spielfeldes")

        spacer = qtw.QWidget()
        spacer.setFixedHeight(40)
        settingscontainergrid.addWidget(self.wallbutton,       0, 0, 1, 1)
        settingscontainergrid.addWidget(playernamebutton, 1, 0, 1, 1)
        settingscontainergrid.addWidget(playernameinput,  2, 0, 1, 1)
        settingscontainergrid.addWidget(label1,           3, 0, 1, 1)
        settingscontainergrid.addWidget(self.gamesize,    4, 0, 1, 1)
        settingscontainergrid.addWidget(spacer,           5, 0, 1, 1)
        settingscontainergrid.addWidget(backbutton,       6, 0, 1, 1)

        self.settings.addWidget(settingscontainer, 0, 0, 1, 1)

    def _pauseinit(self):
        """
        initializes all pausemenu buttons
        """
        scorebutton = self.scoredisplay_pause
        resumebutton = qtw.QPushButton("Resume Game")
        quitbutton = qtw.QPushButton("Quit")
        scorebutton.setDisabled(True)

        self.playerlabel_pause.setFixedWidth(400)
        self.playerlabel_pause.setFixedHeight(40)
        self.playerlabel_pause.setStyleSheet("*{background: 'white';}" + "*:hover{background: '#290000;}")
        self.playerlabel_pause.setAlignment(qtc.Qt.AlignCenter)
        scorebutton.setFixedWidth(400)
        scorebutton.setFixedHeight(40)
        resumebutton.setFixedHeight(40)
        quitbutton.setFixedHeight(40)
        scorebutton.setStyleSheet("color: 'black'")
        scorebutton.setStyleSheet("*{background: 'white';}" + "*:hover{background: '#290000;}")
        scorebutton.setAlignment(qtc.Qt.AlignCenter)
        resumebutton.setFixedWidth(400)
        resumebutton.setStyleSheet("color: 'black'")
        resumebutton.setStyleSheet("background: 'white'")
        quitbutton.setFixedWidth(400)
        quitbutton.setStyleSheet("color: 'black'")
        quitbutton.setStyleSheet("background: 'white'")

        resumebutton.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        quitbutton.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        resumebutton.clicked.connect(self.gotogame)
        quitbutton.clicked.connect(self.gotomenufromgame)

        self.pause.addWidget(self.playerlabel_pause, 0, 0, 1, 1)
        self.pause.addWidget(scorebutton, 1, 0, 1, 1)
        self.pause.addWidget(resumebutton, 2, 0, 1, 1)
        self.pause.addWidget(quitbutton, 3, 0, 1, 1)

    # The Following Three Functions are just here so I don't have to remember the indices :)
    def gotosettings(self):
        self.feld.stoptimer()
        self.stackedwidget.setCurrentIndex(2)

    def gotogame(self):
        self.feld.starttimer()
        self.stackedwidget.setCurrentIndex(1)

    def gotomenu(self):
        self.feld.stoptimer()
        self.highscore.setText("Highscore: " + str(self.feld.highscore))
        self.stackedwidget.setCurrentIndex(0)

    def gotopause(self):
        """
        should only be called while the game is running
        """
        self.scoredisplay_pause.setText("Dein aktueller Score: " + str(self.feld.snake.fruitseaten))
        self.playerlabel_pause.setText(self.playerlabel.text())
        self.feld.stoptimer()
        self.stackedwidget.setCurrentIndex(3)

    def gotomenufromgame(self):
        self.feld.reset()
        self.gotomenu()

    def setplayername(self):
        self.playerlabel.setText("Hallo " + self.playernameinput.text())

    def togglesolidWalls(self):
        self.feld.solidWalls = not self.feld.solidWalls
        if self.feld.solidWalls:
            self.wallbutton.setText("Solid Walls: on")
        else:
            self.wallbutton.setText("Solid Walls: off")


    def changegamesize(self):
        self.feld.changesize(self.gamesize.value())

    def keyPressEvent(self, event):
        if event.key() == qtc.Qt.Key_M:
            if self.feld.gamerunning:
                self.gotopause()
            else:
                self.gotomenu()
        elif event.key() == qtc.Qt.Key_Escape:
            if self.feld.gamerunning:
                self.gotopause()
            elif self.feld.gameended:
                self.gotomenufromgame()
        elif event.key() == qtc.Qt.Key_Up:
            if self.feld.gamerunning and self.feld.direction != 2:
                self.feld.changeddirection = True
                self.feld.direction = 0
        elif event.key() == qtc.Qt.Key_Right:
            if self.feld.gamerunning and self.feld.direction != 3:
                self.feld.changeddirection = True
                self.feld.direction = 1
        elif event.key() == qtc.Qt.Key_Down:
            if self.feld.gamerunning and self.feld.direction != 0:
                self.feld.changeddirection = True
                self.feld.direction = 2
        elif event.key() == qtc.Qt.Key_Left:
            if self.feld.gamerunning and self.feld.direction != 1:
                self.feld.changeddirection = True
                self.feld.direction = 3
