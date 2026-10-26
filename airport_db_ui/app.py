import os
from datetime import date, datetime
from decimal import Decimal

from flask import Flask, flash, redirect, render_template, request, url_for
import mysql.connector
from mysql.connector import Error, IntegrityError

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-for-local-development")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "AirportDB"),
}

# Fixed application metadata keeps identifiers safe. Values are always bound parameters.
TABLES = {
    "AIRPORT": {"label":"Airports","icon":"⌖","pk":["Airport_ID"],"columns":["Airport_ID","AirportName","Country","City"],"required":["Airport_ID","AirportName"],"fields":{"Airport_ID":"number","AirportName":"text","Country":"text","City":"text"},"filters":["Country","City"]},
    "AIRPLANE": {"label":"Airplanes","icon":"✈","pk":["Airplane_ID"],"columns":["Airplane_ID","Capacity","Model","Manufacturer"],"required":["Airplane_ID","Capacity"],"fields":{"Airplane_ID":"number","Capacity":"number","Model":"text","Manufacturer":"text"},"filters":["Model","Manufacturer"]},
    "EMPLOYEE": {"label":"Employees","icon":"♙","pk":["Employee_ID"],"columns":["Employee_ID","Address","Gender","FName","MName","LName","Salary","BDate","Airport_ID"],"required":["Employee_ID","FName","LName"],"fields":{"Employee_ID":"number","Address":"text","Gender":"text","FName":"text","MName":"text","LName":"text","Salary":"number","BDate":"date","Airport_ID":"number"},"filters":["Airport_ID","Gender"]},
    "FLIGHT_ATTENDANT": {"label":"Flight Attendants","icon":"♧","pk":["E_ID"],"columns":["E_ID","FA_Rank"],"required":["E_ID"],"fields":{"E_ID":"number","FA_Rank":"text"},"filters":["FA_Rank"]},
    "PILOT": {"label":"Pilots","icon":"✦","pk":["E_ID"],"columns":["E_ID","PRank","License_Number"],"required":["E_ID","License_Number"],"fields":{"E_ID":"number","PRank":"text","License_Number":"text"},"filters":["PRank"]},
    "PASSENGER": {"label":"Passengers","icon":"♙","pk":["Passenger_ID"],"columns":["Passenger_ID","P_FName","P_MName","P_LName","PhoneNo","BDate","P_Email"],"required":["Passenger_ID","P_FName","P_LName"],"fields":{"Passenger_ID":"number","P_FName":"text","P_MName":"text","P_LName":"text","PhoneNo":"text","BDate":"date","P_Email":"email"},"filters":["P_FName","P_LName","P_Email"]},
    "FLIGHT": {"label":"Flights","icon":"✈","pk":["Flight_ID"],"columns":["Flight_ID","Duration","ALocation","ADate","ATime","DLocation","DDate","DTime","Airplane_ID","Airport_ID"],"required":["Flight_ID","Airplane_ID","Airport_ID"],"fields":{"Flight_ID":"number","Duration":"number","ALocation":"text","ADate":"date","ATime":"time","DLocation":"text","DDate":"date","DTime":"time","Airplane_ID":"number","Airport_ID":"number"},"filters":["DDate","DLocation","ALocation","Airport_ID"]},
    "LUGGAGE": {"label":"Luggage","icon":"▣","pk":["Luggage_ID"],"columns":["Luggage_ID","Weight","Passenger_ID"],"required":["Luggage_ID","Weight","Passenger_ID"],"fields":{"Luggage_ID":"number","Weight":"number","Passenger_ID":"number"},"filters":["Passenger_ID"]},
    "BOOK": {"label":"Bookings","icon":"🎟","pk":["Flight_ID","Passenger_ID"],"columns":["Flight_ID","Passenger_ID","Price","Seat_Number"],"required":["Flight_ID","Passenger_ID","Price","Seat_Number"],"fields":{"Flight_ID":"number","Passenger_ID":"number","Price":"number","Seat_Number":"text"},"filters":["Flight_ID","Passenger_ID","Seat_Number"]},
}
TABLE_NAMES = list(TABLES)

REPORTS = {
    "flight-schedule": {"title":"Flight schedule","subtitle":"Departure and arrival details with aircraft and airport context.","columns":["Flight_ID","DDate","DTime","DLocation","ALocation","Model","AirportName"],"query":"SELECT F.Flight_ID,F.DDate,F.DTime,F.DLocation,F.ALocation,A.Model,AP.AirportName FROM FLIGHT F JOIN AIRPLANE A ON F.Airplane_ID=A.Airplane_ID JOIN AIRPORT AP ON F.Airport_ID=AP.Airport_ID WHERE (%s='' OR F.DLocation LIKE %s OR F.ALocation LIKE %s) ORDER BY F.DDate,F.DTime","params":lambda q:(q,f"%{q}%",f"%{q}%")},
    "passenger-bookings": {"title":"Passenger bookings","subtitle":"Passenger, flight, seat and price information.","columns":["P_FName","P_LName","Flight_ID","Seat_Number","Price"],"query":"SELECT P.P_FName,P.P_LName,B.Flight_ID,B.Seat_Number,B.Price FROM BOOK B JOIN PASSENGER P ON B.Passenger_ID=P.Passenger_ID WHERE (%s='' OR P.P_FName LIKE %s OR P.P_LName LIKE %s OR B.Seat_Number LIKE %s) ORDER BY B.Flight_ID,B.Seat_Number","params":lambda q:(q,f"%{q}%",f"%{q}%",f"%{q}%")},
    "flight-occupancy": {"title":"Flight occupancy","subtitle":"Bookings compared with each aircraft capacity.","columns":["Flight_ID","Model","Capacity","Booked_Passengers","Available_Seats"],"query":"SELECT F.Flight_ID,A.Model,A.Capacity,COUNT(B.Passenger_ID) AS Booked_Passengers,(A.Capacity-COUNT(B.Passenger_ID)) AS Available_Seats FROM FLIGHT F JOIN AIRPLANE A ON F.Airplane_ID=A.Airplane_ID LEFT JOIN BOOK B ON F.Flight_ID=B.Flight_ID WHERE (%s='' OR CAST(F.Flight_ID AS CHAR) LIKE %s) GROUP BY F.Flight_ID,A.Model,A.Capacity ORDER BY F.Flight_ID","params":lambda q:(q,f"%{q}%")},
    "luggage-details": {"title":"Luggage details","subtitle":"Luggage weight linked to passenger records.","columns":["P_FName","P_LName","Luggage_ID","Weight"],"query":"SELECT P.P_FName,P.P_LName,L.Luggage_ID,L.Weight FROM LUGGAGE L JOIN PASSENGER P ON L.Passenger_ID=P.Passenger_ID WHERE (%s='' OR P.P_FName LIKE %s OR P.P_LName LIKE %s) ORDER BY L.Luggage_ID","params":lambda q:(q,f"%{q}%",f"%{q}%")},
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_all(query, params=()):
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(query, params); return cur.fetchall()
    finally:
        cur.close(); conn.close()

def fetch_one(query, params=()):
    rows = fetch_all(query, params); return rows[0] if rows else {}

def db_is_online():
    conn = None
    try:
        conn = get_connection(); return conn.is_connected()
    except Error:
        return False
    finally:
        if conn and conn.is_connected(): conn.close()

def safe_db_message(error):
    app.logger.exception("Database operation failed", exc_info=error)
    text = str(error).lower()
    if isinstance(error, IntegrityError):
        if "duplicate" in text: return "That record already exists. Check the primary key or unique fields."
        if "foreign key" in text: return "This record references a missing related record, or is still referenced by another record."
        if "constraint" in text: return "One or more values do not satisfy the database rules."
    return "The database could not complete that request. Check the connection and your input."

def table_or_404(name):
    key = name.upper(); return key, TABLES.get(key)

def related_options(table_name, field):
    queries = {
        ("EMPLOYEE","Airport_ID"): "SELECT Airport_ID AS value,AirportName AS label FROM AIRPORT ORDER BY AirportName",
        ("FLIGHT","Airplane_ID"): "SELECT Airplane_ID AS value,CONCAT(Model,' (',Airplane_ID,')') AS label FROM AIRPLANE ORDER BY Airplane_ID",
        ("FLIGHT","Airport_ID"): "SELECT Airport_ID AS value,AirportName AS label FROM AIRPORT ORDER BY AirportName",
        ("LUGGAGE","Passenger_ID"): "SELECT Passenger_ID AS value,CONCAT(P_FName,' ',P_LName,' (',Passenger_ID,')') AS label FROM PASSENGER ORDER BY P_LName",
        ("BOOK","Flight_ID"): "SELECT Flight_ID AS value,CONCAT('Flight ',Flight_ID,' — ',DLocation,' to ',ALocation) AS label FROM FLIGHT ORDER BY Flight_ID",
        ("BOOK","Passenger_ID"): "SELECT Passenger_ID AS value,CONCAT(P_FName,' ',P_LName,' (',Passenger_ID,')') AS label FROM PASSENGER ORDER BY P_LName",
        ("FLIGHT_ATTENDANT","E_ID"): "SELECT Employee_ID AS value,CONCAT(FName,' ',LName,' (',Employee_ID,')') AS label FROM EMPLOYEE ORDER BY LName",
        ("PILOT","E_ID"): "SELECT Employee_ID AS value,CONCAT(FName,' ',LName,' (',Employee_ID,')') AS label FROM EMPLOYEE ORDER BY LName",
    }
    return fetch_all(queries[(table_name,field)]) if (table_name,field) in queries else []

def format_value(value):
    if isinstance(value,(date,datetime)): return value.isoformat()
    if isinstance(value,Decimal): return str(value)
    return "" if value is None else str(value)

def key_values(definition, key):
    parts = key.split("|"); return dict(zip(definition["pk"],parts)) if len(parts)==len(definition["pk"]) else None

@app.context_processor
def global_template_values():
    return {"table_names":TABLE_NAMES,"table_defs":TABLES}

@app.route("/")
def dashboard():
    try:
        names={"flights":"FLIGHT","passengers":"PASSENGER","bookings":"BOOK","luggage":"LUGGAGE"}
        stats={key:fetch_one(f"SELECT COUNT(*) AS n FROM {table}").get("n",0) for key,table in names.items()}
        upcoming=fetch_all("SELECT F.Flight_ID,F.DDate,F.DTime,F.DLocation,F.ALocation,A.Model,AP.AirportName FROM FLIGHT F JOIN AIRPLANE A ON F.Airplane_ID=A.Airplane_ID JOIN AIRPORT AP ON F.Airport_ID=AP.Airport_ID ORDER BY F.DDate,F.DTime LIMIT 8")
        return render_template("dashboard.html",stats=stats,upcoming=upcoming,db_online=True)
    except Error as error:
        return render_template("error.html",message=safe_db_message(error),db_online=False),500

@app.route("/health")
def health():
    online=db_is_online(); return ({"database":"online" if online else "offline"},200 if online else 503)

@app.route("/reports/<key>")
def report(key):
    definition=REPORTS.get(key)
    if not definition: return render_template("error.html",message="That report does not exist."),404
    q=request.args.get("q","").strip()[:80]; page=max(1,request.args.get("page",1,type=int)); per_page=12
    try:
        rows=fetch_all(definition["query"],definition["params"](q)); total=len(rows); start=(page-1)*per_page
        return render_template("report.html",definition=definition,rows=rows[start:start+per_page],total=total,page=page,per_page=per_page,q=q,report_key=key)
    except Error as error: return render_template("error.html",message=safe_db_message(error)),500

@app.route("/table/<name>")
def table_data(name):
    table_name,definition=table_or_404(name)
    if not definition: return render_template("error.html",message="Unknown table."),404
    q=request.args.get("q","").strip()[:80]; page=max(1,request.args.get("page",1,type=int)); per_page=10
    filters={field:request.args.get(field,"").strip()[:80] for field in definition["filters"] if request.args.get(field,"").strip()}
    conditions=[]; params=[]
    if q:
        searchable=[c for c in definition["columns"] if definition["fields"].get(c) in {"text","email"}]
        if searchable: conditions.append("("+" OR ".join(f"`{c}` LIKE %s" for c in searchable)+")"); params += [f"%{q}%"]*len(searchable)
    for field,value in filters.items(): conditions.append(f"CAST(`{field}` AS CHAR) LIKE %s"); params.append(f"%{value}%")
    where=(" WHERE "+" AND ".join(conditions)) if conditions else ""
    try:
        total=fetch_one(f"SELECT COUNT(*) AS n FROM `{table_name}`{where}",tuple(params)).get("n",0); offset=(page-1)*per_page
        order=", ".join(f"`{c}`" for c in definition["pk"])
        rows=fetch_all(f"SELECT * FROM `{table_name}`{where} ORDER BY {order} LIMIT %s OFFSET %s",tuple(params)+(per_page,offset))
        return render_template("table.html",table_name=table_name,definition=definition,rows=rows,total=total,page=page,per_page=per_page,q=q,filters=filters)
    except Error as error: return render_template("error.html",message=safe_db_message(error)),500

def form_options(table_name, definition):
    return {field:related_options(table_name,field) for field in definition["columns"] if related_options(table_name,field)}

@app.route("/table/<name>/new",methods=["GET","POST"])
def create_record(name):
    table_name,definition=table_or_404(name)
    if not definition: return render_template("error.html",message="Unknown table."),404
    try: options=form_options(table_name,definition)
    except Error as error: options={}; flash(safe_db_message(error),"error")
    if request.method=="POST":
        values=[request.form.get(c,"").strip() or None for c in definition["columns"]]
        missing=[c for c,v in zip(definition["columns"],values) if c in definition["required"] and v is None]
        if missing: flash("Complete the required fields: "+", ".join(missing),"error"); return render_template("form.html",mode="Create",table_name=table_name,definition=definition,values=request.form,options=options)
        conn=cur=None
        try:
            conn=get_connection(); cur=conn.cursor(); cols=", ".join(f"`{c}`" for c in definition["columns"]); marks=", ".join(["%s"]*len(values))
            cur.execute(f"INSERT INTO `{table_name}` ({cols}) VALUES ({marks})",tuple(values)); conn.commit(); flash("Record created successfully.","success"); return redirect(url_for("table_data",name=table_name))
        except Error as error: flash(safe_db_message(error),"error")
        finally:
            if cur: cur.close()
            if conn: conn.close()
    return render_template("form.html",mode="Create",table_name=table_name,definition=definition,values={},options=options)

@app.route("/table/<name>/edit/<path:key>",methods=["GET","POST"])
def edit_record(name,key):
    table_name,definition=table_or_404(name); primary=key_values(definition,key) if definition else None
    if not definition or not primary: return render_template("error.html",message="That record could not be found."),404
    where=" AND ".join(f"`{c}`=%s" for c in definition["pk"]); conn=cur=None
    try:
        current=fetch_one(f"SELECT * FROM `{table_name}` WHERE {where}",tuple(primary.values()))
        if not current: return render_template("error.html",message="That record could not be found."),404
        options=form_options(table_name,definition)
        if request.method=="POST":
            values=[request.form.get(c,"").strip() or None for c in definition["columns"]]; missing=[c for c,v in zip(definition["columns"],values) if c in definition["required"] and v is None]
            if missing: flash("Complete the required fields: "+", ".join(missing),"error"); return render_template("form.html",mode="Edit",table_name=table_name,definition=definition,values=request.form,options=options,primary=primary)
            conn=get_connection(); cur=conn.cursor(); assignments=", ".join(f"`{c}`=%s" for c in definition["columns"])
            cur.execute(f"UPDATE `{table_name}` SET {assignments} WHERE {where}",tuple(values)+tuple(primary.values())); conn.commit(); flash("Record updated successfully.","success"); return redirect(url_for("table_data",name=table_name))
        return render_template("form.html",mode="Edit",table_name=table_name,definition=definition,values=current,options=options,primary=primary)
    except Error as error: flash(safe_db_message(error),"error"); return redirect(url_for("table_data",name=table_name))
    finally:
        if cur: cur.close()
        if conn: conn.close()

@app.post("/table/<name>/delete")
def delete_record(name):
    table_name,definition=table_or_404(name)
    if not definition: return render_template("error.html",message="Unknown table."),404
    values=[request.form.get(c,"") for c in definition["pk"]]; where=" AND ".join(f"`{c}`=%s" for c in definition["pk"]); conn=cur=None
    try:
        if any(not v for v in values): raise ValueError("Missing primary key")
        conn=get_connection(); cur=conn.cursor(); cur.execute(f"DELETE FROM `{table_name}` WHERE {where}",tuple(values)); conn.commit(); flash("Record deleted successfully.","success")
    except ValueError: flash("The selected record is missing a primary key.","error")
    except Error as error: flash(safe_db_message(error),"error")
    finally:
        if cur: cur.close()
        if conn: conn.close()
    return redirect(url_for("table_data",name=table_name))

@app.route("/tables")
def tables(): return render_template("tables.html")

@app.route("/flights")
def flights(): return redirect(url_for("report",key="flight-schedule"))
@app.route("/bookings")
def bookings(): return redirect(url_for("report",key="passenger-bookings"))
@app.route("/flight-details")
def flight_details(): return redirect(url_for("report",key="flight-schedule"))
@app.route("/passenger-count")
def passenger_count(): return redirect(url_for("report",key="flight-occupancy"))
@app.route("/luggage")
def luggage(): return redirect(url_for("report",key="luggage-details"))

if __name__ == "__main__": app.run(debug=True)
