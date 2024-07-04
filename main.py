from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class PrimeNumber(Base):
    __tablename__ = 'primes'
    id = Column(Integer, primary_key=True)
    prime_number = Column(Integer, unique=True)


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes


def save_primes_to_postgres(primes):
    try:
        engine = create_engine('postgresql://postgres:asd@localhost:5432/primes')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        for prime in primes:
            prime_number = PrimeNumber(prime_number=prime)
            session.add(prime_number)

        session.commit()
        print(f"Successfully saved {len(primes)} prime numbers to PostgreSQL using SQLAlchemy.")

    except Exception as e:
        print("Error while connecting to PostgreSQL or inserting data:", e)

    finally:
        if session:
            session.close()
            print("PostgreSQL session is closed.")


if __name__ == "__main__":
    num_primes_to_generate = 10000
    primes = generate_primes(num_primes_to_generate)
    save_primes_to_postgres(primes)
