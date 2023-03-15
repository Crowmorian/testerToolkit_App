const togglebutton = document.getElementByClassName("toggle-button")[0]
const navbaLinks = document.getElementByClassName("navbar-links")[0]

togglebutton.addEventListener("click", () => {
    navbarLinks.classList("active")
})