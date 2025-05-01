import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from pydantic import BaseModel, validator, ValidationError
from typing import Optional, List
from io import BytesIO
from weasyprint import HTML
import tempfile
from werkzeug.utils import secure_filename
import random
import string
import base64

# Initialize Flask application
app = Flask(__name__)

# Constants
PORT = 5000
DEBUG = True
LOGO_FILE = "extended logo plus.png"
WATERMARK_LOGO_FILE = "extended logo.png"  # Added watermark logo file

# Data models
class AutoSchool(BaseModel):
    name: str
    website: str
    phone: str
    email: str

class Student(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    cnp: Optional[str] = None

class File(BaseModel):
    scholarshipStartDate: str
    criminalRecordExpiryDate: str
    medicalRecordExpiryDate: str
    status: str

    @validator('scholarshipStartDate', 'criminalRecordExpiryDate', 'medicalRecordExpiryDate')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')

class TeachingCategory(BaseModel):
    type: str
    sessionCost: float
    sessionDuration: int
    scholarshipPrice: float
    minDrivingLessonsReq: int

class Vehicle(BaseModel):
    licensePlateNumber: str
    transmissionType: str
    color: str
    licenseType: str

class Instructor(BaseModel):
    fullName: str

class Payment(BaseModel):
    sessionsPayed: int
    scholarshipBasePayment: bool

class InvoiceData(BaseModel):
    autoSchool: AutoSchool
    student: Student
    file: File
    teachingCategory: TeachingCategory
    vehicle: Vehicle
    instructor: Instructor
    payment: Payment

def generate_invoice_html(data):
    """
    Generate an HTML invoice using Jinja2 template
    
    Args:
        data: Validated InvoiceData object
        
    Returns:
        str: HTML content of the invoice
    """
    # Current date and invoice number
    current_date = datetime.now()
    invoice_number = f"INV-{current_date.strftime('%Y%m%d')}-{data.student.lastName[:3]}{data.student.firstName[:3]}".upper()
    
    # Get absolute paths for logos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, 'static', 'logo', LOGO_FILE)
    watermark_logo_path = os.path.join(base_dir, 'static', 'logo', WATERMARK_LOGO_FILE)
    
    # Check if logo exists and prepare paths for template
    logo_exists = os.path.exists(logo_path)
    watermark_logo_exists = os.path.exists(watermark_logo_path)
    
    # Load logo files as base64 for embedding
    logo_b64 = None
    if logo_exists:
        with open(logo_path, "rb") as img_file:
            logo_b64 = f"data:image/png;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    
    watermark_b64 = None
    if watermark_logo_exists:
        with open(watermark_logo_path, "rb") as img_file:
            watermark_b64 = f"data:image/png;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    
    # Calculate invoice items
    invoice_items = []
    total = 0
    
    # Add scholarship if paid
    if data.payment.scholarshipBasePayment:
        invoice_items.append({
            'number': 1,
            'description': f"Școlarizare pentru categoria {data.teachingCategory.type}",
            'quantity': 1,
            'unit_price': f"{data.teachingCategory.scholarshipPrice:.2f} RON",
            'total_price': f"{data.teachingCategory.scholarshipPrice:.2f} RON"
        })
        total += data.teachingCategory.scholarshipPrice
    
    # Add driving sessions if any
    if data.payment.sessionsPayed > 0:
        item_number = 2 if data.payment.scholarshipBasePayment else 1
        session_total = data.payment.sessionsPayed * data.teachingCategory.sessionCost
        
        invoice_items.append({
            'number': item_number,
            'description': f"Ședințe de conducere ({data.teachingCategory.sessionDuration} min)",
            'quantity': data.payment.sessionsPayed,
            'unit_price': f"{data.teachingCategory.sessionCost:.2f} RON",
            'total_price': f"{session_total:.2f} RON"
        })
        total += session_total
    
    # Prepare data for the template
    template_data = {
        'invoice_number': invoice_number,
        'issue_date': current_date.strftime("%d.%m.%Y"),
        'logo_path': logo_b64,
        'logo_exists': logo_exists,
        'watermark_logo_path': watermark_b64,
        'auto_school': data.autoSchool,
        'student': data.student,
        'invoice_items': invoice_items,
        'total': f"{total:.2f} RON",
        'file': data.file,
        'vehicle': data.vehicle,
        'instructor': data.instructor,
        'teaching_category': data.teachingCategory
    }
    
    # Render the template
    html_content = render_template('invoice_template.html', **template_data)
    
    return html_content

def generate_invoice_pdf_from_html(html_content):
    """
    Convert HTML to PDF using WeasyPrint
    
    Args:
        html_content: HTML string to convert
        
    Returns:
        BytesIO: PDF document as a file-like object
    """
    # Create a BytesIO buffer for the PDF
    pdf_buffer = BytesIO()
    
    # Get the base directory for resolving relative URLs
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate PDF directly with WeasyPrint to avoid filesystem usage
    # Set base_url to help with relative URLs in CSS
    HTML(string=html_content, base_url=base_dir).write_pdf(pdf_buffer)
    
    # Return the buffer positioned at the beginning for reading
    pdf_buffer.seek(0)
    return pdf_buffer

@app.route('/')
def index():
    return jsonify({
        "message": "DF-Accountant API",
        "version": "1.0",
        "endpoints": {
            "/api/v1/getInvoice": "Generate PDF invoice (POST)",
            "/preview": "Preview invoice as HTML (POST)"
        }
    })

@app.route('/api/v1/getInvoice', methods=['POST'])
def get_invoice():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate the data
        invoice_data = InvoiceData(**data)

        # Generate invoice HTML
        html_content = generate_invoice_html(invoice_data)
        
        # Convert HTML to PDF
        invoice_stream = generate_invoice_pdf_from_html(html_content)
        
        # Generate random filename
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        filename = f"invoice_{invoice_data.student.lastName}_{invoice_data.student.firstName}_{datetime.now().strftime('%Y%m%d')}_{random_str}.pdf"
        
        # Return the PDF
        return send_file(
            invoice_stream,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=secure_filename(filename)
        )
        
    except ValidationError as e:
        return jsonify({"error": "Data validation failed", "details": json.loads(e.json())}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview_invoice():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate the data
        invoice_data = InvoiceData(**data)

        # Generate invoice HTML
        html_content = generate_invoice_html(invoice_data)
        
        # Return HTML for preview
        return html_content
        
    except ValidationError as e:
        return jsonify({"error": "Data validation failed", "details": json.loads(e.json())}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG) 