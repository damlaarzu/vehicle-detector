import os
from PIL import Image
from tqdm import tqdm

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def convert_vid_annotations(seq_dir, ann_file, labels_seq_dir):
    ensure_dir(labels_seq_dir)
    with open(ann_file) as f:
        anns = [l.strip().split(',') for l in f if l.strip()]
    frames_dict = {}
    for parts in anns:
        if len(parts) < 8:
            continue
        frame_id = int(parts[0])
        left, top, w, h = map(float, parts[2:6])
        score = float(parts[6])
        cat = int(float(parts[7]))
        if score == 0 or cat in [0, 11]:
            continue
        frames_dict.setdefault(frame_id, []).append((left, top, w, h, cat))
    for frame_id, objs in frames_dict.items():
        img_name = f"{frame_id:07d}.jpg"
        img_path = os.path.join(seq_dir, img_name)
        if not os.path.exists(img_path):
            continue
        with Image.open(img_path) as im:
            iw, ih = im.size
        lines_out = []
        for left, top, w, h, cat in objs:
            class_id = cat - 1
            cx = (left + w/2) / iw
            cy = (top + h/2) / ih
            nw = w / iw
            nh = h / ih
            lines_out.append(f"{class_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}")
        out_file = os.path.join(labels_seq_dir, f"{frame_id:07d}.txt")
        with open(out_file, 'w') as out_f:
            out_f.write("\n".join(lines_out))

if __name__ == "__main__":
    base = "VisDrone2019-VID"
    for split in ["train", "val"]:
        seq_base = f"{base}-{split}/sequences"
        ann_base = f"{base}-{split}/annotations"
        for seq_name in tqdm(os.listdir(seq_base)):
            seq_dir = os.path.join(seq_base, seq_name)
            ann_file = os.path.join(ann_base, seq_name + ".txt")
            labels_seq_dir = os.path.join(seq_dir.replace("/sequences/", "/labels/"))
            convert_vid_annotations(seq_dir, ann_file, labels_seq_dir)
