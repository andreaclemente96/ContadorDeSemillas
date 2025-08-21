import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import time

def mostrar_titulo():
    root = tk.Tk()
    root.overrideredirect(True)
    root.configure(bg='black')
    ancho = 400
    alto = 100
    x = (root.winfo_screenwidth() // 2) - (ancho // 2)
    y = (root.winfo_screenheight() // 2) - (alto // 2)
    root.geometry(f"{ancho}x{alto}+{x}+{y}")

    frame = tk.Frame(root, bg='white', bd=4)
    frame.pack(expand=True, fill='both', padx=4, pady=4)

    label = tk.Label(frame, text="Contador de semillas", font=("Helvetica", 24, "bold"), fg="white", bg="black", pady=20)
    label.pack(expand=True)

    root.after(2000, root.destroy)
    root.mainloop()

def mostrar_instrucciones():
    instrucciones = """
PASOS A SEGUIR:

1. Selecciona una imagen con semillas.
2. Recorta el área de interés y presiona ENTER.
3. Ajusta los deslizadores (sliders) según necesites:

- H min/max: Rango de tonalidad (Hue).
- S min/max: Saturación mínima y máxima.
- V min/max: Brillo mínimo y máximo.
- Área min/max: Tamaño de objetos a detectar.
- Dilatar: Engrosar las áreas detectadas.
- Erosionar: Reducir el ruido pequeño.
- Circularidad: Qué tan "circular" debe ser una semilla.
- Al terminar, presiona ESC para cerrar la ventana.

Presiona ENTER para continuar.
"""
    root = tk.Tk()
    root.title("Instrucciones")
    text = tk.Text(root, wrap="word", font=("Helvetica", 12), padx=10, pady=10)
    text.insert("1.0", instrucciones)
    text.config(state="disabled", height=25, width=60)
    text.pack()

    def continuar(event=None):
        root.destroy()

    root.bind("<Return>", continuar)
    root.mainloop()
mostrar_titulo()
mostrar_instrucciones()


def seleccionar_imagen():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.bmp")])
    root.destroy()
    return archivo

def redimensionar_con_padding(img, tamaño_objetivo):
    alto_obj, ancho_obj = tamaño_objetivo
    alto_img, ancho_img = img.shape[:2]
    escala = min(ancho_obj / ancho_img, alto_obj / alto_img)
    nuevo_ancho = int(ancho_img * escala)
    nuevo_alto = int(alto_img * escala)
    img_redim = cv2.resize(img, (nuevo_ancho, nuevo_alto))

    canvas = np.ones((alto_obj, ancho_obj, 3), dtype=np.uint8) * 255
    y_offset = (alto_obj - nuevo_alto) // 2
    x_offset = (ancho_obj - nuevo_ancho) // 2
    canvas[y_offset:y_offset+nuevo_alto, x_offset:x_offset+nuevo_ancho] = img_redim
    return canvas


root = tk.Tk()
pantalla_ancho = root.winfo_screenwidth()
pantalla_alto = root.winfo_screenheight()
root.destroy()


margen_ancho = 100
margen_alto = 150
max_ancho = pantalla_ancho - margen_ancho
max_alto = pantalla_alto - margen_alto

ruta = seleccionar_imagen()
if not ruta:
    print("No se seleccionó imagen.")
    exit()

original = cv2.imread(ruta)
if original is None:
    raise ValueError("No se pudo cargar la imagen.")


alto, ancho = original.shape[:2]
escala = min(max_ancho / ancho, max_alto / alto, 1.0)
if escala < 1.0:
    original = cv2.resize(original, (int(ancho * escala), int(alto * escala)))


alto, ancho = original.shape[:2]


cv2.namedWindow("Recorta la imagen y presiona ENTER", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Recorta la imagen y presiona ENTER", ancho, alto)
pos_x = (pantalla_ancho - ancho) // 2
pos_y = (pantalla_alto - alto) // 2
cv2.moveWindow("Recorta la imagen y presiona ENTER", pos_x, pos_y)

r = cv2.selectROI("Recorta la imagen y presiona ENTER", original, showCrosshair=True)
cv2.destroyWindow("Recorta la imagen y presiona ENTER")
if r == (0, 0, 0, 0):
    print("Recorte cancelado. Cerrando.")
    exit()

x, y, w, h = r
original = original[int(y):int(y+h), int(x):int(x+w)]


cv2.namedWindow("Controles", cv2.WINDOW_NORMAL)
ancho_controles, alto_controles = 700, 400
cv2.resizeWindow("Controles", ancho_controles, alto_controles)


margen_inferior = 200
pos_y_controles = pantalla_alto - alto_controles - margen_inferior
if pos_y_controles < 0:
    pos_y_controles = 0

cv2.moveWindow("Controles", 0, pos_y_controles)


cv2.createTrackbar("H min", "Controles", 0, 179, lambda x: None)
cv2.createTrackbar("H max", "Controles", 24, 179, lambda x: None)
cv2.createTrackbar("S min", "Controles", 60, 255, lambda x: None)
cv2.createTrackbar("S max", "Controles", 255, 255, lambda x: None)
cv2.createTrackbar("V min", "Controles", 30, 255, lambda x: None)
cv2.createTrackbar("V max", "Controles", 255, 255, lambda x: None)
cv2.createTrackbar("Área min", "Controles", 10, 5000, lambda x: None)
cv2.createTrackbar("Área max", "Controles", 1500, 10000, lambda x: None)
cv2.createTrackbar("Dilatar", "Controles", 2, 10, lambda x: None)
cv2.createTrackbar("Erosionar", "Controles", 0, 5, lambda x: None)
cv2.createTrackbar("Circularidad", "Controles", 20, 40, lambda x: None)  


tamaño_img = (500, 1000)   
tamaño_mask = (400, 1000)
tamaño_conteo = (150, 700)

def procesar(hmin, hmax, smin, smax, vmin, vmax, area_min, area_max, dilate_iters, min_circularidad, erosionar_iters):
    hsv = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
    lower = np.array([hmin, smin, vmin])
    upper = np.array([hmax, smax, vmax])
    mask = cv2.inRange(hsv, lower, upper)

    if erosionar_iters > 0:
        mask = cv2.erode(mask, None, iterations=erosionar_iters)
    mask = cv2.dilate(mask, None, iterations=dilate_iters)

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    resultado = original.copy()
    cuenta = 0

    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if area_min < area < area_max:
            perimetro = cv2.arcLength(cnt, True)
            if perimetro == 0:
                continue
            circularidad = 4 * np.pi * area / (perimetro ** 2)
            if circularidad < min_circularidad:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(resultado, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cuenta += 1

    resultado_vis = redimensionar_con_padding(resultado, tamaño_img)
    mask_vis = redimensionar_con_padding(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), tamaño_mask)

    max_width = max(resultado_vis.shape[1], mask_vis.shape[1])
    resultado_vis = redimensionar_con_padding(resultado, (resultado_vis.shape[0], max_width))
    mask_vis = redimensionar_con_padding(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), (mask_vis.shape[0], max_width))

    combined = np.vstack((resultado_vis, mask_vis))

    cv2.imshow("Segmentación", combined)
    cv2.moveWindow("Segmentación", pantalla_ancho - max_width, 0)

    conteo = np.ones((tamaño_conteo[0], tamaño_conteo[1], 3), dtype=np.uint8) * 255
    texto = f"Semillas: {cuenta}"
    cv2.putText(conteo, texto, (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 5)
    cv2.imshow("Conteo", conteo)
    cv2.moveWindow("Conteo", 0, 0)

while True:
    hmin = cv2.getTrackbarPos("H min", "Controles")
    hmax = cv2.getTrackbarPos("H max", "Controles")
    smin = cv2.getTrackbarPos("S min", "Controles")
    smax = cv2.getTrackbarPos("S max", "Controles")
    vmin = cv2.getTrackbarPos("V min", "Controles")
    vmax = cv2.getTrackbarPos("V max", "Controles")
    area_min = cv2.getTrackbarPos("Área min", "Controles")
    area_max = cv2.getTrackbarPos("Área max", "Controles")
    dilate_iters = cv2.getTrackbarPos("Dilatar", "Controles")
    erosionar_iters = cv2.getTrackbarPos("Erosionar", "Controles")
    circularidad_val = cv2.getTrackbarPos("Circularidad", "Controles") / 100.0

    if area_max <= area_min:
        area_max = area_min + 1

    procesar(hmin, hmax, smin, smax, vmin, vmax, area_min, area_max, dilate_iters, circularidad_val, erosionar_iters)

    if cv2.waitKey(100) & 0xFF == 27:
        break

cv2.destroyAllWindows()
