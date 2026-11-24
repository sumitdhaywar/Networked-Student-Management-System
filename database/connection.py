import os

import mysql.connector

# Use environment-provided credentials instead of keeping database secrets in source.
mycon = mysql.connector.connect(
    host=os.environ.get("NSMS_DB_HOST", "localhost"),
    user=os.environ.get("NSMS_DB_USER", "root"),
    password=os.environ.get("NSMS_DB_PASSWORD", ""),
    port=int(os.environ.get("NSMS_DB_PORT", "3306")),
    database=os.environ.get("NSMS_DB_NAME", "SCHOOL_NET"),
)