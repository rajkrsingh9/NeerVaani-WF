document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".speech-button");
  
    buttons.forEach(button => {
      button.addEventListener("click", () => {
        const inputId = button.getAttribute("data-input");
        const inputField = document.getElementById(inputId);
  
        // Check if the browser supports Speech Recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  
        if (SpeechRecognition) {
          const recognition = new SpeechRecognition();
          recognition.lang = "en-US";
  
          recognition.onstart = () => {
            console.log("Speech recognition started...");
          };
  
          recognition.onspeechend = () => {
            recognition.stop();
            console.log("Speech recognition stopped.");
          };
  
          recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            inputField.value = transcript;
          };
  
          recognition.start();
        } else {
          alert("Speech Recognition is not supported in this browser.");
        }
      });
    });
  });