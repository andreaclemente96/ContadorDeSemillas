# ContadorDeSemillas
El ContadorDeSemillas es una herramienta interactiva en Python diseñada para detectar y contar semillas en imágenes mediante procesamiento digital. Combina interfaz gráfica (Tkinter) con visión por computadora (OpenCV), permitiendo al usuario cargar una imagen, recortar la región de interés y ajustar parámetros de segmentación en tiempo real.

El programa inicia mostrando un título y unas instrucciones, luego solicita al usuario seleccionar una imagen. Esta se adapta a la pantalla, se recorta mediante una selección manual y se prepara para análisis. A través de barras deslizantes (trackbars), el usuario ajusta rangos de color (Hue, Saturación, Valor), límites de área, y operaciones morfológicas (dilatación, erosión) para aislar las semillas. También incluye un control de circularidad para filtrar objetos que no correspondan a la forma esperada.

El procesamiento convierte la imagen a espacio HSV, aplica un enmascarado y operaciones morfológicas, encuentra contornos y filtra por área y circularidad. Cada semilla detectada se marca con un rectángulo verde, y el número total se muestra en una ventana dedicada. La interfaz permite visualizar la imagen segmentada junto a la máscara generada, facilitando ajustes iterativos hasta lograr una detección precisa.

Este script es útil para aplicaciones en agronomía, control de calidad o investigación, ya que proporciona una forma visual e intuitiva de contar semillas sin requerir conocimientos avanzados en procesamiento de imágenes. Su arquitectura modular permite adaptarlo a otros objetos o criterios de conteo.

The ContadorDeSemillas is an interactive Python tool designed to detect and count seeds in images using digital image processing. It combines a graphical interface (Tkinter) with computer vision (OpenCV), allowing users to load an image, crop the region of interest, and adjust segmentation parameters in real time.

The program starts by displaying a title and instructions, then prompts the user to select an image. The image is resized to fit the screen, cropped manually, and prepared for analysis. Through adjustable trackbars, users can fine-tune color ranges (Hue, Saturation, Value), area limits, and morphological operations (dilation, erosion) to isolate seeds. It also includes a circularity control to filter out objects that do not match the expected shape.

Processing converts the image to the HSV color space, applies masking and morphological operations, detects contours, and filters them based on area and circularity. Each detected seed is highlighted with a green rectangle, and the total count is displayed in a dedicated window. The interface shows both the segmented image and the generated mask, allowing iterative adjustments until precise detection is achieved.

This script is useful for agronomy, quality control, or research, as it provides a visual and intuitive way to count seeds without requiring advanced knowledge of image processing. Its modular design also makes it adaptable for counting other objects or applying different detection criteria.
