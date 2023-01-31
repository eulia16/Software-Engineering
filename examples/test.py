from flask import Flask
import easygopigo3
from time import sleep

app = Flask(__name__)
gpg3 = EasyGoPiGo3()


@app.route('/')
def index():
    return 'It worked'


@app.route('/forward')
def forward():
    print("Forward")
    gpg3.forward()
    #gpg3.drive_cm(50, True)
    sleep(1)
    return 'forward'


@app.route('/backward')
def backward():
    print("Backward")
    gpg3.backward()
    sleep(2)
    return 'backward'


@pp.route('/left')
def left():
    print("Left")
    gpg3.left()
    sleep(0.5)
    return 'left'


@app.route('/right')
def right():
    print("Right")
    gpg3.right()
    sleep(0.5)
    return 'right'


@app.route('/stop')
def index():
    print("Stop")
    gpg3.stop()
    return 'stop'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', Port=5000)
