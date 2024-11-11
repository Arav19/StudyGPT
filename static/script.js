// Initial tag data
const tags = { examBoard: 'CBSE', level: 'Class 12', subject: 'Biology' };

// Function to display the tags based on user selection
function displayTags() {
    const tagContainer = document.getElementById('tagContainer');
    tagContainer.innerHTML = '';  // Clear previous tags
    for (const [key, value] of Object.entries(tags)) {
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.innerText = value;
        tagContainer.appendChild(tag);
    }
}

// Function to toggle dropdown panel with animation
function toggleDropdown(event) {
    event.preventDefault();
    const dropdownPanel = document.getElementById("dropdownPanel");
    if (dropdownPanel.style.display === "none" || dropdownPanel.style.display === "") {
        dropdownPanel.style.display = "flex";
        dropdownPanel.style.opacity = "1"; // Add opacity for smooth display
    } else {
        dropdownPanel.style.opacity = "0";
        setTimeout(() => dropdownPanel.style.display = "none", 300); // Delay for fade-out effect
    }
}

function applySyllabus() {
    const examBoard = document.getElementById("examBoard").value;
    const classLevel = document.getElementById("classLevel").value;
    const subject = document.getElementById("subject").value;

    // Update the tags object with the selected values
    tags.examBoard = examBoard;
    tags.level = classLevel;
    tags.subject = subject;

    // Display the updated tags on the screen
    displayTags();
    
    // Close the dropdown
    document.getElementById("dropdownPanel").style.display = "none";
}

// Append messages to chatbox
function appendMessage(text, isUser = false) {
    const chatBox = document.getElementById("chatBox");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", isUser ? "user" : "bot");

    const messageText = document.createElement("p");
    messageText.innerText = text;
    messageDiv.appendChild(messageText);

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
}

// Send message to the server
function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;

    appendMessage(userInput, true);
    document.getElementById("userInput").value = "";
    document.getElementById("userInput").focus(); // Re-focus on input field

    fetch('https://study-gpt-vbvw.onrender.com/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput, tags })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.response);
    })
    .catch(error => {
        console.error("Error:", error);
        appendMessage("Unable to connect to the server. Please try again later.");
    });
}

// Enter key to send message
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent default form submission
        sendMessage();
    }
});

// Initialize tags
displayTags();
