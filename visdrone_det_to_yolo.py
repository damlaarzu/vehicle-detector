# visdrone_det_to_yolo.py
import os
from PIL import Image
from tqdm import tqdm

def ensure_dir(p): 
    if not os.path.exists(p): os.makedirs(p)

def clamp01(x):
    return max(0.0, min(1.0, x))

def convert_single_ann_file(ann_file_path, img_w, img_h, classes_map=None, min_area=1):
    """ann_file_path: bir resme ait visdrone .txt (her satır: left,top,w,h,score,cat,trunc,occ)"""
    yolo_lines = []
    with open(ann_file_path, 'r') as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(',') if p.strip()!='']
            if len(parts) < 6:
                continue
            left = float(parts[0]); top = float(parts[1])
            box_w = float(parts[2]); box_h = float(parts[3])
            score = float(parts[4])
            cat = int(float(parts[5]))  # visdrone category
            # ignore score==0 (marked to ignore) and ignore cat==0 (ignored-region) and cat==11 (others)
            if score == 0: 
                continue
            if cat == 0 or cat == 11:
                continue
            # map category -> class_id (YOLO expects 0..)
            # default mapping: class_id = cat - 1  (1->0, 10->9)
            class_id = (cat - 1) if classes_map is None else classes_map.get(cat, None)
            if class_id is None:
                continue
            # compute center coords and normalize
            cx = (left + box_w / 2.0) / img_w
            cy = (top + box_h / 2.0) / img_h
            nw = box_w / img_w
            nh = box_h / img_h
            # small box filter
            if box_w * box_h < min_area:
                continue
            cx = clamp01(cx); cy = clamp01(cy); nw = clamp01(nw); nh = clamp01(nh)
            yolo_lines.append(f"{int(class_id)} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}")
    return yolo_lines

def main(images_dir, ann_dir, out_labels_dir, classes_map=None):
    ensure_dir(out_labels_dir)
    images = [p for p in os.listdir(images_dir) if p.lower().endswith(('.jpg','.png','.jpeg'))]
    for imname in tqdm(sorted(images)):
        stem = os.path.splitext(imname)[0]
        img_path = os.path.join(images_dir, imname)
        ann_path = os.path.join(ann_dir, f"{stem}.txt")  # VISDRONE usually stores per-image .txt with same stem
        if not os.path.exists(ann_path):
            # no annotation file for this image — skip or create empty label
            open(os.path.join(out_labels_dir, stem + '.txt'), 'w').close()
            continue
        # read image size
        with Image.open(img_path) as im:
            w,h = im.size
        yolo_lines = convert_single_ann_file(ann_path, w, h, classes_map=classes_map)
        out_label_path = os.path.join(out_labels_dir, stem + '.txt')
        with open(out_label_path, 'w') as outf:
            outf.write("\n".join(yolo_lines))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--images_dir", required=True, help="VisDrone images folder")
    parser.add_argument("--ann_dir", required=True, help="VisDrone per-image annotations folder (txt files named like 000001.txt)")
    parser.add_argument("--out_labels_dir", required=True, help="Where to put YOLO .txt labels")
    args = parser.parse_args()
    # optional: classes_map None uses default cat-1 mapping
    main(args.images_dir, args.ann_dir, args.out_labels_dir, classes_map=None)
