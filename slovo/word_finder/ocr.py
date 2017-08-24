from PIL import Image
import numpy as np
import time
import re
from subprocess import Popen, PIPE


def extract_gs_letters(image_data):
    image_mod = np.zeros(shape=image_data.shape)
    for i in range(image_data.shape[0]):
        for j in range(image_data.shape[1]):
            if image_data[i][j][0] < 150 and image_data[i][j][1] < 150 and image_data[i][j][2] < 150:
                image_mod[i][j] = image_data[i][j]
            else:
                image_mod[i][j] = (255, 255, 255, 255)
    return image_mod


def run_shell(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    p.communicate()
    if p.returncode != 0:
        return False
    return True

def run_tesseract(image_name):
    cmd = "tesseract " + image_name + " res" + " -l" + " rus"
    run_shell(cmd)


def detect_letters(image_name):
    start = time.time()
    image = Image.open(image_name)
    print("ocr", type(image))
    image_data = np.asarray(image)
    image_mod = extract_gs_letters(image_data)
    image_letters = Image.fromarray(np.uint8(image_mod))
    image_letters.save("image_letters.png")
    run_tesseract("image_letters.png")
    with open('res.txt') as f:
        text = f.read()
    text = re.sub(r"(\n)", "", text.lower())
    print(text)
    print("Detected in %f seconds" %(time.time() - start))
    return text


#detect_letters('s1.png')