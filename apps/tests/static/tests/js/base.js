function showGlobalError(message, timeout = 10000) {
    let container = document.getElementById("global-error-container");

    if (!container) return;

    const el = document.createElement("div");
    el.className = "global-error";
    el.textContent = message;

    container.appendChild(el);

    setTimeout(() => {
        el.style.opacity = "0";
        el.style.transform = "translateY(-10px)";
        setTimeout(() => el.remove(), 300);
    }, timeout);
}