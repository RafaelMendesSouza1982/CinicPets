# Petshop Management System

## Overview
This is a web-based management system for veterinary clinics and petshops. It includes features for managing clients, animals, veterinarians, appointments, and clinical records.

## Features
- User authentication with JWT
- Role-based access control (Admin, Veterinarian, Reception)
- Client, animal, and veterinarian management
- Appointment scheduling with conflict checks
- Clinical attendance and medication tracking
- Public agenda view for daily appointments
- Secure and scalable architecture

## Technologies Used
- **Backend**: FastAPI, Python 3.11
- **Frontend**: HTML5, CSS3, Bootstrap, Jinja2
- **Database**: PostgreSQL
- **Infrastructure**: Docker, Docker Compose, Nginx

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd CinicPets
   ```
3. Start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Access the application:
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - Frontend: [http://localhost:8080](http://localhost:8080)

## Future Enhancements
- Online appointment booking for clients
- Notifications via WhatsApp and email
- Advanced electronic medical records
- Financial and billing management

## Security Measures
- Passwords are hashed using bcrypt
- JWT tokens with expiration
- CORS enabled for specific origins
- Protection against SQL Injection through parameterized queries