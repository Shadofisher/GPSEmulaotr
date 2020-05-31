from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Combobox
from tkinter.ttk import Notebook
from tkinter import filedialog as fd
import serial
import pynmea2
import serial.tools.list_ports
import time

seperator = ','

baudrate = ['1200','2400','4800','9600','57600','115200']


class Window:
    """Create initial button"""
    def __init__(self):
        self.master = Tk()
        self.master.geometry('1200x800')
        self.i = 100
        self.port = ''
        self.button1 = TKButton(self.master,10,20,"Open NMEA file",self.button_callback)
        self.button2 = TKButton(self.master,280,20,"Open Comport",self.button_callback)
        self.button3 = TKButton(self.master,280,80,"Start",self.button_callback)
        self.button4 = TKButton(self.master,180,20,"Pause",self.button_callback)
        self.progressbars = [TKProgress(self.master,10,(self.i+n*25)) for n in range(15)]
        self.progressbars2 = [TKProgress(self.master,300,(self.i+n*25)) for n in range(15)]
        self.label_spd = Label(self.master, text = '0 km/h')
        self.label_spd.place(x =10,y =500)
        self.nmeafilename = ''
        self.cb = Combobox(self.master,values = self.list_comports())
        self.cb.place(x =420, y = 25)
        self.cb.bind('<<ComboboxSelected>>', self.on_select)
        self.cb2 = Combobox(self.master,values = baudrate)
        self.cb2.place(x =420, y = 50)
        self.cb2.bind('<<ComboboxSelected>>', self.baudrate_on_select)

    def baudrate_on_select(self, id):
        print(self.cb2.get())
        self.baudrate = self.cb2.get()
    def on_select(self, id):
        print(self.cb.get())
        self.port = self.cb.get().split(' ')[0]

    def getid(self):
        return(self.master)

    def list_comports(self):
        return serial.tools.list_ports.comports()


    def button_callback(self,i):
        if i == 'Start':
            self.master.after(1000,self.com_periodic_read)
            self.master.after(1000, self.com_periodic_write)
        if i == 'Open NMEA file':
            self.nmeafilename = fd.askopenfilename()
            self.NMEA_DATA = [line.split(',') for line in open(self.nmeafilename,'r') if not "VERSION" in line if not "$PMTK" in line if 'GPS_NMEA_Str' in line ]
            self.NMEA_DATA.sort(key = lambda i: i[4])
            self.timestamps =[self.NMEA_DATA[i][4] for i in range(len(self.NMEA_DATA))]
            current_timestamp = self.timestamps[0]
            for i in range((len(self.NMEA_DATA))):
                #self.com_periodic_read()
                self.msg = ','.join(self.NMEA_DATA[i][5:])
                tmp = self.msg
                #print(self.msg)
                if 'GPGSV' in  tmp:
                    self.use_gps = 1
                else:
                    self.use_gps = 0
                if 'GLGSV' in  tmp:
                    self.use_glonass = 1
                else:
                    self.use_glonass = 0
                self.msg = pynmea2.parse(self.msg)
                #print(str(self.msg.sentence_type) + str(self.timestamps[i]))
                if current_timestamp == self.timestamps[i]:
                    print(tmp)
                else:
                    time.sleep(0.1)
                    current_timestamp = self.timestamps[i]
                    print(current_timestamp)
                if self.msg.sentence_type == 'VTG':
                    self.label_spd['text'] = str(int(self.msg.spd_over_grnd_kmph)) + ' ' +'km/h'
                if self.msg.sentence_type == 'GSV' and self.use_gps == 1:
                    if self.msg.msg_num == '1':
                        if self.msg.snr_1:
                            self.progressbars[0].set_progress(float(self.msg.snr_1))
                        if self.msg.snr_2:
                            self.progressbars[1].set_progress(int(self.msg.snr_2))
                        if self.msg.snr_3:
                            self.progressbars[2].set_progress(int(self.msg.snr_3))
                        if self.msg.snr_4:
                            self.progressbars[3].set_progress(int(self.msg.snr_4))
                    if self.msg.msg_num == '2':
                        if self.msg.snr_1:
                            self.progressbars[4].set_progress(float(self.msg.snr_1))
                        if self.msg.snr_2:
                            self.progressbars[5].set_progress(int(self.msg.snr_2))
                        if self.msg.snr_3:
                            self.progressbars[6].set_progress(int(self.msg.snr_3))
                        if self.msg.snr_4:
                            self.progressbars[7].set_progress(int(self.msg.snr_4))
                    if self.msg.msg_num == '3':
                        if self.msg.snr_1:
                            self.progressbars[8].set_progress(float(self.msg.snr_1))
                        if self.msg.snr_2:
                            self.progressbars[9].set_progress(int(self.msg.snr_2))
                        if self.msg.snr_3:
                            self.progressbars[10].set_progress(int(self.msg.snr_3))
                        if self.msg.snr_4:
                            self.progressbars[11].set_progress(int(self.msg.snr_4))
                    if self.msg.msg_num == '4':
                        if self.msg.snr_1:
                            self.progressbars[12].set_progress(float(self.msg.snr_1))
                        if self.msg.snr_2:
                            self.progressbars[13].set_progress(int(self.msg.snr_2))
                        if self.msg.snr_3:
                            self.progressbars[14].set_progress(int(self.msg.snr_3))
                        if self.msg.snr_4:
                            self.progressbars[15].set_progress(int(self.msg.snr_4))
                    self.master.update_idletasks()

                if self.msg.sentence_type == 'GSV' and self.use_glonass==1:
                    if self.msg.msg_num == '1':
                        if self.msg.snr_1:
                            self.progressbars2[0].set_progress(float(self.msg.snr_1))
                        if self.msg.snr_2:
                            self.progressbars2[1].set_progress(int(self.msg.snr_2))
                        if self.msg.snr_3:
                            self.progressbars2[2].set_progress(int(self.msg.snr_3))
                        if self.msg.snr_4:
                            self.progressbars2[3].set_progress(int(self.msg.snr_4))
                    if self.msg.msg_num == '2':
                        if self.msg.snr_1:
                            self.progressbars2[4].set_progress(float(self.msg.snr_1))
                        if self.msg.snr_2:
                            self.progressbars2[5].set_progress(int(self.msg.snr_2))
                        if self.msg.snr_3:
                            self.progressbars2[6].set_progress(int(self.msg.snr_3))
                        if self.msg.snr_4:
                            self.progressbars2[7].set_progress(int(self.msg.snr_4))
                    if self.msg.msg_num == '3':
                        if self.msg.snr_1:
                            self.progressbars2[8].set_progress(float(self.msg.snr_1))
                        if self.msg.snr_2:
                            self.progressbars2[9].set_progress(int(self.msg.snr_2))
                        if self.msg.snr_3:
                            self.progressbars2[10].set_progress(int(self.msg.snr_3))
                        if self.msg.snr_4:
                            self.progressbars2[11].set_progress(int(self.msg.snr_4))
                    if self.msg.msg_num == '4':
                        if self.msg.snr_1:
                            self.progressbars2[12].set_progress(float(self.msg.snr_1))
                        if self.msg.snr_2:
                            self.progressbars2[13].set_progress(int(self.msg.snr_2))
                        if self.msg.snr_3:
                            self.progressbars2[14].set_progress(int(self.msg.snr_3))
                        if self.msg.snr_4:
                            self.progressbars2[15].set_progress(int(self.msg.snr_4))
                    self.master.update_idletasks()


        if i == 'Open Comport':
            print('Opening port')
            print("Serial port selected is: " + str(self.port))
            self.ser = serial.Serial(self.port, self.baudrate,timeout=1)
            print(self.ser.name)

    def com_periodic_read(self):
        #self.master.after(100, self.com_periodic_read)
        line = self.ser.readline();
        print(line)
        #print("Reading")
    def com_periodic_write(self):
        self.master.after(1000, self.com_periodic_write)
        #print("Writing")
        pass




class TKButton:
    """Create initial button"""
    def __init__(self, win, x, y, text,cb):
        self.posx = x
        self.posy = y
        self.button = Button(win,text = text,command = lambda i=text:cb(i))
        self.button.place(x = self.posx, y=self.posy)
        self.nmeafilename = ''
    def get_position(self):
        return(self.posx,self.posy)


class TKProgress:
    """Create initial button"""
    def __init__(self, win, x, y):
        self.posx = x
        self.posy = y
        self.progress = Progressbar(win,length = 200,mode='determinate')
        self.progress.place(x = self.posx, y=self.posy)
    def get_position(self):
        return(self.posx,self.posy)
    def set_progress(self,value):
        self.progress['value'] = value

def callback():
    pass

def main():
    win = Window()



    win.getid().mainloop()

main()