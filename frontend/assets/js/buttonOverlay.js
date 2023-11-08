var subreddit = document.getElementById('subreddit');
var specific = document.getElementById('secific');
var custom = document.getElementById('custom');
var mainBody = document.getElementById('mainBody');
var input1Label = document.getElementById('input1Label');
var input1 = document.getElementById('input1');
var input2 = document.getElementById('input2');
var submitButton = document.getElementById('submit');
var myBar = document.getElementById('myBar');
var myProgress = document.getElementById('myProgress');
var process = document.getElementById('process');
var buttonsTable = document.getElementById('buttonsTable');
var input1Table = document.getElementById('input1Table');
var submitTable = document.getElementById('submitTable');
var labelProcess = document.getElementById('labelProcess');
var file = document.getElementById('file');
var defultLogo = document.getElementById('defultLogo');
var inputFile = document.getElementById('inputFile');
var AIVoices = document.getElementById('AIVoices');
var AISelect = document.getElementById('AISelect');
var errorMessage = document.getElementById('errorMessage');
var option = 1;

subreddit.onclick = function () {
    reset();
    mainBody.style.display = "none";
    input1Label.innerHTML = "Subreddit";
    input1.placeholder = "AskReddit";
    subreddit.className = "button primary";
    option = 1;

}

specific.onclick = function () {
    reset();
    input1Label.innerHTML = "Specific Post";
    mainBody.style.display = "none";
    input1.placeholder = "https://www.reddit.com/r/AskReddit/comments/13yqbkx/what_can_you_do_better_when_youre_high/";
    specific.className = "button primary";
    option = 2;
}

custom.onclick = function () {
    reset();
    input1Label.innerHTML = "Intro";
    mainBody.style.display = "";
    input1.placeholder = "What can you do better when you’re high?";
    custom.className = "button primary";
    option = 3;
}

file.addEventListener("change", (event) => {
    defultLogo.style.display = "none";
  });

submitButton.onclick = function () {
    
    if (input2.value.length > 160) {
        alert("Please enter a shorter description, the maximum is 160 characters.");
        return;
    }


    var url = "";
    var data = {};
    if (option == 1) {
        data = {
            subreddit: input1.value,
            email: "test@email.com"
        }
        url = "subreddit";
    } else if (option == 2) {
        data = {
            url: input1.value,
            email: "test@email.com"
        }
        url = "subredditpost";
    } else if (option == 3) {
        data = {
            title: input1.value,
            answers: input2.value,
            email: "test@email.com"
        }
        url = "customvideo";
    }
    var fileData = file.files[0];

    var selectedIA = AIVoices.options[AIVoices.selectedIndex].value;
    data["AIvoice"] = selectedIA;

    hideInputs();

    move();
    downloadVideo(data, url, fileData);
}

function reset() {
    subreddit.className = "button";
    specific.className = "button";
    custom.className = "button";
}

// Declare id variable in an outer scope
var id = null;

function move() {
    // Clear any existing interval
    if (id) {
        clearInterval(id);
    }

    // Reset the bar and text to 0
    myBar.style.width = '0%';
    process.innerHTML = '0%';

    // Get the current time
    var start = Date.now();

    // Calculate the end time (3 minutes from now)
    var end = start + (3 * 60 * 1000);

    id = setInterval(frame, 10);
    
    function frame() {
        // Get the current time
        var now = Date.now();

        // Calculate the elapsed time as a percentage of total time
        var width = Math.min(100, ((now - start) / (end - start)) * 100);

        // Update the bar and text
        process.innerHTML = Math.round(width) + "%";
        myBar.style.width = width + "%";

        // If width is 100 or more, stop updating the bar
        if (width >= 100) {
            clearInterval(id);
            id = null;
        }
    }
}


async function downloadVideo(data, url, file) {
    let formData = new FormData();
    formData.append('input', JSON.stringify(data));
    if(file != null){
        formData.append('image', file);
    }

    const response = await fetch('http://reddit-to-video:8000' + url, {
        method: 'POST',
        body: formData
    });

    // Check if the response is OK (status 200-299)
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    } else {
        // Check the content type of the response
        const contentType = response.headers.get("content-type");

        // If the response is JSON, it may be an error message
        if(contentType && contentType.indexOf("application/json") !== -1) {
            const data = await response.json();
            if(data.error) {
                console.error('Server error:', data.error);
                showInputs();
                errorMessage.innerHTML = "Error: " + data.error;
                errorMessage.style.display = "";
            }
        } else {
            // If the response is a stream, stream it to a file
            const reader = response.body.getReader();
            const stream = new ReadableStream({
                start(controller) {
                    function push() {
                        reader.read().then(({done, value}) => {
                            if (done) {
                                controller.close();
                                return;
                            }
                            controller.enqueue(value);
                            push();
                        })
                    }
                    push();
                }
            });
            const newResponse = new Response(stream);
            const blob = await newResponse.blob();
            
            // Save the file using FileSaver
            saveAs(blob, 'myvideo.mp4');
            showInputs();
        }
    }
}


function hideInputs() {
    myProgress.style.display = "";
    process.style.display = "";
    labelProcess.style.display = "";
    errorMessage.style.display = "none";
    buttonsTable.style.display = "none";
    input1Table.style.display = "none";
    submitTable.style.display = "none";
    mainBody.style.display = "none";
    defultLogo.style.display = "none";
    inputFile.style.display = "none";
    AISelect.style.display = "none";
}

function showInputs() {
    myProgress.style.display = "none";
    process.style.display = "none";
    labelProcess.style.display = "none";
    buttonsTable.style.display = "";
    input1Table.style.display = "";
    submitTable.style.display = "";
    mainBody.style.display = option == 3 ? "" : "none";
    defultLogo.style.display = "";
    inputFile.style.display = "";
    AISelect.style.display = "";
    input1.value = "";
    input2.value = "";
    process.innerHTML = 0 + "%";
    myBar.style.width = 0 + "%";
    i = 0;
}


