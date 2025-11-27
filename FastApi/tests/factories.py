import factory
from factory.fuzzy import FuzzyChoice
from app.core.models.user import User

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"

    email = factory.Faker("email")
    password_hash = factory.Faker("password", length=10)
    role = FuzzyChoice(["Student", "Instructor", "Admin"])
