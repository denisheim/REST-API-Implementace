# Flask + Node.js REST API

The project uses REST API built with Flask and Node.js.  
It interacts with a MySQL database to manage data for firms, events, and contacts.

### Features

1. **Flask Backend (port 8081):**
   - Manage **firms**: create, update, list, and delete.
   - Manage **contacts** for specific firms.
   - Import/export firm data.
   - Upload files (e.g., business card images).

2. **Node.js Backend (port 3000):**
   - Manage **events**: create, update, list, and delete.

3. **MySQL Database:**
   - Tables for firms, events, columns, and more.
---
### Requirements

#### Python (Flask Backend)
- Python 3.x
- Install dependencies:
  ```bash
  pip install flask mysql-connector-python
#### Node.js (Node.js Backend)
- Node.js 14.x or newer
- Navigate to the /node/ directory and install dependencies:
  ```bash
  npm install express mysql2
---

### How to start the program

#### - Start the flask backend
  ```bash
  python flask_backend.py
  ```
#### - Start the node.js backend
  ```bash
  node node_backend.js
  ```
---

## Testing the API

#### Flask (port 8081)

- list firms
  ```bash
  curl http://localhost:8081/firms/list
  ```

- create a new firm
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -d '{"active":1,"name":"Denis","surname":"Heim","email":"heimenterprise@support.com"}' \
  http://localhost:8081/firms/save
  ```

#### Node.js (port 3000)

- list events
  ```bash
  curl http://localhost:3000/events/list
  ```

- create a new event
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -d '{"id":1,"name":"My Event","time_start":"2025-01-19 14:00:00"}' \
  http://localhost:3000/events/save
  ```

### Notes

- Make sure both Flask and Node.js apps are running simultaneously.
- Check your database configuration in:
    - database_helper.py (for Flask)
    - db.js (for Node.js)
