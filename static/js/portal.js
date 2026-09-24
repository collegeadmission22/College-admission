document.addEventListener("DOMContentLoaded", () => {
  const applyOverlay = document.getElementById("apply-overlay");
  const applyClose = document.getElementById("apply-close");
  const openApply = (event) => {
    if (!applyOverlay) return;
    applyOverlay.classList.add("open");
    const trigger = event?.currentTarget;
    const sourceInput = applyOverlay.querySelector('input[name="lead_source"]');
    if (sourceInput) sourceInput.value = trigger?.dataset.leadSource || "Website";
    if (trigger?.dataset.college) {
      const college = applyOverlay?.querySelector('select[name="preferred_college"]');
      if (college) college.value = trigger.dataset.college;
    }
    if (trigger?.dataset.course) {
      const course = applyOverlay?.querySelector('select[name="course"]');
      if (course) course.value = trigger.dataset.course;
    }
    if (trigger?.dataset.distanceOnline) {
      const distanceOnline = applyOverlay?.querySelector('select[name="preferred_distance_online"]');
      if (distanceOnline) distanceOnline.value = trigger.dataset.distanceOnline;
    }
  };
  const closeApply = () => applyOverlay?.classList.remove("open");
  document.querySelectorAll("[data-open-apply]").forEach(button => button.addEventListener("click", openApply));
  document.querySelectorAll(".channel-lead").forEach(button => button.addEventListener("click", openApply));
  applyClose?.addEventListener("click", closeApply);
  applyOverlay?.addEventListener("click", event => { if (event.target === applyOverlay) closeApply(); });
  document.addEventListener("keydown", event => { if (event.key === "Escape") closeApply(); });
  if (applyOverlay?.dataset.autoOpen === "true" && !sessionStorage.getItem("applyPopupShown")) {
    window.setTimeout(() => { openApply(null); sessionStorage.setItem("applyPopupShown", "true"); }, Number(applyOverlay.dataset.delay || 5) * 1000);
  }
  const widget = document.getElementById("chat-widget");
  const launcher = document.getElementById("chat-launcher");
  const close = document.getElementById("chat-close");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const messages = document.getElementById("chat-messages");
  if (!widget || !launcher || !form) return;
  const csrf = () => document.cookie.split("; ").find(row => row.startsWith("csrftoken="))?.split("=")[1] || "";
  const addMessage = (text, type) => { const item = document.createElement("div"); item.className = type + "-message"; item.textContent = text; messages.appendChild(item); messages.scrollTop = messages.scrollHeight; };
  const ask = async (question) => {
    addMessage(question, "user"); input.value = ""; input.disabled = true;
    try {
      const response = await fetch("/api/chatbot/", {method:"POST", headers:{"Content-Type":"application/json","X-CSRFToken":csrf()}, body:JSON.stringify({message:question})});
      const data = await response.json(); addMessage(data.reply || data.error || "Please try again.", "bot");
    } catch { addMessage("I am temporarily unavailable. Please use WhatsApp for immediate help.", "bot"); }
    input.disabled = false; input.focus();
  };
  launcher.addEventListener("click", () => { widget.classList.add("open"); input.focus(); });
  close.addEventListener("click", () => widget.classList.remove("open"));
  form.addEventListener("submit", e => { e.preventDefault(); if(input.value.trim()) ask(input.value.trim()); });
  document.querySelectorAll("[data-question]").forEach(button => button.addEventListener("click", () => ask(button.dataset.question)));
});

// Catalogue cards: image click opens the free counselling form.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".apply-image[tabindex]").forEach(el => el.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); el.click(); } }));
  document.addEventListener("copy", e => { if (!e.target.closest("input,textarea")) e.preventDefault(); });
  document.addEventListener("contextmenu", e => { if (e.target.closest("img")) e.preventDefault(); });
});
