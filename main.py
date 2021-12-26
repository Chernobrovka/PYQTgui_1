from PyQt5 import QtWidgets,  uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice


app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("SerialGUI")

serial = QSerialPort()
serial.setBaudRate(115200)
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.coml.addItems(portList)

def onRead():
    rx = serial.readLine()
    rxs = str(rx, 'uft-8').strip()
    data = rxs.split(',')

def onOpen():
    serial.setPortName(ui.coml.currentText())
    serial.open(QIODevice.ReadWrite)

def onClose():
    serial.close()

def ledcontrol(val):
    if val == 2 : val = 1;
    serialSend([0, val])

def fancontrol(val):
    if val == 2: val = 1;
    serialSend([3, val])

def bulbcontrol(val):
    if val == 2: val = 1;
    serialSend([4, val])

def serialSend(data):
    txs = ""
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    serial.write(txs.encode())


def RGBcontrol():
    serialSend([1, ui.RS.value(), ui.GS.value(), ui.BS.value()])

def sendText():
    txs = "5,"
    txs += ui.textF.displayText()
    txs = ';'
    serial.write(txs.encode())


serial.readyRead.connect(onRead)
ui.button_open.clicked.connect(onOpen)
ui.button_close.clicked.connect(onClose)

ui.check_LED.stateChanged.connect(ledcontrol)
ui.check_FAN.stateChanged.connect(fancontrol)
ui.check_BULB.stateChanged.connect(bulbcontrol)
ui.RS.valueChanged.connect(RGBcontrol)
ui.GS.valueChanged.connect(RGBcontrol)
ui.BS.valueChanged.connect(RGBcontrol)
ui.sendB.clicked.connect(sendText)



ui.show()
app.exec()
