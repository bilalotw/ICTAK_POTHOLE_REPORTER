Fixed PWD Dashboard version
---------------------------
This version preloads reports server-side into /pwd/dashboard so the PWD sees a table immediately
and the Leaflet map is built from that server-side data (no initial API fetch required).

Steps:
  1. Create virtualenv and install requirements
  2. Start MongoDB locally or set MONGO_URI
  3. Create a PWD user:
     python create_pwd_user.py pwd_admin admin123
  4. Run app:
     python app.py

