from datetime import date
from io import BytesIO
import os
import textwrap
from utils.constants.default_values import RUTA_IMAGENES
from data.repositories.patient_repository import PatientRepository
from schemas.patient import PatientDataReport
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas


class PdfService:
    
    def generate_pdf(self, patient_data: PatientDataReport):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        fecha_generacion = date.today().strftime("%Y-%m-%d")
        pdf.setTitle(f"Reporte de Paciente - {patient_data.full_name}")
        
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(100, 670, "Diabecare")
        pdf.drawString(100, 650, "Reporte de Paciente")
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, 630, f"Fecha de generación: {fecha_generacion}")
        pdf.drawString(100, 580, "Información del paciente")
        
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 560, f"Nombre: {patient_data.full_name}")
        pdf.drawString(100, 540, f"Correo: {patient_data.email}")
        pdf.drawString(380, 560, f"Género: {patient_data.gender}")
        pdf.drawString(380, 540, f"Edad: {patient_data.age}")
        
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, 490, "Estadísticas de salud")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 470, f"Nivel promedio de glucosa: {patient_data.average_glucose_level} mg/dL")
        pdf.drawString(100, 450, f"Horas promedio de actividad física: {patient_data.average_physical_activity_hours} horas")
        pdf.drawString(100, 430, f"Medicamento más consumido: {patient_data.most_consumed_medication}")
        pdf.drawString(100, 410, f"Comida más consumida: {patient_data.most_consumed_food}")
        
        text = "Este reporte ha sido generado con el objetivo de proporcionar un análisis detallado de la salud del paciente. La información contenida en este documento es confidencial y está destinada exclusivamente para uso del paciente y del profesional de salud asignado."
        x = 100
        y = 360
        width = 450
        
        lines = text.split("\n")
        for line in lines:
            words = line.split(" ")
            current_line = ""
            for word in words:
                if pdf.stringWidth(current_line + word, "Helvetica", 12) < width:
                    current_line += word + " "
                else:
                    pdf.drawString(x, y, current_line)
                    y -= 20  # Espacio entre líneas
                    current_line = word + " "
            pdf.drawString(x, y, current_line)
            y -= 20  # Espacio entre líneas
            
        pdf.setFont("Helvetica-BoldOblique", 10)
        
        text = "**Los datos aquí contenidos son propiedad confidencial de la empresa y están protegidos por las leyes de privacidad aplicables. Se prohíbe su divulgación o uso no autorizado."
        x = 100
        y = 260
        width = 450
        
        lines = text.split("\n")
        for line in lines:
            words = line.split(" ")
            current_line = ""
            for word in words:
                if pdf.stringWidth(current_line + word, "Helvetica", 10) < width:
                    current_line += word + " "
                else:
                    pdf.drawString(x, y, current_line)
                    y -= 20
                    current_line = word + " "
            pdf.drawString(x, y, current_line)
            y -= 20
    
        grey_color = Color(128/255, 128/255, 128/255)
        pdf.setFont("Helvetica", 8)
        pdf.setFillColor(grey_color)
        pdf.drawString(440, 10, " Realizado por DiabeCare Platform")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(435, 115, "(606) 8701096")
        pdf.drawString(435, 80, "contact@diabecare.com")
        pdf.drawString(435, 45, "www.diabecare.com")

        image_logo = os.path.join(RUTA_IMAGENES, "logo_diabacare_blanco.png")

        image_path_banner_inferior = os.path.join(RUTA_IMAGENES, "banner_inferior_izquierdo.png")
        image_path_banner_superior = os.path.join(RUTA_IMAGENES, "banner_superior_derecho.png")
        image_path_firma = os.path.join(RUTA_IMAGENES, "firma.png")
        image_path_icons = os.path.join(RUTA_IMAGENES, "contac_icons.png")

        try:
            image = ImageReader(image_logo)
            pdf.drawImage(image, 35, 715, width=100, height=100)
            image = ImageReader(image_path_banner_inferior)
            pdf.drawImage(image, 0, 0, width=300, height=200)
            image = ImageReader(image_path_banner_superior)
            pdf.drawImage(image, 300, 645, width=300, height=200)
            image = ImageReader(image_path_firma)
            pdf.drawImage(image, 100, 150, width=100, height=50)
            image = ImageReader(image_path_icons)
            pdf.drawImage(image, 400, 20, width=30, height=120)
        except IOError:
            pdf.drawString(100, 630, "Image not available")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(120, 135, "Julio Márquez L.")
        pdf.drawString(120, 120, "Director general")

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        return buffer
        