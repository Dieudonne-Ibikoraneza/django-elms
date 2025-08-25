document.addEventListener("DOMContentLoaded", function () {
  const completeButtons = document.querySelectorAll(".complete-lesson");
  completeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const lessonId = button.dataset.lessonId;
      fetch(window.location.href, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            button.disabled = true;
            button.textContent = "Completed";
            document.querySelector(
              "#progress-bar"
            ).style.width = `${data.progress}%`;
          }
        });
    });
  });
});
