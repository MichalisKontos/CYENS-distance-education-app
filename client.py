import socket
import numpy as np
import cv2
import onnx
from onnx_tf.backend import prepare 
from PIL import Image
import time
import sys

# Promt the user to select if they want to use the client with the server
# or the client alone (action recognition only)
val = str(input("Do you want to use the client with the server or alone? type a for alone or s for server: "))
if val == "s":
    toConnect = True
elif val == "a":
    toConnect = False
else:
    print("Input not recognized try again")
    sys.exit()

# If user wants to connect with the server
if toConnect:
    # host address - if using different pc, the host must have the 
    # ip address of the pc running the server, else leave as is
    # host = '192.168.10.3' #for example
    host = socket.gethostname()
    port = 1234

    ClientSocket = socket.socket()

    print('Waiting for connection')

    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    # First send the ID to the server
    Input = input('Your ID: ')
    ClientSocket.send(str.encode(Input))

#------------------------------
# Load ONNX model
load_model = onnx.load('gnet15D.onnx')
model = prepare(load_model) 

actions = ('Absent', 'Attending', 'Hand raising', 'Looking elsewhere', 'Telephone call', 'Using phone', 'Writing')
#------------------------------

# Start webcam video
cap = cv2.VideoCapture(0)

while True:
    actions_count = {"Absent":0,
                    "Attending" :0,
                    "Hand raising":0,
                    "Looking elsewhere":0,
                    "Telephone call":0,
                    "Using phone":0,
                    "Writing":0}

    time_end = time.time() + 10
    while(time.time() < time_end):

        ret, cv2_img = cap.read()
        
        if ret is True:
            # From cv2 frame to PIL image
            pil_img = Image.fromarray(cv2_img).resize((224, 224))

            # Preprocessing
            # Change pillow image to a numpy array with dimensions (3,224,224)
            input_img = np.asarray(pil_img).astype('float32')
            input_img = np.moveaxis(input_img, -1,0)
            # print(input_img.shape) #(3,224,224)
            
            # Make prediction on image
            predictions = model.run(input_img) 
            
            # Take the index of the maximum probability and define it from the list of actions
            max_index = np.argmax(predictions[0])
            action = actions[max_index]
            # print(action)

            if action in actions_count:
                actions_count[action] += 1
            
            #write action text on webcam video
            # cv2.putText(cv2_img, action, (int(200), int(200)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            # cv2.imshow('img',cv2_img)

        else:
            #------------------------------------------------------------------
            # For testing purposes - if the same pc runs 2 clients, they cannot both
            # use the webcam video, so the second one comes in the else statement 
            actions_count = {"Absent":0,
                    "Attending" :0,
                    "Hand raising":0,
                    "Looking elsewhere":0,
                    "Telephone call":0,
                    "Using phone":0,
                    "Writing":1}
            #------------------------------------------------------------------

            # #kill open cv things		
            # cap.release()
            # cv2.destroyAllWindows()
            # #close socket
            # ClientSocket.close()
    
    max_action = max(actions_count, key=actions_count.get)
    print(f"Most performed action: {max_action} ({actions_count[max_action]} times)")
    if toConnect:
        ClientSocket.send(str.encode(max_action))