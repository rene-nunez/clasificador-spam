import {getModelos} from "./api.js";

const view = {
    _modeloActual: "Regresión Logística", // Modelo ML seleccionado actualmente
    _errorTimeout: null,

    // Elementos de la interfaz
    _display: document.getElementById("display"), // Contenedor principal
    _menu: document.getElementById("modelo-menu"), // Menú desplegable de selección de modelos
    _label: document.getElementById("modelo-label"), // Etiqueta que muestra el modelo activo

    // Métodos

    // Alterna clases CSS del botón del menú de modelos
    _btnClass(active) {
        const base = "w-full text-left px-4 py-2.5 text-sm transition-colors first:rounded-t-xl last:rounded-b-xl flex items-center justify-between";
        return active ? `${base} text-base-content font-medium` : `${base} text-base-content/50 hover:text-base-content/70 hover:bg-base-200/50`;
    },

    // Prevenir inyección XSS en innerHTML
    _escapar(string) {
        const div = document.createElement("div");
        div.textContent = string;
        return div.innerHTML;
    },

    // Devuelve el nombre del modelo ML seleccionado
    getModelo() {
        return this._modeloActual;
    },

    // Puebla el menú desplegable con la lista de modelos disponibles
    llenarModelos(modelos) {
        if (!modelos.length) return;

        // Actualizar UI y atributos
        this._modeloActual = modelos.includes(this._modeloActual) ? this._modeloActual : modelos[0];
        this._label.textContent = this._modeloActual;

        this._menu.innerHTML = modelos.map(modelo => {
            const active = modelo === this._modeloActual; // Bool
            return `<button class="${this._btnClass(active)}" data-value="${modelo}"><span>${modelo}</span>${active ? '<span class="text-[10px] opacity-40">●</span>' : ''}</button>`;
        }).join("");

        this._menu.querySelectorAll("button").forEach(btn => {
            btn.addEventListener("click", () => {
                this._modeloActual = btn.dataset.value;
                this._label.textContent = this._modeloActual;
                this._menu.classList.add("hidden");

                this._menu.querySelectorAll("button").forEach(btn => {
                    const active = btn.dataset.value === this._modeloActual;
                    btn.className = this._btnClass(active);
                    btn.innerHTML = `<span>${btn.dataset.value}</span>${active ? '<span class="text-[10px] opacity-40">●</span>' : ""}`;
                });
            });
        });
    },

    /**
     * Muestra el estado "Procesando..." en el display central.
     * Limpia cualquier error pendiente antes de renderizar.
     */

    // Muestra el placeholder "Procesando con {modelo}..." en el display central
    mostrarProcesando() {
        if (this._errorTimeout) clearTimeout(this._errorTimeout); // Evitar sobrescribir mensaje antes de tiempo
        this._display.innerHTML = `<div class="flex-1 flex items-center justify-center text-base-content/50 text-lg sm:text-xl text-center px-2">Procesando con ${this._modeloActual}...</div>`;
    },

    // Renderizar y mostrar el resultado
    mostrarResultado(mensaje, resultado) {
        if (this._errorTimeout) clearTimeout(this._errorTimeout);

        const esSpam = resultado.etiqueta === "spam"; // Bool
        const color = esSpam ? "text-red-500" : "text-green-600";
        
        this._display.innerHTML = `
        <div class="flex-1 flex flex-col items-center justify-center anim-result max-w-md mx-auto text-center">
            <div class="${color} text-4xl font-black tracking-tight">${resultado.etiqueta.toUpperCase()}</div>
            <div class="mt-5 space-y-2">
                <div class="text-base text-base-content/60">Confianza: ${resultado.confianza}%</div>
                <div class="text-base text-base-content/60">"${this._escapar(mensaje)}"</div>
            </div>
        </div>`;
    },

    // Mostrar mensaje de error por 5 segundos
    mostrarError(texto) {
        if (this._errorTimeout) clearTimeout(this._errorTimeout);
        
        this._display.innerHTML = `
            <div class="flex-1 flex items-center justify-center">
                <span class="text-base-content/50 text-xl anim-result">${this._escapar(texto)}</span>
            </div>`;
            
        this._errorTimeout = setTimeout(() => {
            this._display.innerHTML = "";
            this._errorTimeout = null;
        }, 5000);
    },

    // Habilita o no los controles de entrada durante una petición
    setCargando(activo) {
        document.getElementById("btn").disabled = activo;
        document.getElementById("input").disabled = activo;
    },

    // Inicializa la aplicación, define event listeners del menú desplegable y hace una petición GET de los modelos
    init() {
        document.getElementById("modelo-btn").addEventListener("click", (event) => {
            event.stopPropagation();
            
            if (this._menu.children.length === 0) {
                getModelos().then(modelos => {
                    if (!modelos.length) return;
                    this.llenarModelos(modelos);
                    this._menu.classList.remove("hidden");
                }).catch(() => { });
            }

            this._menu.classList.toggle("hidden");
        });

        document.addEventListener("click", () => this._menu.classList.add("hidden"));
        this._menu.addEventListener("click", (event) => event.stopPropagation());
    }
};

export default view;