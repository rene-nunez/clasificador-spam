import {getModelos, clasificar} from "./api.js";
import view from "./view.js";

const delay = ms => new Promise(r => setTimeout(r, ms));

// Controlador: eventos del formulario, teclado y responsive

const controller = {
    _input: document.getElementById("input"),
    _form: document.getElementById("form"),
    _history: [],
    _historyIndex: -1,

    _autoResize() {
        this._input.style.height = "auto";
        this._input.style.height = this._input.scrollHeight + "px";
    },

    // Inicializa la aplicación
    async init() {
        this._input.focus(); // Cursor en el input al cargar

        // Cargar lista de modelos
        view.mostrarCargandoModelos();
        try {
            const modelos = await getModelos();
            view.llenarModelos(modelos);
            view.mostrarPlaceholder();
        } catch {
            view.mostrarError("No se pudo conectar con el servidor");
        }

        // Auto-ajuste del textarea
        this._input.addEventListener("input", () => this._autoResize());

        // Envío del formulario
        this._form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const mensaje = this._input.value.trim();
            if (!mensaje) return;

            if (this._history[this._history.length - 1] !== mensaje) {
                this._history.push(mensaje);
            }
            this._historyIndex = this._history.length;

            const modelo = view.getModelo();
            this._input.value = "";
            this._input.style.height = "auto";

            view.mostrarProcesando();
            view.setCargando(true);
            await delay(200);

            try {
                const resultado = await clasificar(mensaje, modelo);
                view.mostrarResultado(mensaje, resultado);
            } catch (err) {
                view.mostrarError(err.message);
            } finally {
                view.setCargando(false);
                this._input.focus();
            }
        });

        // Atajos del teclado

        // Escape cierra menú sin importar el foco
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                event.preventDefault();
                const inputFocused = document.activeElement === this._input;
                view.cerrarMenu();
                this._input.focus();

                if (inputFocused) {
                    this._input.value = "";
                    this._input.style.height = "auto";
                }
            }
        });

        this._input.addEventListener("keydown", (event) => {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                this._form.requestSubmit();
                return;
            }

            if (event.key === "ArrowUp" && this._history.length) {
                event.preventDefault();
                const idx = Math.max(0, this._historyIndex - 1);
                if (idx !== this._historyIndex) {
                    this._historyIndex = idx;
                    this._input.value = this._history[this._historyIndex];
                    this._autoResize();
                }
                return;
            }

            if (event.key === "ArrowDown") {
                const next = this._historyIndex + 1;
                if (next < this._history.length) {
                    event.preventDefault();
                    this._historyIndex = next;
                    this._input.value = this._history[this._historyIndex];
                } else {
                    event.preventDefault();
                    this._historyIndex = this._history.length;
                    this._input.value = "";
                }
                this._autoResize();
            }
        });
    }
};

export default controller;