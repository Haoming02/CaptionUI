import os.path

os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")

import glob

import gradio as gr
from PIL import Image


FILES: list[tuple[os.PathLike, os.PathLike]] = []

with open("script.js", "r") as script:
    JS: str = script.read()


def load_pairs_from_path(path: str):
    FILES.clear()

    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        candidates = glob.glob(
            os.path.join(path, "**", f"*{ext}"),
            recursive=True,
        )

        for file in candidates:
            image = os.path.abspath(file)
            text = image.replace(ext, ".txt")
            if os.path.isfile(image) and os.path.isfile(text):
                FILES.append((image, text))


def validate():
    if len(FILES) == 0:
        raise gr.Error("No Files Found...", duration=3)

    gr.Info(f"Loaded {len(FILES)} Image-Caption Pairs", duration=3)
    images = [os.path.basename(img) for (img, txt) in FILES]
    return gr.update(open=False), gr.update(value=images[0], choices=images)


def next(index: int) -> int:
    return os.path.basename(FILES[(index + 1) % len(FILES)][0])


def prev(index: int) -> int:
    return os.path.basename(FILES[(index + len(FILES) - 1) % len(FILES)][0])


def load_pair(index: int) -> tuple[Image.Image, str]:
    img_path, txt_path = FILES[index]

    image = Image.open(img_path)
    with open(txt_path, "r") as file:
        caption = file.read()

    return gr.update(value=image), gr.update(value=caption)


def save(text: str, index: int):
    with open(FILES[index][1], "w") as f:
        f.write(text.strip())
    gr.Info("Saved...", duration=1)


with gr.Blocks(title="CaptionUI", analytics_enabled=False).queue() as app:

    with gr.Sidebar(width="24vw") as menu:
        dataset_path = gr.Textbox(
            value=None,
            lines=1,
            max_lines=1,
            label="Path to Dataset",
            info="absolute path is recommended",
        )

        with gr.Row():
            prev_btn = gr.Button("\U00002b05", elem_id="prev_btn")
            save_btn = gr.Button("\U0001f4be", elem_id="save_btn")
            next_btn = gr.Button("\U000027a1", elem_id="next_btn")

    selected_index = gr.Dropdown(
        value=None,
        choices=None,
        container=False,
        type="index",
    )
    preview_image = gr.Image(
        value=None,
        type="pil",
        sources="upload",
        show_label=False,
        show_download_button=False,
        show_fullscreen_button=False,
        show_share_button=False,
        interactive=False,
        height="72vh",
    )
    image_caption = gr.Textbox(
        value=None,
        lines=4,
        max_lines=4,
        container=False,
        interactive=True,
    )

    dataset_path.submit(
        fn=load_pairs_from_path,
        inputs=[dataset_path],
        show_progress="hidden",
    ).success(fn=validate, outputs=[menu, selected_index], show_progress="hidden")

    next_btn.click(
        fn=next,
        inputs=[selected_index],
        outputs=[selected_index],
        show_progress="hidden",
    )
    prev_btn.click(
        fn=prev,
        inputs=[selected_index],
        outputs=[selected_index],
        show_progress="hidden",
    )
    save_btn.click(
        fn=save,
        inputs=[image_caption, selected_index],
        show_progress="hidden",
    )

    selected_index.change(
        fn=load_pair,
        inputs=[selected_index],
        outputs=[preview_image, image_caption],
        show_progress="hidden",
    )

    app.load(fn=None, js=JS)

if __name__ == "__main__":
    app.launch()
