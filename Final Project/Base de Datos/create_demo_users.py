from app import create_app, db
from app.models import Role, User

app = create_app()

with app.app_context():
    # Crear roles si no existen
    roles = ['Admin', 'Professor', 'Student']
    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            print(f'✅ Rol "{role_name}" creado.')

    db.session.commit()  # Importante para que los roles existan en BD antes de asignar a usuarios

    users_data = [
        {
            "username": "Administrator",
            "email": "admin@example.com",
            "password": "admin123",
            "role_name": "Admin"
        },
        {
            "username": "John Doe",
            "email": "prof@example.com",
            "password": "prof123",
            "role_name": "Professor"
        },
        {
            "username": "Steve Jobs",
            "email": "student@example.com",
            "password": "student123",
            "role_name": "Student"
        }
    ]

    for user_info in users_data:
        existing_user = User.query.filter_by(email=user_info['email']).first()
        if existing_user:
            print(f'ℹ️ El usuario con email {user_info["email"]} ya existe.')
            continue

        role = Role.query.filter_by(name=user_info['role_name']).first()
        if not role:
            print(f'⚠️ El rol "{user_info["role_name"]}" no existe, no se puede asignar al usuario {user_info["username"]}.')
            continue

        user = User(
            username=user_info['username'],
            email=user_info['email'],
            role=role
        )
        user.set_password(user_info['password'])
        db.session.add(user)
        print(f'✅ Usuario "{user.username}" creado con rol "{role.name}".')

    db.session.commit()
    print("✅ Todos los usuarios fueron procesados correctamente.")
