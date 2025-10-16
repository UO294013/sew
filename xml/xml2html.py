import xml.etree.ElementTree as ET

# Comienza el archivo HTML con la cabecera y el estilo de línea
def prologoHTML(outFile):
    outFile.write('<!DOCTYPE html>\n')
    outFile.write('<html lang="es">\n')
    outFile.write('<head>\n')
    outFile.write('  <meta charset="UTF-8">\n')
    outFile.write('  <meta name="author" content="Vicente Megido García (UO294013)" />\n')
    outFile.write('  <meta name="description" content="Menú con información relativa al circuito de Le Mans para la web MotoGP - Desktop, totalmente extraída del fichero circuitoEsquema.xml" />\n')
    outFile.write('  <meta name="keywords" content="MotoGP, motos, carreras, Francia, circuito, Le Mans, motociclismo" />\n')
    outFile.write('  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    outFile.write('  <title>MotoGp - Circuito de Le Mans</title>\n')
    outFile.write('  <link rel="stylesheet" type="text/css" href="estilo/estilo.css">\n')
    outFile.write('  <link rel="stylesheet" type="text/css" href="estilo/layout.css">\n')
    outFile.write('</head>\n')
    outFile.write('<body>\n')

# Cierra el documento HTML
def epilogoHTML(outFile):
    outFile.write('</body>\n')
    outFile.write('</html>\n')

# Escribe en el HTML la información del circuito
def escribeLinea(outFile, nombre, coords):
    outFile.write("    <Placemark>\n")
    outFile.write(f"      <name>{nombre}</name>\n")
    outFile.write("      <styleUrl>#lineaRoja</styleUrl>\n")
    outFile.write("      <LineString>\n")
    outFile.write("        <extrude>1</extrude>\n")
    outFile.write("        <tessellate>1</tessellate>\n")
    outFile.write("        <coordinates>\n")
    for lon, lat in coords:
        outFile.write(f"          {lon},{lat}\n")
    outFile.write("        </coordinates>\n")
    outFile.write("      </LineString>\n")
    outFile.write("    </Placemark>\n\n")

# Función principal que procesa el archivo XML y genera el archivo HTML
def main():
    try:
        tree = ET.parse("circuitoEsquema.xml")
    except Exception as e:
        print("No se puede abrir 'circuitoEsquema.xml':", e)
        return

    ns = {'ns': 'http://www.uniovi.es'}
    root = tree.getroot() # Raíz del XML, <circuito>

    nombre = root.get("nombre")
    html_filename = "InfoCircuito.html"

    with open(html_filename, "w", encoding="utf-8") as outFile:
        prologoHTML(outFile)


        epilogoHTML(outFile)

    print(f"HTML generado: {html_filename}")

if __name__ == "__main__":
    main()
