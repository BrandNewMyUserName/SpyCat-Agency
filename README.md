# SpyCat Agency Management System

A Django REST API application for managing spy cats, missions, and targets for the SpyCat Agency (SCA).

## Features

- **Spy Cat Management**: Create, read, update, and delete spy cats with breed validation
- **Mission Management**: Create missions with targets, assign cats to missions
- **Target Management**: Update target notes and mark targets as completed
- **Business Logic**: Automatic mission completion when all targets are completed
- **Data Validation**: Breed validation using TheCatAPI, business rule enforcement

## Technology Stack

- **Backend**: Django 5.2.7
- **API**: Django REST Framework 3.16.1
- **Database**: PostgreSQL
- **External API**: TheCatAPI for breed validation
- **Environment Management**: python-decouple

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SpyCat-Agency
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\Activate.ps1
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   - Create a PostgreSQL database named `spycat_agency`
   - Update database credentials in your environment variables or `.env` file

5. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   DB_NAME=spycat_agency
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

6. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Postaman collection link
https://illia-9660995.postman.co/workspace/Illia's-Workspace~9f2fd924-c272-455d-82fe-925a3d3edbf2/collection/44354128-635869d8-3b37-4be4-b340-cc1d1358217d?action=share&creator=44354128

### Spy Cats

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cats/` | List all spy cats |
| POST | `/api/cats/` | Create a new spy cat |
| GET | `/api/cats/{id}/` | Get single spy cat |
| PATCH | `/api/cats/{id}/` | Update spy cat |
| DELETE | `/api/cats/{id}/` | Delete spy cat |
| PATCH | `/api/cats/{id}/salary/` | Update spy cat salary |
| GET | `/api/cats/available/` | Get available cats |

### Missions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/missions/` | List all missions |
| POST | `/api/missions/` | Create mission with targets |
| GET | `/api/missions/{id}/` | Get single mission |
| PUT | `/api/missions/{id}/` | Update mission |
| DELETE | `/api/missions/{id}/` | Delete mission |
| POST | `/api/missions/{id}/assign/{cat_id}/` | Assign cat to mission |
| GET | `/api/missions/{id}/targets/` | Get mission targets |

### Targets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/targets/{id}/` | Get single target |
| PATCH | `/api/targets/{id}/` | Update target notes or completion status |

## API Usage Examples

### Create a Spy Cat
```bash
curl -X POST http://localhost:8000/api/cats/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Whiskers",
    "years_of_experience": 5,
    "breed": "Persian",
    "salary": 50000.00
  }'
```

### Create a Mission with Targets
```bash
curl -X POST http://localhost:8000/api/missions/ \
  -H "Content-Type: application/json" \
  -d '{
    "cat": 1,
    "targets": [
      {
        "name": "John Doe",
        "country": "USA",
        "notes": "Initial surveillance notes"
      },
      {
        "name": "Jane Smith",
        "country": "Canada",
        "notes": "Target in Toronto"
      }
    ]
  }'
```

### Update Target Notes
```bash
curl -X PATCH http://localhost:8000/api/targets/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Updated surveillance notes"
  }'
```

## Business Rules

1. **Spy Cats**:
   - Breed must be validated against TheCatAPI
   - Cannot delete cats with active missions
   - Only one mission per cat at a time

2. **Missions**:
   - Must have 1-3 targets
   - Cannot delete missions assigned to cats
   - Automatically marked as completed when all targets are completed

3. **Targets**:
   - Notes cannot be updated if target or mission is completed
   - Mission completion is checked after each target update

## Postman Collection

A complete Postman collection is included: `SpyCat_Agency_API.postman_collection.json`

**Import Instructions:**
1. Open Postman
2. Click "Import" button
3. Select the `SpyCat_Agency_API.postman_collection.json` file
4. Set the `base_url` variable to `http://localhost:8000`

## Database Schema

### SpyCat Model
- `id`: Primary key
- `name`: Cat name (CharField, max 100)
- `years_of_experience`: Experience in years (PositiveIntegerField)
- `breed`: Cat breed (CharField, max 100, validated against TheCatAPI)
- `salary`: Monthly salary (DecimalField)
- `is_available`: Availability status (BooleanField)
- `created_at`, `updated_at`: Timestamps

### Mission Model
- `id`: Primary key
- `cat`: Foreign key to SpyCat
- `status`: Mission status (pending, in_progress, completed)
- `created_at`, `updated_at`: Timestamps

### Target Model
- `id`: Primary key
- `mission`: Foreign key to Mission
- `name`: Target name (CharField, max 100)
- `country`: Target country (CharField, max 100)
- `notes`: Surveillance notes (TextField)
- `is_completed`: Completion status (BooleanField)
- `created_at`, `updated_at`: Timestamps

## Testing


## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to manage data through the web interface.

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `500`: Internal Server Error

Error responses include descriptive messages:
```json
{
  "error": "Breed 'InvalidBreed' is not valid. Please check TheCatAPI for valid breeds."
}
```

## Development

### Project Structure
```
SpyCat-Agency/
├── manage.py
├── requirements.txt
├── README.md
├── SpyCat_Agency_API.postman_collection.json
├── spycat_agency/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── agency/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    └── views.py
```

### Adding New Features

1. Update models in `agency/models.py`
2. Create/update serializers in `agency/serializers.py`
3. Add views in `agency/views.py`
4. Update URL patterns in `agency/urls.py`
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`

## License

This project is created for assessment purposes.

## Contact

For questions or issues, please contact the development team.
