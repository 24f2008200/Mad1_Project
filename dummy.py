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
            if roles and getattr(user, "type", None) not in roles:
                if api_mode:
                    return {"error": f"Access denied. Requires one of: {sorted(roles)}"}, 403
                return redirect(url_for("index"))

            # Expose to downstream
            g.user = user
            return fn(*args, **kwargs)
        return wrapper
    return decorator