from PIL import Image, ImageDraw, ImageFont

WIDTH = 1600
HEIGHT = 900
BG = (247, 248, 252)
NAVY = (18, 42, 76)
BLUE = (34, 102, 255)
CYAN = (0, 168, 204)
GREEN = (38, 166, 91)
ORANGE = (245, 124, 0)
GRAY = (95, 105, 120)
WHITE = (255, 255, 255)


def font(size: int, bold: bool = False):
    names = ["DejaVuSans-Bold.ttf", "Arial Bold.ttf"] if bold else ["DejaVuSans.ttf", "Arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def rounded_box(draw, xy, fill, outline=None, radius=24, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def centered_text(draw, box, text, fnt, fill=(0, 0, 0)):
    x1, y1, x2, y2 = box
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, align="center", spacing=6)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = x1 + (x2 - x1 - tw) / 2
    ty = y1 + (y2 - y1 - th) / 2
    draw.multiline_text((tx, ty), text, font=fnt, fill=fill, align="center", spacing=6)


def arrow(draw, start, end, color=BLUE, width=6):
    draw.line([start, end], fill=color, width=width)
    ex, ey = end
    draw.polygon([(ex, ey), (ex - 16, ey - 8), (ex - 16, ey + 8)], fill=color)


def build_architecture(path: str):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)

    d.text((70, 45), "Intelligent Test Selection Architecture", font=font(52, True), fill=NAVY)
    d.text((70, 110), "Machine Learning Based Test Subset Prediction for CI/CD", font=font(28), fill=GRAY)

    boxes = [
        ((70, 240, 300, 400), "Code\nChanges", (227, 242, 253), BLUE),
        ((340, 240, 600, 400), "Feature\nExtraction", (232, 245, 233), GREEN),
        ((640, 240, 930, 400), "ML Test\nSelector", (255, 243, 224), ORANGE),
        ((970, 240, 1270, 400), "Selected\nPlaywright\nTests", (230, 247, 255), CYAN),
        ((1310, 240, 1530, 400), "CI\nExecution", (236, 239, 241), NAVY),
    ]

    for box, label, fill, outline in boxes:
        rounded_box(d, box, fill=fill, outline=outline)
        centered_text(d, box, label, font(28, True), fill=NAVY)

    for i in range(len(boxes) - 1):
        b1 = boxes[i][0]
        b2 = boxes[i + 1][0]
        arrow(d, (b1[2] + 10, (b1[1] + b1[3]) // 2), (b2[0] - 10, (b2[1] + b2[3]) // 2))

    # feedback loop
    d.arc((440, 430, 1420, 840), start=20, end=188, fill=BLUE, width=7)
    d.polygon([(455, 552), (480, 540), (478, 570)], fill=BLUE)
    d.text((700, 725), "Execution Logs + Outcomes -> Periodic Retraining", font=font(30, True), fill=NAVY)

    d.text((70, 830), "Independent research prototype | Synthetic non-proprietary dataset", font=font(24), fill=GRAY)
    img.save(path, quality=95)


def build_results(path: str):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)

    d.text((70, 45), "CI Runtime Comparison", font=font(52, True), fill=NAVY)
    d.text((70, 110), "Full Regression vs Intelligent Test Selection (illustrative experiment)", font=font(28), fill=GRAY)

    chart_left, chart_top, chart_right, chart_bottom = 140, 220, 1460, 760
    d.rectangle((chart_left, chart_top, chart_right, chart_bottom), outline=(210, 216, 230), width=2, fill=WHITE)

    # axes
    d.line((chart_left + 70, chart_top + 40, chart_left + 70, chart_bottom - 70), fill=GRAY, width=4)
    d.line((chart_left + 70, chart_bottom - 70, chart_right - 50, chart_bottom - 70), fill=GRAY, width=4)

    # bars
    max_minutes = 30
    bars = [
        ("Full Suite", 26, NAVY),
        ("Selected Tests", 7, GREEN),
    ]

    x_positions = [520, 980]
    bar_width = 180
    for (label, value, color), x in zip(bars, x_positions):
        h = int((value / max_minutes) * 420)
        y1 = chart_bottom - 70 - h
        y2 = chart_bottom - 70
        d.rounded_rectangle((x - bar_width // 2, y1, x + bar_width // 2, y2), radius=20, fill=color)
        d.text((x - 95, y1 - 44), f"{value} min", font=font(30, True), fill=NAVY)
        d.text((x - 100, chart_bottom - 40), label, font=font(28, True), fill=NAVY)

    # speedup
    speedup = int((1 - 7 / 26) * 100)
    rounded_box(d, (1040, 240, 1430, 365), fill=(232, 245, 233), outline=GREEN, radius=16)
    d.text((1080, 270), f"~{speedup}% faster", font=font(44, True), fill=GREEN)

    d.text((170, 785), "Note: values represent prototype run profile; real gains depend on repository and test topology.", font=font(23), fill=GRAY)
    d.text((170, 825), "Dataset source: synthetic commit-impact history (no company data).", font=font(23), fill=GRAY)

    img.save(path, quality=95)


if __name__ == "__main__":
    build_architecture("/Users/rajeevsrivastava/workspace/intelligent-test-selection-ml/docs/images/architecture.jpg")
    build_results("/Users/rajeevsrivastava/workspace/intelligent-test-selection-ml/docs/images/results-comparison.jpg")
    print("Generated JPG files.")
