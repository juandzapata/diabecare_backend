from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
#from schemas.appointment import AppointmentOut, AppointmentRegister, GetAppointmentByDoctorIdByUser
#from services.appointment import get_appointments, get_appointments_by_user_id, create_appointment_function, get_available_hours_by_date, patch_appointment_state, post_appointment
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder