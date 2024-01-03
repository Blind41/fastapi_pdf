from fastapi import FastAPI, HTTPException, Response
from fpdf import FPDF
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por tus orígenes permitidos si es posible
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/crear_pdf")
async def crear_pdf(servicios: dict):
    if not servicios:
        raise HTTPException(status_code=400, detail="No se han proporcionado servicios")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Factura de Servicios", ln=True, align="C")
    pdf.ln(10)

    # ... (resto del código para generar el PDF) ...
    # Encabezados de la tabla
    pdf.set_fill_color(200)
    pdf.cell(100, 10, txt="Servicio", border=1, fill=True)
    pdf.cell(50, 10, txt="Precio", border=1, fill=True)
    pdf.ln()

    total = 0

    # Agregar servicios al PDF y calcular el precio total
    for servicio, precio in servicios.items():
        pdf.cell(100, 10, txt=servicio, border=1)
        pdf.cell(50, 10, txt=str(precio), border=1)
        pdf.ln()
        total += precio

    # Mostrar el precio total al final
    pdf.cell(100, 10, txt="Total", border=1, fill=True)
    pdf.cell(50, 10, txt=str(total), border=1, fill=True)

    nombre_archivo = "factura_servicios.pdf"
    pdf.output(nombre_archivo)

    # Abrir el archivo PDF generado y enviarlo como respuesta
    with open(nombre_archivo, "rb") as file:
        content = file.read()

    response = Response(content, media_type="application/pdf")
    response.headers["Content-Disposition"] = f"attachment; filename={nombre_archivo}"

    return response