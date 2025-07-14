# URL-shortener
This API allows users to create short URLs from long ones, redirect to the original URL, track access statistics, and manage existing URLs.
📌 [Project Roadmap Source](https://roadmap.sh/projects/url-shortening-service)

---

## 🚀 Features
- ✅ Create short URLs from long ones
- ✅ Redirect from short URL to original URL
- ✅ Track access count and statistics
- ✅ Retrieve statistics for each short URL
- 🔒 UUID for internal reference and integrity
- 🧰 Production-ready with Supabase PostgreSQL
---

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Auth**: JWT (JSON Web Tokens)
- **Database**: SQLite (testing), Supabase PostgreSQL (production)
- **Database**:  Python Logging w/ Rich + RotatingFileHandler
- **Testing**: Pytest, httpx, pytest-asyncio
- **Deployment**: None(for now)

---

## 📦 Installation

1. Clone the repository

```bash
git clone https://github.com/eniolaomotee/URL-shortener
cd url-shortener-api
```

2. Create and activate a Virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
DATABASE_URL=sqlite:///./test.db  # or your Supabase URL
SECRET_KEY=your-secret
ALGORITHM=your-algorithm-key
```

5. Running Tests
``` bash
pytest
```



### This project is licensed under the MIT License.
