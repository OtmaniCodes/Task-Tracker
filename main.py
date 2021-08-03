'''
_Name: TASK TRACKER
_Dev: Ahmed El Otmani
_Description:
    this app helps you keep track of your daily and weekly tasks in order for you to
    manage and optimize your time more efficiently. the app lets you accompany your task with
    a description text as well as a deadline that is in date/time format which helps keeeping things
    well organized, you can also pick out a color to determine the priority of your task...
_The Main Techs Used Are: python, kivy, kivymd
'''

#imports:
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from task_generator import TheCard
from task_adder import PopContent
from tasks_db import GetData
from task_adder import PopContent
from kivymd.uix.snackbar import Snackbar
from kivymd.toast import toast
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from random import randint
from time import sleep


class MainApp(MDApp):
    deadline_date= ''
    deadline_time= ''
    colored_btn= False
    tasks_count= []
    clor= ''
    data_ids=[]
    r_date=''

    def build(self):
        self.theme_cls.primary_palette= 'DeepOrange'
        self.theme_cls.primary_hue= "A400" 
        self.theme_cls.theme_style= "Light"
        Window.size=(360, 640)
        return Builder.load_file('main.kv')

    # this method checks if the task adder popup is satisfied:
    def check_three(self):
        if self.colored_btn == True and self.r_date == 'ok':
            return True
        else:
            return False

    # this method updates the tasks count label:
    def count_update(self, task, desc, clr, date, time, w):
        self.tasks_count.append(-1)
        self.root.ids.score.text=('[u]Tasks Count[/u]: [b]'+str(sum(self.tasks_count))+'[/b]'
                                    if sum(self.tasks_count) >= 0 else '[/u]Tasks Count[/u]: [b]0[/b]')
        app_db0= GetData('','','','','')
        app_db0.delete_data(task, desc, clr, date, time)
        if w == 'delete':
            toast('task was successfuly deleted!'.title(), 1)
        elif w == 'done':
            toast('task completed!'.title(), 1)
        self.lbl_remover()

        
    # this method is responsible for showing the popup on the screen.
    def open_pop(self):
        pop= PopContent(app)
        pop.open()

    # these methods below are responsible for getting the deadline data from the users.
    def show_datepicker(self, *args):
        date_picker= MDDatePicker(callback=self.stored_date)
        date_picker.open()
    def show_timepicker(self, *args):
        time_picker= MDTimePicker()
        time_picker.bind(time=self.stored_time)
        time_picker.open()
    def stored_date(self, date):
        self.deadline_date= str(date)
        self.show_timepicker()
    def stored_time(self, picker_widget, time):
        self.deadline_time= str(time)
        self.r_date='ok'

    # choosing the MDCard color:
    def which_clr(self, clr):
        self.colored_btn= True
        self.colors=[[1.0,199/255,115/255,1.0], [251/255,170/255,48/255,1.0], [247/255,154/255,16/255,1.0],
                    [215/255,133/255,9/255,1.0], [189/255,116/255,5/255,1.0], [155/255,97/255,9/255,1.0],
                    [119/255,71/255,0.0,1.0], [121/255,78/255,15/255,1.0], [89/255,58/255,11/255,1.0]]
        self.bg_color=self.colors[clr]
        self.clor= self.bg_color

    # makes snackbar pop up:
    def warning(self, who):
        if who == 'add_btn':
            Snackbar(text='make sure everything is entered (Task, Date, Time, Color)'.title(),font_size= '14dp').show()
    
    def get_task_description(self, task_txt, description_txt):
        self.task= task_txt
        self.description= description_txt
        self.add_task('user')

    # Adding the MDCards to the screen:
    def add_task(self, side):
        self.side= side
        if self.side == 'user':
            self.tasks_count.append(1)
            self.root.ids.score.text= ('[u]Tasks Count[/u]: [b]'+str(sum(self.tasks_count))+'[/b]' if
                                        sum(self.tasks_count) >= 0 else '[/u]Tasks Count[/u]: [b]0[/b]')
            self.box_out= self.root.ids.box1
            self.bg_color= self.bg_color
            self.task_txt= self.task
            self.description_txt= self.description
            self.box_out.add_widget(TheCard(app ,self.task_txt, self.description_txt, self.bg_color,
                                            self.deadline_date, self.deadline_time))
        elif self.side == 'database':
            self.good_data= self.good_data
            for self.one_round in self.good_data:
                self.tasks_count.append(1)
                self.root.ids.score.text=('[u]Tasks Count[/u]: [b]'+str(sum(self.tasks_count))+'[/b]' if
                                            sum(self.tasks_count) >= 0 else '[u]Tasks Count[/u]: [b]0[/b]')
                self.box_out= self.root.ids.box1
                self.bg_color= [float(self.one_round[3]),float(self.one_round[4]),float(self.one_round[5]),float(self.one_round[6])]
                self.task_txt= self.one_round[0]
                self.description_txt= self.one_round[1]
                self.box_out.add_widget(TheCard(app ,self.task_txt, self.description_txt,
                                                self.bg_color, self.one_round[2][:10], self.one_round[2][11:]))
        self.lbl_remover()
    
    # this method runs automaticlay when the app runs, it checks if they're any tasks stored in the database:     
    def on_start(self):
        self.good_data=[]
        app_db= GetData('','','','','')  
        self.all_data= app_db.send_data()
        if self.all_data != 'database empty':
            for one_data in self.all_data:
                self.good_data.append(one_data[5:].split(';'))
            self.add_task('database')
        else: pass
        self.lbl_remover()

    # this method bellow kills the app entirely:
    def exit_app(self):
        ask= MDDialog(title='Exit',text='are you sure you want to exit the app?',
                    size_hint=(.8, .3), pos_hint={'center_x':.5, 'center_y':.5}, auto_dismiss=False,
                    text_button_ok='Cancel', text_button_cancel='Yes', events_callback= self.exit_or_not).open()
    
    def exit_or_not(self,*args):
        if args[0] == 'Yes':
            self.stop()
        elif args[0] == 'Cancel':
            pass
    
    # this method generates Quotes:
    def quotes_generator(self):
        with open('database\\quotes_generator.txt') as quote:
            self.all_quotes= quote.readlines()
            self.all_quotes_= [quo.strip() for quo in self.all_quotes[1:]]
            self.chosen= self.all_quotes_[randint(0, len(self.all_quotes_))]
            self.the_quote= self.chosen[:self.chosen.find(';')]
            self.whose= self.chosen[self.chosen.find(';')+1:].title()
            show_it= MDDialog(title='Valuable Quote', text=('[color=FF3D00]\"[/color][b]'+self.the_quote+
                            '[/b][color=FF3D00]\"[/color]\n\n'+'By: [b][color=FF3D00]'+self.whose+'[/color][/b]'),
                             size_hint=(.9, .38), pos_hint={'center_x':.5, 'top':.65},text_button_ok='OK',
                             auto_dismiss=False)
            show_it.open()
    
    def about_us(self):
        with open('database\\about_app.txt') as about:
            self.content= about.read()
            about_it= MDDialog(title='About This App?', text=self.content+'\n\nAll Rights Reserved \N{copyright sign} 2020',
                             size_hint=(.98, .80), pos_hint={'center_x':.5, 'top':.90},
                             text_button_ok='OK', auto_dismiss=False).open()

    # this method removes the displayed label on the home screen whenever the user adds a new task:
    def lbl_remover(self):
        if len(self.root.ids['box1'].children) == 0:
            self.root.ids['icon'].text_color= [0,0,0,.6]
            self.root.ids['txtt'].text_color= [0,0,0,.6]
        elif len(self.root.ids['box1'].children) > 0:
            self.root.ids['icon'].text_color= [0,0,0,0]
            self.root.ids['txtt'].text_color= [0,0,0,0]


    #the method(s) below are responsible for making some animations/features...
    def anime1(self, target):
        anime= Animation(ele=0, d=0.05)
        anime+=Animation(ele=8, d=0.05)
        anime.start(target)

    def anime2(self, target2):
        self.target2= target2
        anime= Animation(height=70,md_bg_color=[1,0,0,0.2],elevation=0, d=0.3)
        anime.start(self.target2)
        anime.bind(on_complete= self.dele)
    def dele(self, *args):
        self.root.ids['box1'].remove_widget(self.target2)

    def anime3(self, target3):
        self.target3= target3
        anime= Animation(height=70,md_bg_color=[0,1,0,0.2],elevation=0, d=0.3)
        anime.start(self.target3)
        anime.bind(on_complete= self.dele2)
    def dele2(self, *args):
        self.root.ids['box1'].remove_widget(self.target3)

if __name__ == '__main__':
    app= MainApp()
    app.run()
