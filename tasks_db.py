class GetData:
    def __init__(self, task_data, desc_data, color_data, deadline_date, deadline_time):
        self.task_data= task_data
        self.desc_data= desc_data
        self.color_data= color_data
        self.jump= ''
        self.deadline_data= deadline_date +'-'+deadline_time
        
    def get_data(self):
        with open('database\\tasks_db.txt', 'r') as db0: 
            self.data_lines= db0.readlines()
        with open('database\\tasks_db.txt', 'r') as db00:
            self.content= db00.read()
        self.store_data()
            
    # this method is responsible for storing the tasks data in the database file when they get added:
    def store_data(self):
        self.descision=[]
        with open('database\\tasks_db.txt', 'a') as db1:
            if self.content == '':
                self.idd= '1'
            else:
                self.idd= str(int(self.data_lines[-1][3])+1)
    
            if len(self.data_lines) != 0:
                for line in self.data_lines:
                    line= str(line[5:].strip())
                    if line == f'{self.task_data};{self.desc_data};{self.deadline_data};{self.color_data[0]};{self.color_data[1]};{self.color_data[2]};{self.color_data[3]}':
                        self.descision.append(1)
                    elif line != f'{self.task_data};{self.desc_data};{self.deadline_data};{self.color_data[0]};{self.color_data[1]};{self.color_data[2]};{self.color_data[3]}':
                        pass
                if len(self.descision) == 0:   
                    db1.write(f'ID:{self.idd}>{self.task_data};{self.desc_data.strip()};{self.deadline_data};{self.color_data[0]};{self.color_data[1]};{self.color_data[2]};{self.color_data[3]}\n')
                else:
                    pass
            elif len(self.data_lines) == 0:
                db1.write(f'ID:{self.idd}>{self.task_data};{self.desc_data.strip()};{self.deadline_data};{self.color_data[0]};{self.color_data[1]};{self.color_data[2]};{self.color_data[3]}\n')

    # this method is responsible for sending the tasks data to the cards generator when the app starts
    def send_data(self):
        with open('database\\tasks_db.txt', 'r') as db2:
            self.data_lines2= db2.readlines()
            if len(self.data_lines2) == 0:
                return 'database empty'
            else:
                self.data_lines2 = [line.strip() for line in self.data_lines2]
                return self.data_lines2

    # this method is responsible for deleting the task data from the database file:
    def delete_data(self,task, desc, clr, date, time):
        self.task=task
        self.desc=desc
        self.clr=clr
        self.date=('-').join(date)+'-'+(':').join(time)
        self.victim= str(self.task)+';'+str(self.desc)+';'+str(self.date)+';'+str(self.clr[0])+';'+str(self.clr[1])+';'+str(self.clr[2])+';'+str(self.clr[3])
        self.the_lines=[]

        with open('database\\tasks_db.txt', 'r') as target:
            self.lista= target.readlines()
        for one in self.lista:
            self.the_lines.append(one[5:].strip())

        for line in self.the_lines:
            if line == self.victim:
                self.the_lines.remove(line)
            elif line != self.victim:
                pass

        with open('database\\tasks_db.txt', 'w') as target1:
            target1.write('')

        with open('database\\tasks_db.txt', 'w+') as target2:
            for num, the_line in enumerate(self.the_lines):
                target2.write('ID:'+str(num+1)+'>'+the_line+'\n')
