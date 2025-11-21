

# ===========================
# Stage 1: Build React frontend
# ===========================
FROM node:20-alpine AS frontend-build

WORKDIR /frontend

# מעתיקים רק package* קודם בשביל cache טוב יותר
COPY frontend/package*.json ./
RUN npm ci

# עכשיו מעתיקים את שאר קבצי ה-frontend
COPY frontend/ ./

# build ל-React → יוצרת תקיית dist
RUN npm run build


# ===========================
# Stage 2: Backend + built UI
# ===========================
FROM python:3.11-slim AS backend

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# מתקינים תלות של Flask
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# מעתיקים את קבצי ה-backend
COPY backend/ ./

# מעתיקים את ה-build של ה-frontend לתקייה frontend-dist
COPY --from=frontend-build /frontend/dist ./frontend-dist

# נוודא ש-Flask מאזין על 8080
ENV PORT=8080

# נחשוף את הפורט החוצה
EXPOSE 8080

# מריצים את האפליקציה
CMD ["python", "app.py"]


# לבנות את האפליקציה:

# docker build -t currency-app .

# להריץ:

#     docker run -p 8080:8080 currency-app
