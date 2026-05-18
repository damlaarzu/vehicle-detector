import random
import os
import cv2

# Görüntü ve etiket klasörlerinin yolu
img_dir = "datasets/visdrone/images/train"
lbl_dir = "datasets/visdrone/labels/train"

# 5 rastgele görüntü seçip etiketleri üzerinde göster
for i in range(5):
    fname = random.choice(os.listdir(img_dir))  # rastgele bir resim seç
    img_path = os.path.join(img_dir, fname)
    img = cv2.imread(img_path)
    if img is None:
        print(f"{fname} dosyası okunamadı, atlanıyor.")
        continue
    h, w = img.shape[:2]

    # Aynı isimli .txt dosyasını bul
    label_path = os.path.join(lbl_dir, os.path.splitext(fname)[0] + ".txt")

    if os.path.exists(label_path):
        with open(label_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                class_id, cx, cy, nw, nh = parts
                cx, cy, nw, nh = float(cx), float(cy), float(nw), float(nh)
                # YOLO formatı (normalized center x, center y, width, height)
                x1 = int((cx - nw / 2) * w)
                y1 = int((cy - nh / 2) * h)
                x2 = int((cx + nw / 2) * w)
                y2 = int((cy + nh / 2) * h)

                # Kutu çizimi (yeşil)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Sınıf id'si kutu üzerinde yazı olarak
                cv2.putText(img, class_id, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    else:
        print(f"{fname} için etiket dosyası bulunamadı.")

    # İşlenmiş resmi dosyaya kaydet
    out_path = f"debug_{i}_{fname}"
    cv2.imwrite(out_path, img)
    print(f"{out_path} kaydedildi.")
