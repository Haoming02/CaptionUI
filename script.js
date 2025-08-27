() => {
    const footer = document.querySelector("footer");
    footer.remove();

    const prev_btn = document.getElementById("prev_btn");
    prev_btn.title = "Previous Image";
    const save_btn = document.getElementById("save_btn");
    save_btn.title = "Save";
    const next_btn = document.getElementById("next_btn");
    next_btn.title = "Next Image";

    for (const btn of [prev_btn, save_btn, next_btn])
        btn.style.minWidth = "unset";

    window.addEventListener("keydown", (e) => {
        if (e.code === "Tab") {
            (e.shiftKey ? prev_btn : next_btn).click();
            e.preventDefault();
            return false;
        }
        if (e.code === "KeyS" && e.ctrlKey) {
            save_btn.click();
            e.preventDefault();
            return false;
        }
    });
}
