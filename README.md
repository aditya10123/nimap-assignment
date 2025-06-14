## 📦 Installation & Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/aditya10123/nimap-assignment
   cd nimap-assignment
   ```

2. **Create a virtual environment**

   * For **Windows**:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * For **Linux/macOS**:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Update database settings**
   In `settings.py`, configure your `DATABASES` setting as required for your system.

5. **Run migrations (no need to run makemigrations)**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

---

### 🔐 Obtain JWT Token

**POST** `/api/token/`

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Returns:

* `access`: JWT access token
* `refresh`: JWT refresh token

Use `Authorization: Bearer <access_token>` in all protected API requests.

---

## 📁 API Endpoints

### 1. **Client List & Create**

**GET/POST** `/client/api/clients/`

* GET: List all clients
* POST body example:

```json
{
  "name": "Client A"
}
```

---

### 2. **Client Detail, Update, Delete**

**GET/PUT/PATCH/DELETE** `/client/api/clients/<id>/`

* GET: Client info + associated projects
* PUT/PATCH: Update client
* DELETE: Removes client

  * ✅ Returns:

    ```json
    {
      "message": "Client deleted successfully"
    }
    ```

---

### 3. **Create Project for Client**

**POST** `/client/api/clients/<client_id>/projects/`
Example Request:

```json
{
  "title": "New Project",
  "team_members": [
    { "id": 1 },
    { "id": 2 }
  ]
}
```

---

### 4. **Get Projects for Current User**

**GET** `/client/api/projects/`
Returns a list of projects the authenticated user is assigned to.

---
