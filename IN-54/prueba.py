from reportlab.pdfgen import canvas
import os

file = canvas.Canvas('IN-54.pdf')
os.startfile("ejemplo.xlsx","print")
