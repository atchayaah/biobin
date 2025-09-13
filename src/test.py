import RPi.GPIO as GPIO
import time
import serial
import cv2
from ultralytics import YOLO

# Serial setup
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Set up GPIO pins
TRIG1 = 25
ECHO1 = 8
TRIG2 = 10
ECHO2 = 9
TRIG3 = 19
ECHO3 = 26

# Motor control pins
MOTOR_LEFT_FORWARD = 27
MOTOR_LEFT_BACKWARD = 18
MOTOR_RIGHT_FORWARD = 20
MOTOR_RIGHT_BACKWARD = 16

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)

GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)

# Load YOLO model
model = YOLO('best.pt')  # Replace with your YOLOv8 model path

last_u_turn_right = True  # Start with a right U-turn
object_detected = False  # Flag to track object detection

def measure_distance(TRIG, ECHO):
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.000005)
    GPIO.output(TRIG, GPIO.LOW)

    signaloff, signalon = time.time(), time.time()

    start_time = time.time()  # Start timeout counter
    while GPIO.input(ECHO) == 0 and time.time() - start_time < 0.04:  # 40ms timeout
        signaloff = time.time()

    start_time = time.time()  # Reset timeout counter for echo
    while GPIO.input(ECHO) == 1 and time.time() - start_time < 0.04:
        signalon = time.time()

    timepassed = signalon - signaloff
    distance = (timepassed * 34300) / 2
    return round(distance, 2)


def drive_forward():
    GPIO.output(MOTOR_LEFT_FORWARD, True)
    GPIO.output(MOTOR_RIGHT_FORWARD, True)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

def stop():
    GPIO.output(MOTOR_LEFT_FORWARD, True)
    GPIO.output(MOTOR_RIGHT_FORWARD, True)
    GPIO.output(MOTOR_LEFT_BACKWARD, True)
    GPIO.output(MOTOR_RIGHT_BACKWARD, True)

def turn_right():
    GPIO.output(MOTOR_LEFT_FORWARD, True)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, True)


def turn_left():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, True)
    GPIO.output(MOTOR_LEFT_BACKWARD, True)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)


def detect_objects():
    global object_detected
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to match model input size
        frame_resized = cv2.resize(frame, (640, 640))  # Resize to 640x640

        # Perform inference on the resized frame
        results = model(frame_resized, conf=0.7)  # Adjust confidence threshold if necessary
        if results[0].boxes:
            for box in results[0].boxes:
                class_name = model.names[int(box.cls)]
                if class_name == 'Syringe':
                    print("Syringe detected, sending 'L'")
                    ser.write(b'P')
                    time.sleep(20)
                    ser.write(b'L')  # Send 'L' for syringe
                    time.sleep(20)
                    ser.write(b'Z')
                   
                    object_detected = True
                elif class_name == 'cotton':
                    print("Cotton detected, sending 'R'")
                    ser.write(b'P')
                    time.sleep(20)
                    ser.write(b'R')  # Send 'L' for cotton
                    time.sleep(20)
                    ser.write(b'Z')
                   
                    object_detected = True

                if object_detected:
                    break

        # Correctly indented
        cv2.imshow('Detections', results[0].plot())
        
        if object_detected:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

try:
    while True:
        distance_front = measure_distance(TRIG1, ECHO1)
        distance_left = measure_distance(TRIG2, ECHO2)
        distance_right = measure_distance(TRIG3, ECHO3)
        
        


        print(f"Left: {distance_left} cm, Front: {distance_front} cm, Right: {distance_right} cm")

        if distance_front < 20:
            stop()
            object_detected=False
            print("Stopping due to obstacle in front!")
            if not object_detected:
                detect_objects()  # Start object detection
            continue

        elif distance_left < 25 and distance_right < 25:
            stop()
            if last_u_turn_right:
                print("Making a right U-turn")
                turn_right()  # Make a right U-turn
                time.sleep(2)
                drive_forward()
                time.sleep(1)  # Brief pause before continuing
                turn_right()
                time.sleep(2)
                last_u_turn_right = False  # Next turn will be left
            else:
                print("Making a left U-turn")
                turn_left()  # Make a left U-turn
                time.sleep(2)    
                drive_forward()
                time.sleep(0.5)  # Brief pause before continuing            
                turn_left()
                time.sleep(2)
                last_u_turn_right = True  # Next turn will be right

        else:
            drive_forward()

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopping the robot...")

finally:
    stop()
    GPIO.cleanup()
