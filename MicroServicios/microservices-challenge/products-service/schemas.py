from pydantic import BaseModel, ConfigDict

#Esquema base donde se define los campos que el usuario enviará al crear o actualizar
class ProductBase(BaseModel):
    name            : str
    description     : str | None = None #Puede ser  String o Nose
    price           : float
    stock           : int

#Input para post, es igual a productbase pero luego se le puede agregar más campos
class ProductCreate(ProductBase):
    pass

#
class Product(ProductBase):
    id : int

    # Configuración de Pydantic: Permite que el esquema se mapee a los objetos de SQLAlchemy.
    #Para trabajar con sqlalchemy
    # #pydantic y fastapi usa este. Usar from_attributes en lugar de orm_mode
    model_config = ConfigDict(from_attributes=True)
