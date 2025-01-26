
#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """
    DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
          email (str): The email of the user.
          hashed_password (str): The hashed password of the user.

        Returns:
          object: The newly created user object.

        Raises:
          ValueError: If either email or hashed_password is not
            provided.
          ValueError: If a user with the same email already
            exists in the database.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided criteria.

        Args:
          **kwargs: Keyword arguments representing the criteria to
                    search for. The keys should correspond to the
                    column names in the User table.

        Returns:
          User: The user object that matches the provided criteria.

        Raises:
          NoResultFound: If no user is found that matches the
                          provided criteria. InvalidRequestError:
                          If the query is invalid or the database
                          connection is not established.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update the attributes of a user with the given user_id.

        Args:
          user_id (int): The ID of the user to update.
          **kwargs: Keyword arguments representing the attributes
                    to update.

        Raises:
          ValueError: If any of the provided attributes do not exist
                      in the user object.

        Returns:
          None
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound
        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise ValueError(f"Invalid attribute: {k}")
        self._session.commit()
