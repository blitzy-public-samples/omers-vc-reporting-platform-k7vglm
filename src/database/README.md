# Database Component

This README provides a comprehensive overview and documentation for the database component of the financial reporting metrics backend system.

## Introduction

The database component is responsible for storing and managing quarterly reporting metrics from portfolio companies. It utilizes Azure Database for PostgreSQL as the primary data store and implements a robust data model to support the financial reporting requirements of the VC firm.

## Database Models

The database component defines the following main models:

1. Company
2. MetricsInput
3. ReportingFinancials
4. ReportingMetrics

These models are defined in the `src/database/models` package and are imported in the `src/database/models/__init__.py` file for easy access throughout the application.

For detailed information about each model, refer to their respective files:

- `src/database/models/company.py`
- `src/database/models/metrics_input.py`
- `src/database/models/reporting_financials.py`
- `src/database/models/reporting_metrics.py`

## Configuration

The database configuration is managed through the `src/database/config.py` file. It provides environment-specific settings for development, staging, and production environments. The configuration includes:

- Database URL
- Maximum connections
- Connection pool size
- Connection pool recycle time
- SQL echo mode (for debugging)

To set up the database configuration:

1. Create a `.env` file in the project root directory.
2. Set the `ENVIRONMENT` variable to either "development", "staging", or "production".
3. Set the appropriate database connection parameters for your environment.

Example `.env` file:

```
ENVIRONMENT=development
DATABASE_URL=postgresql://user:password@localhost:5432/financial_metrics
DATABASE_MAX_CONNECTIONS=20
DATABASE_POOL_SIZE=5
DATABASE_POOL_RECYCLE=3600
DATABASE_ECHO_SQL=True
```

Ensure that sensitive information such as database credentials are stored securely and not committed to version control.

## Session Management

Database session management is handled by the `src/database/session.py` file. It sets up the database engine, session factory, and provides utility functions for working with database sessions.

Key features:

- Connection pooling for optimal performance
- Asynchronous session support
- Dependency function for FastAPI to inject database sessions into route handlers

To use a database session in your FastAPI route:

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.session import get_db

@app.get("/companies")
async def get_companies(db: Session = Depends(get_db)):
    # Use the db session to query the database
    pass
```

## Migrations

Database migrations are managed using Alembic. The migration scripts are located in the `src/database/migrations` directory.

To create and apply migrations:

1. Create a new migration:
   ```
   alembic revision --autogenerate -m "Description of the change"
   ```

2. Apply migrations:
   ```
   alembic upgrade head
   ```

3. Rollback migrations:
   ```
   alembic downgrade -1
   ```

Always review auto-generated migration scripts before applying them to ensure they accurately reflect the intended changes.

## Usage Examples

### Initializing the Database

```python
from src.database.session import init_db

async def initialize_database():
    await init_db()
```

### Using the Database Session

```python
from src.database.session import get_db
from src.database.models import Company
from sqlalchemy.orm import Session

def get_all_companies(db: Session):
    return db.query(Company).all()

# In a FastAPI route
@app.get("/companies")
async def list_companies(db: Session = Depends(get_db)):
    companies = get_all_companies(db)
    return [company.to_dict() for company in companies]
```

### Async Database Operations

```python
from src.database.session import AsyncDatabaseSession
from src.database.models import MetricsInput
from sqlalchemy.future import select

async def get_metrics():
    async with AsyncDatabaseSession() as session:
        result = await session.execute(select(MetricsInput))
        metrics = result.scalars().all()
        return [metric.to_dict() for metric in metrics]

# In a FastAPI route
@app.get("/metrics")
async def list_metrics():
    return await get_metrics()
```

## Performance Considerations

To optimize database performance:

1. Use appropriate indexes on frequently queried columns. Refer to `src/database/utils/indexing.py` for index management.
2. Implement database sharding for large tables (e.g., Metrics Input and Quarterly Reporting tables). See `src/database/utils/sharding.py` for sharding strategies.
3. Utilize read replicas for read-heavy operations.
4. Implement caching mechanisms for frequently accessed data.
5. Regularly analyze and optimize slow queries using PostgreSQL's EXPLAIN ANALYZE.
6. Use database connection pooling to efficiently manage connections.
7. Implement proper database partitioning for large tables to improve query performance.

## Backup and Recovery

Regular backups are crucial for data integrity and disaster recovery. Refer to `src/database/scripts/backup_db.py` for the backup process. Ensure that backups are stored securely and tested regularly for restoration.

## Troubleshooting

Common issues and solutions:

1. Connection errors:
   - Verify the database connection string in the configuration.
   - Check network connectivity and firewall rules.
   - Ensure the database server is running and accessible.

2. Slow queries:
   - Analyze query execution plans using EXPLAIN ANALYZE.
   - Add necessary indexes based on query patterns.
   - Optimize complex queries or consider using materialized views.
   - Review and optimize database schema if necessary.

3. Connection pool exhaustion:
   - Increase the `DATABASE_MAX_CONNECTIONS` and `DATABASE_POOL_SIZE` settings.
   - Ensure connections are properly closed after use.
   - Implement connection timeouts to prevent hanging connections.

4. Migration errors:
   - Ensure all model changes are reflected in migration scripts.
   - Run `alembic history` to check the current migration state.
   - Manually resolve conflicts in migration scripts if necessary.

5. Data inconsistencies:
   - Implement database constraints to enforce data integrity.
   - Use transactions for operations that modify multiple related records.
   - Regularly run data validation scripts to detect and correct inconsistencies.

## Monitoring and Logging

Implement comprehensive monitoring and logging for the database:

1. Set up PostgreSQL query logging for slow queries.
2. Use a monitoring tool like Azure Monitor or Prometheus to track database metrics.
3. Implement application-level logging for all database operations.
4. Set up alerts for critical database events (e.g., high CPU usage, low disk space).

## Security Considerations

1. Use strong, unique passwords for database accounts.
2. Implement least privilege access for database users.
3. Enable SSL/TLS for database connections.
4. Regularly audit and rotate database access credentials.
5. Implement data encryption at rest and in transit.

For further assistance, consult the Azure Database for PostgreSQL documentation or contact the development team.

## Contributing

When contributing to the database component:

1. Follow the established coding standards and naming conventions.
2. Write unit tests for all new database-related functionality.
3. Update this README and other relevant documentation when making significant changes.
4. Perform thorough testing, including performance impact, before submitting changes.

## License

This project is licensed under [INSERT LICENSE HERE]. See the LICENSE file in the project root for full license information.