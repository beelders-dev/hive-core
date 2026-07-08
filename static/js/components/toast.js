document.body.addEventListener("htmx:afterSwap", (event) => {
    const container = document.getElementById("toast-container");
    if (!container) return;

    container.querySelectorAll(".toast").forEach((toast) => {
        if (toast.dataset.timerStarted) return;

        toast.dataset.timerStarted = "true";
        

        setTimeout(() => {
       

            setTimeout(() => toast.remove(), 500);
        }, 2000);
    });
});