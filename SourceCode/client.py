# Echo client program
#import socket
import time
from datetime import datetime
import can
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import threading
from threading import Thread, Lock
import pandas as pd
import copy
import http.client
import subprocess

dic = {'Time': None, 'Steering_Angle': None, 'Drive_Torque':None, 'Engine_RPM':None, 'Vechlie_Speed':None, \
       'Steering_Torque':None, 'Yaw_Rate':None, 'SAS_Angle':None, 'SAS_Speed':None}



frame3dArray = []
frameArray = []

json_file = open('/home/pi/model/model_rnn5.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

predict_progress = 0
q =0
#one process
model= model_from_json(loaded_model_json)
dummy_array = np.array(np.zeros((100,100,2 )))

#model.load_weights("/home/pi/model/model_rnn5.h5")
#model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
#model.predict(dummy_array)

wait_10sec = 0

predict_cnt =0

def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

def make_list(type, value):
    # 0: Time(timestamp)
    # 1: Steering_Angle(deg)
    # 2: Drive_Torque(Nm)
    # 3: Engine_RPM(RPM)
    # 4: Vechlie_Speed(km/h)
    # 5: Steering_Torque(Nm)
    # 6: Yaw_Rate
    # 7: SAS_Angle(deg)
    # 8: SAS_Speed(deg/s)

    if type == 0:
        dic['Time'] = value
    elif type == 1:
        dic['Steering_Angle'] = value
    elif type == 2:
        dic['Drive_Torque'] = value
    elif type == 3:
        dic['Engine_RPM'] = value
    elif type == 4:
        dic['Vechlie_Speed'] = value
    elif type == 5:
        dic['Steering_Torque'] = value
    elif type == 6:
        dic['Yaw_Rate'] = value
    elif type == 7:
        dic['SAS_Angle'] = value
    elif type == 8:
        dic['SAS_Speed'] = value

time_length = 50

time_time = time.time()
drowsy_time = 0

def predict_rule(angList, sasSpdList):
    global time_time
    global drowsy_time
    time_time = time.time()
    if (np.abs(np.max(angList) - np.min(angList)) > 40) & (np.max(sasSpdList) > 150):
        if (time_time - drowsy_time) > 2 :
            drowsy_time = time.time()
            print("drowsy!!!!!! ", predict_cnt)
            t = send_message_phone()
            t.start()
            return 1
    return 0
        
    #else :
    #    print("wake")

def ready_to_send():
    # all data gathered
    if (sum(x is not None for x in dic.values()) == 9):
        # ok

        send_list = []
        send_list.append(dic['Time'])
        send_list.append(dic['Steering_Angle'])
        send_list.append(dic['SAS_Speed'])
        send_list.append(dic['Drive_Torque'])
        send_list.append(dic['Engine_RPM'])
        send_list.append(dic['Vechlie_Speed'])
        send_list.append(dic['Steering_Torque'])
        send_list.append(dic['Yaw_Rate'])
        send_list.append(dic['SAS_Angle'])


        # initialize
        dic['Time'] = None
        dic['Steering_Angle'] = None
        dic['Drive_Torque'] = None
        dic['Engine_RPM'] = None
        dic['Vechlie_Speed'] = None
        dic['Steering_Torque'] = None
        dic['Yaw_Rate'] = None
        dic['SAS_Angle'] = None
        dic['SAS_Speed'] = None

        #print(send_list)
        return send_list

    else:
        return False

host = 'fcm.googleapis.com'
url = '/fcm/send'

headers={'Content-type': 'application/json; charset=utf-8', 'Authorization':'key=AAAAMNnIqHM:APA91bG5jhFHpFL08BFVAHXf9bklXz4tL3AG815yXFa5q-Dp4yXN-gkSzW2cP4rBpXcYFWzLNgKV2FJX9JWrKcuVvmqd-QGAQMu2D1FoAXhdQ9gNZkz7OKiswUPk3CePmtatKtzVxOUBLfX2kazG6Uzy89rO-0gnUw'}

request_body = '{"data" : {"message" : "message"},"to" : "/topics/notice"}'
conn = http.client.HTTPSConnection(host)
k=0
send_threads=[]
class send_message_phone(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        print('start')
        conn.request("POST", url, headers=headers, body=request_body.encode('utf-8'))
        response = conn.getresponse()
        data = response.read()
        print(data.decode("utf-8"))


class predict(Thread):
    def __init__(self, name, frame_Array, model_index):
        Thread.__init__(self)
        self.name=name
        self.fixed=0
        self.frame_Array = frame_Array
        self.model_index = model_index

    def run(self):
        predict_drowsy = 0
        #one thread
        predict_val = model.predict(np.array(self.frame_Array))

        print(q)
        #multi threads
        #predict_val = model_list[self.model_index].predict(np.array(self.frame_Array))
        #print(predict_val.shape[0])
        for i in range(predict_val.shape[0]):
            if predict_val[i,1] > 0.501 :
                predict_drowsy = predict_drowsy + 1
                if predict_drowsy == 5:
                    print('drowsy')
                    predict_progress = 0
                    threds = send_message_phone()
                    send_threads.append(threds)
                    threds.start()
                    #wait_10sec = 1
                    #send_message_phone()
                    break
        #print('predict end')


if __name__ == "__main__":

    how_many_subprocess = 0
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((HOST, PORT))

    i = 0
    j = 0

    #data = '1479999575.683247  000e  000  8 3f ff 20 00 00 00 00 2b '


    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

    threds_list=[]

    #send_message_phone()

    for msg in bus:
        if msg.arbitration_id == 897 or \
                    msg.arbitration_id == 870 or \
                    msg.arbitration_id == 593 or \
                    msg.arbitration_id == 544 or \
                    msg.arbitration_id == 688:

            # block padding
            if 8 != len(msg.data):
                pad = [0] * (8 - len(msg.data))
                msg.data.extend(pad)

            data = str(msg)
            # print(data)
            # print(len(data))

            # convert #
            message = data.split()

            time_now = float(message[0])
            make_list(0, time_now)

            if (message[1] == '0381'):

                ############angle############################
                #angle = str(int(message[-4],16) << 8 ) + str(int(message[-5],16) & 0xff)
                angle = message[8] + message[7]
                #str(int(message[-4],16) & 0x7f)
                #print('Steering_Angle(deg) :', int(angle, 16) * 0.1)
                ##make_list(1, int(angle, 16) * 0.1)
                #############################################

                #print(twos_comp(int(angle, 16), 16))
                
                #strAnglemsb = int(message[8],16)
                #strAnglelsb = int(message[7],16)
                #print(bin(strAnglelsb), message[7])
                strAngle = twos_comp(int(angle, 16), 16) * 0.1
                #print("Angle = ", strAngle)
                #str(int(message[-4],16) & 0x7f)
                #print('Steering_Angle(deg) :', int(angle, 16) * 0.1)
                make_list(1, strAngle)

                ############drive_torque#####################
                bin_a = int(message[6], 16)
                bin_b = int(message[5], 16)
                drive_torque = (bin_a << 5 | bin_b >> 3) * 0.01 - 20.48
                #print('Drive_Torque(Nm) : ', drive_torque)
                make_list(2, drive_torque)
                #############################################

            elif (message[1] == '0366'):
                ############engine_rpm & vechile speed#####################
                bin_a = int(message[6], 16)
                bin_b = int(message[5], 16)
                bin_vs = int(message[9], 16)
                engine_rpm = (bin_a << 8 | bin_b) * 0.25
                vechile_speed = bin_vs * 1.00
                #print('Engine_RPM(RPM) : ', engine_rpm)
                make_list(3, engine_rpm)
                #print('Vechlie_Speed(km/h) : ', vechile_speed)
                make_list(4, vechile_speed)

            elif (message[1] == '0251'):
                ############Steering_Torque######################
                strTqlsb = int(message[9], 16)
                strTqmsb = int(message[10], 16)
                strTq = (strTqmsb << 8 | strTqlsb) * 0.01 - 20.48
                #print('Steering_Torque(Nm) : ', strTq)
                make_list(5, strTq)

            elif (message[1] == '0220'):
                ############Yaw_Rate######################
                yawRatelsb = int(message[9], 16)
                yawRatemsb = int(message[10], 16) & int('0x1F', 16)
                yawRate = (yawRatemsb << 8 | yawRatelsb) * 0.01 - 40.95
                #print('Yaw_Rate : ', yawRate)
                make_list(6, yawRate)

            elif (message[1] == '02b0'):
                ############Steering Angle & Speed######################
                sasAnglelsb = int(message[4], 16)
                sasAnglemsb = int(message[5], 16)
                sasAngle = (sasAnglemsb << 8 | sasAnglelsb) * 0.1
                #sasSpeed = twos_comp(int(message[6], 16), 8) * 4
                sasSpeed = int(message[6], 16) * 4
                #print("speed = ", sasSpeed)
                #print('SAS_Angle(deg) : ', sasAngle)
                make_list(7, sasAngle)
                #print('SAS_Speed(deg/s) : ', sasSpeed)
                make_list(8, sasSpeed)


        dataFrame = ready_to_send()
        if dataFrame is not False:
            ##################################
            #print(type(dataFrame))
            #msg = ','.join(str(v) for v in dataFrame)
            #print(str(how_many_subprocess) + 'call')
            #subprocess.Popen("/usr/bin/python3 /home/pi/PycharmProjects/pican_snc/sender.py " + msg + ' ' + str(how_many_subprocess), shell=True)
            #print(str(how_many_subprocess) + 'end')
            #how_many_subprocess = how_many_subprocess + 1
            ##################################


            dataFrame_for_predict = copy.copy(dataFrame[1:3])

            frameArray.append(dataFrame_for_predict)
            ax = np.array(frameArray)

            #predict_rule(ax[:, 0], ax[:,1])
            drowsy_predict_val = 0

            if ax.shape[0] > 50:
                del frameArray[0]
                drowsy_predict_val = predict_rule(ax[:,0], ax[:,1])
                if(k==0):
                    print("ready to start")
                    k=k+1
             
            ##################################
            #print(type(dataFrame))
            msg = ','.join(str(v) for v in dataFrame)
            msg = msg+','+str(drowsy_predict_val)
            #print(str(how_many_subprocess) + 'call')
            subprocess.Popen("/usr/bin/python3 /home/pi/PycharmProjects/pican_snc/sender.py " + msg + ' ' + str(how_many_subprocess), shell=True)
            #print(str(how_many_subprocess) + 'end')
            how_many_subprocess = how_many_subprocess + 1
            ##################################



            # send dataframe

            #s.sendall(pickle.dumps(dataFrame))
            #sign = s.recv(2)
            #if sign.decode() == 'ok':
                #print ('Sended Completed !')
            #    continue

    #s.close()