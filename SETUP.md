# Setup and Installation Guide

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
2. **pip** - Usually comes with Python
3. **Web Browser** - Chrome, Firefox, Safari, or Edge
4. **VS Code** (optional but recommended)

### Verify Installation

```bash
python --version
pip --version
```

## Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd "c:\Users\ferna\OneDrive\Desktop\project\Web-based software effort estimation and cost planning system"
```

### Step 2: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- Flask 2.3.3 - Web framework
- Flask-SQLAlchemy 3.0.5 - ORM for database
- SQLAlchemy 2.0.21 - Database toolkit
- python-dotenv 1.0.0 - Environment variable loader

**Expected Output:**
```
Successfully installed Flask-2.3.3 Flask-SQLAlchemy-3.0.5 SQLAlchemy-2.0.21 python-dotenv-1.0.0
```

### Step 3: Run the Flask Application

```bash
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 4: Open in Web Browser

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You should see the SPM Effort Estimation System home page

## Database Setup

The SQLite database is automatically created when you first run the Flask application.

- **Database Location:** `database/spm_estimation.db`
- **Tables Created Automatically:**
  - projects
  - estimations
  - risks
  - evm_tracking

No manual database setup is required.

## Configuration

### Environment Variables (.env file)

The system uses a `.env` file for configuration. Default values are already set:

```
FLASK_APP=backend/app.py
FLASK_ENV=development
DATABASE_PATH=sqlite:///database/spm_estimation.db
SECRET_KEY=your-secret-key-change-in-production
```

### For Production Deployment (Change These):
1. Set `FLASK_ENV=production`
2. Update `SECRET_KEY` to a random secure string
3. Update `DATABASE_PATH` if using different database

## Running the System

### Development Mode (Default)

```bash
cd backend
python app.py
```

The Flask development server will:
- Enable debug mode
- Auto-reload on code changes
- Show detailed error messages

### Stopping the Server

Press `CTRL+C` in the terminal where Flask is running

## Troubleshooting

### Issue: Python not found
**Solution:** Add Python to PATH environment variables
- Windows: Search "Environment Variables" → Edit System Variables → Add Python to PATH

### Issue: pip not found
**Solution:** Use Python module installer instead
```bash
python -m pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** Change the port in `app.py`
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Issue: Database file permission error
**Solution:** Check file permissions
- Ensure `database/` folder is writable
- Windows: Right-click folder → Properties → Security

### Issue: Cannot connect to localhost:5000
**Verify:**
1. Flask server is running (check terminal)
2. Correct URL: `http://localhost:5000` (not `https://`)
3. No firewall blocking port 5000
4. Close and reopen browser

### Issue: Modules not found (ModuleNotFoundError)
**Solution:** Ensure you're in the backend directory and requirements are installed
```bash
cd backend
pip list  # Verify all packages are installed
python app.py
```

## Verify Installation

Once running, test the system:

1. **Test Frontend:**
   - Navigate to `http://localhost:5000`
   - You should see the main page with navigation menu

2. **Test API:**
   - Open browser DevTools (F12)
   - Console should show no errors
   - Try creating a project in the "Project Input" module

3. **Test Database:**
   - Create a project
   - Close and restart the application
   - The project should still exist

## File Permissions (Windows)

If you encounter permission issues:

```bash
# Run Command Prompt as Administrator
cd project_directory
icacls "database" /grant:r "%username%:F"
```

## Backup and Recovery

### Backup Your Data
```bash
# Copy the database file
copy "database\spm_estimation.db" "database\spm_estimation_backup.db"
```

### Reset Database (Remove all data)
```bash
# Delete the database file (CAREFUL!)
del database\spm_estimation.db
# Restart the application - new empty database will be created
```

## Next Steps

1. **Read README.md** - Understand system features
2. **Start using the system:**
   - Create a sample project
   - Run COCOMO estimations
   - Explore all modules
3. **Prepare for presentation:**
   - Create sample projects
   - Take screenshots
   - Prepare explanations for each module

## System Requirements

| Component | Requirement |
|-----------|------------|
| **OS** | Windows/Mac/Linux |
| **Python** | 3.8 or higher |
| **RAM** | 512 MB minimum |
| **Disk Space** | 100 MB |
| **Browser** | Modern browser with JavaScript enabled |
| **Internet** | Not required (runs locally) |

## Performance Notes

- **Database:** SQLite is suitable for this academic project (supports up to hundreds of projects)
- **Concurrent Users:** Flask development server handles single user. For multi-user, deploy with production server (Gunicorn/Apache)
- **Browser Compatibility:** Modern browsers only (Bootstrap 5 requires IE11+)

## Development Tips

### Enable More Verbose Logging
Add to `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Access Database Directly
```bash
# Windows Command Prompt
sqlite3 database\spm_estimation.db
# Then use SQL commands

# Or use Python
cd backend
python
>>> from models import *
>>> projects = Project.query.all()
>>> for p in projects: print(p.project_name)
```

### Clear All Data
```bash
cd backend
python
>>> from app import db, app
>>> with app.app_context():
...     db.drop_all()
...     db.create_all()
>>> exit()
```

## Getting Help

### Common Errors

**"ModuleNotFoundError: No module named 'flask'"**
- Solution: `pip install -r requirements.txt` in backend directory

**"Address already in use"**
- Solution: Change port number in `app.py` line: `app.run(port=5001)`

**"No such table: projects"**
- Solution: Database not initialized. Restart Flask app to create tables.

**"CORS error in browser console"**
- Normal if frontend and backend are separate. System is configured to handle this.

## Support

For issues beyond this guide:
1. Check Flask documentation: https://flask.palletsprojects.com/
2. Check SQLAlchemy ORM: https://docs.sqlalchemy.org/
3. Check Bootstrap documentation: https://getbootstrap.com/docs/5.0/

---

**Last Updated:** January 2026
**Tested On:** Windows 10/11, Python 3.8+
