# Author: Kamva Poswa
# 20 June 2024

import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class GuessingGame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent) 
        
        # Set window properties
        self.setWindowTitle("Guessing Game")
        self.setGeometry(150, 150, 600, 400)
        
        # Outer grid layout
        self.outer_grid = QGridLayout()
        self.setLayout(self.outer_grid)
        
        # Inner grid layout
        self.inner_grid = QGridLayout()
        
        # Picture widget
        self.mickey_picture = QLabel()
        self.upload_picture("mickey.gif") 
        
        # Guesses widgets
        self.guess_label = QLabel('Guesses:')
        self.guess_label.setFont(QFont('Times', 14, 100))
        self.edit_line = QLineEdit()
        self.guess_button = QPushButton('Guess')
        self.guess_button.clicked.connect(self.guess_loop)
        
        # Interface widgets
        self.interface_label = QLabel('Interface:')
        self.interface_label.setFont(QFont('Times', 14, 100))
        self.picture_label = QLabel('Picture:')
        self.colour_label = QLabel('Colour:')
        
        self.picture = QComboBox()
        self.picture.addItems(['Mickey', 'Pluto'])
        
        self.colour = QComboBox()
        self.colour.addItems(['Red', 'Blue','white'])
        
        self.change_button = QPushButton('Change')
        self.change_button.clicked.connect(self.handle_interface_change)
        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close)
        self.newgame_button = QPushButton('New Game')
        self.newgame_button.clicked.connect(self.new_game)
        
        # Adding widgets to the inner grid layout
        self.inner_grid.addWidget(self.guess_label, 0, 0)
        self.inner_grid.addWidget(self.interface_label, 5, 0)
        self.inner_grid.addWidget(self.picture_label, 6, 0)
        self.inner_grid.addWidget(self.colour_label, 7, 0)
        self.inner_grid.addWidget(self.close_button, 8, 0)
        self.inner_grid.addWidget(self.edit_line, 4, 1)
        self.inner_grid.addWidget(self.picture, 6, 1)
        self.inner_grid.addWidget(self.colour, 7, 1)
        self.inner_grid.addWidget(self.newgame_button, 8, 1)
        self.inner_grid.addWidget(self.guess_button, 4, 2)
        self.inner_grid.addWidget(self.change_button, 7, 2)
        
        # Label to display the number of guesses
        self.num_guesses_label = QLabel('Number of guesses: 0')
        self.inner_grid.addWidget(self.num_guesses_label, 9, 0, 1, 2)
        
        # Adding widgets to the outer grid layout
        self.outer_grid.addWidget(self.mickey_picture, 0, 0)
        self.outer_grid.addLayout(self.inner_grid, 0, 1)
        
        # Initialize game variables
        self.target_number = random.randint(1, 10)
        self.guess_count = 0
        self.feedback_label = QLabel('')
        self.inner_grid.addWidget(self.feedback_label, 10, 0, 1, 3)
    
    def upload_picture(self, filename):
        pix = QPixmap(filename)
        self.mickey_picture.setPixmap(pix)
        
    def guess_loop(self):
        guess = self.edit_line.text()
        if guess.isdigit():
            guess = int(guess)
            feedback = self.check_guess(guess)
            self.upload_feedback(guess, feedback)
            if feedback == "Correct":
                self.end_game()
        else:
            self.feedback_label.setText("Invalid guess")
        self.num_guesses_label.setText(f'Number of guesses: {self.guess_count}')
            
    def check_guess(self, guess):
        self.guess_count += 1
        if guess == self.target_number:
            return "Correct"
        elif guess < self.target_number:
            return "Too small"
        else:
            return "Too big"
    
    def upload_feedback(self, guess, feedback):
        self.feedback_label.setText(f'Your guess: {guess} is {feedback}')
        if feedback == "Correct":
            label_guess = QLabel(str(guess))
            label_feedback = QLabel(feedback)
            self.inner_grid.addWidget(label_guess, self.guess_count, 1)
            self.inner_grid.addWidget(label_feedback, self.guess_count, 2)
    
    def handle_interface_change(self):
        selected_picture = self.picture.currentText()
        if selected_picture == 'Mickey':
            self.upload_picture("mickey.gif")
        elif selected_picture == 'Pluto':
            self.upload_picture("pluto.gif")
        
        selected_colour = self.colour.currentText()
        self.setStyleSheet("background-color: " + selected_colour.lower())
    
    def new_game(self):
        self.target_number = random.randint(1, 10)
        self.guess_count = 0
        self.edit_line.clear()
        for i in range(1, 4):
            widget_item = self.inner_grid.itemAtPosition(i, 1)
            if widget_item is not None:
                widget = widget_item.widget()
                if widget is not None:
                    widget.clear()
            widget_item = self.inner_grid.itemAtPosition(i, 2)
            if widget_item is not None:
                widget = widget_item.widget()
                if widget is not None:
                    widget.clear()
    
    def end_game(self):
        self.guess_button.setEnabled(False)
        self.edit_line.setEnabled(False)
        self.newgame_button.setEnabled(True)    

def main():
    app = QApplication(sys.argv)
    widget = GuessingGame()
    widget.show()
    sys.exit(app.exec_())

main()