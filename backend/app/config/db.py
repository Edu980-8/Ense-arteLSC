from sqlmodel import Session, create_engine, select

from app.models.categories import Category
from app.models.signs import Sign
from app.services import users
from app.config.settings import settings
from app.models.users import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # 1. Crear superusuario si no existe
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = users.create_user(session=session, user_create=user_in)

    # 2. Crear categorías únicas si no existen
    unique_categories = [
        "Familia",
        "Actividades",
        "Necesidades",
        "Emociones",
        "Sociales",
        "Pronombres",
    ]

    category_map = {}  # Mapa de nombre de categoría a objeto Category

    for category_value in unique_categories:
        existing_category = session.exec(
            select(Category).where(Category.value == category_value)
        ).first()
        if not existing_category:
            new_category = Category(
                value=category_value,
                medal_image_url="https://example.com/medal.png"
            )
            session.add(new_category)
            session.commit()  # commit para obtener ID
            category_map[category_value] = new_category
        else:
            category_map[category_value] = existing_category

    # 3. Crear señas iniciales si no existen
    initial_signs = [
        {"name": "MAMÁ", "category": "Familia", "description": "Descripción del curso 1"},
        {"name": "PAPÁ", "category": "Familia", "description": "Descripción del curso 2"},
        {"name": "JUGAR", "category": "Actividades", "description": "Descripción del curso 3"},
        {"name": "COMER", "category": "Necesidades", "description": "Descripción del curso 3"},
        {"name": "HAMBRE", "category": "Necesidades", "description": "Descripción del curso 3"},
        {"name": "FELIZ", "category": "Emociones", "description": "Descripción del curso 3"},
        {"name": "TRISTE", "category": "Emociones", "description": "Descripción del curso 3"},
        {"name": "HOLA", "category": "Sociales", "description": "Descripción del curso 3"},
        {"name": "GRACIAS", "category": "Sociales", "description": "Descripción del curso 3"},
        {"name": "YO", "category": "Pronombres", "description": "Descripción del curso 3"},
        {"name": "TÚ", "category": "Pronombres", "description": "Descripción del curso 3"},
        {"name": "ABUELO", "category": "Familia", "description": "Descripción del curso 3"},
        {"name": "TE AMO", "category": "Sociales", "description": "Descripción del curso 3"},
        {"name": "SED", "category": "Necesidades", "description": "Descripción del curso 3"},
        {"name": "POR FAVOR", "category": "Sociales", "description": "Descripción del curso 3"},
    ]

    for sign_data in initial_signs:
        existing_sign = session.exec(
            select(Sign).where(Sign.name == sign_data["name"])
        ).first()
        if not existing_sign:
            category = category_map.get(sign_data["category"])
            if category:
                new_sign = Sign(
                    name=sign_data["name"],
                    description=sign_data["description"],
                    url_video="https://example.com/video_placeholder.mp4",  # Reemplaza con URL real
                    category_id=category.id
                )
                session.add(new_sign)

    session.commit()
    session.close()