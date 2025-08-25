document.addEventListener("DOMContentLoaded", function () {
  // Lesson completion
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

  // Notification mark as read
  const notificationItems = document.querySelectorAll(".notification-item");
  notificationItems.forEach((item) => {
    item.addEventListener("click", function () {
      const notificationId = item.dataset.notificationId;
      fetch('{% url "notifications:notification_list" %}', {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `notification_id=${notificationId}`,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            item.classList.add("opacity-50");
          }
        });
    });
  });
});
