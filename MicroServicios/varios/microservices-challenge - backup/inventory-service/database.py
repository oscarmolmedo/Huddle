from sqlalchemy import create_engine                        #crea un motor de base de datos
#ORM es trabajar con sql escribiendo python en pocas palabras
from sqlalchemy.orm import sessionmaker, declarative_base   #session | crea sesiones para realizar (SELECT, INSERT, UPDATE, DELETE)
                                                            #declarative_base | crea tablas en base a clases
                                                            
#URL para SQLite. '///' ruta relativa en el directorio actual
SQLALCHEMY_DATABASE_URL = "sqlite:///./inventory.db"

#Creamos motor de conexion | check_same_thread maneja si se usa el mismo hilo para prevenir corrupción de datos
#True evita que se use el mismo hilo, False lo contrario.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#Clase para crear sesiones DB
#autocommit | nosotros controlamos cuando hacer commit y por ende guardado
#autoflush  | no guarda los cambios automaticamente antes de la consulta
#bind       | asociamos a la variable anterior 'engine'
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Esta clase Base es la que heredarán todos nuestros modelos de DB
Base = declarative_base()

#Esta función es un generador que abrirá y cerrará la sesión de DB.
def get_db():
    db = SessionLocal()
    try:
        #yield pausa la función, devuelve el valor y recuerda su estado, la funcion se convierte en un tipo iterador
        yield db    #devuelve la db al endpoint de fastapi
    #finally ejecuta lo que contiene idenpendientemente si se produce o no una excepción
    finally:
        db.close()