const URL_RECORD = '/api/voice';
const URL_TRANSCRIBE = '/api/transcribe'; 

// messages area
let div = document.createElement('div');
div.id = 'messages';

// start button
let start = document.createElement('button');
start.id = 'start';
start.innerHTML = 'Start Recording';

// stop button 
let stop = document.createElement('button');
stop.id = 'stop';
stop.innerHTML = 'Stop Recording';
stop.disabled = true;

// transcribe button
let transcribe = document.createElement('button');
transcribe.id = 'transcribe';
transcribe.innerHTML = 'Transcription';
transcribe.disabled = true;

document.body.appendChild(div);
document.body.appendChild(start);
document.body.appendChild(stop);
document.body.appendChild(transcribe);

let mediaRecorder;
let audioChunks = [];
let lastAudioPath = "";

// запрашиваем доступ к микрофону
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        start.addEventListener('click', function() {
            audioChunks = [];
            mediaRecorder.start();
            start.disabled = true;
            stop.disabled = false;
            transcribe.disabled = true;
            div.innerHTML += '<h3>Recording started...</h3>';
        });

        mediaRecorder.addEventListener("dataavailable", function(event) {
            audioChunks.push(event.data);
        });

        stop.addEventListener('click', function() {
            mediaRecorder.stop();
            start.disabled = false;
            stop.disabled = true;
            transcribe.disabled = false;
            div.innerHTML += '<h3>Recording stopped.</h3>';
        });

        mediaRecorder.addEventListener("stop", function() {
            const audioBlob = new Blob(audioChunks, {
                type: 'audio/webm'
            });

            let fd = new FormData();
            fd.append('voice', audioBlob, 'recording.webm');

            sendVoice(fd);
        });

        transcribe.addEventListener('click', function() {
            start.disabled = false;
            stop.disabled = true;
            transcribe.disabled = true;
            div.innerHTML += '<h3>Transcribing...</h3>';

            /*            
            const audioBlob = new Blob(audioChunks, {
                type: 'audio/webm'
            });

            let fd = new FormData();
            fd.append('voice', audioBlob, 'recording.webm');
            transcribeVoice(fd);
            */

            transcribeVoice();
        });

    })
    .catch(error => {
        console.error('Error accessing microphone:', error);
        div.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    });

async function sendVoice(form) {
    try {
        let response = await fetch(URL_RECORD, {
            method: 'POST',
            body: form
        });

        let result = await response.json();

        if (result.result === 'OK') {
            let audio = document.createElement('audio');
            audio.src = result.data;
            audio.controls = true;
            audio.style.display = 'block';
            audio.style.margin = '10px 0';

            let audioContainer = document.createElement('div');
            audioContainer.style.border = '1px solid #ccc';
            audioContainer.style.padding = '10px';
            audioContainer.style.margin = '10px 0';
            audioContainer.appendChild(audio);

            lastAudioPath = result.data;

            document.querySelector('#messages').appendChild(audioContainer);
        } else {
            console.error('Server error:', result.data);
            div.innerHTML += `<p style="color: red;">Error: ${result.data}</p>`;
        }
    } catch (error) {
        console.error('Error sending voice:', error);
        div.innerHTML += `<p style="color: red;">Network error: ${error.message}</p>`;
    }
}

async function transcribeVoice() {
    try {
        /*
        let response = await fetch(URL_TRANSCRIBE, {
            method: 'POST',
            body: form
        });
        */
        let response = await fetch(URL_TRANSCRIBE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'filename': lastAudioPath
            })
        });

        let result = await response.json();

        if (result.result === 'OK') {
            let textContainer = document.createElement('div')

            textContainer.textContent = result.data
            // textContainer.textContent = lastAudioPath;
            textContainer.style.border = '1px solid #ccc';
            textContainer.style.padding = '10px';
            textContainer.style.margin = '10px 0';

            document.querySelector('#messages').appendChild(textContainer);
 
        } else {
            console.error('Server error:', result.data);
            div.innerHTML += `<p style="color: red;">Error: ${result.data}</p>`;
        }
    } catch (error) {
        console.error('Error sending voice:', error);
        div.innerHTML += `<p style="color: red;">Network error: ${error.message}</p>`;
    }
}
