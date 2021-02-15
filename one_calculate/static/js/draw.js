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
var name;

/*
prepare the drawing canvas 
*/
$(function() {
    canvas = window._canvas = new fabric.Canvas('canvas');

    canvas.backgroundColor = '#ffffff';
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.color = "black";
    canvas.freeDrawingBrush.width = 25;
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
    erase();
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
      url: "/pred/" + name,
      data: img,
      success: function(data){
        $('#statusTemp').text(name + ' ' + data);
      }
    });
}

function getMaxIndex(arr) {
    var max = arr[0];
    var index = 0;
    for (var i = 0; i < arr.length; i++) {
        if (max < arr[i]) {
            max = arr[i];
            index = i;
        }
    }
    return index;
}

/*
load the model
*/
async function start(na, rkl) {
    name = na
    users = ['xiaoli','boshi','dage','haoliu']
    let i = getMaxIndex(rkl)
    $('#first').text(users[i] + ' ' + rkl[i])
    rkl[i] = -1
    
    i = getMaxIndex(rkl)
    $('#second').text(users[i] + ' ' + rkl[i])
    rkl[i] = -1
    
    i = getMaxIndex(rkl)
    $('#third').text(users[i] + ' ' + rkl[i])
    rkl[i] = -1
    
    i = getMaxIndex(rkl)
    $('#fourth').text(users[i] + ' ' + rkl[i])
    rkl[i] = -1
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
    document.getElementById('status').innerHTML = 'Model Loaded';
}

/*
clear the canvs 
*/
function erase() {
    canvas.clear();
    canvas.backgroundColor = '#ffffff';
    coords = [];
}
