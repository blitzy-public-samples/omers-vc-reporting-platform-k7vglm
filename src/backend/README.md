# VC Financial Reporting Backend

This is the backend component of the VC Financial Reporting system, providing a robust API for storing and retrieving financial reporting metrics from portfolio companies.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup Instructions](#setup-instructions)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Environment Variables](#environment-variables)
   - [Database Setup](#database-setup)
3. [Running the Application](#running-the-application)
   - [Local Development](#local-development)
   - [Docker](#docker)
4. [API Documentation](#api-documentation)
5. [Testing](#testing)
6. [Database Migrations](#database-migrations)
7. [Code Style and Linting](#code-style-and-linting)
8. [Deployment](#deployment)
9. [Contributing](#contributing)
10. [Monitoring and Logging](#monitoring-and-logging)
11. [Security](#security)
12. [Performance Optimization](#performance-optimization)
13. [Troubleshooting](#troubleshooting)
14. [License](#license)

## Project Structure

The backend project is structured as follows:

```
src/backend/
├── api/
│   └── v1/
│       └── endpoints/
│           ├── companies.py
│           ├── metrics_input.py
│           ├── reporting_financials.py
│           ├── reporting_metrics.py
│           └── __init__.py
├── core/
│   ├── config.py
│   ├── dependencies.py
│   ├── security.py
│   └── __init__.py
├── crud/
│   ├── base.py
│   ├── company.py
│   ├── metrics_input.py
│   ├── reporting_financials.py
│   ├── reporting_metrics.py
│   └── __init__.py
├── db/
│   ├── base.py
│   ├── session.py
│   └── __init__.py
├── models/
│   ├── company.py
│   ├── metrics_input.py
│   ├── reporting_financials.py
│   ├── reporting_metrics.py
│   └── __init__.py
├── schemas/
│   ├── company.py
│   ├── metrics_input.py
│   ├── reporting_financials.py
│   ├── reporting_metrics.py
│   └── __init__.py
├── services/
│   ├── data_transformation.py
│   ├── currency_conversion.py
│   ├── metrics_calculation.py
│   └── __init__.py
├── tests/
│   ├── api/
│   │   └── v1/
│   │       ├── test_companies.py
│   │       ├── test_metrics_input.py
│   │       ├── test_reporting_financials.py
│   │       ├── test_reporting_metrics.py
│   │       └── __init__.py
│   ├── services/
│   │   ├── test_data_transformation.py
│   │   ├── test_currency_conversion.py
│   │   ├── test_metrics_calculation.py
│   │   └── __init__.py
│   ├── conftest.py
│   └── __init__.py
├── utils/
│   ├── logging.py
│   ├── rate_limiter.py
│   ├── error_handlers.py
│   └── __init__.py
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── __init__.py
├── alembic.ini
├── config.py
├── Dockerfile
├── .dockerignore
├── main.py
├── README.md
└── requirements.txt
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- PostgreSQL 13+ (if running locally without Docker)
- Git

### Installation

1. Clone the repository:
   ```
   git clone <repository_url>
   cd src/backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the `src/backend` directory with the following variables:

```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
LOG_LEVEL=INFO
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60
```

Replace the values with your actual database connection details and desired settings. For production, ensure you use a strong, unique `SECRET_KEY`.

### Database Setup

1. Create a PostgreSQL database for the project:
   ```
   createdb vc_financial_reporting
   ```

2. Run the database migrations:
   ```
   alembic upgrade head
   ```

## Running the Application

### Local Development

To run the application locally using uvicorn:

```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### Docker

To build and run the Docker container:

```
docker build -t vc-financial-reporting-backend .
docker run -p 8000:8000 --env-file .env vc-financial-reporting-backend
```

## API Documentation

Once the application is running, you can access the auto-generated API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

To run the test suite:

```
pytest
```

To generate a coverage report:

```
pytest --cov=. --cov-report=html
```

The HTML coverage report will be available in the `htmlcov` directory.

## Database Migrations

To create a new migration after modifying models:

```
alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:

```
alembic upgrade head
```

## Code Style and Linting

This project uses Black for code formatting, Flake8 for linting, and isort for import sorting. To format the code:

```
black .
isort .
```

To run the linter:

```
flake8
```

## Deployment

The backend is designed to be deployed to Azure. Refer to the infrastructure documentation in the `infrastructure/` directory for detailed deployment instructions using Terraform.

For CI/CD, refer to the GitHub Actions workflows in the `.github/workflows/` directory.

## Contributing

1. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name`
2. Make your changes and write tests if applicable.
3. Run the test suite and ensure all tests pass: `pytest`
4. Format your code using Black and ensure it passes Flake8: `black . && flake8`
5. Commit your changes: `git commit -am 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Create a pull request with a clear description of your changes.

## Monitoring and Logging

- Application logs are handled by the custom logging utility in `utils/logging.py`.
- For production monitoring, we use Azure Application Insights. Refer to the `infrastructure/modules/monitoring/` directory for setup details.

## Security

- API authentication is implemented using JWT tokens. Refer to `core/security.py` for details.
- Rate limiting is implemented to prevent abuse. See `utils/rate_limiter.py`.
- Ensure all sensitive information is stored in Azure Key Vault in production. Refer to `infrastructure/modules/key_vault/` for setup.

## Performance Optimization

- Database queries are optimized using SQLAlchemy's lazy loading and joining techniques.
- For high-traffic endpoints, consider implementing caching using Redis.

## Troubleshooting

- Check the application logs for detailed error messages.
- Ensure all environment variables are correctly set.
- Verify database connectivity and migrations are up to date.
- For deployment issues, check the Azure resource logs and Application Insights.

## License

[MIT License](LICENSE)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full license text...]

---

This README provides an overview of the VC Financial Reporting backend component. For more detailed information on specific modules or deployment processes, please refer to the respective documentation in each directory.