import os
from zipfile import ZipFile
import shutil
import csv
import time
from datetime import datetime

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class DirPath:
    STAGING = "data/staging/"
    PROCESSED = "data/processed/"
    ERRORED = "data/errored/"

class CONVERSIONS:
    DOLLAR_EURO = 0.92
    ACRES_SQUARE_MEETRS = 4.047
    SQ_FEET_SQ_MEETRS = 0.092903
    
class DataBaseCommunication:
    @staticmethod   
    def update_database(row, models, db) -> None:
        """
        Inserts the row into the database, if the database encounters an error the insertion will be rolledback
        
        Args:
            row  (dict) - row of data from the file that we want to process
            models (:file:) - file where the classes for SQLAlchemy ORM are stored 
            db (:obj:) - database instace 

            """
        try:
            new_building = models.Building(
                                    price = row['price'],
                                    rooms = row["rooms"],
                                    bathrooms = row["bathrooms"],
                                    land_area = row['land_area'],
                                    square_footage = row["square_footage"],
                                    )
            db.session.add(new_building)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Something went wrong during the insertion into the database")


class DataProcessing:
    """ Processes the data from www.kaggle.com """

    is_processing = False

    @staticmethod
    def convert(data, conversion):
        if data == "":
            return 
        return round(float(data) * conversion, 2)
    
    @staticmethod
    def set_dic_columns(row) -> dict:
        """
        Setting the corect column names and converting their value to the correct one
        
        Args:
            row  (dict) - row of data from the file that we want to process
        Return:
            row (dict) - row with corrected formating 
             """
        row["price"] = DataProcessing.convert(row.pop("price"), CONVERSIONS.DOLLAR_EURO)
        row["rooms"] = row.pop("bed")
        row["bathrooms"] = row.pop("bath")
        row["land_area"] = DataProcessing.convert(row.pop("acre_lot"), CONVERSIONS.ACRES_SQUARE_MEETRS)
        row["square_footage"] = DataProcessing.convert(row.pop("house_size"), CONVERSIONS.SQ_FEET_SQ_MEETRS)
        return row
    
    @staticmethod
    def is_valid_row(row) -> bool:
        """
        Here we want to check if some pieces of data are invalid
        
        Args:
            row  (dict) - row of data from the file that we want to process
        """
        important_fields = ["price", "rooms", "bathrooms", "land_area", "square_footage"]
        for field in important_fields:
            if row.get(field) in (None, ""):
                return False
        return True

    @staticmethod
    def is_allready_processed(file, path_to) -> bool:
        """
        Args:
            file (str) - file that we want to check
            path_to (str) - where we want to check if the file is already present
        Return:
            bool
        """
        list_processed_files = os.listdir(path_to)
        if file in list_processed_files:
            print("The file is already processed")
            return True
        return False

    @staticmethod
    def file_mover(path_from, path_to) -> None:
        """
        Args:
            path_from (str) - path where the file is currently located
            path_to (str) - path to the folder wherer we want to move the file
        """
        for file in os.listdir(path_from):
            #print(file)
            if file.endswith("zip"):
                print("Extraction in process...")
                filepath = os.path.join(path_from, file)
                try:
                    with ZipFile(filepath) as zip_file:
                        zip_file.extractall(path=path_to)
                        os.remove(filepath)
                        print("Extraction complete")
                        return 
                except Exception as e:
                    print(f"Failed to extract {file}: {e}")
                    path_to = os.path.join(basedir, DirPath.ERRORED)
                    shutil.move(filepath, path_to)
                
            elif file.endswith("csv"):
                print("Moving csv files...")
                filepath = os.path.join(path_from, file)
                shutil.move(filepath, path_to)
                print("Finished")
                return 
            
            else:
                continue

        print("Nothing to extract or move")
        return 
    
    @staticmethod
    def parsing_csv_file(db, models) -> None:
        """
        Args:
            db (:obj:) - database instace 
            models (:file:) - file where the classes for SQLAlchemy ORM are stored 

        """
        DataProcessing.is_processing = True
        path_to_folder = os.path.join(basedir, DirPath.STAGING)

        for file in os.listdir(path_to_folder):
            if DataProcessing.is_allready_processed(file, DirPath.PROCESSED):
                file_path = os.path.join(path_to_folder, file)
                os.remove(file_path)
                continue
            file_path = os.path.join(path_to_folder, file)
            before_parsing = time.time()

            with open(file_path, "r") as csv_file:
                print("Parsing the data...")
                reader = csv.DictReader(csv_file)
                headers = reader.fieldnames
                if not headers or "status" not in headers:
                    print("CSV file missing status or no headers at all")
                    path_to = os.path.join(basedir, DirPath.ERRORED)
                    shutil.move(file_path, path_to)
                    return

                for row in reader:
                    if row["status"] == "for_sale":
                        if DataProcessing.is_valid_row(row):
                            new_row = DataProcessing.set_dic_columns(row)
                            DataBaseCommunication.update_database(new_row, models, db)

            after_parsing = time.time()
            print("Time it took to parse the file: ", before_parsing - after_parsing)
            DataProcessing.file_mover(path_to_folder, DirPath.PROCESSED)
            DataProcessing.is_processing = False


    @staticmethod
    def data_proccesing(db, models, app):
            """
            Checks in the root directory if there are files for the processing, if there are moves them to staging area, after that it checks if
            the file was already proccesed, if it didnt, it proceeds

            Args:
                db (:obj:) - database instace 
                models (:file:) - file where the classes for SQLAlchemy ORM are stored 
                app (:obj:) - flask instance 

            """
                
            with app.app_context():
                staging_folder = os.path.join(basedir, DirPath.STAGING)
                DataProcessing.file_mover(basedir, DirPath.STAGING)
                if DataProcessing.is_processing == False and len(os.listdir(staging_folder)) > 0:
                    DataProcessing.parsing_csv_file(db, models) 
                else:
                    print("No data to process")       