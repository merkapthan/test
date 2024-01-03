#bullet2
#тут у меня будут колхозно летать всякие штуки через ткинтер 
from tkinter import*
import sys
import time
from PIL import Image, ImageTk
import random
import threading 
from tsfigures import Heart #импортирую свой класс из своей библиотеки,
#подробности этого класса можно прочитать в модуле heart.py в папке tsfigures
def close_window():
    print("закрытие")
    #tk1.destroy()
    sys.exit()

tk1=Tk()
tk1.title('а***мация') 
tk1.geometry("700x700")
class Animapp:
    def __init__(self):
        self.canv=Canvas(tk1, width=600, height=600)
        self.canv.grid(row=0, column=0, columnspan=5, padx=10, pady=10)  
        self.text_test_1=None #отладочная переменная, для test_command в btn_test ниже
        self.bullets=[] #список объектов, которые будут летать 
        self.bullets_id=[] #список id объектов, которые будут летать
        self.life_id_list=[] #список id жизней 
        self.hp=3 #буквально хп (здоровье)
        #self.delta=3 #3 потому что первый объект - рамки, второй - свинья, остальные начнутся с третьего
        

        self.frame=self.canv.create_rectangle(5, 5, 600, 600, outline="red", width=1, tags="board")#граница холста

        self.platform=Platform(self.canv)
        #создаю хрюшу
        self.acorns=[] #список желудей
        #self.acorn=Acorn(self.canv)
        

        self.bullet_types=["ball", "heart", "polygon", "rectangle"]

        #кнопка создания снаряда (пока только мяч)
        self.btn_set_bullet_type= Button(tk1, text="шар", command=lambda:self.set_bullet_type(bullet_type="ball"))
        self.btn_set_bullet_type.grid(row=1, column=2, padx=1, pady=1)

        #кнопка создания снаряда (сердце)
        self.btn_set_bullet_type= Button(tk1, text="сердце", command=lambda:self.set_bullet_type(bullet_type="heart"))
        self.btn_set_bullet_type.grid(row=1, column=3, padx=1, pady=1)
       
       #кнопка отвечающая за анимацию
        self.btn_start=Button(tk1,text="Анимация (вкл.)", command=self.toggle_animation)
        self.btn_start.grid(row=1, column=4, padx=5, pady=5)
        self.anim_is_running=False #переменная проверяющая наличие анимации

        self.threads=[] #список потоков

        

        self.canv.bind_all('<KeyPress-Right>', self.move_platform)
        self.canv.bind_all('<KeyPress-Left>', self.move_platform)
        self.canv.bind_all('<KeyPress-space>', self.throw_bullet)
        #self.canv.bind_all('<KeyPress-Return>', self.move_platform) - если на энтер
        #self.canv.bind_all('<KeyPress>', self.move_platform) - если на любую клавишу
        self.platform_position=self.canv.bbox(self.platform.plat)
        self.set_life(10, 35)
       # self.spawn_acorns()
        self.spawn_acorns_is_active=False
        self.current_press="right" #последнее нажатие клавиши
        self.last_press="right" #предпоследнее нажатие клавиши #сделал их правыми потому что у платформы правая ориентация вначале
        #self.lattice=Lattice(self.canv)
        #self.testbrick=Brick(self.canv, 1, 25, 25,60,60)
        self.testmap=Map(self.canv)
        self.delay=0

    @classmethod    
    def list_to_dict(cls,input_list, list_elems_to_ignore): #вспомогательный метод, превращает список в словарь "элемент:количество"
        out_dict={}
        for elem in input_list:
            if elem in list_elems_to_ignore or (isinstance(elem, (int, float)) or (isinstance(elem, str) and elem.isdigit())):
                continue
            if elem in out_dict:
                out_dict[elem]+=1
            else:
                out_dict[elem]=1
        return out_dict        


    def platform_delay(self):#метод для временной переменной       
        
        def zero_delay():
            self.delay=1
            #print(self.delay)            
            time.sleep(0.1)
            self.delay=0
            #print(self.delay)
        self.delay_thread=threading.Thread(target=zero_delay)
        self.delay_thread.start()         
        #print(delay)    

    def spawn_acorns(self): #метод спавна желудей
        #потом доделать метод, если его вызывать включением анимации несколько раз, то частота спавна растет
        #поэтому надо через переменную спавн из эктив запретить его включение если он уже включен
       # if not self.spawn_acorns_is_active:
           # self.spawn_acorns_is_active=True
            def spawn_accorns_helper(): #вспомогательная внутренняя функция           
                to_spawn=random.randint(0, 2) 
                if to_spawn==2: #and to_spawn_helper:

                    print("tospawn=", to_spawn)
                    new_accorn=Acorn(self.canv)
                    #print("создан желудь")
                    self.acorns.append(new_accorn)
                        
                    new_accorn.start_move_thread()
                    tk1.update()
                        
                    self.canv.update_idletasks() 
                else:                        
                    tk1.update()                    
                    self.canv.update_idletasks()

                if self.anim_is_running: 
                    self.canv.after(4000, spawn_accorns_helper)

            spawn_accorns_helper()           

                #спавн_акорнс_хелпер планирует свой вызов через секунду внутри вызова себя, так и зацикливается
          
            

    def move_platform(self,event):
        #потом весь этот метод перенесу в класс Platform
        self.platform.SW_coord_x=self.canv.bbox(self.platform.plat)[0] #координаты юго-восточного угла для метода отражения
        self.platform.SW_coord_y=self.canv.bbox(self.platform.plat)[3]
        
        if event.keysym=="Right":
            self.last_press=self.current_press
            self.current_press="right"
            if self.last_press!=self.current_press:
                self.platform.reflect_image(app.canv)
            self.platform_position=self.canv.bbox(self.platform.plat)
            if self.platform_position[2]>=599:
                None
            else:
                app.canv.move(self.platform.plat, self.platform.velocity, 0)  
                app.canv.move(self.platform.rightline, self.platform.velocity, 0)
                app.canv.move(self.platform.leftline, self.platform.velocity, 0)
                app.canv.move(self.platform.upline, self.platform.velocity, 0)
                app.canv.move(self.platform.downline, self.platform.velocity, 0) 
                app.canv.move(self.platform.line_spawn, self.platform.velocity, 0)
                self.platform.right_spawn=self.platform.right_spawn+self.platform.velocity
                self.platform.left_spawn=self.platform.left_spawn+self.platform.velocity
                self.platform_delay()
            #print(pos) 
        elif event.keysym=="Left":
            self.last_press=self.current_press
            self.current_press="left"
            if self.last_press!=self.current_press:
                self.platform.reflect_image(app.canv)
            self.platform_position=self.canv.bbox(self.platform.plat)
            if self.platform_position[0]<=6:
                None
            else:    
                app.canv.move(self.platform.plat, -self.platform.velocity, 0) 
                app.canv.move(self.platform.rightline, -self.platform.velocity, 0)
                app.canv.move(self.platform.leftline, -self.platform.velocity, 0)
                app.canv.move(self.platform.upline, -self.platform.velocity, 0)
                app.canv.move(self.platform.downline, -self.platform.velocity, 0)
                app.canv.move(self.platform.line_spawn, -self.platform.velocity, 0)
                self.platform.right_spawn=self.platform.right_spawn-self.platform.velocity
                self.platform.left_spawn=self.platform.left_spawn-self.platform.velocity
                self.platform_delay()
                #потом весь этот метод перенесу в класс Platform
    
    def set_life(self,xy1, xy2):
        for i in range(1,self.hp+1):
            newlife=Life(xy1, xy2, self.canv)
            self.life_id_list.append(newlife.life_id)
            self.canv.move(self.life_id_list[-1], i*30-30, 0)
        print(self.life_id_list)  

    def set_life_extra(self,xy1, xy2):        
        newlife=Life(xy1, xy2, self.canv)
        self.life_id_list.append(newlife.life_id)
        self.canv.move(self.life_id_list[-1], (self.hp+1)*30-30, 0)
        print(self.life_id_list)
        self.hp=self.hp+1       

    def is_dead(self):
        #self.canv.delete(self.life_id_list[-1])
        try: 
            self.canv.delete(self.canv.find_withtag("life")[-1])
            self.hp=self.hp-1
            if len(self.life_id_list)==0:
                self.toggle_animation()
                print("смэрть")
            else:
                self.set_bullet_type(bullet_type="ball")    
        except IndexError:
            self.toggle_animation()  
            print("смэрть") 



        

    def set_bullet_type(self, bullet_type=None, left_spawn=None, height=None, right_spawn=None, down=None):#метод создания снаряда
        if bullet_type is None:
            bullet_type = "ball"
        if left_spawn is None:
            left_spawn = self.platform.left_spawn + 1
        if height is None:
            height = self.platform.height - self.platform.delta - 4
        if right_spawn is None:
            right_spawn = self.platform.right_spawn
        if down is None:
            down = self.platform.height - 4
         
        self.new_bullet=Bullet(bullet_type, left_spawn, height, right_spawn, down)
        
        self.bullets_id=app.canv.find_withtag("bullet")#создаем список форм объектов с тегом баллет
        self.new_bullet.start_move_thread()    
        print("вызвана сетбаллеттайп")   

    def show_threads(self): #показать запущенные потоки
        listthreads=threading.enumerate()   
        iter_listthreads=enumerate(listthreads)
        for index, thrd in iter_listthreads:
            print(f"Поток{index}:{thrd}")
            print(self.life_id_list) #-  с потоками не связана, добавил для отладки
         
    def stop_animation(self):
        self.anim_is_running=False 
        #self.spawn_acorns_is_active=False
    
        
    def start_animation(self):
        self.anim_is_running = True 
       # self.acorns_to_spawn=True   
        #ВКЛЮЧЕНИЕ СПАВНА ЖЕЛУДЕЙ      
        self.spawn_acorns()
        
    def go_on_animation(self):
        if not self.anim_is_running:
            return        
    def toggle_animation(self):
        if self.anim_is_running:
            self.stop_animation()
            self.btn_start.config(text="Анимация (вкл)")
            print(self.anim_is_running)
            try:
                if self.newtext:
                    self.canv_app.delete(self.newtext)
            except:AttributeError        
        else:
            self.start_animation()
           
            self.btn_start.config(text="Анимация (выкл)")
            print(self.anim_is_running)
            
    def move_all_bullets(self): #метод движения всех снарядов ПОКА ОН НЕ НУЖЕН и потом наверняка тоже, оставлю его для столкновений снарядов
        for i in range(len(self.bullets)):
            pass

    def brick_counter(self):
        self.brick_counter+=1


    def bullet_hits_platform(self, hitting_bullet, hited_platform):#метод проверки столкновения с платформой
        #N, S, E, W - север, юг, восток, запад
        #в hitting_bullet передается bullet_id то есть форма
        #в hited_platform передается self.platform
        try:
            overlapping_objects = self.canv.find_overlapping(*self.canv.bbox(hitting_bullet))
           
            if hited_platform.upline in overlapping_objects:
                if hited_platform.rightline in overlapping_objects:
                    return "NE_hit"
                elif hited_platform.leftline in overlapping_objects:
                    return "NW_hit"
                return "N_hit" 
            elif hited_platform.downline in overlapping_objects:
                return "S_hit"  
            elif hited_platform.rightline in overlapping_objects:
                return "E_hit"
            elif hited_platform.leftline in overlapping_objects:
                return "W_hit"
        except TypeError:
            print("шар пролетел")   

    def bullet_hits_bricks(self, hitting_bullet):#метод проверки столкновений с кубиками
         #в hitting_bullet передается bullet_id то есть форма
        #try:
            overlapping_objects = self.canv.find_overlapping(*self.canv.bbox(hitting_bullet))
            alltags=[]
            dict_boards_1={"upboard":0, "leftboard":0, "downboard":0, "rightboard":0}  #словарь линия:число пересечений линии с пулей
            dict_boards={'upline': 0, 'leftline': 0, 'rightline': 0, 'downline': 0}
            print(f"оверлапин_обджектс: {overlapping_objects}")
            for object in overlapping_objects:
                i=0
                tags=self.canv.gettags(object)
                print(f"теги: {tags}")
                alltags+=tags
                print(f"всетеги {i}-я итерация: {alltags}")  
                i+=1
                
                if "brick" and "rectangle" in tags: #если срабатывает, значит мы нашли brick.form
                    print("нашли брик и ректангл")
                    
                    brick=self.testmap.form_and_brick_dict[object]#получаем наш объект кубика из словаря по ключу его формы

                    #логика возвращающая переменные ударов зависимо от того что в оверлапингобджектс
                    #brick.change_brick_hp(self.canv) #меняем хп кубика
                    print(self.testmap.form_and_brick_dict[object])
                    #dict_boards=Animapp.brick_boards_over_bullet(hitting_bullet, brick, dict_boards)
                    dict_boards=self.brick_boards_over_bullet(hitting_bullet,brick, dict_boards )
                    Brick.change_brick_hp(self.testmap.form_and_brick_dict[object],self.canv) #меняем хп кубика
                    print(f"cнова теги: {tags}")
                else:
                    print("в тегах нет брик и ректангл")
                    continue #если иф не сработал, значит объект не форма, а нам такое не надо
              
            #tags_to_ignore=["bullet", "brick", "line", "rectangle"]  
            tags_to_ignore=[]      
            dict_tags=Animapp.list_to_dict(alltags, tags_to_ignore)
            #
            #hit=self.bhb_switch_1(hitting_bullet, dict_tags)
            hit=self.bhb_switch_1(hitting_bullet, dict_boards)
            print(hit)
            return hit                                   
           
        #except TypeError:
            print("по традиции тайпэррор")  

    
    def brick_boards_over_bullet(self, hitting_bullet, brick, dict_boards):
        #dict_boards_moment={"upboard":0, "leftboard":0, "downboard":0, "rightboard":0} 
        upline_coords=[brick.x0, brick.y0-1, brick.x1, brick.y0+1]
        leftline_coords=[brick.x0-1, brick.y0, brick.x0+1, brick.y1]
        rightline_coords=[brick.x1-1, brick.y0, brick.x1+1, brick.y1]
        downline_coords=[brick.x0, brick.y1-1, brick.x1, brick.y1+1]
        upline_overlaping=self.canv.find_overlapping(*upline_coords)
        leftline_overlaping=self.canv.find_overlapping(*leftline_coords)  
        rightline_overlaping=self.canv.find_overlapping(*rightline_coords)  
        downline_overlaping=self.canv.find_overlapping(*downline_coords)  
        if hitting_bullet in upline_overlaping:
            dict_boards["upline"]+=1
        if hitting_bullet in leftline_overlaping:
            dict_boards["leftline"]+=1
        if hitting_bullet in rightline_overlaping:
            dict_boards["rightline"]+=1
        if hitting_bullet in downline_overlaping:
            dict_boards["downline"]+=1
        return dict_boards                  



    def bhb_switch_1(self, hitting_bullet, dict_tags):
            if 'upline' not in dict_tags:
                dict_tags["upline"]=0
            if  'leftline' not in dict_tags:
                dict_tags["leftline"]=0
            if  'downline' not in dict_tags:   
                dict_tags["downline"]=0
            if 'rightline' not in dict_tags:    
                dict_tags["rightline"]=0
            #угловой удар в 3 кубика
            if dict_tags["upline"]==1 and dict_tags["leftline"]==2 and dict_tags["rightline"]==1 and dict_tags["downline"]==2:
                print(dict_tags)
                return "SW_hit"
            elif dict_tags["upline"]==1 and dict_tags["leftline"]==1 and dict_tags["rightline"]==2 and dict_tags["downline"]==2:
                print(dict_tags)
                return "SE_hit"
            elif dict_tags["upline"]==2 and dict_tags["leftline"]==1 and dict_tags["rightline"]==2 and dict_tags["downline"]==1:
                print(dict_tags)
                return "NE_hit" 
            elif dict_tags["upline"]==2 and dict_tags["leftline"]==2 and dict_tags["rightline"]==1 and dict_tags["downline"]==1:
                print(dict_tags)
                return "NW_hit"
            #прямой удар по стыку двух кубиков
            elif dict_tags["leftline"]==1 and dict_tags["rightline"]==1 and dict_tags["downline"]==2 and dict_tags["upline"]==0: 
                print(dict_tags)
                return "S_hit"
            elif dict_tags["upline"]==1 and dict_tags["rightline"]==2 and dict_tags["downline"]==1 and dict_tags["leftline"]==0: #  
                print(dict_tags)
                return "E_hit"
            elif dict_tags["upline"]==2 and dict_tags["leftline"]==1 and dict_tags["rightline"]==1 and dict_tags["downline"]==0: # 
                print(dict_tags)
                return "N_hit"
            elif dict_tags["upline"]==1 and dict_tags["leftline"]==2 and dict_tags["downline"]==1 and dict_tags["rightline"]==0 :  #
                print(dict_tags)
                return "W_hit"
            #теперь угловые столкновения на стыке двух кубиков
            elif dict_tags["upline"]==1 and dict_tags["leftline"]==1 and dict_tags["rightline"]==1 and dict_tags["downline"]==1:
                if hitting_bullet.current_x0>hitting_bullet.last_x0 and hitting_bullet.current_y0>hitting_bullet.last_y0:
                    print(dict_tags)
                    return "NW_hit"
                elif hitting_bullet.current_x0>hitting_bullet.last_x0 and hitting_bullet.current_y0<hitting_bullet.last_y0:
                    print(dict_tags)
                    return "SW_hit"
                elif hitting_bullet.current_x0<hitting_bullet.last_x0 and hitting_bullet.current_y0>hitting_bullet.last_y0:
                    print(dict_tags)
                    return "NE_hit"
                elif hitting_bullet.current_x0<hitting_bullet.last_x0 and hitting_bullet.current_y0<hitting_bullet.last_y0:
                    print(dict_tags)
                    return "SE_hit"
            #теперь просто угловые с одним 
            elif  dict_tags["upline"]==1 and dict_tags["rightline"]==1 and dict_tags["leftline"]==0 and dict_tags["downline"]==0:  
                print(dict_tags)
                return "NE+hit"
            elif  dict_tags["upline"]==1 and dict_tags["leftline"]==1 and dict_tags["rightline"]==0 and dict_tags["downline"]==0:
                print(dict_tags)
                return "NW_hit"
            elif  dict_tags["downline"]==1 and dict_tags["leftline"]==1 and dict_tags["rightline"]==0 and dict_tags["upline"]==0:
                print(dict_tags)
                return "SW_hit"
            elif  dict_tags["downline"]==1 and dict_tags["rightline"]==1 and dict_tags["leftline"]==0 and dict_tags["upline"]==0:
                print(dict_tags)
                return "SE_hit"
            #теперь прямые с одним
            elif  dict_tags["upline"]==1:  
                print(dict_tags)  
                return "N_hit"
            elif dict_tags["leftline"]==1:
                print(dict_tags)
                return "W_hit"
            elif dict_tags["downline"]==1:
                print(dict_tags)
                return "S_hit"
            elif dict_tags["rightline"]==1:
                print(dict_tags)
                return "E_hit"
            elif dict_tags["upline"]==0 and dict_tags["rightline"]==0 and dict_tags["leftline"]==0 and dict_tags["downline"]==0:
                return "nothing"
            else:
                print(dict_tags)
                print("хз что за ситуация")
                return "nothing"                   
                    

    def acorn_hits_platform(self, hitting_acorn, hited_platform):#метод проверки столкновения с платформой
        #N, S, E, W - север, юг, восток, запад
        #в hitting_bullet передается bullet_id то есть форма
        #в hited_platform передается self.platform
        try:
            overlapping_objects = self.canv.find_overlapping(*self.canv.bbox(hitting_acorn))
            if hited_platform.upline in overlapping_objects:
                return "N_hit" 
            elif hited_platform.downline in overlapping_objects:
                return "S_hit"  
            elif hited_platform.rightline in overlapping_objects:
                return "E_hit"
            elif hited_platform.leftline in overlapping_objects:
                return "W_hit"
        except TypeError:
            print("желудь пролетел")           
            
                  
    def move_bullet_random1(self, bullet_id): #метод движения одного снаряда 1
            self.count=0
            while True:
                if not self.anim_is_running:    
                    app.canv.move(bullet_id, 0, 0) #самый колхозный вариант постановки на паузу
                else:
                
                    
                    self.x_move=random.randint(-3,3)
                    self.y_move=random.randint(-3,3)
                    app.canv.move(bullet_id, self.x_move, self.y_move)
                    #print(f"объект {bullet_id} подвинут")  
                    self.count+=0 #больше не нужен
                    if self.count==100:
                        break
             
                tk1.update()
                time.sleep(0.01)  
                self.canv.update_idletasks()

    def throw_bullet(self, event):
        if event.keysym=="space":  
            for obj in self.bullets:  
                obj.on_platform=False


    def move_bullet(self, bullet_obj): #метод движения одного снаряда 2 с отскоком от границ
            #bullet_id - это форма объекта класса Bullet
            self.count=0
            #if not self.bullets[self.bullets_id.index(bullet_id)].on_canvas:
                #self.canv.delete(self.bullets[self.bullets_id.index(bullet_id)])
            #x_velocity=bullet_obj.vx_current
            while bullet_obj.on_canvas:
                
                if bullet_obj.on_platform:
                    while bullet_obj.on_platform:
                        if self.delay==0:
                            bullet_obj.vx_current=bullet_obj.vx_0

                        while self.canv.coords(bullet_obj.form)[0]!=self.platform.left_spawn:
                            self.canv.coords(bullet_obj.form, self.platform.left_spawn, self.platform.height-25-4, self.platform.right_spawn, self.platform.height-4)
                            #x_velocity=bullet_obj.vx_current
                            if self.current_press=="right" and bullet_obj.vx_current>0:
                                if self.delay==1:
                                
                                    bullet_obj.vx_current=bullet_obj.vx_0*(1+self.delay*2)
                                else:
                                    bullet_obj.vx_current=bullet_obj.vx_0 
                                #new_velocity=x_velocity
                                print(f"скорость из класса{bullet_obj.vx_0}")
                                print(f"скорость текущая{bullet_obj.vx_current}")
                                #None
                            elif self.current_press=="left" and bullet_obj.vx_current<0:
                                if self.delay==1:
                                
                                    bullet_obj.vx_current=bullet_obj.vx_0*(1+self.delay*2)
                                else:
                                    bullet_obj.vx_current=bullet_obj.vx_0    
                               #new_velocity=x_velocity
                                print(f"скорость из класса{bullet_obj.vx_0}")
                                print(f"скорость текущая{bullet_obj.vx_current}")
                                #None
                            else:
                                bullet_obj.vx_0=bullet_obj.vx_0*(-1)
                                bullet_obj.vx_current=bullet_obj.vx_0
                                #bullet_obj.vx_current=bullet_obj.vx_current*(-1)
                                #x_velocity=bullet_obj.vx_current
                                #print(bullet_obj.vx_current)  
                                      
                        else:
                            None
                        #app.canv.move(bullet_obj.form, (app.canv.coords(self.platform.line_spawn)[0]-app.canv.coords(bullet_obj.form)[0]))
                    #if event.keysym=="Right":
                        #app.canv.move(bullet_obj.form, self.platform.velocity, 0)
                    #elif event.keysym=="Left":
                        #app.canv.move(bullet_obj.form, -self.platform.velocity, 0)    
                elif not self.anim_is_running:    
                    app.canv.move(bullet_obj.form, 0, 0) #самый колхозный вариант постановки на паузу
                else:
                    try:
                        
                        app.canv.move(bullet_obj.form, bullet_obj.vx_current, bullet_obj.vy_0)
                          
                        pos=app.canv.coords(bullet_obj.form)
                        #[0]- это х0, 1 - это у0, 2 - это х1, 3 - это у1.
                        #следующие два аргумента нужны для определения направления движения при некоторых столкновениях 
                        bullet_obj.current_x0=pos[0] 
                        bullet_obj.current_y0=pos[1]
                        if pos[0]<=6 or pos[2]>=599: #проверка столкновений с боковыми границами
                           bullet_obj.vx_current=bullet_obj.vx_current*(-1)
                            
                        if pos[1]<=6: #проверка столкновений с верхней границей
                            bullet_obj.vy_0=bullet_obj.vy_0*(-1)    

                            #проверка падения шара
                        if pos[3]>=599 and not bullet_obj.is_fallen: #проверка столкновений с нижней границей
                            #app.canv.move(bullet_id, 0, 0)
                            bullet_obj.is_fallen=True
                            
                            bullet_obj.on_canvas=False   
                            self.canv.delete(bullet_obj.form)
                            self.canv.delete(bullet_obj)
                            self.is_dead() 

                        #отскоки от платформы
                        if self.bullet_hits_platform(bullet_obj.form, self.platform)=="NE_hit" or self.bullet_hits_platform(bullet_obj.form, self.platform)=="NW_hit":
                            #проверка столкновений с верхними углами платформы
                            bullet_obj.vy_0=bullet_obj.vy_0*(-1) 
                            bullet_obj.vx_current=bullet_obj.vx_current*(-1)  
                        if self.bullet_hits_platform(bullet_obj.form, self.platform)=="N_hit": #проверка столкновений с верхом платформы
                            bullet_obj.vy_0=bullet_obj.vy_0*(-1)  
                        if self.bullet_hits_platform(bullet_obj.form, self.platform)=="E_hit" or self.bullet_hits_platform(bullet_obj.form, self.platform)=="W_hit": #проверка столкновений с краями платформы
                           bullet_obj.vx_current=bullet_obj.vx_current*(-1)    
                        #отскоки от кубиков
                        hit=self.bullet_hits_bricks(bullet_obj.form)   
                        if hit=="NE_hit" or hit=="NW_hit" or hit=="SW_hit" or hit=="SE_hit":
                            bullet_obj.vy_0=bullet_obj.vy_0*(-1)
                            bullet_obj.vx_current=bullet_obj.vx_current*(-1)  
                            print("отскок")  
                        if hit=="N_hit" or hit=="S_hit":
                            bullet_obj.vy_0=bullet_obj.vy_0*(-1)  
                            print("отскок") 
                        if hit=="E_hit" or hit=="W_hit": 
                           bullet_obj.vx_current=bullet_obj.vx_current*(-1)    
                           print("отскок") 
                        if hit=="nothing":
                            None   
                        #следующие два так же нужны для определения направления при столкновениях (в коде выше)    
                        #возможная ошибка - если в самый начальный момент времени происходит то редкое столкновение, а эти два аргумента =None
                        #в этом случае будет происходить сравнение чисел с None. Но такие ситуации по идее невозможны по сценарию, но можно и обработать   
                        bullet_obj.last_x0=pos[0]
                        bullet_obj.last_y0=pos[1]
                    except ValueError:
                        print("ошибка в методе мувбаллет, элемент не найден в списке")        
                    self.count+=0 #больше не нужен
                    if self.count==100:
                        break
             
                tk1.update()
                #скорость отрисовки снарядов
                #time.sleep(0.04) 
                time.sleep(0.05)  
                self.canv.update_idletasks()            
                

   
class Bullet:
    def __init__(self, btype, ox1, oy1, ox2, oy2):
        self.i=0
        self.btype=btype
        self.ox1=ox1
        self.oy1=oy1
        self.ox2=ox2
        self.oy2=oy2
        self.is_fallen=False
        #размеры снаряда 25х25 пикселей
        self.is_moving=False 
        self.on_canvas=True
        self.on_platform=True #проверка нахождения на платформе, при создании он там
        self.vx_0=0
        self.vy_0=0
        self.vx_current=0
        self.last_x0=None
        self.last_y0=None
        self.current_x0=None
        self.current_y0=None
        while self.vx_0==0 or self.vy_0==0: #цикл делает так, что ни одна компонента скорости не равна 0
            #self.vx_0=random.randint(-5,5)
            if app.current_press=="right":
                self.vx_0=5
            elif app.current_press=="left":
                self.vx_0=-5  
            self.vx_current=self.vx_0  
            #self.vy_0=random.randint(-5,0)
            self.vy_0=-5
        if self.btype=="ball":
            self.colorframe="#" + ("%06x" % random.randint(0, 0xFFFFFF))
            self.innercolor="#" + ("%06x" % random.randint(0, 0xFFFFFF))
          # Генерация случайного цвета в формате "#RRGGBB"
          
            self.ball=app.canv.create_oval(self.ox1, self.oy1, self.ox2, self.oy2, outline=self.colorframe, fill=self.innercolor, tags="bullet")
            print("создан мяч")  
            self.form=self.ball #атрибут, напрямую сохраняющий в себе форму
            print("есть форма")
            app.bullets.append(self) #добавление снаряда-объекта в список снарядов
            print("добавлен в список")
            app.canv.update()
            print(app.bullets) #вывод списка объектов-снарядов
            print(f"их {len(app.bullets)}") 
        elif self.btype=="heart":
            self.colorframe="#" + ("%06x" % random.randint(0, 0xFFFFFF))
            self.innercolor="#" + ("%06x" % random.randint(0, 0xFFFFFF))
          # Генерация случайного цвета в формате "#RRGGBB"
            self.ht=Heart(self.ox1, self.ox2, self.colorframe, self.innercolor, app.canv)
            app.canv.addtag_withtag("bullet", self.ht.figure)
            self.form=self.ht.figure #атрибут, напрямую сохраняющий в себе форму
            app.bullets.append(self)
            app.canv.update()
            print(app.bullets) #вывод списка объектов-снарядов
            print(f"их {len(app.bullets)}") 
        elif self.btype=="polygon":
             pass
        elif self.btype=="rectangle":
             pass     
 
        
    def start_move_thread(self):
        self.bullet_thread = threading.Thread(target=app.move_bullet, args=(self,))
        self.bullet_thread.start() 
        app.threads.append(self.bullet_thread)   
        #print(f"создан {len(app.threads)}-й поток") #по факту проверка колхозная

class Platform:
    def __init__(self, app_canv):
        #self.image_path_rl=PhotoImage(file='C:\\Users\\dermo\\pyimages\\pigplatform_rl.gif')
        self.image_path_rl=PhotoImage(file='bullet_images/pigplatform_rl.gif')
        #self.image_path_lr=PhotoImage(file='C:\\Users\\dermo\\pyimages\\pigplatform_lr.gif')
        self.image_path_lr=PhotoImage(file='bullet_images/pigplatform_lr.gif')
        #self.image_path=Image.open("C:\\Users\\dermo\\pyimages\\pigplatform.gif")
        self.image_resized=self.image_path_lr.subsample(5,5)
        self.delta=25 # смещение верхней границы относительно границ рисунка
        self.plat=app_canv.create_image(250, 599, anchor=SW, image=self.image_resized)
        
        self.upline=app_canv.create_line(app_canv.bbox(self.plat)[0],app_canv.bbox(self.plat)[1]+self.delta,app_canv.bbox(self.plat)[2],app_canv.bbox(self.plat)[1]+self.delta, width=4, tags="plat_frame")
        self.leftline=app_canv.create_line(app_canv.bbox(self.plat)[0],app_canv.bbox(self.plat)[1]+self.delta,app_canv.bbox(self.plat)[0],app_canv.bbox(self.plat)[3], width=4, tags="plat_frame")
        self.rightline=app_canv.create_line(app_canv.bbox(self.plat)[2],app_canv.bbox(self.plat)[1]+self.delta,app_canv.bbox(self.plat)[2],app_canv.bbox(self.plat)[3], width=4, tags="plat_frame")
        self.downline=app_canv.create_line(app_canv.bbox(self.plat)[0],app_canv.bbox(self.plat)[3],app_canv.bbox(self.plat)[2],app_canv.bbox(self.plat)[3],  width=4, tags="plat_frame")
        self.SW_coord_x=app_canv.bbox(self.plat)[0] #координаты юго-восточного угла для метода отражения изображения при его движении влево-вправо
        self.SW_coord_y=app_canv.bbox(self.plat)[3]

        #левая и правая границы зоны спавна снаряда по горизонтали
        self.left_spawn=app_canv.bbox(self.plat)[0]+2*self.delta+4
        self.right_spawn=app_canv.bbox(self.plat)[2]-2*self.delta-4
        #высота спавна по вертикали
        self.height=app_canv.bbox(self.plat)[1]+self.delta
        #линия, задающая границы спавна снаряда
        self.line_spawn=app_canv.create_line(self.left_spawn,app_canv.bbox(self.plat)[1]+self.delta,self.right_spawn,app_canv.bbox(self.plat)[1]+self.delta, width=8, tags="spawn_line")

        self.velocity=10 #начальная скорость платформы

    def reflect_image(self, app_canv):
        app_canv.delete(self.plat)#нельзя пил с ткинтером использовать, потом переделаю по босяцки, через два изображения, обычное и отраженное мной непосредственно на компе
        if app.last_press=="left" and app.current_press=="right":
            self.image_resized=self.image_path_lr.subsample(5,5)
        elif app.last_press=="right" and app.current_press=="left":
            self.image_resized=self.image_path_rl.subsample(5,5)
        else:
            None            
           
            
            # Создать новое отраженное изображение
        self.plat = app_canv.create_image(self.SW_coord_x, self.SW_coord_y, anchor=SW, image=self.image_resized)    

class Life:
    def __init__(self, x1,  x2, app_canv):
        self.oxy1=x1
        
        self.oxy2=x2
        
        self.colorframe="red"
        self.innercolor="pink"
        #self.innercolor="#" + ("%06x" % random.randint(0, 0xFFFFFF))
        self.life=Heart(self.oxy1, self.oxy2, self.colorframe, self.innercolor, app_canv)
        self.life_id=self.life.figure
        app_canv.itemconfig(self.life_id, width=1, tags="life")
       
       

class Acorn:
    def __init__(self, app_canv):
        #app_canv это app.canv
        #self.image_path=PhotoImage(file='C:\\Users\\dermo\\pyimages\\acorn.gif')
        self.image_path=PhotoImage(file='bullet_images/acorn.gif') 
        #self.image_path=Image.open("C:\\Users\\dermo\\pyimages\\pigplatform.gif")
        self.image_resized=self.image_path.subsample(15,15)
        self.x0=random.randint(6, 573)
    
        self.y0=-40
      
        self.vx=0
        self.vy=5
        self.is_fallen=False
        self.on_canvas=True
        self.plat=app_canv.create_image(self.x0, self.y0, anchor=SW, image=self.image_resized)
        #print("форма желудя есть")
        
        self.form_box=app_canv.bbox(self.plat)
        self.upline=app_canv.create_line(app_canv.bbox(self.plat)[0],app_canv.bbox(self.plat)[1],app_canv.bbox(self.plat)[2],app_canv.bbox(self.plat)[1], width=0, fill="white", tags="acorn_frame")
        self.leftline=app_canv.create_line(app_canv.bbox(self.plat)[0],app_canv.bbox(self.plat)[1],app_canv.bbox(self.plat)[0],app_canv.bbox(self.plat)[3], width=0, fill="white", tags="acorn_frame")
        self.rightline=app_canv.create_line(app_canv.bbox(self.plat)[2],app_canv.bbox(self.plat)[1],app_canv.bbox(self.plat)[2],app_canv.bbox(self.plat)[3], width=0, fill="white", tags="acorn_frame")
        self.downline=app_canv.create_line(app_canv.bbox(self.plat)[0],app_canv.bbox(self.plat)[3],app_canv.bbox(self.plat)[2],app_canv.bbox(self.plat)[3], width=0, fill="white", tags="acorn_frame")
        print("Высота желудя") # Высота желудя равна 40 пикселей
        print(app_canv.bbox(self.plat)[3]-app_canv.bbox(self.plat)[1])

    def move_acorn(self, vx_variable, vy_variable, app_canv):
        while True:
            if app.anim_is_running:
                vx=vx_variable
                vy=vy_variable
            else:
                vx=0
                vy=0    
            #app.canv.after(0, self.move_acorn_helper, vx, vy)
            app_canv.move(self.upline, vx, vy)
            app_canv.move(self.leftline, vx, vy)
            app_canv.move(self.rightline, vx, vy)
            app_canv.move(self.downline, vx, vy)
            app_canv.move(self.plat, vx, vy)
            
            #проверка падения 
            try:
                if app_canv.bbox(self.plat)[3]>=615 and not self.is_fallen: #проверка столкновений с нижней границей
        
                    self.is_fallen=True                            
                    self.on_canvas=False   
                    self.delacorn(app_canv)
                    #видимо, если не удалить вручную линии, то они остаются. Пока оставлю так
            except TypeError as e:
                    print("TypeError: Исключение для закрытия потока")
                    raise TypeError("Исключение для закрытия потока") from None
                
                   

            #проверка столкновения с платформой 
            if app.acorn_hits_platform(self.plat, app.platform)=="N_hit" or app.acorn_hits_platform(self.plat, app.platform)=="E_hit" or app.acorn_hits_platform(self.plat, app.platform)=="W_hit": #проверка столкновений с краями платформы
                app.set_life_extra(10,35) 
                print(app.hp) 
                app_canv.delete(self) 
                app_canv.delete(self.upline) 
                app_canv.delete(self.rightline) 
                app_canv.delete(self.downline) 
                app_canv.delete(self.leftline) 
                app_canv.delete(self.plat)   
                #self.cleanup()#метод почему-то удаляет объекты других классов, в частности рамки и правую линию платформы         

            #print("желудь подвинут")
            tk1.update()
            time.sleep(0.04)
            app_canv.update_idletasks() 
           
    def move_acorn_helper(self, vx, vy, app_canv):    
        app_canv.move(self.upline, vx, vy)
        app_canv.move(self.leftline, vx, vy)
        app_canv.move(self.rightline, vx, vy)
        app_canv.move(self.downline, vx, vy)
        app_canv.move(self.plat, vx, vy)

    def start_move_thread(self):
        self.acorn_thread = threading.Thread(target=self.move_acorn, args=(self.vx,self.vy,app.canv,))
        self.acorn_thread.start() 
        app.threads.append(self.acorn_thread)   
        #print(f"создан {len(app.threads)}-й поток") #по факту проверка колхозная    

    def cleanup(self):#удаление объекта
        for attribute in self.__dict__:
            app.canv.delete(self.__dict__[attribute])    

    def delacorn(self, app_canv):
        app_canv.delete(self.plat) 
        app_canv.delete(self.upline) 
        app_canv.delete(self.rightline) 
        app_canv.delete(self.downline) 
        app_canv.delete(self.leftline) 
         
        app_canv.delete(self) 
        del self 


    
class CustomException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Lattice: #решетка 
    def __init__(self, app_canv):
        #self.lines=[[app_canv.create_line(0,0,x,y, fill="red", width=1, tags="lattice") for x in range(50, 600, 50)] for y in range(50,600,50)]
        #оставил потому что красивый рисуночек вышел но неправильный
        self.vertical_lines=[app_canv.create_line(x,0,x,600, fill="red", width=1, tags="lattice") for x in range(50, 650, 50)]
        self.horizontal_lines=[app_canv.create_line(0,y,600,y, fill="red", width=1, tags="lattice") for y in range(50, 650, 50)]
        self.inner_radius=25 #радиус вписанной окружности, от центров до границ квадратов сетки
        self.points=[[(x, y) for x in range(25, 625, 50)] for y in range(25, 625, 50)] #двумерный список с координатами центров квадратов сетки
        #ниже двумерный список самих этих точек (реализованы в виде кругов радиусом в пиксель, считай что точки)
        self.centres=[[app_canv.create_oval(x-1,y-1,x+1,y+1,fill="red", width=1, tags="centres") for x in range (25, 625, 50)] for y in range(25, 625, 50)]
        print(self.points)

class Brick: #кубики, которые и надо выбивать
    link_and_counter=1
   
    def __init__(self, app_canv, hp, x0, y0, x1, y1):

        self.brick_link=Brick.link_and_counter
        Brick.link_and_counter+=1
        
        #app_canv.brick_counter+=1
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1
        self.hp=hp #буквально хп кубика, сколько раз по нему надо ударить чтобы он сломался
        self.inner_item=random.randint(1,8)
        
        self.form=app_canv.create_rectangle(x0, y0, x1, y1, outline="blue", width=(hp*2), tags=("brick", "rectangle", f"{self.brick_link}")) #форма кубика
        self.upline=app_canv.create_line(x0,y0,x1,y0, fill="blue", width=(hp*2), tags=("brick_part", "line", "upline"))
        self.rightline=app_canv.create_line(x1,y0,x1,y1, fill="blue", width=(hp*2), tags=("brick_part", "line", "rightline"))
        self.downline=app_canv.create_line(x0,y1,x1,y1, fill="blue", width=(hp*2), tags=("brick_part", "line", "downline"))
        self.leftline=app_canv.create_line(x0,y0,x0,y1, fill="blue", width=(hp*2), tags=("brick_part", "line", "leftline"))
        #
        self.tags=app_canv.gettags(self.form)
        print(self.tags)

    def __str__(self):
        return f"Куб: форма {self.form}, аплайн {self.upline}, райтлайн {self.rightline}, даунлайн {self.downline}, лефтлайн {self.leftline}, хп {self.hp} "

        
    def add_to_dict(self, app_canv):
        if app:
            app.testmap.form_and_brick_dict[self.form]=self
        else:
           app_canv.after(200, self.add_to_dict(app_canv))    

        
    def cleanup(self):
         for attribute in self.__dict__:
            app.canv.delete(self.__dict__[attribute])

    def delbrick(self, app_canv):
        del self.hp 
        if self.inner_item==1:
            app.set_bullet_type(left_spawn=self.x0+12, right_spawn=self.x1-13, height=self.y0+12, down=self.y1-13)
        try:
            if  self.form:
                print(f"у объекта {self.form}:")
                print("форма")
            app_canv.delete(self.form)
            del self.form
            if not self.form:
                print("ноу форма")
        except AttributeError:
            print("минус форма")    
        try:    
            if self.upline:
                print("аплайн")            
            app_canv.delete(self.upline)
            del self.upline
            if not self.upline:
                print("ноу аплайн")
        except:
            print("минус аплайн")  
        try:          
            if self.rightline:
                print(" райтлайн")    
            app_canv.delete(self.rightline)
            del self.upline
            if not self.rightline:
                print("ноу райтлайн")
        except:
            print("минус райтлайн")      
        try:      
            if self.downline:
                print("даунлайн")
            app_canv.delete(self.downline)
            del self.downline
            if not self.downline:
                print("ноу даунлайн")
        except:
            print("минус даунлайн")  
        try:          
            if self.leftline:
                print("лефтлайн")     
            app_canv.delete(self.leftline) 
            del self.leftline
            if not self.leftline:
                print("ноу лефтлайн") 
        except:
            print("минус лефтлайн") 
        del self.x0
        del self.y0
        del self.x1
        del self.y1    
        del self

    @classmethod
    def change_brick_hp(cls, brick,app_canv):
        #if isinstance(brick.form, int): #проверка, существует ли форма
             # return
        brick.hp=brick.hp-1
        hp=brick.hp
        if brick.hp==0 or brick.hp<0:
            blabla=brick.form
            brick.delbrick(app_canv)
            print(f"отвалился {blabla}")
        elif brick.hp>0:  
            #if isinstance(brick.form, int): #проверка, существует ли форма
              #return  
            app_canv.itemconfig(brick.form, width=(hp*2) ) 
            app_canv.itemconfig(brick.upline, width=(hp*2) )
            app_canv.itemconfig(brick.rightline, width=(hp*2) )
            app_canv.itemconfig(brick.downline, width=(hp*2) )
            app_canv.itemconfig(brick.leftline, width=(hp*2) )  
            print(f"изменился {brick.form}")        

    def change_brick_hp_1(self,app_canv):
        #if isinstance(self.form, int): #проверка, существует ли форма
             # return
        self.hp=self.hp-1
        hp=self.hp
        if self.hp==0 or self.hp<0:
            blabla=self.form
            self.delbrick(app_canv)
            print(f"отвалился {blabla}")
        elif self.hp>0:  
            #if isinstance(self.form, int): #проверка, существует ли форма
              #return  
            app_canv.itemconfig(self.form, width=(hp*2) ) 
            app_canv.itemconfig(self.upline, width=(hp*2) )
            app_canv.itemconfig(self.rightline, width=(hp*2) )
            app_canv.itemconfig(self.downline, width=(hp*2) )
            app_canv.itemconfig(self.leftline, width=(hp*2) )  
            print(f"изменился {self.form}")                

    


        
                
class Map: #карта, на которой расположатся кубики
    def __init__(self, app_canv): 
        self.to_choose=[1,2,3]
        self.form_and_brick_dict={} #Пока пустой словарь, для хранения ключ(форма):значение(объект) для кубиков   
        #создаю двумерный список, создающий с вероятностью 50 на 50 кубик в заданных координатах
        self.bricks=[[Brick(app_canv, random.choice(self.to_choose), x-25, y-25, x+25, y+25) if random.random() <= 0.5 else None for x in range(25, 625, 50)] for y in range(25, 525, 50)]
        print(self.bricks)
        self.to_change=[] #объекты, которые пересекает пуля, которые будут изменены (или выбиты)
        self.not_none_bricks=0
        for row in self.bricks:
            for brick in row:
                if brick  is not None:
                    self.not_none_bricks+=1 #для счетчика, проверки количества
                    self.form_and_brick_dict[brick.form]=brick  #заполняем словарь
        print(f"число кубов = {self.not_none_bricks}")   

         
        #print(f"словарь:{self.form_and_brick_dict}")   
        self.print_dict(self.form_and_brick_dict)     

        #self.wait_for_bullet_hit(app_canv)

    def print_dict(self, dict): #метод вывода словаря в столбик для удобства
        for key, value in dict.items():
            print(f"форма:{key}, объект: {value}, линк: {value.brick_link}")   
                            
    def wait_for_bullet_hit(self, app_canv):
        #метод, проверяющий для каждого кубика столкновения с пулей и удаляющий их
        #но попробую по другому, потому что кубиков по факту больше, чем пуль
        #и оптимальнее будет проверять столкновения пули с объектами
        def wait_helper():
            print("вызов")
           # try:
            for row in self.bricks:
                for brick in row:
                    if brick and brick.form is not None:
                        bbox=app_canv.bbox(brick.form)
                        if bbox is not None:
                            overlapping_objects=app_canv.find_overlapping(*bbox)
                            for object in overlapping_objects:
                                tags=app_canv.gettags(object)
                                if "bullet" in tags:
                                    brick.change_brick_hp(app_canv)      
            app_canv.after(150, wait_helper)       
           # except TypeError:
                #print("тайпэррор")
        wait_helper()        

        
app=Animapp() 

app.canv.tag_raise("life") #отображение жизней поверх всего

butt_on_test1=False  
def test_command_1(): #для тестовой кнопки
        #этой кнопкой проверял независимость обработки объектов-форм и объектов-текста
        global  butt_on_test1
        if not butt_on_test1:
            app.text_test_1=app.canv.create_text(220, 200, text='тестовая команда 1', font=('Courier',10))
            #app.delta=app.delta+1
            butt_on_test1=True
            print("тест команда 1 вкл")
        else:   
            app.canv.delete(app.text_test_1)
            print("тест команда 1 выкл")
            butt_on_test1=False
        print(app.bullets)  
        print(app.bullets_id)
        print(app.bullets[app.bullets_id[-app.delta]])#- как и задумано, эта строчка выдаст AttributeError     

def test_command_2():
    print(app.bullets)  
    print(app.bullets_id)
    print(app.bullets[app.bullets_id[-app.delta]])                

btn_test= Button(tk1, text="тест.кн.Потоки", command=app.show_threads)
#btn_test= Button(tk1, text="тест.кн.", command=test_command_2)
#btn_test= Button(tk1, text="тест.кн.", command=test_command_1)
btn_test.grid(row=1, column=1, padx=1, pady=1)
print(app.platform_position)
print(f"Длина платформы {app.platform_position[2]-app.platform_position[0]}, высота {app.platform_position[3]-app.platform_position[1]}")

print("спавн акорнс")
app.platform_delay()

#print(f"Длина желудя {app.acorn.form_box[2]-app.acorn.form_box[0]}, высота {app.acorn.form_box[3]-app.acorn.form_box[1]}")
app=mainloop()
if not app:
    sys.exit()



tk1.protocol("WM_DELETE_WINDOW", close_window)
if not app:
    sys.exit()
if not tk1.winfo_exists():
    sys.exit()    
tk1.mainloop()
if tk1.winfo_exists():
    sys.exit()
sys.exit()    

