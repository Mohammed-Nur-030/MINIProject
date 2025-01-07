document.getElementById("tts-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const text = document.getElementById("text").value;
    const fileName = document.getElementById("fileName").value;
   
    const selectedVoice = document.getElementById("voice-dropdown").value;

    
    const responseDiv = document.getElementById("response");
    console.log(text,fileName,responseDiv,selectedVoice)

    if (!text.trim()) {
        responseDiv.innerHTML = "Please enter some text!";
        return;
    }

    responseDiv.innerHTML = "Generating audio...";

    try {
        const response = await fetch("/generate-audio", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text, fileName,voice_id }),
        });

        const result = await response.json();
        if (result.success) {
            responseDiv.innerHTML = `Audio saved successfully as <strong>${fileName}.mp3</strong>.`;
        } else {
            responseDiv.innerHTML = `Error: ${result.error}`;
        }
    } catch (error) {
        console.error("Error:", error);
        responseDiv.innerHTML = "Something went wrong. Please try again.";
    }
});
