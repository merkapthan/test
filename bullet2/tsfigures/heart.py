#тут описан класс Heart моей библиотеки tsfigures
#объекты этого класса - графические объекты в форме сердца для рисования их с помощью библиотеки
#tkinter на холсте canvas. 
class Heart:    
    def _addpoint(self, point):
        self.points.append(point)
    def __init__(self, xy1,  xy2, outline1, inner_color, canvas_object):
        #сердце строится по двум точкам - левая верхняя и правая нижняя 
        #координаты остальных точек берутся из координат этих двух
        #аутлайн1 - переменная для цвета
        #canvas_object - переменная, которая примет в себя переменную объекта холста в программе
        self.x1=xy1
        self.y1=xy1
        self.q1=xy1 #это была установка начальных координат
        self.x2=xy2
        self.y2=xy2
        self.q2=xy2# это была установка конечных координат
        self.points=[]
        self.fill_color=inner_color
        self.d=xy2-xy1
        self.heart_outline=outline1
        #далее идет добавление точек на холст, по которым потом 
        #с помощью полигона будет построено сердце
        self._addpoint(self.q1)
        self._addpoint(self.q1+(self.d/4))#1
        self._addpoint(self.q1+(self.d*3/32))
        self._addpoint(self.q1+(self.d*3/32))#2
        self._addpoint(self.q1+(self.d/4))
        self._addpoint(self.q1)#3
        self._addpoint(self.q1+(self.d*13/32))
        self._addpoint(self.q1+(self.d*3/32))#4
        self._addpoint(self.q1+(self.d*15/32))
        self._addpoint(self.q1+(self.d*4/32))#4.9
        self._addpoint(self.q1+(self.d/2))
        self._addpoint(self.q1+(self.d/4))#5
        self._addpoint(self.q1+(self.d*17/32))
        self._addpoint(self.q1+(self.d*4/32))#5.1
        self._addpoint(self.q1+(self.d*19/32))
        self._addpoint(self.q1+(self.d*3/32))#6
        self._addpoint(self.q1+(self.d*3/4))
        self._addpoint(self.q1)#7
        self._addpoint(self.q2-(self.d*3/32))
        self._addpoint(self.q1+(self.d*3/32))#8
        self._addpoint(self.q2)
        self._addpoint(self.q1+(self.d/4))#9
        self._addpoint(self.q2-(self.d*2/32))
        self._addpoint(self.q1+(self.d*16/32))#10
        self._addpoint(self.q2-(self.d*8/32))
        self._addpoint(self.q2-(self.d*8/32))#11
        #self._addpoint(self.q1+(self.d*18/32))
        #self._addpoint(self.q2-(self.d*2/32))#12.1
        self._addpoint(self.q1+(self.d*18/32))
        self._addpoint(self.q2)#12.2
        self._addpoint(self.q1+(self.d*14/32))
        self._addpoint(self.q2-(self.d*2/32))#12.3
        self._addpoint(self.q1+(self.d*8/32))
        self._addpoint(self.q2-(self.d*8/32))#13
        self._addpoint(self.q1+(self.d*2/32))
        self._addpoint(self.q1+(self.d*16/32))#14
        self.figure=canvas_object.create_polygon(self.points, outline=self.heart_outline, fill=self.fill_color, smooth=True)
        #
    def coords(self):
        return [self.x1, self.y1, self.x2, self.y2]
