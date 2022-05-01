from tkinter import Canvas
import cv2 as cv
import numpy as np

class Fox():
    def __init__(self,line,char) -> None:
        self.MAX_ROW=line
        self.MAX_COLUMN=char*2
        self.row=0
        self.column=0
        
        self.canvas=np.zeros((self.MAX_ROW*64+40,self.MAX_COLUMN*14+40,1), np.uint8)
        self.canvas.fill(255)
    
    def check_position(self, next_character_num):
        if self.row >= self.MAX_ROW or self.column >= self.MAX_COLUMN:
            self.save("output.jpg")
            raise Exception("Canvas out of space, finish drawing!")
        if next_character_num > self.MAX_COLUMN:
            self.save("output.jpg")
            raise Exception("Word too long, finish drawing!")
        if next_character_num+self.column > self.MAX_COLUMN:
            self.row+=1
            self.column=0
            if self.row >= self.MAX_ROW:
                self.save("output.jpg")
                raise Exception("Canvas out of space, finish drawing!")

    def do_draw_character(self,canvas,color,origin_x,origin_y,character_code):
        if character_code & 0b00000000000001:
            cv.line(canvas,(origin_x+28,origin_y+16),(origin_x+14,origin_y+8),color,1,cv.LINE_AA)
        if character_code & 0b00000000000010:
            cv.line(canvas,(origin_x+14,origin_y+8),(origin_x+0,origin_y+16),color,1,cv.LINE_AA)
        if character_code & 0b00000000000100:
            cv.line(canvas,(origin_x+0,origin_y+16),(origin_x+0,origin_y+32),color,1,cv.LINE_AA)
        if character_code & 0b00000000001000:
            cv.line(canvas,(origin_x+0,origin_y+40),(origin_x+0,origin_y+48),color,1,cv.LINE_AA)
        if character_code & 0b00000000010000:
            cv.line(canvas,(origin_x+0,origin_y+48),(origin_x+14,origin_y+56),color,1,cv.LINE_AA)
        if character_code & 0b00000000100000:
            cv.line(canvas,(origin_x+14,origin_y+56),(origin_x+28,origin_y+48),color,1,cv.LINE_AA)
        if character_code & 0b00000001000000:
            cv.line(canvas,(origin_x+14,origin_y+24),(origin_x+28,origin_y+16),color,1,cv.LINE_AA)
        if character_code & 0b00000010000000:
            cv.line(canvas,(origin_x+14,origin_y+24),(origin_x+14,origin_y+8),color,1,cv.LINE_AA)
        if character_code & 0b00000100000000:
            cv.line(canvas,(origin_x+14,origin_y+24),(origin_x+0,origin_y+16),color,1,cv.LINE_AA)
        if character_code & 0b00001000000000:
            cv.line(canvas,(origin_x+14,origin_y+40),(origin_x+0,origin_y+48),color,1,cv.LINE_AA)
        if character_code & 0b00010000000000:
            cv.line(canvas,(origin_x+14,origin_y+40),(origin_x+14,origin_y+56),color,1,cv.LINE_AA)
        if character_code & 0b00100000000000:
            cv.line(canvas,(origin_x+14,origin_y+40),(origin_x+28,origin_y+48),color,1,cv.LINE_AA)
        if character_code & 0b01000000000000:
            cv.line(canvas,(origin_x+14,origin_y+24),(origin_x+14,origin_y+32),color,1,cv.LINE_AA)
        if character_code & 0b10000000000000:
            cv.circle(canvas,(origin_x+14,origin_y+59),3,color,1,cv.LINE_AA)
        cv.line(canvas,(origin_x+0,origin_y+32),(origin_x+28,origin_y+32),color,1,cv.LINE_AA)
    
    def draw_character(self,character_code):
        self.do_draw_character(self.canvas,0,self.column*14+20,self.row*64+20,character_code)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    def draw_space(self):
        if self.column==0:
            return
        self.column+=1
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    def draw_newline(self):
        self.column=0
        self.row+=1
    
    def draw_comma(self):
        self.check_position(2)
        cv.putText (self.canvas, ',' ,(self.column*14+20+9,self.row*64+20+36), cv.FONT_HERSHEY_PLAIN, 2,1,1,cv.LINE_AA)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    def draw_full_stop(self):
        self.check_position(2)
        cv.putText (self.canvas, '.' ,(self.column*14+20+9,self.row*64+20+36), cv.FONT_HERSHEY_PLAIN, 2,1,1,cv.LINE_AA)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    def draw_exclamation_mark(self):
        self.check_position(2)
        cv.putText (self.canvas, '!' ,(self.column*14+20+9,self.row*64+20+42), cv.FONT_HERSHEY_PLAIN, 2,1,1,cv.LINE_AA)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    def draw_question_mark(self):
        self.check_position(2)
        cv.putText (self.canvas, '?' ,(self.column*14+20+6,self.row*64+20+42), cv.FONT_HERSHEY_PLAIN, 2,1,1,cv.LINE_AA)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1

    def draw_word(self,code_list):
        self.check_position(len(code_list)*2)
        for code in code_list:
            self.draw_character(code)

    def draw(self,rune_list):
        for item in rune_list:
            if isinstance(item,list):
                self.draw_word(item)
            elif item == -1:
                self.draw_space()
            elif item == -2:
                self.draw_comma()
            elif item == -3:
                self.draw_full_stop()
            elif item == -4:
                self.draw_exclamation_mark()
            elif item == -5:
                self.draw_question_mark()
            elif item == -10:
                self.draw_newline()

    
    def save(self,path):
        cv.imwrite(path, self.canvas)
