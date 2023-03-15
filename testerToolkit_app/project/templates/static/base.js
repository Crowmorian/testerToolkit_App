const togglebutton = document.getElementByClassName("toggle-button")
const navbarLinks = document.getElementByClassName("navbar-links")

togglebutton.addEventListener("click", () => {
    navbarLinks.classList("active")
})