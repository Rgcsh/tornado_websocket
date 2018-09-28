var ws = new WebSocket("ws://127.0.0.1:8000/web");
const recordedVideo = document.querySelector('video#recorded');

function secMsg() {
    if ("WebSocket" in window) {
        var name = document.getElementById("name").value
        var talk = document.getElementById("talk").value
        var to = document.getElementById("to").value
        ws.onclose = function () {
            alert("请重新连接...");
        };
        var htmltext=$('.content').html()+"<p style='width:100%;text-align: left;'>"+talk+"</p>";
        $('.content').html(htmltext);
        ws.send(name + '#' + talk + '#' + to);
        ws.onmessage = function (evt) {
            if (evt.data.startsWith('data:video/webm;') == true) {
                function dataURLtoBlob(dataurl) {
                    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
                        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
                    while (n--) {
                        u8arr[n] = bstr.charCodeAt(n);
                    }
                    return new Blob([u8arr], {type: mime});
                }
               var vid=$('.getvideo').html()+'<video src='+window.URL.createObjectURL(dataURLtoBlob(evt.data))+' controls="controls" loop="loop" autoplay="autoplay" width="200" height="200">';
               $('.getvideo').html(vid);
               
            }else{
            	var html=$('.content').html()+"<p style='width:100%;text-align: left;'>"+evt.data+"</p>";
            	$('.content').html(html);
               // alert(evt.data);
            }

        };
    }
}

'use strict';

/* globals MediaRecorder */

const constraints = {
  audio: true,
  video: {
    width: 1280, height: 720
  }
};
const mediaSource = new MediaSource();
mediaSource.addEventListener('sourceopen', handleSourceOpen, false);
let mediaRecorder;
let recordedBlobs;
let sourceBuffer;

const errorMsgElement = document.querySelector('span#errorMsg');
const recordButton = document.querySelector('button#record');
recordButton.addEventListener('click', () => {
  if (recordButton.textContent === 'Start') {
    startRecording();
  } else {
    stopRecording();
    recordButton.textContent = 'Start';
    downloadButton.disabled = false;
  }
});


const downloadButton = document.querySelector('button#download');

function secMsg_video() {
  
    const blob = new Blob(recordedBlobs, {type: 'video/webm'});
    console.log(blob)
    var vid=$('.getvideo').html()+'<video src='+window.URL.createObjectURL(blob)+' controls="controls" loop="loop" autoplay="autoplay" width="200" height="200">';
               $('.getvideo').html(vid);
  function blobToDataURL(blob, callback) {
        var a = new FileReader();
        a.onload = function (e) { callback(e.target.result); }
        a.readAsDataURL(blob);
    }

      var name = document.getElementById("name").value
      var to = document.getElementById("to").value
    alert(name)
    alert(to)
    secMsg
    if ("WebSocket" in window) {

        ws.onclose = function () {
            alert("请重新连接...");
        };
         blobToDataURL(blob, function (dataurl) {
           console.log(name+'#'+dataurl+'#'+to)
            ws.send(name+'#'+dataurl+'#'+to);
         });
    }

}


function handleSourceOpen(event) {
  console.log('MediaSource opened');
  sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8"');
  console.log('Source buffer: ', sourceBuffer);
}

function handleDataAvailable(event) {
  if (event.data && event.data.size > 0) {
    recordedBlobs.push(event.data);
  }
}

function startRecording() {
  recordedBlobs = [];
  let options = {mimeType: 'video/webm;codecs=vp9'};
  if (!MediaRecorder.isTypeSupported(options.mimeType)) {
    console.error(`${options.mimeType} is not Supported`);
    errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
    options = {mimeType: 'video/webm;codecs=vp8'};
    if (!MediaRecorder.isTypeSupported(options.mimeType)) {
      console.error(`${options.mimeType} is not Supported`);
      errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
      options = {mimeType: 'video/webm'};
      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        console.error(`${options.mimeType} is not Supported`);
        errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
        options = {mimeType: ''};
      }
    }
  }

  try {
    mediaRecorder = new MediaRecorder(window.stream, options);
  } catch (e) {
    console.error('Exception while creating MediaRecorder:', e);
    errorMsgElement.innerHTML = `Exception while creating MediaRecorder: ${JSON.stringify(e)}`;
    return;
  }

  console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
  recordButton.textContent = 'Stop';
  downloadButton.disabled = true;
  mediaRecorder.onstop = (event) => {
    console.log('Recorder stopped: ', event);
  };
  mediaRecorder.ondataavailable = handleDataAvailable;
  mediaRecorder.start(10); // collect 10ms of data
  console.log('MediaRecorder started', mediaRecorder);
}

function stopRecording() {
  mediaRecorder.stop();
  console.log('Recorded Blobs: ', recordedBlobs);
}

function handleSuccess(stream) {
  recordButton.disabled = false;
  console.log('getUserMedia() got stream:', stream);
  window.stream = stream;

  const gumVideo = document.querySelector('video#gum');
  gumVideo.srcObject = stream;
}

async function init() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
  } catch (e) {
    console.error('navigator.getUserMedia error:', e);
    errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
  }
}

init();