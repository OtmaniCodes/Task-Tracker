from kivy.uix.popup import Popup
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex

class PopContent(Popup):
    def __init__(self, app, **kwargs):
        super(PopContent, self).__init__(**kwargs)
        self.app= app
        self.title='add a new task'.upper()
        self.title_size= "24dp"
        self.title_color= get_color_from_hex('#FF3D00')
        self.title_align= 'center'
        self.size_hint= None, None
        self.width=340
        self.height=480
        self.pos_hint= {'top':.9, 'center_x':.5}
        self.containerr= FloatLayout()
        self.separator_color= [1,0,0,1]
        self.auto_dismiss= False
        # the task and description text feilds:
        self.task = MDTextFieldRect(size_hint=(.98, .1), pos_hint={'top':.97,'center_x':.5}, font_size='20sp',multiline=False,
                                    hint_text="task".title(),background_color=[139/255,139/255,139/255,1],
                                    hint_text_color=[40/255,40/255,40/255,1])
        self.describe = MDTextFieldRect(size_hint=(.98, .2), pos_hint={'top':.82,'center_x':.5},
                                        hint_text='Brief Description...', font_size='16sp',
                                        background_color=[139/255,139/255,139/255,1], hint_text_color=[40/255,40/255,40/255,1], )
        self.task.bind(on_text_validate= self.focus_descp)
        # the deadline picker btn:
        self.deadline = MDRaisedButton(size_hint=(.98, .08), pos_hint={'center_x':.5, 'top':.58},
                                     text='Pick a Deadline', font_size='20dp')
        self.deadline.bind(on_release= self.app.show_datepicker)

        self.priority= MDLabel(text='select a lavel of priority:'.upper(), size_hint=(.9, None), height=100, pos_hint={'top':.56, 'x':.015}, 
                                text_size= '4sp', theme_text_color="Custom", text_color=get_color_from_hex('#FF3D00'), bold=True)
        self.btns_box= GridLayout(rows=1, size_hint=(.98,.2),
                                pos_hint={'top':.399, 'x':.01}, spacing=6)
        # colored btns in btns_box1                  
        self.priority1= Button(text='', background_normal='', background_color=[1.0,199/255,115/255,1.0])
        self.priority2= Button(text='', background_normal='', background_color=[251/255,170/255,48/255,1.0])
        self.priority3= Button(text='', background_normal='', background_color=[247/255,154/255,16/255,1.0])                  
        self.priority4= Button(text='', background_normal='', background_color=[215/255,133/255,9/255,1.0])
        self.priority5= Button(text='', background_normal='', background_color=[189/255,116/255,5/255,1.0])
        self.priority6= Button(text='', background_normal='', background_color=[155/255,97/255,9/255,1.0])
        self.priority7= Button(text='', background_normal='', background_color=[119/255,71/255,0.0,1.0])
        self.priority8= Button(text='', background_normal='', background_color=[121/255,78/255,15/255,1.0])
        self.priority9= Button(text='', background_normal='', background_color=[89/255,58/255,11/255,1.0])
        
        # adding colored btns to the boxlayout
        self.btns_box.add_widget(self.priority1)
        self.btns_box.add_widget(self.priority2)
        self.btns_box.add_widget(self.priority3)
        self.btns_box.add_widget(self.priority4)
        self.btns_box.add_widget(self.priority5)
        self.btns_box.add_widget(self.priority6)
        self.btns_box.add_widget(self.priority7)
        self.btns_box.add_widget(self.priority8)
        self.btns_box.add_widget(self.priority9)
        
        # making callbacks of the colores btns
        self.priority1.bind(on_release=lambda x: self.app.which_clr(0))
        self.priority2.bind(on_release=lambda x: self.app.which_clr(1))
        self.priority3.bind(on_release=lambda x: self.app.which_clr(2))
        self.priority4.bind(on_release=lambda x: self.app.which_clr(3))
        self.priority5.bind(on_release=lambda x: self.app.which_clr(4))
        self.priority6.bind(on_release=lambda x: self.app.which_clr(5))
        self.priority7.bind(on_release=lambda x: self.app.which_clr(6))
        self.priority8.bind(on_release=lambda x: self.app.which_clr(7))
        self.priority9.bind(on_release=lambda x: self.app.which_clr(8))

        # ADD and CANCEL btns
        self.bottom_box= BoxLayout(orientation='horizontal',size_hint=(.98, .08),
                            pos_hint={'top':.1, 'x':.01}, spacing=14)
        
        self.add= MDRaisedButton(text='ADD', font_size='20dp', size_hint=(1,1))
        self.cancel= MDRaisedButton(text='CANCEL', font_size='20dp', size_hint=(1,1))

        # adding ADD and CANCEL btns to the boxlayout
        self.bottom_box.add_widget(self.cancel)
        self.bottom_box.add_widget(self.add)

        # making callbacks of the ADD and CANCEL btns
        self.add.bind(on_press=lambda x: self.app.get_task_description(self.task.text, self.describe.text)
             if self.task.text != '' and app.check_three() == True else app.warning('add_btn'))
        self.add.bind(on_release=lambda x: self.dismiss() if self.task.text != '' and app.check_three() == True else self.dismiss==False)
        self.cancel.bind(on_release=self.dismiss)

        self.arrow= MDIcon(icon='ray-start-arrow', theme_text_color='Custom',
                            text_color=get_color_from_hex('#FF3D00'), size_hint=(None, None),font_size='55sp',
                            size=(50,50),pos_hint={'top':.22, 'x':0})

        # adding all widgets to the container which is a floatlayout
        self.containerr.add_widget(self.task)
        self.containerr.add_widget(self.describe)
        self.containerr.add_widget(self.deadline)
        self.containerr.add_widget(self.priority)
        self.containerr.add_widget(self.btns_box)
        self.containerr.add_widget(self.arrow)
        self.containerr.add_widget(self.bottom_box)
        self.add_widget(self.containerr)

    def focus_descp(self, *args):
        self.describe.focus= True