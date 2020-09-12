import tkinter as tk
from tkinter import filedialog
import numpy as np
import plotly.graph_objects as go
import struct

class Vector:
    X :any
    Y :any
    
    def __init__(self, x, y):
        self.X = x
        self.Y = y

class Data:
    Len : Vector
    Step : Vector
    Start : Vector
    Last : Vector
    Size : Vector
    Level : float
    
    def __init__(self, args:[]):
        self.Len = Vector(int(args[0]), int(args[1]))
        self.Step = Vector(float(args[2].replace(',', '.')), float(args[3].replace(',', '.')))
        self.Start = Vector(int(args[4]), int(args[5]))
        self.Last = Vector(int(args[6]), int(args[7]))
        self.Size = Vector(int(args[8]), int(args[9]))
        self.Level = float(args[10].replace(',', '.'))

floats = []
root = tk.Tk()
root.withdraw()

filePath = filedialog.askopenfilename()

with open(filePath, 'r') as file:
        data = Data(file.readline().split('|'))    
        skiped = int(file.readline())  

with open(filePath, 'rb') as file:
    file.read(skiped)
    while True:
        bytess = file.read(4)
        if not bytess:
            break              
        floats.append(struct.unpack('<f', bytearray(bytess)))
        
matrixZ = np.zeros((data.Len.Y, data.Len.X), 'float32')
index = 0
for y in range(data.Len.Y):
    for x in range(data.Len.X):
        matrixZ[y][x] = data.Level + floats[index][0]
        index += 1

go.Figure(go.Surface(contours = {
    "x": { "show": True, "start": data.Start.X, "end": data.Last.X, "size": data.Step.X, "color":"white" },
    "z": { "show": True, "start": data.Start.Y, "end": data.Last.Y, "size": data.Step.Y }
},
x = np.arange(data.Len.X),
y = np.arange(data.Len.Y),
z = matrixZ)).show()