import cv2 as cv
import numpy as np
import base64

class Fox():
    #init canvas
    def __init__(self,line,char) -> None:
        self.MAX_ROW=line
        self.MAX_COLUMN=char*2
        self.row=0
        self.column=0
        
        self.canvas=np.zeros((self.MAX_ROW*64+40,self.MAX_COLUMN*14+40,1), np.uint8)
        self.canvas.fill(255)
    
    #create new canvas
    def refresh(self,line,char): 
        self.MAX_ROW=line
        self.MAX_COLUMN=char*2
        self.row=0
        self.column=0
        
        self.canvas=np.zeros((self.MAX_ROW*64+40,self.MAX_COLUMN*14+40,1), np.uint8)
        self.canvas.fill(255)
    
    #check if the character to be painted will still be in the canvas, if not, try line feed or raise exception
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

    #function to draw tonic character
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
    
    #function to draw tonic character(1 tonic chatacter = 2 columns width)
    def draw_character(self,character_code):
        self.do_draw_character(self.canvas,0,self.column*14+20,self.row*64+20,character_code)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    #function to draw space(1 space = 1 columns width)
    def draw_space(self):
        if self.column==0:
            return
        self.column+=1
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    #function to switch to a new line
    def draw_newline(self):
        self.column=0
        self.row+=1
    
    #function to draw ,(1 , = 2 columns width)
    def draw_comma(self):
        self.check_position(2)
        cv.putText (self.canvas, ',' ,(self.column*14+20+9,self.row*64+20+36), cv.FONT_HERSHEY_PLAIN, 2,1,1,cv.LINE_AA)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    #function to draw .(1 . = 2 columns width)
    def draw_full_stop(self):
        self.check_position(2)
        cv.putText (self.canvas, '.' ,(self.column*14+20+9,self.row*64+20+36), cv.FONT_HERSHEY_PLAIN, 2,1,1,cv.LINE_AA)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    #function to draw !(1 ! = 2 columns width)
    def draw_exclamation_mark(self):
        self.check_position(2)
        cv.putText (self.canvas, '!' ,(self.column*14+20+9,self.row*64+20+42), cv.FONT_HERSHEY_PLAIN, 2,1,1,cv.LINE_AA)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1
    
    #function to draw ?(1 ? = 2 columns width)
    def draw_question_mark(self):
        self.check_position(2)
        cv.putText (self.canvas, '?' ,(self.column*14+20+6,self.row*64+20+42), cv.FONT_HERSHEY_PLAIN, 2,1,1,cv.LINE_AA)
        self.column+=2
        if self.column>=self.MAX_COLUMN:
            self.column=0
            self.row+=1

    #function to draw a sequence of tunic charactors
    def draw_word(self,code_list):
        self.check_position(len(code_list)*2)
        for code in code_list:
            self.draw_character(code)

    #function to draw a paragraph
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

    #convert canvas to base64 stream
    def to_base64(self):
        image = cv.imencode('.jpg', self.canvas)[1]
        image_code = str(base64.b64encode(image))[2:-1]
        return image_code

    #save the canvas as an image
    def save(self,path):
        cv.imwrite(path, self.canvas)
