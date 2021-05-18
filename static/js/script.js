function show_loading(theForm) {
    const
        search_button = document.querySelector('#search_button'),
        loader_window = document.querySelector('.loader_js'),
        overlay = document.querySelector('.overlay_js')

    search_button.addEventListener('click', () => {
        loader_window.style.display = 'flex'
        overlay.style.display = 'block'
    })

    return false
}

if (window.location.href == 'http://127.0.0.1:8880/' || window.location.href == 'http://localhost:8880/')
    document.addEventListener('DOMContentLoaded', show_loading)