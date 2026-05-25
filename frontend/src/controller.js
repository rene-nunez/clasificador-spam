import {getModelos, clasificar} from "./api.js";
import view from "./view.js";

const delay = ms => new Promise(r => setTimeout(r, ms));

const controller = {
    _input: document.getElementById("input"),
    _form: document.getElementById("form"),
    _history: [], // Historial de mensajes enviados
    _historyIndex: -1, // -1 = input vacío; 0..n = posición en el historial

    // Resetear a "auto" antes de medir scrollHeight es necesario para que se encoja al borrar texto
    _autoResize() {
        this._input.style.height = "auto";
        this._input.style.height = this._input.scrollHeight + "px";
    },

    async init() {
        this._input.focus();

        view.mostrarCargandoModelos();
        try {
            const modelos = await getModelos();
            view.llenarModelos(modelos);
            view.mostrarPlaceholder();
        } catch {
            view.mostrarError("No se pudo conectar con el servidor");
        }

        this._input.addEventListener("input", () => this._autoResize());

        this._form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const mensaje = this._input.value.trim();
            if (!mensaje) return;

            // Evita duplicados consecutivos en el historial
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

        document.addEventListener("keydown", (event) => {
            // Escape: cierra menú; si el input está enfocado además borra el mensaje
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
            // Enter sin Shift envía el formulario
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                this._form.requestSubmit();
                return;
            }

            // Flecha arriba: navega hacia atrás en el historial
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

            // Flecha abajo: navega hacia adelante
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