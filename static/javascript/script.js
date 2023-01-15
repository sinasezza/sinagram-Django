function remove()
{
    let elem = document.getElementById('messages') || null
    if (elem != null){
        elem.remove()
    } 
}

// -----------------------------------------
function showOriginal(img){
    $('#mask').css('display','block');
    var orig = document.createElement('img')
    orig.src = img.src
    orig.style.width = "680px"
    orig.style.height = "500px"
    orig.style.position = "absolute"
    orig.style.zIndex = "9999"
    var w = window.innerWidth
    var h = window.innerHeight
    
    orig.style.left = (w-650)/2 + 'px';
    orig.style.top = (h-500)/2  + 'px';

    orig.id = "original"
    document.body.appendChild(orig)
}
// --------------------------
function hideImg(){
    document.body.removeChild(document.getElementById('original'))
    document.getElementById('mask').style.display = "none"
}
