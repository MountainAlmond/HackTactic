from models.role import Role
def init_roles_and_routes(db):
    # Создание ролей с разрешенными маршрутами
    roles_data = [
        {
            'name': 'admin',
            'description': 'Administrator role',
            'routes': ['/protected']
        },
        {
            'name': 'editor',
            'description': 'Editor role',
            'routes': ['/admin/users']
        },
        {
            'name': 'user',
            'description': 'Regular user role',
            'routes': ['/user/profile']
        }
    ]

    for role_data in roles_data:
        role = Role.query.filter_by(name=role_data['name']).first()
        if not role:
            role = Role(
                name=role_data['name'],
                description=role_data['description'],
                routes=role_data['routes']
            )
            db.session.add(role)

    db.session.commit()