function doReloadTheFrame()
{
    var frame = document.getElementById('paste_window');
    frame.contentWindow.location.reload(true);
}

window.addEventListener('load', function ()
{
    setInterval(doReloadTheFrame, 2500);
});