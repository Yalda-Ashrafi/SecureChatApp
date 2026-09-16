document.addEventListener("DOMContentLoaded", () => {
    const algorithm = document.querySelector("#algorithm");
    const help = document.querySelector("#key-help");
    const message = document.querySelector("#plaintext");
    const key = document.querySelector("#key");

    if (algorithm && help && message && key) {
        const examples = {
            vigenere: {
                message: "Example: Meet me at the library at 5 PM.",
                key: "Example: LEMON",
                help: "Use ASCII letters only. Spaces and punctuation are preserved. Example key: LEMON."
            },
            vernam: {
                message: "Example: HELLO",
                key: "Example: XMCKL",
                help: "Use a key with exactly the same UTF-8 byte length as the message. Example: HELLO + XMCKL."
            },
            otp: {
                message: "Example: Secret meeting at 8 PM.",
                key: "Example: enter a key matching the message length",
                help: "Use a fresh random key with exactly the same UTF-8 byte length as the message. Never reuse it."
            }
        };

        const updateExamples = () => {
            const example = examples[algorithm.value] || examples.vigenere;
            message.placeholder = example.message;
            key.placeholder = example.key;
            help.textContent = example.help;
        };

        algorithm.addEventListener("change", updateExamples);
        updateExamples();
    }

    document.querySelectorAll("[data-password-toggle]").forEach((toggle) => {
        toggle.addEventListener("click", () => {
            const input = document.getElementById(toggle.dataset.target);
            if (!input) return;
            const isVisible = input.type !== "password";
            input.type = isVisible ? "password" : "text";
            toggle.innerHTML = isVisible
                ? '<svg class="eye-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z"></path><circle cx="12" cy="12" r="2.5"></circle></svg>'
                : '<svg class="eye-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="m3 3 18 18M10.6 6.2A10.8 10.8 0 0 1 12 6c6 0 9.5 6 9.5 6a18.8 18.8 0 0 1-3.1 3.7M6.2 6.8C3.8 8.4 2.5 12 2.5 12s3.5 6 9.5 6c1.5 0 2.8-.4 4-.9"></path></svg>';
            toggle.setAttribute("aria-label", `${isVisible ? "Show" : "Hide"} ${input.id === "key" ? "key" : "password"}`);
        });
    });

    document.querySelectorAll("[data-loading-form]").forEach((form) => {
        form.addEventListener("submit", () => {
            const submit = form.querySelector("button[type='submit']");
            if (!submit) return;
            submit.disabled = true;
            submit.classList.add("is-loading");
            submit.setAttribute("aria-busy", "true");
            const loadingLabel = submit.dataset.loadingLabel;
            if (loadingLabel) submit.childNodes[0].textContent = `${loadingLabel} `;
        });
    });

    document.querySelectorAll("[data-toast]").forEach((toast) => {
        const dismiss = toast.querySelector(".alert-dismiss");
        if (dismiss) {
            dismiss.addEventListener("click", () => dismissToast(toast));
        }
        if (toast.classList.contains("success")) {
            window.setTimeout(() => dismissToast(toast), 6500);
        }
    });

    document.querySelectorAll("[data-copy-target]").forEach((button) => {
        button.addEventListener("click", async () => {
            const target = document.getElementById(button.dataset.copyTarget);
            if (!target) return;
            const value = target.value !== undefined ? target.value : target.textContent.trim();
            const status = button.closest(".result-callout, .demo-output-card")?.querySelector(".copy-status");
            try {
                await copyText(value);
                if (status) status.textContent = "Copied";
                window.setTimeout(() => {
                    if (status) status.textContent = "";
                }, 2200);
            } catch (error) {
                if (status) status.textContent = "Select and copy manually";
            }
        });
    });
});

function dismissToast(toast) {
    if (!toast || toast.classList.contains("is-dismissing")) return;
    toast.classList.add("is-dismissing");
    window.setTimeout(() => toast.remove(), 220);
}

async function copyText(value) {
    if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(value);
        return;
    }
    const helper = document.createElement("textarea");
    helper.value = value;
    helper.setAttribute("readonly", "");
    helper.style.position = "fixed";
    helper.style.opacity = "0";
    document.body.appendChild(helper);
    helper.select();
    const copied = document.execCommand("copy");
    helper.remove();
    if (!copied) throw new Error("Copy was not available");
}
