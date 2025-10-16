import xml.etree.ElementTree as ET

# Lee el XML y devuelve una lista de tuplas para coordenada: [(lat1, lon1, alt1), (lat2, lon2, alt2), ...]
def parse_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
    except Exception as e:
        print(f"Error al leer '{xml_file}': {e}")
        return []

    root = tree.getroot()
    ns = {'ns': 'http://www.uniovi.es'}
    coords_circuito = []

    # Coordenadas de inicio
    coord_inic = root.find("ns:coordenadas_inicio/ns:coordenada", namespaces=ns)
    if coord_inic is not None:
        coords_circuito.append({
            "lat": float(coord_inic.find("ns:latitud", namespaces=ns).text),
            "lon": float(coord_inic.find("ns:longitud", namespaces=ns).text),
            "alt": float(coord_inic.find("ns:altitud", namespaces=ns).text)
        })

    # Coordenadas de cada tramo
    for tramo in root.findall("ns:tramos/ns:tramo", namespaces=ns):
        coord_tramo = tramo.find("ns:coordenada", namespaces=ns)
        if coord_tramo is not None:
            coords_circuito.append({
                "lat": float(coord_tramo.find("ns:latitud", namespaces=ns).text),
                "lon": float(coord_tramo.find("ns:longitud", namespaces=ns).text),
                "alt": float(coord_tramo.find("ns:altitud", namespaces=ns).text),
            })
        
    return coords_circuito

# Genera el contenido SVG para el circuito
def crear_contenido_svg(coords_circuito, width=800, height=400, margin=50):
    
    altitudes = [p['alt'] for p in coords_circuito]
    min_alt, max_alt = min(altitudes), max(altitudes)
    rango_alt = max_alt - min_alt

    # Salto horizontal entre cada punto
    step_x = (width - 2 * margin) / (len(coords_circuito) - 1)

    # Cálculo de la posición vertical (altitud) en escalado
    if rango_alt == 0:
        y0 = height - margin
    else:
        escala = (0 - min_alt) / rango_alt
        y = height - 2 * margin
        y0 = (height - margin) - escala * y

    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'  <rect x="0" y="0" width="{width}" height="{height}" fill="white" stroke="black" stroke-width="3" />'
    ]

    # Inicio en (margin, height) => Esquina inferior izquierda + márgenes
    points = []

    for i, p in enumerate(coords_circuito):
        x = margin + i * step_x

        if rango_alt == 0:
            y = height - margin
        else:
            escala = (p['alt'] - min_alt) / rango_alt
            y = height - 2 * margin
            y0 = (height - margin) - escala * y

        points.append(f"{x:.2f},{y0:.2f}")

    # Punto final de la base y cierre de perfil
    base_y = height - 10
    pts = [f"{margin},{base_y}"] + points + [f"{width-margin},{base_y}", f"{margin},{base_y}"]
    pts_str = " ".join(pts)
    svg_lines.append(
        f'  <polyline points="{pts_str}" '
        'style="fill:pink;stroke:red;stroke-width:2" />'
    )

    # Marcadores de los puntos tomados para definir los tramos
    for i, p in enumerate(coords_circuito):
        x = margin + i*step_x

        if rango_alt == 0:
            y = height - margin
        else:
            escala = (p['alt'] - min_alt) / rango_alt
            y = (height - margin) - escala * (height - 2 * margin)
        svg_lines.append(
            f'  <circle cx="{x:.2f}" cy="{y:.2f}" r="2" '
            'fill="red" stroke="black" stroke-width="1" />'
        )

    svg_lines.append('</svg>')

    return svg_lines

# Guarda el contenido SVG en un archivo
def save_svg(svg_content, svg_file):
    try:
        with open(svg_file, 'w', encoding='utf-8') as f:
            for line in svg_content:
                f.write(line)
    except IOError as e:
        print(f"Error al guardar '{svg_file}': {e}")

# Función principal que orquesta el proceso de conversión de XML a SVG
def main():
    xml_file = "circuitoEsquema.xml"
    coordinates = parse_xml(xml_file)
    if not coordinates:
        print("No se ha podido extraer el circuito del archivo.")
        return

    svg = crear_contenido_svg(coordinates)
    save_svg(svg, "altimetria.svg")
    print(f"Conversión completada con éxito: altimetria.svg creado.")

if __name__ == "__main__":
    main()
