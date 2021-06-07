#!/usr/bin/env python
# coding: utf-8

# In[16]:


import tkinter as tk
from tkinter import *
from tkinter import messagebox


# In[117]:
# Cửa sổ chương trình
window=tk.Tk()
window.title("Project") 
window.resizable(0,0)
window.geometry("300x450+500+100")
# ô viết số
canvas1  = Canvas(window, width=200, height=200, bg='black') 
canvas1.place(x=50, y=100)
# Tên chương trình
l1=tk.Label(window,text="Nhận diện chữ số",font=('Helvetica',16,'bold'))
l1.place(x=55,y=40)

def activate_paint(e):
    global lastx, lasty
    canvas1.bind('<B1-Motion>', paint)
    lastx, lasty = e.x, e.y
    
def paint(e):
    global lastx, lasty
    x,y = e.x, e.y
    canvas1.create_line((lastx,lasty,x,y), width=11, fill="white")
    lastx, lasty = x,y

canvas1.bind('<1>', activate_paint)    
   
def clear():
    canvas1.delete("all")
#nút xóa
btn = tk.Button(window, text="Clear", fg="white", bg="green", command=clear)
btn.place(x=200,y=320)

# ---------
def prediction():
    import cv2
    import numpy as np
    from PIL import ImageGrab
# chụp lại hình ảnh màn hình vị trí ô viết chữ kích thước 200*200  
    img=ImageGrab.grab(bbox=(560,230,760,430))
# set kích thước ảnh test từ 200*200 xuống còn 20*20 giống kí tự mẫu
    img = img.resize((20,20))
    img.save("paint.png")
# đọc dữ liệu train, chia ảnh lớn thành 50 hàng và 50 cột
# chuyển ảnh từ 2 chiều về 1 chiều và chuyển kiểu dữ liệu
    digits = cv2.imread("digits.png", cv2.IMREAD_GRAYSCALE)
    rows = np.vsplit(digits, 50)
    cells = []
    for row in rows:
        row_cells = np.hsplit(row, 50)
        for cell in row_cells:
            cell = cell.flatten()
            cells.append(cell)
    cells = np.array(cells, dtype=np.float32)
# tạo mảng nhãn từ 0 đến 9 cho 2500 mẫu
    k = np.arange(10)
    cells_labels = np.repeat(k, 250)
# đọc và xử lí dữ liệu test tương tự như dữ liệu train
    test_digit = cv2.imread("paint.png",cv2.IMREAD_GRAYSCALE)
    test_digit = test_digit.flatten()
    test_cells = []
    test_cells.append(test_digit)
    test_cells = np.array(test_cells, dtype=np.float32)
# cdùng knn train dữ liệu và tìm nhãn cho dữ liệu test
    knn = cv2.ml.KNearest_create()
    knn.train(cells, cv2.ml.ROW_SAMPLE, cells_labels)
    ret, result, neighbours, dist = knn.findNearest(test_cells, k=7)
    resToShow =str(result[0])

# print result: resToShow có dạng [1.] [2.]...
    res_place = tk.Label(window, text=resToShow[1])
    res_place.place(x=150, y=370)
    
#     ----end find digit
# nút Predict
btn2=tk.Button(window,text="Predict",bg="white",fg="red",command=prediction)
btn2.place(x=50, y=320)

res_place_text = tk.Label(window, text='Kết quả:')
res_place_text.place(x=80, y=370)

window.mainloop()


# In[ ]:





# In[ ]:




