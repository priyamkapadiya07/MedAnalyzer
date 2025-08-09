const chatForm = document.getElementById("chat-form");
  const chatBox = document.getElementById("chat-box");
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  const clearChatButton = document.getElementById("delete-button");

  // Modal elements
  const confirmationModal = document.getElementById("confirmation-modal");
  const modalConfirmButton = document.getElementById("modal-confirm");
  const modalCancelButton = document.getElementById("modal-cancel");

  function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  document.addEventListener("DOMContentLoaded", scrollToBottom);

  chatForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const message = messageInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    messageInput.value = "";

    const typingIndicator = document.createElement("div");
    typingIndicator.className = "typing-indicator";
    typingIndicator.textContent = "✨ Bot is typing...";
    chatBox.appendChild(typingIndicator);
    scrollToBottom();

    try {
      const response = await fetch("{% url 'chatbot' %}", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": "{{ csrf_token }}",
        },
        body: new URLSearchParams({ message }),
      });

      const data = await response.json();
      typingIndicator.remove();
      appendMessage("bot", data.reply);
      scrollToBottom();
    } catch (error) {
      typingIndicator.remove();
      appendMessage("bot", "Oops! Something went wrong.");
    }
  });

  function appendMessage(sender, text) {
    const noChat = document.getElementById("no-chat");
    if (noChat) noChat.style.display = "none";

    const message = document.createElement("div");
    message.className = `chat-message ${sender}`;

    const icon = document.createElement("div");
    icon.className = "profile-icon";
    icon.innerHTML = sender === "user" ? "🧑🏻" : "✨";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    if (sender === "bot") {
      bubble.innerHTML = marked.parse(text);
    } else {
      bubble.textContent = text;
    }

    message.appendChild(icon);
    message.appendChild(bubble);
    chatBox.appendChild(message);
    scrollToBottom();
  }

  // Function to show the modal
  function showModal() {
    confirmationModal.style.display = "flex";
    setTimeout(() => confirmationModal.classList.add("show"), 10);
  }

  function hideModal() {
    confirmationModal.classList.remove("show");
    confirmationModal.addEventListener("transitionend", function handler() {
      confirmationModal.style.display = "none";
      confirmationModal.removeEventListener("transitionend", handler);
    });
  }

  clearChatButton.addEventListener("click", function () {
    showModal();
  });

  modalConfirmButton.addEventListener("click", async function () {
    hideModal();
    try {
      const response = await fetch("{% url 'clear_chat' %}", {
        method: "POST",
        headers: {
          "X-CSRFToken": "{{ csrf_token }}",
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      if (data.status === "success") {
        chatBox.innerHTML = `
                    <div class="no-chat-message" id="no-chat">
                        ✨ Ask me anything about your health to get started!
                    </div>
                `;
        document.getElementById("no-chat").style.display = "block";
        scrollToBottom();
        console.log(data.message);
      } else {
        console.warn(data.message);
      }
    } catch (error) {
      console.error("Error clearing chat:", error);
      alert("Failed to clear chat history. Please try again.");
    }
  });

  modalCancelButton.addEventListener("click", function () {
    hideModal();
  });

  confirmationModal.addEventListener("click", function (event) {
    if (event.target === confirmationModal) {
      hideModal();
    }
  });

  // speech script for microphone

//   {% comment %} const micIcon = document.getElementById("mic-icon");

//   const SpeechRecognition =
//     window.SpeechRecognition || window.webkitSpeechRecognition;

//   if (SpeechRecognition) {
//     const recognition = new SpeechRecognition();
//     recognition.continuous = false;
//     recognition.interimResults = true;
//     recognition.lang = "en-US";

//     micIcon.addEventListener("click", () => {
//       finalTranscript = "";
//       recognition.start();
//       micIcon.classList.add("listening");
//     });

//     let finalTranscript = "";

//     recognition.onresult = (event) => {
//       let interimTranscript = "";

//       for (let i = event.resultIndex; i < event.results.length; i++) {
//         const transcript = event.results[i][0].transcript;

//         if (event.results[i].isFinal) {
//           finalTranscript += transcript;
//         } else {
//           interimTranscript += transcript;
//         }
//       }

//       messageInput.value = finalTranscript + interimTranscript;
//       messageInput.scrollLeft = messageInput.scrollWidth;
//     };

//     recognition.onerror = (event) => {
//       console.error("Speech recognition error:", event.error);
//       micIcon.classList.remove("listening");
//     };

//     recognition.onend = () => {
//       micIcon.classList.remove("listening");
//       messageInput.focus();
//     };
//   } else {
//     alert("Your browser does not support Speech Recognition.");
//   } {% endcomment %}



  const micIcon = document.getElementById("mic-icon");

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    const wakeRecognition = new SpeechRecognition();
    wakeRecognition.continuous = true;
    wakeRecognition.interimResults = false;
    wakeRecognition.lang = "en-US";

    let finalTranscript = "";

    // 🟢 Wake word detection
    wakeRecognition.onresult = function (event) {
      const transcript = event.results[event.resultIndex][0].transcript.trim().toLowerCase();
      console.log("Wake heard:", transcript);
      if (transcript.includes("hi nova")) {
        wakeRecognition.stop(); // stop wake listener
        startListening(); // start main speech
      }
    };

    wakeRecognition.onend = () => {
      // restart wake detection if not actively recognizing
      if (!micIcon.classList.contains("listening")) {
        try { wakeRecognition.start(); } catch (e) {}
      }
    };

    wakeRecognition.onerror = (e) => {
      console.warn("Wake error:", e.error);
    };

    // 🟢 Mic click
    micIcon.addEventListener("click", () => {
      wakeRecognition.stop(); // prevent overlap
      startListening();
    });

    // 🎤 Start recognition
    function startListening() {
      finalTranscript = "";
      micIcon.classList.add("listening");
      recognition.start();
    }

    // ✍️ Live update
    recognition.onresult = (event) => {
      let interim = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const text = event.results[i][0].transcript;
        if (event.results[i].isFinal) finalTranscript += text;
        else interim += text;
      }
      messageInput.value = finalTranscript + interim;
      messageInput.scrollLeft = messageInput.scrollWidth;
    };

    recognition.onerror = (e) => {
      console.error("Speech error:", e.error);
      micIcon.classList.remove("listening");
    };

    recognition.onend = () => {
      micIcon.classList.remove("listening");
      messageInput.focus();
      try { wakeRecognition.start(); } catch (e) {}
    };

    // 🔄 Start wake listener on load
    window.addEventListener("load", () => {
      try { wakeRecognition.start(); } catch (e) {}
    });
  } else {
    alert("Speech recognition not supported in this browser.");
  }