class Ciudad {

    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre; /* "Le Mans"; */
        this.pais = pais; /* "Francia"; */
        this.gentilicio = gentilicio; /* "Manceaux"; */
        this.poblacion; /* 146000; */
        this.coordenadas; /* { latitud: 48.007755, longitud: 0.199860 }; */
    }

    completarInfo() {
        this.poblacion = 146000;
        this.coordenadas = {
            latitud: 48.007755,
            longitud: 0.199860
        };
    }

    getNombre() {
        return this.nombre;
    }

    getPais() {
        return this.pais;
    }

    getInfoSecundaria() {
        return "<ul><li>Gentilicio: " + this.gentilicio + "</li><li>Población: " + this.poblacion + "</li></ul>";
    }

    getCoordenadas() {
        document.write("<p>Latitud: " + this.coordenadas.latitud + "</p>"); /* Marcado como "deprecated" */
        document.write("<p>Longitud: " + this.coordenadas.longitud + "</p>");
    }
}