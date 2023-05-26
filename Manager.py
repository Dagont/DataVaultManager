from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    fullname = Column(String(255))
    password = Column(String(255))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password
        )

# Connect to the database
#engine = create_engine('mssql+pyodbc://jobreadinessadmin:5t4r3e2w1q+.@dbserver.database.windows.net/<database_name>')

# Create the table
#Base.metadata.create_all(engine)

# Start a session
#Session = sessionmaker(bind=engine)
#session = Session()
student_info = {
"Estudiante": [
"CODIGO",
"APELLIDOS",
"NOMBRES",
"DOCUMENTO",
"ESTADO_CIVIL",
"SEXO",
"FECHA_NAC",
"NACIONALIDAD",
"PAIS_NAC",
"DEPTO_NAC",
"CIUDAD_NAC",
"DIRECCION",
"CIUDAD_DIRECCION",
"PAIS_DIRECCION",
"INDICADOR_TEL",
"TEL",
"EXT_TEL",
"CEL",
"EMAIL",
"INTERESES_ACADEMICOS",
"EXPERIENCIA_INVESTIGACION",
"EXPERIENCIA_LABORAL",
"DISTINCIONES",
"REFERENCIA_ACADEMICA",
"CONOCIMIENTO_PROGRAMA",
"FINANCIACION",
"REQUIERE_APOYO_FIN",
"LENGUA_AMTERNA",
"INGLES_LECTURA",
"INGLES_ESCRITURA",
"INGLES_ORAL",
"DEDICACION",
"EDAD",
"Comentarios",
"Decisión comité",
"Comentarios comité",
"Correo UNIANDES"
],
"Matrícula": [
"PERIODO",
"ESTADO",
"GRADUADO",
"ALERTAS",
"Fecha cierre",
"Cierre",
"fecha INICIO DE CLASES",
"AÑOS EXPERIENCIA TOTAL AL INICIO DE CLASES/desde la fecha de grado",
"Matriculado ciclo I?"
],
"Programa de Estudios": [
"CODIGO_PROGRAMA",
"NIVEL",
"FACULTAD"
],
"Universidad de Pregrado": [
"UNIVERSIDAD_PREGRADO",
"UNIVERSIDAD_CIUDAD",
"UNIVERSIDAD_PAIS",
"FECHA_INICIO_EST",
"FECHA_FIN_EST",
"TITULO_OBTENIDO",
"PROMEDIO",
"FECHA_GRADO",
"AREA_INVESTIGACION"
]}

print(student_info['Programa de Estudios'])
