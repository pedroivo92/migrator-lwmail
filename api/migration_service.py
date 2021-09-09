from flask import make_response, jsonify
from datetime import datetime
from http import HTTPStatus

from sqlalchemy import create_engine, exc
from sqlalchemy.sql import text, select
from cryptography.fernet import Fernet
import pytz
import re

from settings import *


class MigrationHandler:

    def __init__(self, migration_list):
        self.migration_list = migration_list
        self.engine = create_engine(DATABASE_CONNECTION_URL, pool_recycle=30, pool_pre_ping=True)
        self.database_conn = self.engine.connect()
        self.encrypt_session = Fernet(APPLICATION_SECRETS.encode('utf8'))

    def migration_handler(self):
        errors = self.validations()
        if not errors:
            return self.schedule_migration()

        return errors

    def validations(self):
        total_errors = []

        for item in self.migration_list:
            errors = []

            if not self._is_valid_email(item["current_email_address"]):
                errors.append({"campo": "current_email_address", "mensagem": "its not a valid email"})

            is_valid_password = self._is_valid_password(item["password"])
            if not is_valid_password[0]:
                errors.append({"campo": "password", "mensagem": is_valid_password[1]})

            if not self._is_valid_person_type(item["person_type"]):
                errors.append({"campo": "person_type", "mensagem": "person_type doesn't match with PF or PJ"})

            if not self._is_valid_company_name(item):
                errors.append({"campo": "company_name", "mensagem": "company_name must be declared"})

            if not self._is_valid_name(item):
                errors.append({"campo": "name", "mensagem": "invalid name"})

            if not self._is_valid_cnpj(item):
                errors.append({"campo": "cnpj", "mensagem": "invalid cnpj length or type"})

            if not self._is_valid_cpf(item):
                errors.append({"campo": "cpf", "mensagem": "invalid cpf length or type"})

            if not self._is_main_email(item["emails"]):
                errors.append({"campo": "email", "mensagem": "must have a main email"})

            if not self._is_valid_email_list(item["emails"]):
                errors.append({"campo": "email", "mensagem": "invalid email"})

            if not self._is_valid_addres(item["address"]):
                errors.append({"campo": "addres", "mensagem": "Invalid address"})

            if not self._is_valid_state(item["address"]):
                errors.append({"campo": "addres.state", "mensagem": "Must have 2 caracters"})

            if not self._is_valid_country(item["address"]):
                errors.append({"campo": "addres.country", "mensagem": "Must have 2 caracters"})

            if len(errors) > 0:
                total_errors.append({"id_globo": item["id_globo"], "divergencias": errors})

        if len(total_errors) > 0:
            return make_response(jsonify(total_errors), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        return None

    def schedule_migration(self):
        try:
            container_number = 0
            for item in self.migration_list:
                container_number += 1
                if container_number > int(CONTAINER_QUANTITY):
                    container_number = 1

                self._insert_migration_data(item, container_number)
                self._insert_address(item)
                self._insert_email(item)
                self._insert_phone(item)

        except exc.IntegrityError as e:
            code, message = e.orig.args
            self.database_conn.close()
            return {"error_message": message, "error_code": code}, HTTPStatus.BAD_REQUEST.value
        except Exception as e:
            self.database_conn.close()
            raise Exception(f"NotAcceptableFormatError: {e}")
        finally:
            self.database_conn.close()

        return "", HTTPStatus.ACCEPTED.value

    def migration_status(self):
        result = []
        try:

            for item in self.migration_list:
                sql_status = "m.id_globo, m.login, m.new_email_address, sm.id_status_migration, m.status_date, sm.description_status from migration m " \
                    "inner join status_migration sm on sm.id_status_migration = (CASE  WHEN m.id_status=4 THEN 2 ELSE m.id_status END) " \
                    "where m.id_globo = " + f"'{item['id_globo']}'"
                data = self.database_conn.execute(select(text(sql_status)))
                data = data.fetchone()
                if data is not None:
                    result.append(
                        {"id_globo": data["id_globo"], "login": data["login"], "email": data["new_email_address"],
                         "status_code": data["id_status_migration"], "status_name": data["description_status"],
                         "status_date": data["status_date"].strftime('%d/%m/%Y %H:%M:%S')})
                else:
                    result.append({"id_globo": item["id_globo"], "status_code": 4, "status_name": "Não Encontrado",
                                   "status_date": datetime.today().strftime('%d/%m/%Y %H:%M:%S')})
        except Exception as e:
            raise Exception(f"Exception: {e}")
        finally:
            self.database_conn.close()

        return make_response(jsonify(result), HTTPStatus.OK.value)
    
    def migration_status_v2(self):
        result = []
        try:

            for item in self.migration_list:
                response = self._get_migration_status_process(item)
                result.append(response)
                          
        except Exception as e:
            raise Exception(f"Exception: {e}")
        finally:
            self.database_conn.close()

        return make_response(jsonify(result), HTTPStatus.OK.value)

    def reprocess(self):
        try:
            for item in self.migration_list:
                self._update_process_information(item)
                          
        except Exception as e:
            raise Exception(f"Exception: {e}")
        finally:
            self.database_conn.close()

        return make_response("", HTTPStatus.OK.value)
    
    def submit_banner(self):
        try:
            for item in self.migration_list:
                self._insert_banner(item)

        except Exception as e:
            raise Exception(f"Exception: {e}")
        finally:
            self.database_conn.close()

        return make_response(jsonify({"result": "banner successfully submitted"}), HTTPStatus.OK.value)
        
    def banner_historic(self):
        result = []
        try:

            for item in self.migration_list:
                banner_historic = self._get_banner_historic(item)
                result.append(banner_historic)
                
        except Exception as e:
            raise Exception(f"Exception: {e}")
        finally:
            self.database_conn.close()

        return make_response(jsonify(result), HTTPStatus.OK.value)
    
    def _insert_migration_data(self, item, container_number):
        current_date = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%dT%H:%M:%S.%f')
        alias_email_address = item["alias_email_address"] if "alias_email_address" in item else ""
        rg = item["rg"]
        if not item["rg"] or item["rg"] == " ":
            rg = "9999999999"

        container_id = f'c{container_number}'
        item['password'] = self._encrypt_password(item)

        if item["person_type"].upper() == "PF":
            query = "INSERT INTO migration (id_globo, person_type, current_email_address, alias_email_address, password, name, cpf, rg, id_status, status_date, container_id) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '1', %s, %s)"

            data = (item["id_globo"], item["person_type"], item["current_email_address"], alias_email_address,
                    item["password"], item["name"], item["cpf"], rg, current_date, container_id)
        else:
            query = "INSERT INTO migration (id_globo, person_type, current_email_address, alias_email_address, password, name, rg, company_name, cnpj, cpf, id_status, status_date, container_id) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '1', %s, %s)"

            data = (item["id_globo"], item["person_type"], item["current_email_address"], alias_email_address,
                    item["password"], item["name"], rg, item["company_name"], item["cnpj"], item["cpf"], current_date, container_id)

        self.database_conn.execute(query, data)

    def _insert_phone(self, item):
        for phone in item["phones"]:
            phone["number"] = phone["number"].replace("-", "")
            phone["number"] = phone["number"][2:]
            if len(phone["number"]) not in [10, 11] or not phone["number"].isdigit() \
                    or not phone["number"] or phone["number"] == " ":
                phone["number"] = '11999999090'

            query = "INSERT INTO phone (id_migration, phone_number) VALUES (%s, %s)"
            data = (item["id_globo"], phone["number"])
            self.database_conn.execute(query, data)

    def _insert_email(self, item):
        for email in item["emails"]:
            query = "INSERT INTO email (id_migration, email_address, main, confirmed) VALUES (%s, %s, %s, %s)"
            data = (item["id_globo"], email["address"], 1 if email["main"] else 0, 1 if email["confirmed"] else 0)
            self.database_conn.execute(query, data)

    def _insert_address(self, item):
        if not any(item["address"].values()):
            item["address"]["city"] = "Sao Paulo"
            item["address"]["state"] = "SP"
            item["address"]["postal_code"] = "05707-001"
            item["address"]["country"] = "BR"
            item["address"]["number"] = "2434"
            item["address"]["street"] = "Rua Itapaiuma"

        query = "INSERT INTO address (id_migration, city, state, postal_code, country, number, street) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)"

        data = (item["id_globo"], item["address"]["city"], item["address"]["state"], item["address"]["postal_code"],
                        item["address"]["country"], item["address"]["number"], item["address"]["street"])

        self.database_conn.execute(query, data)
    
    def _insert_banner(self, item):
        query = "INSERT INTO integratordb.banners (id_migration, current_email_address, message, " \
                "background_color, message_link, redirect_link, titulo_alert, message_alert, message_link_alert, redirect_link_alert) VALUES " \
                f"('{item['id_migration']}', '{item['current_email_address']}', '{item['message']}', '{item['background_color']}', " \
                f"'{item['message_link']}', '{item['redirect_link']}', '{item['titulo_alert']}', '{item['message_alert']}', " \
                f"'{item['message_link_alert']}', '{item['redirect_link_alert']}') " \
                "ON DUPLICATE KEY UPDATE " \
                f"message = '{item['message']}', background_color = '{item['background_color']}', " \
                f"message_link = '{item['message_link']}', redirect_link = '{item['redirect_link']}', " \
                f"titulo_alert = '{item['titulo_alert']}', message_alert = '{item['message_alert']}', " \
                f"message_link_alert = '{item['message_link_alert']}', redirect_link_alert = '{item['redirect_link_alert']}'"

        self.database_conn.execute(text(query))
    
    def _get_migration_status_process(self, item):
        query = "m.id_globo, m.login, m.new_email_address, sm.id_status_migration, m.status_date, " \
                "sm.description_status, ps.error_description, ps.id_stage from migration m " \
                "inner join status_migration sm on sm.id_status_migration = (CASE  WHEN m.id_status=4 THEN 2 ELSE m.id_status END) " \
                "left join process ps on m.id_globo = ps.id_migration " \
                "where m.id_globo = " + f"'{item['id_globo']}'"
                
        data = self.database_conn.execute(select(text(query)))
        data = data.fetchone()

        if data is not None:
            description_stage = self._get_stage_description(data["id_stage"])
            result = {
                "id_globo": data["id_globo"], "login": data["login"], "email": data["new_email_address"],
                "status_code": data["id_status_migration"], "status_name": data["description_status"], "stage_description": description_stage,
                "error_description": data["error_description"], "status_date": data["status_date"].strftime('%d/%m/%Y %H:%M:%S')
            }
        else:
            result = {
                "id_globo": item["id_globo"], "status_code": 4, "status_name": "Não Encontrado",
                "status_date": datetime.today().strftime('%d/%m/%Y %H:%M:%S')
            }
        
        return result
    

    def _get_banner_historic(self, item):
        query = "SELECT * FROM integratordb.status_banner " \
                f"WHERE id_globo = '{item['id_globo']}'"
        data = self.database_conn.execute(text(query))
        data = data.fetchone()
        if data is not None:
            return {"id_globo": data["id_globo"], "current_email_address": data["current_email_address"], "count_clique_message": data["count_clique_message"], 
                    "first_date_clique": data["first_date_clique"].strftime('%d/%m/%Y %H:%M:%S'), "last_date_clique": data["last_date_clique"].strftime('%d/%m/%Y %H:%M:%S')}
        else:
            return {"id_globo": item["id_globo"], "banner_historic": "Não Encontrado"}
    
    def _update_process_information(self, item):
        query = f"UPDATE integratordb.process SET reprocess = 1 WHERE id_migration = '{item['id_globo']}'"

        if item['id_globo'] == "":
            query = f"UPDATE integratordb.process SET reprocess = 1 WHERE id_migration != '0'"

        self.database_conn.execute(text(query))

    def _is_valid_email(self, email):
        if not re.match(
                "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",
                email):
            return False

        return True

    def _is_valid_password(self, password):
        if len(password) < 12:
            return False, "password size is less than 12 characters"
        elif re.search('[0-9]', password) is None:
            return False, "password doesn't have a number"
        elif re.search('[A-Z]', password) is None:
            return False, "password doesn't have a uppercase letter"
        elif re.search('[a-z]', password) is None:
            return False, "password doesn't have a lowercase letter"
        elif re.search('[^\w\*]', password) is None:
            return False, "password doesn't have a special character"
        else:
            return True, "password seems fine"

    def _is_valid_person_type(self, person_type):
        if person_type.upper() != "PF" and person_type.upper() != "PJ":
            return False

        return True

    def _is_valid_company_name(self, person):
        if person["person_type"].upper() == "PF" or person[
            "person_type"].upper() == "PJ" and "company_name" in person and \
                person["company_name"] is not None and person["company_name"].replace(" ", "") != "":
            return True

        return False

    def _is_valid_name(self, person):
        name = person["name"].split()

        if len(name) >= 2:
            return True

        return False

    def _is_valid_cnpj(self, person):
        if person["person_type"].upper() == "PF" or person["person_type"].upper() == "PJ" and "cnpj" in person and \
                person["cnpj"] is not None and isinstance(person["cnpj"], str) and \
                len(person["cnpj"]) == 14 and person["cnpj"].isdigit():
            return True

        return False

    def _is_valid_cpf(self, person):
        if person["person_type"].upper() == "PJ" or person["person_type"].upper() == "PF" and "cpf" in person and \
                person["cpf"] is not None and isinstance(person["cpf"], str) and \
                len(person["cpf"]) == 11 and person["cpf"].isdigit():
            return True

        return False

    def _is_main_email(self, email_list):
        valid_email = False
        for email in email_list:
            if email["main"] == True:
                valid_email = True
                break

        if valid_email:
            return True

        return False

    def _is_valid_email_list(self, email_list):
        invalid = False
        for email in email_list:
            if not re.match(
                    "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",
                    email["address"]):
                invalid = True
                break

        if invalid:
            return False

        return True

    def _is_valid_addres(self, addres):
        if not any(addres.values()):
            return True

        nones = not all(addres.values())

        if nones:
            return False

        return True

    def _is_valid_state(self, addres):
        if len(addres['state']) > 2:
            return False

        return True

    def _is_valid_country(self, addres):
        if len(addres['country']) > 2:
            return False

        return True

    def _encrypt_password(self, item):
        cipher_pass = self.encrypt_session.encrypt(item['password'].encode('utf8'))
        return cipher_pass.decode('utf8')

    def _get_stage_description(self, id_stage):
        if id_stage == 1:
            return 'CAPI: Create Customer'
        
        if id_stage == 2:
            return 'CAPI: Get Customer by ID'
        
        if id_stage == 3:
            return 'Bluebird: Create Payment Method'

        if id_stage == 4:
            return 'Bluebird: Create Cart'

        if id_stage == 5:
            return 'Bluebird: Checkout Cart'
        
        if id_stage == 6:
            return 'AKAKO: Create Akako Customer'
        
        if id_stage == 7:
            return 'Globomail Procedure'
        
        if id_stage == 8:
            return 'Roundcube Procedure'
        
        if id_stage == 9:
            return 'Notification Service'
        
        return None