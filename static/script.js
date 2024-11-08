const tags = { examBoard: 'CBSE', level: 'Class 12', subject: 'Biology' };

function displayTags() {
    const tagContainer = document.getElementById('tagContainer');
    tagContainer.innerHTML = '';
    for (const [key, value] of Object.entries(tags)) {
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.innerText = value;
        tagContainer.appendChild(tag);
    }
}

function toggleDropdown(event) {
    event.preventDefault(); // Prevent link navigation
    const dropdownPanel = document.getElementById("dropdownPanel");
    dropdownPanel.style.display = dropdownPanel.style.display === "none" || dropdownPanel.style.display === "" ? "flex" : "none";
}

function applySyllabus() {
    const examBoard = document.getElementById("examBoard").value;
    const classLevel = document.getElementById("classLevel").value;
    const subject = document.getElementById("subject").value;

    // Update tags based on selected options
    tags.examBoard = examBoard;
    tags.level = classLevel;
    tags.subject = subject;

    // Display updated tags and close dropdown
    displayTags();
    document.getElementById("dropdownPanel").style.display = "none";
}

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

function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;

    appendMessage(userInput, true);
    document.getElementById("userInput").value = "";

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput, tags })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        appendMessage(data.response);
    })
    .catch(error => {
        console.error("Fetch error:", error);
        appendMessage("An error occurred: " + error.message);
    });
}

document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") sendMessage();
});

// Display default tags on page load
displayTags();
