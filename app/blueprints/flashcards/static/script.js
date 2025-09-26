let currentCardIndex = 0;
let knowCount = 0;
let forgetCount = 0;
const cards = document.querySelectorAll(".card");



function showCard() {
  cards.forEach((c, i) => {
    c.style.zIndex = cards.length - i;
    c.style.opacity = (i < currentCardIndex) ? "0" : "1";
    c.style.display = (i < currentCardIndex + 1) ? "block" : "none";
  });
}
showCard();

// flip card
cards.forEach(card => {
  card.addEventListener("click", () => {
    card.classList.toggle("flipped");
  });
});



// swipe function
function swipe(event, status) {
  event.preventDefault();
  const card = cards[currentCardIndex];
  if (!card) return;

    // cập nhật biến đếm tại đây
  if (status === "know") {
    card.status = "know";   // gán trực tiếp cho object
    knowCount++;
  } else if (status === "forget") {
    card.status = "forget";
    forgetCount++;
  }

    // gửi request đến Flask
    fetch("/flashcards/update_status", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        card_id: card.dataset.id,
        status: status
      })
    })
    .then(res => res.json())
    .then(data => {
      if (!data.success) {
        console.error("Update failed:", data.error);
      }
    });

  card.style.transform = (status === "know")
    ? "translateX(500px) rotate(20deg)"
    : "translateX(-500px) rotate(-20deg)";
  card.style.opacity = "0";



// Khi user chọn Know
function markKnow() {
  cards[currentCardIndex].status = "know";
  knowCount++;
}

// Khi user chọn Forget
function markForget() {
  cards[currentCardIndex].status = "forget";
  forgetCount++;
}

setTimeout(() => {
  currentCardIndex++;
    if (currentCardIndex < cards.length) {
        showCard();
    } else if (forgetCount > 0) {
    const setName = document.querySelector('.flashcard-wrapper').dataset.setName;
    const container = document.querySelector(".flashcard-wrapper");
    const retryUrl = `/flashcards/retry/${encodeURIComponent(setName)}`;
    const total = cards.length;
    container.innerHTML = `
      <p>🎉 Great job! You finished all cards in ${setName}.</p>
      <p>✅ Known: ${knowCount}/${total} &nbsp; ❌ Forgotten: ${forgetCount}</p>
      <a href="${retryUrl}" class="button">Retry Forgotten Cards</a>
    `;
    }
      else {
        const setName = document.querySelector('.flashcard-wrapper').dataset.setName;
        const container = document.querySelector(".flashcard-wrapper");
        const flashcardsUrl = `/flashcards/`;
        const total = cards.length;
        container.innerHTML = `
          <p>🎉 Amazing! You mastered all cards in ${setName}. No forgotten cards left 🎯</p>
          <p>✅ Known: ${knowCount}/${total}</p>
          <a href="${flashcardsUrl}" class="button">Go to Flashcards</a>
        `;
      }

    }, 300);
}



// Drag to swipe (Tinder effect)
let startX, currentCard;
document.querySelectorAll(".card").forEach(card => {
  card.addEventListener("mousedown", e => {
    startX = e.clientX;
    currentCard = card;
  });

  document.addEventListener("mouseup", e => {
    if (!currentCard) return;
    let diffX = e.clientX - startX;

    if (diffX > 100) {
      swipe(e, "know");
    } else if (diffX < -100) {
      swipe(e, "forget");
    } else {
      currentCard.style.transform = "translateX(0) rotate(0)";
    }
    currentCard = null;
  });

  document.addEventListener("mousemove", e => {
    if (!currentCard) return;
    let diffX = e.clientX - startX;
    currentCard.style.transform = `translateX(${diffX}px) rotate(${diffX / 10}deg)`;
  });
});



// extra flip class (optional animation)
document.querySelectorAll(".card").forEach(card => {
  card.addEventListener("click", () => {
    card.classList.toggle("is-flipped");
  });
});
