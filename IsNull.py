import os

lbl_dir = "datasets/visdrone/labels/train"

empty_files = []
total_files = 0

for fname in os.listdir(lbl_dir):
    if not fname.endswith(".txt"):
        continue
    total_files += 1
    path = os.path.join(lbl_dir, fname)
    if os.path.getsize(path) == 0:
        empty_files.append(fname)

print(f"Toplam etiket dosyası: {total_files}")
print(f"Boş etiket dosyası sayısı: {len(empty_files)}")
print("Boş dosya örnekleri (en fazla 10):")
print(empty_files[:10])
