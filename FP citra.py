from tkinter import *
from tkinter import filedialog
import tkinter as tk 
from scipy import ndimage
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import sobel
from math import log10, sqrt
from sklearn.metrics import mean_squared_error

class window(Frame):
    def __init__(self, parent, title):
        self.parent = parent
        self.aturWindow(title)

    def aturWindow(self, title):
        self.parent.geometry("300x300+300+300")
        self.parent.title(title)
        self.frame = tk.Frame(root, bg="orange")
        self.frame.pack(fill=BOTH, expand=1)
        button_open = tk.Button(self.frame, text="Choose picture", command=self.UploadAct)
        button_open.pack(side=LEFT)
        button_proses = tk.Button(self.frame, text="Proses citra", fg="green", command=self.citra)
        button_proses.pack(side=LEFT)
        button_evalError = tk.Button(self.frame, text="Proses eval error", fg="blue", command=self.evalError)
        button_evalError.pack(side=LEFT)
        button_out = tk.Button(self.frame, text="Keluar", fg="red", command=quit)
        button_out.pack(side=LEFT)

    def UploadAct(self):
        filename = filedialog.askopenfilename()
        self.filename = filename

    def citra(self):
        foto = cv2.imread(str(self.filename)) #output masih int
        gray = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY) # convert to gray
        self.gray = gray


        #sobel
        sobx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        soby = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
        sobelx = cv2.filter2D(gray, -1, sobx)
        sobely = cv2.filter2D(gray, -1, soby)
        sobel = sobelx + sobely

        self.sobel = sobel

        #canny

        canny = cv2.Canny(gray, 100, 200)
        self.canny = canny

        plt.subplot(3,3,1), plt.imshow(foto,cmap = 'gray')
        plt.title('Original'), plt.xticks([]), plt.yticks([])
        
        plt.subplot(3,3,2), plt.imshow(sobel,cmap = 'gray')
        plt.title('Sobel'), plt.xticks([]), plt.yticks([])

        plt.subplot(3,3,3), plt.imshow(sobelx,cmap = 'gray')
        plt.title('Sobelx'), plt.xticks([])
        
        plt.subplot(3,3,4), plt.imshow(sobely,cmap = 'gray')
        plt.title('Sobely'), plt.xticks([])
        
        plt.subplot(3,3,5), plt.imshow(canny,cmap = 'gray')
        plt.title('Canny'), plt.xticks([]), plt.yticks([])

        plt.show()

    def evalError(self):
        gray = self.gray
        canny = self.canny
        sobel = self.sobel
        mseCanny = mean_squared_error(gray, canny)
        
        
        max_pixel = 255
        psnrCanny = 20 * log10(max_pixel / sqrt(mseCanny))
        
        mseSobel = np.sum((gray.astype("float") - sobel.astype("float")) ** 2)
        mseSobel /= float(gray.shape[0] * gray.shape[1])
        
    
        psnrSobel = 20 * log10(max_pixel / sqrt(mseSobel))

        # Create text widget and specify size.
        T = Text(root, height = 5, width = 52)
        l = Label(root, text = "Evauation error")
        l.config(font =("Courier", 14))

        Mse1 = "mse canny :"  + str(mseCanny) + "\n" + "mse sobel : " + str(mseSobel) + "\n" + "psnr canny :"  + str(psnrCanny) + "\n" + "psnr sobel : " + str(psnrSobel)

        l.pack()
        T.pack()
        T.insert(tk.END, Mse1)
   
    
        # print("mseCanny : ")
        # print(psnrCanny)
        # print("psnrCanny : ")
        # print(psnrCanny)
        
        # print("mseSobel : ")
        # print(mseSobel)
        # print("psnrSobel : ")
        # print(psnrSobel)

root = tk.Tk()
app = window(root,"Edge Detection sobel, prewitt, laplacian")
root.mainloop()