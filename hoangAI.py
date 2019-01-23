from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import random


def start():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--prototxt", required=True,
                    help="pridej k argumentu -p path k prototxt souboru")
    ap.add_argument("-m", "--model", required=True,
                    help="pridej path k trenovacimu modelu")
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
                    help="minimalni sance (na odstraneni tzv slabych detekci")
    args = vars(ap.parse_args())
    # "nacteni" hoangAI :D
    print("Loading hoangAI(TM) V.1.0.0")
    time.sleep(2.0)
    # nacteme si list stitku veci, ktere byly pouzity pri detekcnim treningu hoangAI, a pak nahodne vybereme barvu pro objektove ramecky
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    CLASSES_RANDOM = CLASSES[random.randint(0, len(CLASSES) - 1)]
    print("vygoogli si " + CLASSES_RANDOM)
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # nacteme si serializovany model caffe
    print("[INFO] nacitani modelu...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    # zacatek video snimani
    # a take zacneme pocitat fps
    print("[INFO] video snimani zacina...TED")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()

    # cyklus/smycka pres ramecek vystupu videa

    while True:
        # vezmeme ramecek z threadovaneho video vystupu a omezime sirku ramecku na 400 pixelu(aby to nebylo moc narocne na vykon)
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # vezmem rozmery ramecku a prevedeme do blobu(objektu)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)

        # objekt(blob) projde siti aby ziskal detekce a predpovedi
        net.setInput(blob)
        detections = net.forward()

        # cyklus/smycka pres detekce
        detected_class = (0, 0)
        for i in np.arange(0, detections.shape[2]):
            # vytahnout confidence (tedy jak si je svym uhodnutim pocitac jisty) spojeny s predpovedi
            confidence = detections[0, 0, i, 2]

            # odstranime "slabe" detekce s tim ze `confidence` (tedy jak si je svym uhodnutim pocitac jisty) je vetsi nez minimalni confidence uvedeny v argumentaci pri spusteni
            if confidence > args["confidence"]:
                # vytahneme index ze stitku tridy
                # `detections`, a pak vypocitame souradnice (x, y)
                # pro ohranicujici ramecek objektu
                idx = int(detections[0, 0, i, 1])

                # zkontrolujeme pokud nova trida ma nejvetsi pravdepodobnost
                if confidence > detected_class[0]:
                    detected_class = (confidence, CLASSES[idx])

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # vykresleni "uhodnuti" pocitace
                label = "{}: {:.2f}%".format(CLASSES[idx],
                                             confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        if detected_class[1] == CLASSES_RANDOM:
            # ukonceni pocitani fps a ukonceni casovace (pouze pro test jestli to funguje)
            fps.stop()
            cv2.destroyAllWindows()
            return True

        # vystup z kamery a z detekcniho programu
        cv2.imshow("detekce veci :DDDDDDDDDDDDDDD", frame)
        key = cv2.waitKey(1) & 0xFF

        # funkce ktera aktualizuje fps
        fps.update()
