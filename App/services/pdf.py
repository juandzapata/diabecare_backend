from io import BytesIO
import os
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas


class PdfService:
    
    def __init__(self, db):
        self.pdf_repository = db
    
    def generate_pdf(self):
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer)
            
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawString(100, 670, "Diabacare")
            pdf.drawString(100, 650, "Reporte de Usuario")
            
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, 600, f"Nombre: {self.user_data.name + ' ' + self.user_data.last_name}")
            pdf.drawString(100, 580, f"Correo: {self.user_data.email}")
        
            grey_color = Color(128/255, 128/255, 128/255)
            pdf.setFont("Helvetica", 8)
            pdf.setFillColor(grey_color)
            pdf.drawString(500, 10, f"Realizado por DiabeCare")

            #(*)
            pdf.drawString(300, 150, "Julio Marquez")
            pdf.drawString(300, 140, "1002633638")
            pdf.drawString(300, 130, "Director general DiabeCare")

            image_logo = os.path.join("img", "logo_diabacare_blanco.png")

            # toma de imagenes, subirlas al contenedor y modificar su ruta.
            image_path_banner_inferior = os.path.join("img", "banner_inferior_izquierdo.png")
            image_path_banner_superior = os.path.join("img", "banner_superior_derecho.png")
            image_path_firma = os.path.join("img", "firma.png")

            # Modificar la ruta para el contenedor de Azure. Se puede agregar nuestras firmas y nombres en las partes
            # correspondientes (*) Alternando aleatoriamente entre documento y documento. Se podría crear un usuario 
            # especial en la base de datos que contenga otro rol y su id puede hacer referencia a la firma en el contenedor.
            # El resto del código es completamente dinámico y se puede utilizar para cualquier usuario.

            try:
                image = ImageReader(image_logo)
                pdf.drawImage(image, 35, 715, width=100, height=100)
                image = ImageReader(image_path_banner_inferior)
                pdf.drawImage(image, 0, 0, width=300, height=200)
                image = ImageReader(image_path_banner_superior)
                pdf.drawImage(image, 300, 645, width=300, height=200)
                image = ImageReader(image_path_firma)
                pdf.drawImage(image, 300, 180, width=200, height=100)
            except IOError:
                pdf.drawString(100, 630, "Image not available")

            pdf.showPage()
            pdf.save()

            buffer.seek(0)
            return buffer    
        