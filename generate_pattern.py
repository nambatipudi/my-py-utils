import numpy as np
from PIL import Image, ImageDraw

# -------------- TWEAK ME -----------------
canvas_px   = 800   # final image size
grain_px    = 15     # ONE speckle = 5×5 pixels  ← change this!
# -----------------------------------------

# 1) compute the size of the coarse (small) noise grid
small_side = canvas_px // grain_px          # e.g. 800/5 = 160

# 2) make random 0-255 greys at that coarse resolution
noise_small = (np.random.rand(small_side, small_side) * 255).astype(np.uint8)
noise_img   = Image.fromarray(noise_small, mode="L")

# 3) blow it up to full size with NEAREST so each value
#    becomes a block of grain_px × grain_px identical pixels
noise_big = noise_img.resize((canvas_px, canvas_px), resample=Image.NEAREST)

# 4) same circular mask as before
radius = canvas_px // 2 - 10
mask = Image.new("L", (canvas_px, canvas_px), 0)
ImageDraw.Draw(mask).ellipse(
    [canvas_px//2 - radius, canvas_px//2 - radius,
     canvas_px//2 + radius, canvas_px//2 + radius],
    fill=255
)

# 5) composite onto a white background
canvas = Image.new("L", (canvas_px, canvas_px), 255)
canvas.paste(noise_big, (0, 0), mask)

canvas.save("speckle_grain5.png")
