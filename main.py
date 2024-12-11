import tkinter as tk
from tkinter import filedialog
from colorization import colorize_image
import cv2

# Tkinter arayüzü
def select_and_colorize():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        return

    try:
        bw_image, colorized_image = colorize_image(file_path)

        # Sonuçları göster
        cv2.imshow("BW Image", bw_image)
        cv2.imshow("Colorized Image", colorized_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Tkinter ana penceresi
root = tk.Tk()
root.title("Fotoğraf Renklendirme Uygulaması")

button = tk.Button(root, text="Fotoğraf Seç ve Renklendir", command=select_and_colorize)
button.pack(pady=20)

root.mainloop()
