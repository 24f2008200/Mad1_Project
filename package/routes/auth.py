import os
from functools import wraps
from flask import request, jsonify,redirect, url_for, g
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, User,  Doctor, Patient
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


def is_api_request() -> bool:
    # Any of these signals "API style" request
    return (
        request.path.startswith("/api/")
        or request.headers.get("Authorization", "").startswith("Bearer ")
        or "application/json" in request.headers.get("Accept", "")
    )

def get_request_user():
    # 1) Browser session user
    if current_user.is_authenticated:
        return current_user

    # 2) Bearer token user
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        if token:
            return User.query.filter_by(api_token=token).first()

    return None

def require_auth(roles: set[str] | None = None):
    roles = set(roles or [])

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_mode = is_api_request()
            user = get_request_user()

            # Not authenticated
            if user is None:
                if api_mode:
                  return {"error": "Unauthorized"}, 401
                return redirect(url_for("login"))

            # Role check (assuming user.type holds 'admin'/'doctor'/'patient')
            if roles and getattr(user, "role", None) not in roles:
                if api_mode:
                    return {"error": f"Access denied. Requires one of: {sorted(roles)}"}, 403
                return redirect(url_for("index"))

            # Expose to downstream
            g.user = user
            return fn(*args, **kwargs)
        return wrapper
    return decorator

login_or_token_required = require_auth()

admin_required  = require_auth({"admin"})
doctor_required = require_auth({"doctor"})
patient_required = require_auth({"patient"})

# def role_required(*role_name):
#     # Generic role-based decorator: admin, doctor, patient.
#     def decorator(fn):
#         @wraps(fn)
#         @login_required
#         def wrapper(*args, **kwargs):
#             user = current_user
#             if user is None:
#                 return {"msg": "Not authenticated"}, 401
#             print (user,user.type, role_name)
#             if user.type not in role_name:
#                 return {"msg": f"Access denied, must be {role_name}"}, 403

#             return fn(*args, **kwargs)
#         return wrapper
#     return decorator




# def api_login_required(fn):
    
#     # Allows either:
#     # - Flask-Login session (browser user), OR
#     # - Bearer token (external API user)
    
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         # If user logged in via browser
#         if current_user.is_authenticated:
#             return fn(*args, **kwargs)

#         # If called externally with Bearer token
#         auth_header = request.headers.get("Authorization")
#         if auth_header and auth_header.startswith("Bearer "):
#             token = auth_header.split(" ")[1]
#             user = User.query.filter_by(api_token=token).first()
#             if user:
#                 return fn(*args, **kwargs)

#         return {"error": "Unauthorized"}, 401
#     return wrapper


# # Specializations
# admin_required = role_required("admin")
# doctor_required = role_required("doctor")
# patient_required = role_required("patient")
