/*
variables
*/
var model;
var classNames = [];
var canvas;
var tmpCanvas;// resize img
var coords = [];
var mousePressed = false;
var mode;
var index;

/*
prepare the drawing canvas 
*/
$(function() {
    canvas = window._canvas = new fabric.Canvas('canvas');
    tmpCanvas = window._canvas = new fabric.Canvas('canvasTemp');
    tmpCtx =  tmpCanvas.getContext("2d");

    canvas.backgroundColor = '#ffffff';
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.color = "black";
    canvas.freeDrawingBrush.width = 7;
    canvas.renderAll();
    //setup listeners 
    canvas.on('mouse:up', function(e) {
        mousePressed = false
    });
    canvas.on('mouse:down', function(e) {
        mousePressed = true
    });
    canvas.on('mouse:move', function(e) {
        recordCoor(e)
    });
})

function convertImg(){
    document.getElementById('statusTemp').innerHTML = "Please wait a second";
    getImageData();
}

function recordCoor(event) {
    var pointer = canvas.getPointer(event.e);
    var posX = pointer.x;
    var posY = pointer.y;

    if (posX >= 0 && posY >= 0 && mousePressed) {
        coords.push(pointer)
    }
}

/*
get the current image data 
*/
function getImageData() {
    //get the minimum bounding box around the drawing 
    var img = canvas.toDataURL();
    $.ajax({
      type: "POST",
      url: "/predict/",
      data: img,
      success: function(data){
        data = data.replace(/\n/g, '<br>')
        $('#statusTemp').html(data);
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
      }
    });
}


/*
load the model
*/
async function start() {
     
    //allow drawing on the canvas 
    allowDrawing()
    
}

/*
allow drawing on canvas
*/
function allowDrawing() {

    $('button').prop('disabled', false);
    var slider = document.getElementById('myRange');
    slider.oninput = function() {
        canvas.freeDrawingBrush.width = this.value;
    };
}

/*
clear the canvs 
*/
function erase() {
    canvas.clear();
    canvas.backgroundColor = '#ffffff';
    coords = [];
}
