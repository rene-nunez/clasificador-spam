import "./css/style.css";
import view from "./view.js";
import controller from "./controller.js";

// Elementos de la interfaz
const checkbox = document.getElementById("theme-checkbox");
const html = document.documentElement;

// localStorage del tema (DaisyUI)
function setTheme(theme) {
    html.setAttribute("data-theme", theme);
    checkbox.checked = theme === "dim";
    localStorage.setItem("theme", theme);
};

checkbox.addEventListener("change", () => {
    setTheme(checkbox.checked ? "dim" : "nord");
});

const saved = localStorage.getItem("theme");

if (saved) {
    setTheme(saved);
} else {
    setTheme(window.matchMedia("(prefers-color-scheme: dark)").matches ? "dim" : "nord");
}

view.init(); // Menú desplegable de modelos
controller.init(); // Formulario, teclado, autoResize, mobile keyboard