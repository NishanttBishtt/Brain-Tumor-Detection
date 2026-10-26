
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path("segmentation/dataset/brisc2025/segmentation_task")
image_dir = ROOT / "train" / "images"
mask_dir = ROOT / "train" / "masks"

images = sorted(image_dir.glob("*.jpg"))

# Inspect one example for each tumor category.
selected = {}
for path in images:
    category = path.stem.split("_")[3]
    if category not in selected:
        selected[category] = path
    if len(selected) == 4:
        break

fig, axes = plt.subplots(len(selected), 3, figsize=(12, 4 * len(selected)))
if len(selected) == 1:
    axes = np.expand_dims(axes, axis=0)

for row, (category, image_path) in enumerate(selected.items()):
    mask_path = mask_dir / f"{image_path.stem}.png"

    image = np.array(Image.open(image_path).convert("RGB"))
    mask = np.array(Image.open(mask_path).convert("L"))

    axes[row, 0].imshow(image)
    axes[row, 0].set_title(f"{category}: MRI")

    axes[row, 1].imshow(mask, cmap="gray", vmin=0, vmax=255)
    axes[row, 1].set_title("Original mask")

    axes[row, 2].imshow(image)
    axes[row, 2].imshow(mask > 127, cmap="Reds", alpha=0.45, vmin=0, vmax=1)
    axes[row, 2].set_title("Thresholded overlay")

    for ax in axes[row]:
        ax.axis("off")

plt.tight_layout()
plt.show()
