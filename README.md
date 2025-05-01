<p align="center">
  <img src="static/logo/extended logo plus.png" alt="DriveFlow Logo" width="400">
</p>

# DriveFlow Accountant API

DriveFlow Accountant is a microservice built for driving schools to generate professional invoices for their students. This API service can generate and serve both HTML previews and PDF invoice documents.

## Features

- Generate PDF invoices with detailed student, instructor, and vehicle information
- Preview HTML version of the invoice before generation
- Beautifully styled invoices with responsive layout
- Romanian date formatting (DD Month YYYY) for better readability
- Docker support for easy deployment
- Heroku-ready configuration

## API Documentation

### Endpoints

#### 1. Get Invoice (PDF)

Generates and returns a PDF invoice document.

- **URL:** `/api/v1/getInvoice`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Response:** PDF file (application/pdf)

#### 2. Preview Invoice (HTML)

Generates and returns an HTML preview of the invoice.

- **URL:** `/preview`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Response:** HTML content

### Request Data Format

Both endpoints accept the same JSON data format:

```json
{
  "autoSchool": {
    "name": "Auto School Name",
    "website": "www.example.com",
    "phone": "+40 123 456 789",
    "email": "contact@example.com"
  },
  "student": {
    "firstName": "First",
    "lastName": "Last",
    "email": "student@example.com",
    "phone": "+40 712 345 678",
    "cnp": "1990123456789"  // Optional
  },
  "file": {
    "scholarshipStartDate": "2023-05-01",  // Format: YYYY-MM-DD (will be displayed as "01 Mai 2023")
    "criminalRecordExpiryDate": "2023-12-31",  // Format: YYYY-MM-DD (will be displayed as "31 Decembrie 2023")
    "medicalRecordExpiryDate": "2023-12-31",  // Format: YYYY-MM-DD (will be displayed as "31 Decembrie 2023")
    "status": "Activ"
  },
  "teachingCategory": {
    "type": "B",
    "sessionCost": 150.0,
    "sessionDuration": 60,
    "scholarshipPrice": 2000.0,
    "minDrivingLessonsReq": 30
  },
  "vehicle": {
    "licensePlateNumber": "B 123 ABC",
    "transmissionType": "Manual",
    "color": "White",
    "licenseType": "B"
  },
  "instructor": {
    "fullName": "Instructor Name"
  },
  "payment": {
    "sessionsPayed": 10,
    "scholarshipBasePayment": true
  }
}
```

## Date Formatting

All dates in the generated invoice are automatically formatted in Romanian style:
- Input format: YYYY-MM-DD (ISO standard)
- Display format: DD Month YYYY (e.g., "01 Mai 2023")
- Month names are in Romanian language

This formatting applies to:
- Issue Date
- Medical Record Expiry Date
- Criminal Record Expiry Date
- Scholarship Start Date

## Setup and Deployment

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/DF-Accountant.git
   cd DF-Accountant
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

### Docker Deployment

1. Build and run using Docker Compose:
   ```bash
   ./docker_run.sh
   ```

   Or manually:
   ```bash
   docker-compose up --build -d
   ```

2. Access the API at: http://localhost:5000

### Heroku Deployment with Docker

1. Install the Heroku CLI and log in:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set the stack to container:
   ```bash
   heroku stack:set container
   ```

4. Push to Heroku:
   ```bash
   git push heroku main
   ```

## Project Structure

- `app.py` - Main application code
- `wsgi.py` - WSGI entry point for production servers
- `templates/` - HTML templates and CSS files
  - `invoice_template.html` - The invoice HTML template
  - `invoice.css` - CSS styles for the invoice
- `static/` - Static assets (logos, fonts)
- `Dockerfile` - Docker container configuration
- `docker-compose.yml` - Docker Compose service definition
- `heroku.yml` - Heroku Docker deployment configuration
- `requirements.txt` - Python dependencies
- `test_data.json` - Example data for testing the API

## Dependencies

- Flask - Web framework
- WeasyPrint - HTML to PDF conversion
- Pydantic - Data validation
- Gunicorn - WSGI HTTP Server for production

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or support, please contact the DriveFlow development team.

