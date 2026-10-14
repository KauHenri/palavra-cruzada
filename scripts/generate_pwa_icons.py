from PIL import Image, ImageDraw, ImageFont
import os

def create_pwa_icon(size, is_maskable=False):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background
    bg_color = (59, 130, 246, 255) # #3b82f6
    radius = int(size * 0.23)
    if is_maskable:
        # Full square for maskable
        draw.rectangle([0, 0, size, size], fill=bg_color)
    else:
        # Rounded rectangle
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=bg_color)

    # Scale elements based on size
    # 512 base:
    # tiles: (76, 76), size 160x160, gap: 40, border_radius: 36
    scale = size / 512.0

    tile_size = int(160 * scale)
    tile_radius = int(36 * scale)
    p1 = int(76 * scale)
    p2 = int(276 * scale)

    # Tile 1: Top-left, White, 'P'
    draw.rounded_rectangle([p1, p1, p1 + tile_size, p1 + tile_size], radius=tile_radius, fill=(255, 255, 255, 255))

    # Tile 2: Top-right, Yellow, 'C'
    draw.rounded_rectangle([p2, p1, p2 + tile_size, p1 + tile_size], radius=tile_radius, fill=(253, 224, 71, 255))

    # Tile 3: Bottom-left, Pink, Heart
    draw.rounded_rectangle([p1, p2, p1 + tile_size, p2 + tile_size], radius=tile_radius, fill=(236, 72, 153, 255))

    # Tile 4: Bottom-right, White, 'X'
    draw.rounded_rectangle([p2, p2, p2 + tile_size, p2 + tile_size], radius=tile_radius, fill=(255, 255, 255, 255))

    # Fonts
    font_size = int(105 * scale)
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Draw letters centered
    # 'P'
    draw.text((p1 + tile_size // 2, p1 + tile_size // 2), "P", fill=(30, 41, 59, 255), font=font, anchor="mm")

    # 'C'
    draw.text((p2 + tile_size // 2, p1 + tile_size // 2), "C", fill=(30, 41, 59, 255), font=font, anchor="mm")

    # '♥'
    try:
        heart_font = ImageFont.truetype("seguiemj.ttf", int(90 * scale))
        draw.text((p1 + tile_size // 2, p2 + tile_size // 2), "❤", fill=(255, 255, 255, 255), font=heart_font, anchor="mm")
    except:
        draw.text((p1 + tile_size // 2, p2 + tile_size // 2), "♥", fill=(255, 255, 255, 255), font=font, anchor="mm")

    # 'X'
    draw.text((p2 + tile_size // 2, p2 + tile_size // 2), "X", fill=(37, 99, 235, 255), font=font, anchor="mm")

    return img

os.makedirs("public", exist_ok=True)
create_pwa_icon(192).save("public/pwa-192x192.png", "PNG")
create_pwa_icon(512).save("public/pwa-512x512.png", "PNG")
create_pwa_icon(512, is_maskable=True).save("public/pwa-maskable-512x512.png", "PNG")
create_pwa_icon(180).save("public/apple-touch-icon.png", "PNG")

print("Generated PWA PNG icons successfully!")
