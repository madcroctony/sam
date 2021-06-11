// フレームをreloadする方法
function doReloadTheFrame() {

    // フレームのDOM要素を取得
    var iframe = document.getElementById('paste_window');

    // フレームをreload
    iframe.contentWindow.location.reload(true);

}
window.addEventListener('load', function () {

    // 2.5秒ごとに、フレームをreload
    setInterval(doReloadTheFrame, 2500);

});