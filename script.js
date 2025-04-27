document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    if (!loginForm) {
        console.error("Error: loginForm not found");
        return;
    }
document.getElementById("username").value=localStorage.getItem("username") || "User name";
document.getElementById("password").value=localStorage.getItem("password") || "";
	
});

document.getElementById("loginForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(loginForm);
        const jsonData = Object.fromEntries(formData.entries()); // ✅ Avoids eval-like behavior
	  console.log(jsonData);
	localStorage.setItem("username",document.getElementById("username").value);
	localStorage.setItem("password", document.getElementById("password").value);
        const json_val=JSON.stringify(jsonData) 
        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: json_val
            });

            const result = await response.json();
            const messageElement = document.getElementById("loginMessage");

            if (!messageElement) {
                console.error("Error: loginMessage element not found");
                return;
            }

            messageElement.innerText = result.message || result.error;
            messageElement.classList.toggle("error", !response.ok);
        } catch (error) {
            console.error("Fetch error:", error);
            const messageElement = document.getElementById("loginMessage");
            if (messageElement) {
                messageElement.innerText = "An error occurred";
                messageElement.classList.add("error");
            }
        }
    });

