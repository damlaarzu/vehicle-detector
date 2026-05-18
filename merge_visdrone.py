#!/usr/bin/env python3
import os, shutil
from tqdm import tqdm

def ensure_dir(p): 
    os.makedirs(p, exist_ok=True)

def copy_det_split(det_base, split, out_images_dir, out_labels_dir):
    images_dir = os.path.join(det_base + "-" + split, "images")
    labels_dir = os.path.join(det_base + "-" + split, "labels")
    ensure_dir(out_images_dir); ensure_dir(out_labels_dir)
    for fname in tqdm(sorted(os.listdir(images_dir)), desc=f"DET {split}"):
        if not fname.lower().endswith(('.jpg','.jpeg','.png')): continue
        src_img = os.path.join(images_dir, fname)
        dst_img = os.path.join(out_images_dir, fname)
        shutil.copy2(src_img, dst_img)
        label_name = os.path.splitext(fname)[0] + ".txt"
        src_label = os.path.join(labels_dir, label_name)
        dst_label = os.path.join(out_labels_dir, label_name)
        if os.path.exists(src_label):
            shutil.copy2(src_label, dst_label)
        else:
            open(dst_label, "w").close()

def copy_vid_split(vid_base, split, out_images_dir, out_labels_dir):
    seqs_dir = os.path.join(vid_base + "-" + split, "sequences")
    ensure_dir(out_images_dir); ensure_dir(out_labels_dir)
    for seq_name in tqdm(sorted(os.listdir(seqs_dir)), desc=f"VID {split}"):
        seq_dir = os.path.join(seqs_dir, seq_name)
        if not os.path.isdir(seq_dir): continue
        # label dir is expected next to sequence (e.g. seq_dir/../labels/) or inside seq_dir/labels
        # We'll check two possibilities:
        labels_in_seq = os.path.join(seq_dir, "labels")
        labels_next_to_seq = os.path.join(os.path.dirname(seq_dir), "labels")
        if os.path.isdir(labels_in_seq):
            labels_dir = labels_in_seq
        elif os.path.isdir(labels_next_to_seq):
            labels_dir = labels_next_to_seq
        else:
            labels_dir = None
        for imgname in sorted(os.listdir(seq_dir)):
            if not imgname.lower().endswith(('.jpg','.jpeg','.png')): continue
            new_name = f"{seq_name}_{imgname}"
            src_img = os.path.join(seq_dir, imgname)
            dst_img = os.path.join(out_images_dir, new_name)
            shutil.copy2(src_img, dst_img)
            # corresponding label
            label_old = os.path.splitext(imgname)[0] + ".txt"
            dst_label = os.path.join(out_labels_dir, os.path.splitext(new_name)[0] + ".txt")
            if labels_dir:
                src_label = os.path.join(labels_dir, label_old)
                if os.path.exists(src_label):
                    shutil.copy2(src_label, dst_label)
                else:
                    open(dst_label, "w").close()
            else:
                open(dst_label, "w").close()

if __name__ == "__main__":
    # Düzenle: dosya adlarını kendi klasör yapına göre değiştir
    DET_BASE = "VisDrone2019-DET"   # expects VisDrone2019-DET-train and -val folders
    VID_BASE = "VisDrone2019-VID"   # expects VisDrone2019-VID-train and -val folders
    OUT_BASE = "datasets/visdrone"

    OUT_IMAGES_TRAIN = os.path.join(OUT_BASE, "images", "train")
    OUT_IMAGES_VAL   = os.path.join(OUT_BASE, "images", "val")
    OUT_LABELS_TRAIN = os.path.join(OUT_BASE, "labels", "train")
    OUT_LABELS_VAL   = os.path.join(OUT_BASE, "labels", "val")

    ensure_dir(OUT_IMAGES_TRAIN); ensure_dir(OUT_IMAGES_VAL)
    ensure_dir(OUT_LABELS_TRAIN); ensure_dir(OUT_LABELS_VAL)

    # copy DET
    copy_det_split(DET_BASE, "train", OUT_IMAGES_TRAIN, OUT_LABELS_TRAIN)
    copy_det_split(DET_BASE, "val",   OUT_IMAGES_VAL,   OUT_LABELS_VAL)

    # copy VID (with prefix)
    copy_vid_split(VID_BASE, "train", OUT_IMAGES_TRAIN, OUT_LABELS_TRAIN)
    copy_vid_split(VID_BASE, "val",   OUT_IMAGES_VAL,   OUT_LABELS_VAL)

    print("Tamam. Birleştirme bitti.")
