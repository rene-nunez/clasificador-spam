import {getModelos, clasificar} from "./api.js";
import view from "./view.js";

const delay = ms => new Promise(r => setTimeout(r, ms));

// Controlador: eventos del formulario, teclado y responsive

const controller = {
    _input: document.getElementById("input"), // Textarea del mensaje
    _form: document.getElementById("form"), // Formulario

    // Ajusta altura del textarea al contenido
    _autoResize() {
        this._input.style.height = "auto";
        this._input.style.height = this._input.scrollHeight + "px";
    },

    // Inicializa la aplicación
    async init() {
        this._input.focus(); // Cursor en el input al cargar

        // Cargar lista de modelos
        try {
            const modelos = await getModelos();
            view.llenarModelos(modelos);
        } catch {
            view.mostrarError("No se pudo conectar con el servidor");
        }

        // Auto-ajuste del textarea
        this._input.addEventListener("input", () => this._autoResize());

        // Ajuste para teclado móvil
        if (window.visualViewport) {
            const fixHeight = () => {
                document.body.style.minHeight = visualViewport.height + "px";
                window.scrollTo(0, 0);
            };
            window.visualViewport.addEventListener("resize", fixHeight);
            fixHeight();
        }

        // Envío del formulario
        this._form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const mensaje = this._input.value.trim();
            if (!mensaje) return;

            const modelo = view.getModelo();
            this._input.value = "";
            this._input.style.height = "auto";

            view.mostrarProcesando();
            view.setCargando(true);
            await delay(500);

            try {
                const resultado = await clasificar(mensaje, modelo);
                view.mostrarResultado(mensaje, resultado);
                getModelos().then(modelos => view.llenarModelos(modelos)).catch(() => {});
            } catch (err) {
                view.mostrarError(err.message);
            } finally {
                view.setCargando(false);
                this._input.focus();
            }
        });

        // Atajos de teclado
        this._input.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                this._input.value = "";
                this._input.style.height = "auto";
            } else if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                this._form.requestSubmit();
            }
        });
    }
};

export default controller;
