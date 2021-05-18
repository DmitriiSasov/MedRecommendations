function show_loading() {
    const
        loader_window = document.querySelector('.loader_js'),
        overlay = document.querySelector('.overlay_js')

    loader_window.style.display = 'flex'
    overlay.style.display = 'block'

    console.log('show')

    return false
}

function hide_loading() {
    const
        loader_window = document.querySelector('.loader_js'),
        overlay = document.querySelector('.overlay_js')

    if (loader_window != null && overlay != null) {
        loader_window.style.display = 'none'
        overlay.style.display = 'none'
    }

    console.log('close')

    return false
}

document.addEventListener('DOMContentLoaded', hide_loading)