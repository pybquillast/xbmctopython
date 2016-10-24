# pilFilters.py
'''Este modulo muestra los diferentes efectos que tiene los filtros implementados en Pillow
   muestra la imagen comleta y sus bandas RGBA. (solo probadozs en archivo .png) y utilizado
   para ver que efectos aplicar a las textures a ser desplegadas en la implementación del xbmcgui'''

import os
import Tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import tkFileDialog

class pilFilters:

    filters = ['DETAIL', 'SHARPEN', 'BLUR', 'CONTOUR', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE',
               'EMBOSS', 'FIND_EDGES', 'SMOOTH', 'SMOOTH_MORE']
    clases = ['GaussianBlur', 'UnsharpMask', 'MedianFilter', 'MinFilter',
              'MaxFilter', 'ModeFilter']

    def __init__(self, parent):
        self.nim = len(self.filters + self.clases) + 1
        self.offset = 200
        self.imArray = None
        self.iniDir = r'C:\testFiles\Confluence'
        self.parent = parent
        self.setGUI()

    def setGUI(self):
        root = self.parent
        vbar = tk.Scrollbar(root)
        hbar = tk.Scrollbar(root, orient='horizontal')
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas = canvas = tk.Canvas(root, bg='black')
        canvas.pack(fill=tk.BOTH, expand=tk.YES)
        vbar.config(command=canvas.yview)
        hbar.config(command=canvas.xview)
        canvas.config(xscrollcommand=hbar.set)
        canvas.config(yscrollcommand=vbar.set)

        self.textureName = textureName = tk.StringVar()
        textureName.trace('w', self.popCanvas)

        frame = tk.Frame(canvas, width=400, height=200)
        edit = tk.Entry(frame, width=40, textvariable=textureName)
        edit.pack(side=tk.LEFT, padx=5)
        boton = tk.Button(frame, text='boton', command=self.getFilename)
        boton.pack(side=tk.RIGHT)
        canvas.create_window(20, 20, window=frame, anchor=tk.NW)


    def getFilename(self):
        iniDir = self.iniDir
        filename = tkFileDialog.askopenfilename(defaultextension='.png', initialdir=iniDir,
                                                title='Choose a texture file to draw',
                                                filetypes=[('image files', '.png'), ('all files', '.*')])
        iniDir, filename = os.path.split(filename)
        self.textureName.set(filename)

    def popCanvas(self, *args):
        textureName = self.textureName
        offset, nim = self.offset, self.nim
        canvas, clases, filters = self.canvas, self.clases, self.filters
        filename = r'C:\testFiles\Confluence\%s' % textureName.get()
        im = Image.open(filename)
        iw, ih = im.size
        cellW = max(200, (20 + iw))
        cellH = max( 50, (20 + ih))
        canvas.delete('txtimg')
        canvas.config(scrollregion=(0, 0, offset + 6*cellW, offset + nim*cellH))

        self.imArray = imArray = [im]
        for filter in filters:
            fltr = getattr(ImageFilter, filter)
            imArray.append(im.filter(fltr))

        for clase in clases:
            clsfltr = getattr(ImageFilter, clase)()
            try:
                imArray.append(im.filter(clsfltr))
            except:
                imArray.append(None)

        for k, imgLabel in enumerate(['Original Image'] + filters + clases):
            yPos = offset + k*cellH
            canvas.create_text(20, yPos, text=imgLabel, fill='white', anchor=tk.NW, tags='txtimg')
            if imArray[k]:
                img = imArray[k]
                bands = img.split()
                out = [ImageTk.PhotoImage(img)]
                for band in bands:
                    out.append(ImageTk.PhotoImage(band))
                imArray[k] = out
                for m in range(len(out)):
                    canvas.create_image(20 + (m + 1)*cellW, yPos, image=imArray[k][m], anchor=tk.NW, tags='txtimg')

if __name__ == '__main__':
    root = tk.Tk()
    pilFilters(root)
    root.mainloop()