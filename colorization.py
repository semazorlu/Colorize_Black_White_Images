import numpy as np
import cv2

# Model ve kernel dosyalarının yollarını belirtiyoruz
PROTOTXT_PATH = 'models/colorization_deploy_v2.prototxt'
MODEL_PATH = 'models/colorization_release_v2.caffemodel'
KERNEL_PATH = 'models/pts_in_hull.npy'

# Modeli ve kernel dosyasını yükleyen ve renklendirme işlemini yapan işlev
def colorize_image(image_path):
    # Modeli yükle
    net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)
    points = np.load(KERNEL_PATH)
    points = points.transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype(np.float32)]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    # Görüntüyü işleme
    bw_image = cv2.imread(image_path)
    normalized = bw_image.astype("float32") / 255.0
    lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Model ile tahmin
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (bw_image.shape[1], bw_image.shape[0]))
    L = cv2.split(lab)[0]

    # Renklendirme
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = (255.0 * colorized).astype("uint8")

    return bw_image, colorized
