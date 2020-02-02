from PIL import Image , ImageDraw , ImageFilter , ImageFont
import math
# width , height = 1000,1000
# r = 150
# mid_x  , mid_y = width/2 , height/2
# image = Image.new("RGBA" , (width,height))
#image = Image.open("./manager/template.png")



class lightTheme:
    def __init__(self , template , attendance, name):
        self.compression_ratio = 0.4
        self.fontColor = (23, 23, 23)
        self.name = name
        self.font = ImageFont.truetype("./manager/BROWNIEregular.otf" , 74)
        self.attendance = attendance
        self.radius = 115
        self.template = template
        self.image = Image.open(template)
        self.draw = ImageDraw.Draw(self.image)
        self.width , self.height = self.image.size
        # in the form : (circle_x , circle_y , text_x , text_y , perc_x , perc_y)
        self.subject_coords = [(140 ,938 , 140 , 1187 , 225 , 1019) , (429,938 , 429 , 1187 , 510 ,1019 ) , (717 ,938 , 717 , 1187 , 795 , 1019),
                               (140 ,1276 , 140 , 1522 , 225 , 1360) , (429,1276 , 429 , 1522 , 510 , 1360) , (717 ,1276, 717 , 1522 ,795 , 1360),
                               (140 ,1626 , 140 , 1872 , 225,1711) , (429,1626 , 429 , 1872 , 510 , 1711) , (717 ,1626 , 717 , 1872 , 795 , 1711) ]


    def centerText(self , text):
        maxSize = 14
        initials = "".join([i[0] for i in text.split(" ") if i[0].isupper()])
        if(len(text)+len(initials) > maxSize):
            return text[:maxSize-len(initials)-2]+".."+"("+str(initials)+")"
        else:
            remain = maxSize - len(text) - len(initials) - 2
            padding = math.ceil(remain/2)
            return (" "*padding)+text+"("+initials+")"+(" "*padding)

    def getColor(self , att_perc):
        if(int(att_perc)>75):
            return (10, 189, 227,255)
        else:
            return (238, 82, 83,255)


    def draw_pie(self , x , y ,tx , ty ,px , py,radius ,  ratio , data):
        font1 = ImageFont.truetype("./manager/manager/CallingCode-Regular.otf" , 25)
        font2 = ImageFont.truetype("./manager/manager/CallingCode-Regular.otf" , 50)
        self.draw = ImageDraw.Draw(self.image)
        r = radius
        attended , bunked , subject = data[0] , data[1] , self.centerText(data[2])
        self.draw.text((tx , ty),subject,fill = self.fontColor,font=font1)
        total = attended+bunked
        att_perc = attended/total
        bun_perc = bunked/total
        att_start = 0
        att_end =  att_perc * 360
        bun_start = att_end
        bun_end = 360
        outer_radius = 10
        origin_x , origin_y = x+r , y+r
        #OUTER
        self.draw.pieslice([(x, y ),(x + 2*r, y + 2*r)] , att_start , att_end , fill=(10, 189, 227,255))
        self.draw.pieslice([(x, y ),(x + 2*r, y + 2*r)] , bun_start , bun_end , fill=(238, 82, 83,255))#BUNKED
        #INNER
        self.draw.pieslice([(x+outer_radius, y+outer_radius ),(x + 2*r - outer_radius, y + 2*r - outer_radius)] , att_start , att_end , fill=(72, 219, 251,255))#ATTENDED
        self.draw.pieslice([(x+outer_radius, y+outer_radius ),(x + 2*r - outer_radius, y + 2*r - outer_radius)] , bun_start , bun_end , fill=(255, 107, 107,255))#BUNKED
        self.draw.ellipse([(x + (radius*ratio), y + (radius*ratio)),(x + (2*r) - (radius*ratio), y + (2*r) - (radius*ratio))] , fill=(255,255,255,255))
        self.draw.text((px , py),str(attended),fill = self.getColor(attended),font=font2)
        del self.draw
        
    def loadPieCharts(self):
        i = 0
        for x , y , t_x , t_y , p_x , p_y in self.subject_coords:
            if(i<len(self.attendance)):
                self.draw_pie(x = x, y = y ,tx = t_x , ty = t_y,px = p_x , py = p_y ,radius = self.radius , ratio = 0.4 , data = self.attendance[i])
                i+=1
    def generateName(self):
        self.draw = ImageDraw.Draw(self.image)
        concatName = self.name[:15]
        concatName += "..." if len(concatName)>=15 else ""
        self.draw.text((64, 708),concatName,fill = self.fontColor,font=self.font)

    def saveImage(self , file_name = "temp.png"):
        self.image = self.image.resize((math.floor(self.width*self.compression_ratio),math.floor(self.height*self.compression_ratio)),Image.ANTIALIAS)
        self.image.save(file_name , optimize=True,quality=95)

    def getCompressed(self):
        self.image = self.image.resize((math.floor(self.width*self.compression_ratio),math.floor(self.height*self.compression_ratio)),Image.ANTIALIAS)
        return self.image

    def loadProfilePic(self , path):
        profPic = Image.open(path)
        profPic = profPic.resize((280,310))
        mask = Image.new("RGBA", (self.width , self.height),(0))
        drawMask = ImageDraw.Draw(mask)
        drawMask.ellipse((405, 289, 676, 560), fill=(255,255,255,255))
        background = Image.new("RGBA", (self.width , self.height),(255,255,255,255))
        background.paste(profPic , (400, 290))
        self.image = Image.composite(background,self.image, mask)


class darkTheme:
    def __init__(self , template , attendance, name):
        self.compression_ratio = 0.4
        self.fontColor = (240,240,240)
        self.name = name
        self.font = ImageFont.truetype("./manager/BROWNIEregular.otf" , 74)
        self.attendance = attendance
        self.radius = 115
        self.template = template
        self.image = Image.open(template)
        self.draw = ImageDraw.Draw(self.image)
        self.width , self.height = self.image.size
        # in the form : (circle_x , circle_y , text_x , text_y , perc_x , perc_y)
        self.subject_coords = [(140 ,938 , 140 , 1187 , 225 , 1019) , (429,938 , 429 , 1187 , 510 ,1019 ) , (717 ,938 , 717 , 1187 , 795 , 1019),
                               (140 ,1276 , 140 , 1522 , 225 , 1360) , (429,1276 , 429 , 1522 , 510 , 1360) , (717 ,1276, 717 , 1522 ,795 , 1360),
                               (140 ,1626 , 140 , 1872 , 225,1711) , (429,1626 , 429 , 1872 , 510 , 1711) , (717 ,1626 , 717 , 1872 , 795 , 1711) ]


    def centerText(self , text):
        maxSize = 14
        initials = "".join([i[0] for i in text.split(" ")])
        if(len(text)+len(initials) > maxSize):
            return text[:maxSize-len(initials)-2]+".."+"("+str(initials)+")"
        else:
            remain = maxSize - len(text) - len(initials) - 2
            padding = math.ceil(remain/2)
            return (" "*padding)+text+"("+initials+")"+(" "*padding)

    def getColor(self , att_perc):
        if(int(att_perc)>75):
            return (23, 212, 117,255)
        else:
            return (238, 82, 83,255)
            
    def draw_pie(self , x , y ,tx , ty ,px , py,radius ,  ratio , data):
        font1 = ImageFont.truetype("./manager/CallingCode-Regular.otf" , 25)
        font2 = ImageFont.truetype("./manager/CallingCode-Regular.otf" , 50)
        self.draw = ImageDraw.Draw(self.image)
        r = radius
        attended , bunked , subject = data[0] , data[1] , self.centerText(data[2])
        self.draw.text((tx , ty),subject,fill = self.fontColor,font=font1)
        total = attended+bunked
        att_perc = attended/total
        bun_perc = bunked/total
        att_start = 0
        att_end =  att_perc * 360
        bun_start = att_end
        bun_end = 360
        outer_radius = 10
        origin_x , origin_y = x+r , y+r
        #OUTER
        self.draw.pieslice([(x, y ),(x + 2*r, y + 2*r)] , att_start , att_end , fill=(10, 189, 227,255))#ATTENDED
        self.draw.pieslice([(x, y ),(x + 2*r, y + 2*r)] , bun_start , bun_end , fill=(238, 82, 83,255))#BUNKED
        #INNER
        self.draw.pieslice([(x+outer_radius, y+outer_radius ),(x + 2*r - outer_radius, y + 2*r - outer_radius)] , att_start , att_end , fill=(72, 219, 251,255))#ATTENDED
        self.draw.pieslice([(x+outer_radius, y+outer_radius ),(x + 2*r - outer_radius, y + 2*r - outer_radius)] , bun_start , bun_end , fill=(255, 107, 107,255))#BUNKED
        self.draw.ellipse([(x + (radius*ratio), y + (radius*ratio)),(x + (2*r) - (radius*ratio), y + (2*r) - (radius*ratio))] , fill=(33,33,33,0))
        self.draw.text((px , py),str(attended),fill = self.getColor(attended),font=font2)
        del self.draw
        
    def loadPieCharts(self):
        i = 0
        for x , y , t_x , t_y , p_x , p_y in self.subject_coords:
            if(i<len(self.attendance)):
                self.draw_pie(x = x, y = y ,tx = t_x , ty = t_y,px = p_x , py = p_y ,radius = self.radius , ratio = 0.4 , data = self.attendance[i])
                i+=1
    def generateName(self):
        self.draw = ImageDraw.Draw(self.image)
        concatName = self.name[:15]
        concatName += "..." if len(concatName)>=15 else ""
        self.draw.text((64, 708),concatName,fill = self.fontColor,font=self.font)

    def saveImage(self , file_name = "temp.png"):
        self.image = self.image.resize((math.floor(self.width*self.compression_ratio),math.floor(self.height*self.compression_ratio)),Image.ANTIALIAS)
        self.image.save(file_name , optimize=True,quality=95)

    def getCompressed(self):
        self.image = self.image.resize((math.floor(self.width*self.compression_ratio),math.floor(self.height*self.compression_ratio)),Image.ANTIALIAS)
        return self.image
        
    def loadProfilePic(self , path):
        profPic = Image.open(path)
        profPic = profPic.resize((280,310))
        mask = Image.new("RGBA", (self.width , self.height),(0))
        drawMask = ImageDraw.Draw(mask)
        drawMask.ellipse((405, 289, 676, 560), fill=(255,255,255,255))
        background = Image.new("RGBA", (self.width , self.height),(255,255,255,255))
        background.paste(profPic , (400, 290))
        self.image = Image.composite(background,self.image, mask)
