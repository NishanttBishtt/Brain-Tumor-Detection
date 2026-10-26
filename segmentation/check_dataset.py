
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path("segmentation/dataset/brisc2025/segmentation_task")

for split in ("train", "test"):
    image_dir = ROOT / split / "images"
    mask_dir = ROOT / split / "masks"

    images = sorted(image_dir.glob("*.jpg"))
    masks = {p.stem: p for p in mask_dir.glob("*.png")}

    matched = 0
    missing = []
    mask_values = set()
    empty_masks = 0
    sample_shapes = []

    for image_path in images:
        # Match using the filename stem, not list position.
        mask_path = masks.get(image_path.stem)

        if mask_path is None:
            missing.append(image_path.name)
            continue

        matched += 1

        with Image.open(image_path) as img:
            image_size = img.size

        with Image.open(mask_path) as mask:
            arr = np.array(mask.convert("L"))
            mask_values.update(np.unique(arr).tolist())

        if not np.any(arr > 0):
            empty_masks += 1

        if len(sample_shapes) < 3:
            sample_shapes.append(
                (image_path.name, image_size, arr.shape)
            )

    print(f"\n{split.upper()}")
    print("Images:", len(images))
    print("Masks:", len(masks))
    print("Matched pairs:", matched)
    print("Missing masks:", len(missing))
    print("Empty masks:", empty_masks)
    print("Mask pixel values:", sorted(mask_values)[:30])
    print("Sample dimensions:", sample_shapes)

    if missing:
        print("First missing filenames:", missing[:5])
