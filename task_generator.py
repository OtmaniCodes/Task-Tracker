from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from datetime import datetime
from kivy.clock import Clock
from tasks_db import GetData
from kivymd.toast import toast
from kivy.utils import get_color_from_hex


class TheCard(MDCard):
    def __init__(self, app2,task_txt,description_txt, bg_color, deadline_date, deadline_time, **kwargs):
        super(TheCard, self).__init__(**kwargs)
        self.task_txt= str(task_txt)
        self.app2= app2
        self.description_txt= str(description_txt)
        self.deadline_date= deadline_date
        self.deadline_time= deadline_time
        self.bg_color= bg_color
        self.fields_clr= list(self.bg_color)
        self.fields_clr.remove(self.fields_clr[1])
        self.fields_clr.insert(1, self.bg_color[1]+(62/255))
        self.orientation= 'vertical'
        self.size_hint_y= None
        self.md_bg_color= self.bg_color
        self.temp_height= 290
        self.height= self.temp_height
        self.elevation= 12
        self.float= FloatLayout()
        self.turn= []

        #send data to the database to get stored:
        self.data= GetData(self.task_txt, self.description_txt, self.bg_color,
                            self.deadline_date, self.deadline_time)
        self.data.get_data()

        # edit and delete btns:
        self.upper_btns= BoxLayout(orientation='horizontal', size_hint=(.4, .20),
                                   pos_hint={'top':.99, "right":.4}, spacing=14, padding=8)
        self.done= MDFloatingActionButton(md_bg_color= get_color_from_hex('#FF3D00'), icon='calendar-check',size_hint=(None, None), size=(50,50),elevation=10, theme_text_color='Custom',text_color=[1,1,0,1])
        self.delete= MDFloatingActionButton(icon='calendar-remove',size_hint=(None, None), size=(50,50),elevation=10)
        self.upper_btns.add_widget(self.done)
        self.upper_btns.add_widget(self.delete)

        # adding callbacks to the edit and delete btns:
        self.delete.bind(on_press=lambda x:self.app2.count_update(self.task_txt, self.description_txt, self.bg_color,
                         self.deadline_date, self.deadline_time, 'delete'))
        self.delete.bind(on_release= lambda x :self.app2.anime2(self)) 
        
        self.done.bind(on_press= lambda x:self.app2.count_update(self.task_txt, self.description_txt, self.bg_color,
                         self.deadline_date, self.deadline_time, 'done'))
        self.done.bind(on_release= lambda x :self.app2.anime3(self)) 
        
        # adding the task and description holders:
        self.task_place= MDTextFieldRect(size_hint=(.95, .2), pos_hint={'center_x':.5, 'top':.77}, font_size='20sp',
                                         text=self.task_txt,readonly=True, background_color=self.fields_clr)
        self.desc_place= MDTextFieldRect(size_hint=(.95, .35), pos_hint={'center_x':.5, 'top':.55},
                                         text=self.description_txt, readonly=True, hint_text='No Description...',
                                         background_color=self.fields_clr, font_size='18sp')
        # adding the deadline on the MDCard                            
        if self.deadline_date != '' and self.deadline_time != '':
            self.deadline_date=self.deadline_date.split('-')
            self.deadline_time=self.deadline_time.split(':')
            if float(self.deadline_time[0]) >= 12:
                a="PM"
            else:
                a="AM"
            self.show_deadline= MDLabel(text=f'Deadline: {str(self.deadline_date[1])+"/"+str(self.deadline_date[2])+"/"+str(self.deadline_date[0])} at {str(self.deadline_time[0])+":"+str(self.deadline_time[1])} {a}',
            size_hint=(.95,.1), pos_hint={'top':.18, "center_x":.5})
            self.days_left_count()
            Clock.schedule_interval(self.update_txt, 0.5)            

            self.float.add_widget(self.show_deadline)
            self.app2.deadline_date=""
            self.app2.deadline_time=""

        else: 
            self.show_deadline= MDLabel(text= 'No Deadline', size_hint=(.95,.1), pos_hint={'top':.18, "center_x":.5})
            self.app2.deadline= self.show_deadline.text
            self.float.add_widget(self.show_deadline)
            self.app2.deadline_date=""
            self.app2.deadline_time=""

        self.float.add_widget(self.upper_btns)
        self.float.add_widget(self.task_place)
        self.float.add_widget(self.desc_place)
        self.add_widget(self.float)

    def days_left_count(self):
        self.show_days_left= MDLabel(text='', size_hint=(1,.12), pos_hint={'top':.11, "x":.025}, theme_text_color='Custom', bold= True, markup= True)
        self.float.add_widget(self.show_days_left)

    def update_txt(self, *args):
        year_now= datetime.now().date().year
        month_now= datetime.now().date().month
        day_now= datetime.now().date().day
        year= int(self.deadline_date[0])
        month= int(self.deadline_date[1])
        day= int(self.deadline_date[2])
        hour_now= datetime.now().time().hour
        minute_now= datetime.now().time().minute
        sec_now= datetime.now().time().second
        self.days_left= [(year-year_now)*365, (month-month_now)*30, (day-day_now)]
        self.days_left=sum(self.days_left)
        self.hours_left= 24-hour_now
        self.minutes_left= 60-minute_now
        self.second_left= 60-sec_now
        if self.days_left==0:
            self.txt='Task is [color=#00FF00]TODAY[/color]'
            self.clr= [0,0,0,1]
        elif self.days_left<0:
            self.txt='Task is [color=#FF0000]OVERDUE[/color]'
            self.clr= [0,0,0,1]
        else:     
            self.txt='ONLY [color=#0000BB][b]'+str(self.days_left)+'days, '+str(self.hours_left)+'h, '+str(self.minutes_left)+'min, '+str(self.second_left)+'s[/b][/color] REMAINING'
            self.clr= [0,0,0,1]

        self.show_days_left.text=self.txt
        self.show_days_left.text_color=self.clr