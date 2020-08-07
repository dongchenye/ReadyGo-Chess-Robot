#!/usr/bin/env python
# coding: utf-8

from playsound import playsound
class Speaker:

    def __init__(self,test_flag):
        self.test_flag = test_flag

    def inCheck(self):
        '''
        Plays audio and alerts user they are in check
        '''
        playsound('wavAudioFiles/YouAreInCheck.wav')
        if self.test_flag:
            print("Audio: You are in Check")
    
    def ReadyGoMoveError(self):
        '''
        Plays audio and alerts user that the move they made is not the same as the ReadyGo requested
        '''
        playsound('wavAudioFiles/IncorrectReadyGoMove.wav')
        if self.test_flag:
            print("Audio: That was not the correct ReadyGo move, please try again.")
            
    def PlayerMoveError(self):
        '''
        Plays audio and alerts the user they made an invalid move
        '''
        playsound('wavAudioFiles/IllegalUserMove.wav')
        if self.test_flag:
            print("Audio: This is an invaild move, please try again.")            
 
            
    def GameOver(self, winner):
        '''
        Play audio and announce the winner. The value of 'winner' will be either "You win!" or "ReadyGo Wins!""
        '''
        if winner == "You win!":
            playsound('wavAudioFiles/YouWin.wav')
            pass
        else:
            playsound('wavAudioFiles/ReadyGoWins.wav')
            pass
        
        if self.test_flag:
            print("Audio:",winner)
