// Capa de comunicación HTTP con el backend

async function fetchJSON(url, opts) {
    let res;
    
    try {
        res = await fetch(url, opts);
    } catch {
        throw new Error("No se pudo conectar con el servidor");
    }

    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || "No se pudo conectar con el servidor");
    }
    
    return res.json();
}

export function getModelos() {
    return fetchJSON("/api/modelos");
}

export function clasificar(mensaje, modelo) {
    return fetchJSON("/api/clasificar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({mensaje, modelo}),
    });
}