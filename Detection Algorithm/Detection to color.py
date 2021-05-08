
#red colour 166,84,141   (180,255,255)
#green 66, 122, 129  (86,255,255)  
#blue      97, 100, 117       (117,255,255)    orange  0, 50, 80   20,255,255
 
HUE_VAL = 10
#                      
# lower_color = np.array([166, 84, 141])
#     upper_color = np.array([180,255,255])
# #
# lower_color = np.array([66,122,129])#green
# upper_color = np.array([80,255,255])            
# #
# lower_color = np.array([0,100,100])#blue
# upper_color = np.array([20,255,255])


 
lower_color = np.array([HUE_VAL-10,100,100])
upper_color = np.array([HUE_VAL+10, 255, 255])


def init():    
 
 
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
def forward():
    init()
    GPIO.output(17, True)
    GPIO.output(22, False)
    GPIO.output(23, True)
    GPIO.output(24, False)
    time.sleep(0.5)

def reverse():
    init()
    GPIO.output(17, False)
    GPIO.output(22, True)
    GPIO.output(23, False)
    GPIO.output(24, True)
    time.sleep(0.5)
   
def left_turn():
    init()
    GPIO.output(17, False)
    GPIO.output(22, False)
    GPIO.output(23, True)
    GPIO.output(24, False)
    time.sleep(0.5)
 
def right_turn():
    init()
    GPIO.output(17, True)
    GPIO.output(22, False)
    GPIO.output(23, False)
    GPIO.output(24, False)
    time.sleep(0.5)
   
def stop():
    init()
    GPIO.output(17, False)
    GPIO.output(22, False)
    GPIO.output(23, False)
    GPIO.output(24, False)
    time.sleep(0.5)
   
def ultra_r():
    global distance_r  
    GPIO.output(TRIG, False)                 #Set TRIG as LOW

    time.sleep(1)                            #Delay of 2 seconds

    GPIO.output(TRIG, True)                  #Set TRIG as HIGH
    time.sleep(0.00001)                      #Delay of 0.00001 seconds
    GPIO.output(TRIG, False)#Set TRIG as LOW

 

    while GPIO.input(ECHO)==0:
        #Check whether the ECHO is LOW
        pulse_start = time.time()              #Saves the last known time of LOW pulse
    while GPIO.input(ECHO)==1:
        #Check whether the ECHO is HIGH
        pulse_end = time.time()
        #Saves the last known time of HIGH pulse
        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable
        distance_r= pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance_r = round(distance_r, 2)
        print("distance_r=",distance_r)#Round to two decimal points

def ultra_l():
    global distance_l  
    GPIO.output(TRIG1, False)                 #Set TRIG as LOW
    time.sleep(1)                            #Delay of 2 seconds
    GPIO.output(TRIG1, True)                  #Set TRIG as HIGH
    time.sleep(0.00001)                      #Delay of 0.00001 seconds
    GPIO.output(TRIG1, False)#Set TRIG as LOW
    while GPIO.input(ECHO1)==0:
        #Check whether the ECHO is LOW
        pulse_start1 = time.time()              #Saves the last known time of LOW pulse
    while GPIO.input(ECHO1)==1:
        #Check whether the ECHO is HIGH
        pulse_end1 = time.time()
        #Saves the last known time of HIGH pulse
        pulse_duration1 = pulse_end1 - pulse_start1 #Get pulse duration to a variable
        distance_l= pulse_duration1 * 17150        #Multiply pulse duration by 17150 to get distance
        distance_l = round(distance_l, 2)
        print("distance_l=",distance_l)#Round to two decimal points    
         
        
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
   
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     os.system('ULTRA.py')
    color_mask = cv2.inRange(hsv, lower_color, upper_color)
 
    ultra_r()
   
    countours, hierarchy = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     os.system('python3 ULTRA.py')
    object_area = 0
    object_x = 0
    object_y = 0
#     os.system('python3 right.py')
    ultra_l()
    pk=image
    for contour in countours:
        x, y, width, height = cv2.boundingRect(contour)
        found_area = width * height
     
        if found_area>1000 :
           
            object_area = found_area
            center_x = x + (width / 2)
            center_y = y + (height / 2)
            object_x = center_x
            object_y = center_y
           
#             print("found_area",found_area)
            pk=cv2.rectangle(image, (x, y),(x+width,y+height),(255,0,0), 2)
    if object_area > 0:
        ball_location = [object_area, object_x, object_y]
       
    else:
        ball_location = None
    if  distance_l > 20 and distance_r > 20 :            
        if ball_location:
            if (ball_location[0] > minimum_area) and (ball_location[0] < maximum_area):
                print('.............')
#                 print('ball_location',ball_location[1])
#                 print('x_location_right',center_image_x + (image_width/5))
#                 print('x_location_left',center_image_x - (image_width/5))
                print('.............')
                if ball_location[1] > (center_image_x + (image_width/5)):
          #      robot.right(turn_speed)    
                    right_turn()
                    print(" Target move RIGHT")                        
                elif ball_location[1] < (center_image_x - (image_width/5)):
         #       robot.left(turn_speed)
                    left_turn()
                    print(" Target move  LEFT")        
                else:
                    print(" TRACGET is coming ")
                    forward()
                #time.sleep(2)
     
            elif (ball_location[0] < minimum_area):
               
                 
                stop()
                print("Target isn't large enough, searching")
     
            else:
        #    robot.stop()
              print("  Target large enough, stopping")
              stop()    
        else:
       # robot.left(turn_speed)
            print("Target not found, searching")
            stop()
    else:
        print("Hurdle Detected")
        print("Trolley stop")
        stop()
    cv2.imshow("masking",pk)
    cv2.waitKey(1)
    rawCapture.truncate(0)
