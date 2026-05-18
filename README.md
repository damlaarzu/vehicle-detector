# Vehicle Detector (YOLO11 + VisDrone)

VisDrone veri seti üzerinde eğitilmiş **YOLO11** modeli ile hava/drone görüntülerinde nesne tespiti yapan proje. **Streamlit** web arayüzü üzerinden fotoğraf, video ve canlı kamera ile tespit yapılabilir.

## Özellikler

- **Web arayüzü** (`app.py`): fotoğraf yükleme, video işleme, gerçek zamanlı kamera
- **10 sınıf**: yaya, insan kalabalığı, bisiklet, araba, van, kamyon, üç tekerlekli, tenteli üç tekerlekli, otobüs, motosiklet
- **Veri hazırlama**: VisDrone DET/VID → YOLO formatı dönüştürme ve birleştirme scriptleri
- **Eğitim**: Ultralytics YOLO11 (`yolo11s.pt`) ile özelleştirilmiş model

## Proje yapısı

```
.
├── app.py                    # Streamlit web uygulaması
├── visdrone_det_to_yolo.py   # VisDrone DET etiketlerini YOLO'ya çevirir
├── convert_vid_to_yolo.py    # VisDrone VID etiketlerini YOLO'ya çevirir
├── merge_visdrone.py         # DET + VID verilerini tek data setinde birleştirir
├── check_labels.py           # Etiket kontrolü
├── datasets/visdrone/
│   └── data.yaml             # Sınıf tanımları ve yol ayarları
├── projects/visdrone/        # Eğitim çıktıları (weights, grafikler)
├── yolo11s.pt                # Temel / eğitilmiş model (yerel)
└── requirements.txt
```

## Gereksinimler

- Python 3.10+
- (Önerilir) NVIDIA GPU + CUDA — eğitim ve canlı tespit için
- Web kamerası — “Camera (Real-Time)” modu için

## Kurulum

```bash
# Depoyu klonla
git clone https://github.com/damlaarzu/vehicle-detector.git
cd vehicle-detector

# Sanal ortam
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

### Model dosyası

`app.py` varsayılan olarak `yolo11s.pt` kullanır. Kendi eğittiğiniz modeli kullanmak için:

```python
MODEL_PATH = "projects/visdrone/exp12/weights/best.pt"
```

Model dosyası repoda yoksa [Ultralytics YOLO11](https://github.com/ultralytics/ultralytics) ilk çalıştırmada indirir veya eğitim sonrası `projects/visdrone/exp*/weights/best.pt` yolunu kullanın.

### VisDrone veri seti (eğitim için)

Ham veri repoda **yer almaz**. [VisDrone](http://aiskyeye.com/download/visdrone-2019/) sitesinden indirip proje köküne çıkarın:

- `VisDrone2019-DET-train`, `VisDrone2019-DET-val`
- `VisDrone2019-VID-train`, `VisDrone2019-VID-val` (isteğe bağlı)

Ardından dönüştürme ve birleştirme scriptlerini çalıştırın:

```bash
python visdrone_det_to_yolo.py
python convert_vid_to_yolo.py
python merge_visdrone.py
```

## Kullanım

### Web uygulaması

```bash
streamlit run app.py
```

Tarayıcıda açılan arayüzden **Photo**, **Video** veya **Camera (Real-Time)** seçin.

### Model eğitimi

```bash
yolo detect train data=datasets/visdrone/data.yaml model=yolo11s.pt epochs=50 imgsz=416 batch=8 project=projects/visdrone name=exp12
```

## Sınıflar (`data.yaml`)

| ID | Sınıf |
|----|--------|
| 0 | pedestrian |
| 1 | people |
| 2 | bicycle |
| 3 | car |
| 4 | van |
| 5 | truck |
| 6 | tricycle |
| 7 | awning-tricycle |
| 8 | bus |
| 9 | motor |

## GitHub’a yükleme — önemli notlar

Mevcut depoda **venv**, **VisDrone ham verileri** ve **binlerce eğitim görseli** commit edilmiş durumda; depo boyutu yaklaşık **13 GB**. GitHub tek dosya için **100 MB**, önerilen repo boyutu çok daha küçüktür; bu haliyle `git push` büyük olasılıkla **başarısız olur**.

### Yapmanız gerekenler (özet)

1. **`.gitignore` kullanın** (projede eklendi) — `venv/`, `VisDrone*/`, büyük `datasets/visdrone/images/` klasörlerini hariç tutun.
2. **Repoyu sadeleştirin** — yanlışlıkla eklenen dosyaları git geçmişinden çıkarın veya yeni, temiz bir repo başlatın.
3. **Sadece kaynak kodu push edin**: `*.py`, `data.yaml`, `requirements.txt`, `README.md`, isteğe bağlı küçük örnek görseller.
4. **`.pt` model dosyalarını** GitHub’a doğrudan koymayın; [Git LFS](https://git-lfs.github.com/) veya **Releases** ile paylaşın.
5. **VisDrone** görsellerini repoya koymayın; README’de indirme linki verin (lisans koşullarına uyun).

### Temiz repo ile GitHub (önerilen)

```powershell
cd "C:\Users\90506\Desktop\yolov11 photo vid realtime web"

# Uzak repo zaten tanımlı: origin -> vehicle-detector
git remote -v

# Yeni commit: README, .gitignore, requirements.txt
git add README.md .gitignore requirements.txt app.py *.py datasets/visdrone/data.yaml
git status

git commit -m "README ve proje dokümantasyonu eklendi"
git push -u origin main
```

Push hâlâ başarısız olursa, geçmişi temizlemeniz gerekir. **Yedek aldıktan sonra** yeni bir dal veya sıfırdan repo:

```powershell
# Örnek: sadece kaynak kodu yeni bir commit geçmişiyle (dikkat: eski geçmiş silinir)
git checkout --orphan clean-main
git add README.md .gitignore requirements.txt app.py visdrone_det_to_yolo.py convert_vid_to_yolo.py merge_visdrone.py check_labels.py IsNull.py datasets/visdrone/data.yaml
git commit -m "İlk temiz sürüm: kaynak kod ve dokümantasyon"
git branch -D main
git branch -m main
git push -f origin main
```

`git push -f` yalnızca uzak repoda eski (büyük) geçmişi silmek istediğinizde kullanın.

### GitHub’da repo oluşturma (henüz yoksa)

1. [github.com](https://github.com) → **New repository** → `vehicle-detector`
2. Yerelde: `git remote add origin https://github.com/KULLANICI/vehicle-detector.git`
3. `git push -u origin main`

Kimlik doğrulama: **Personal Access Token** (HTTPS) veya **SSH anahtarı** gerekir.

## Lisans ve veri seti

- **VisDrone** veri seti kendi kullanım koşullarına tabidir; dağıtım ve ticari kullanım için [resmi siteyi](http://aiskyeye.com/) kontrol edin.
- **Ultralytics YOLO**: [AGPL-3.0](https://github.com/ultralytics/ultralytics/blob/main/LICENSE)

## Katkı

Issue ve pull request ile katkıda bulunabilirsiniz.
