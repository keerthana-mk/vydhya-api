import os
from passlib.totp import TOTP
import logging
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import mail_config, templates
from databases.db_models.users import UserLogin, UserProfile
from databases.repository.users import UserProfileRepository, UserLoginRepository
from pathlib import Path
from typing import Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime
from services.authentication.default_auth_service import DefaultAuthentication
class ResetPasswordServices:
            
    @staticmethod
    def generate_otp():
        
        otp = TOTP('s3jdvb7qd2r7jpxx', digits=int(os.getenv("SECRET_CODE_LEN")), period=(60*15))
        token = otp.generate()
        logging.info(f'token generated={token}')
        return token.token, datetime.now().strftime('%y-%m-%d %H:%M:%S')
    
    @staticmethod
    async def generate_reset_password_email(user_id, email):
        
        reset_code, expiry = ResetPasswordServices.generate_otp()
        reset_details = {"reset_code" : reset_code,
                         "reset_expiry" : expiry}
        # logging.info(f'reset_code: {reset_code, expiry}')
        
        subject = ' Reset Password for Vydhya Account'
        body = f'<p> Dear User,</p> \
                <p> Your reset code is {reset_code}. <br/>\
                Do not share your password.</p>\
                Regards, <br> \
                <i>Vydhya team</i> \
                '
        # body = {'title' : 'You have requested for reset password',
        #         'name' : 'The code to reset your password is: {}'.format(reset_code)}

        # await ResetPasswordServices.send_reset_email(subject, email_to, body)
        print("otp from genrate mail")
        message = MessageSchema(
            subject = subject,
            recipients = [email],
            body = body,
            subtype ='html',              
        )
        fm = FastMail(mail_config)    
        print("in send_reset_email ")   
        return_value = await fm.send_message(message, template_name="reset_password.html")
        logging.info(f'send_message returned: {return_value}')
        UserLoginRepository.update_reset_code(user_id, reset_details)

        
           
    @staticmethod
    async def send_reset_email(subject: str, email_to:str, body:dict):
        message = MessageSchema(
            subject = subject,
            recipients = [email_to],
            body = body,
            subtype ='html',              
        )
        fm = FastMail(mail_config)    
        print("in send_reset_email ")   
        await fm.send_message(message, template_name="reset_password.html")
        
    @staticmethod
    def update_reset_code_db(user_id, reset_details):
        UserLoginRepository.update_reset_code(user_id, reset_details)
        logging.info ("queryresults from resetpassword:{}".format(query_result))
        return query_result
    
    @staticmethod
    def verify_update_password(user_id, reset_code_details):
        try:
            query = UserLoginRepository.get_user_login(user_id)
            if query is None:
                raise Exception('user_id does not exist')
            # print("reset_code_details", reset_code_details, query)
            reset_code, expiry_date = query.reset_code, query.reset_expiry
            if reset_code is None or reset_code=='':
                raise Exception('reset code is empty')
            if reset_code_details.reset_code != reset_code:
                raise Exception('Reset code does not match')
            date_format_str = '%y-%m-%d %H:%M:%S'
            difference =( datetime.strptime(datetime.now().strftime(date_format_str), date_format_str) - datetime.strptime(expiry_date, date_format_str)).total_seconds()/60
            # print(f"In verify_update_password Reset code ={reset_code} and reset_expiry={expiry_data}")
            # print(f"In verify_update_password Reset code ={reset_code_details['reset_code']} and reset_expiry={expiry_date}")
            hashed_password = DefaultAuthentication.generate_hash(reset_code_details.user_password)
            if difference>15:
                error_message =f'Reset code has expired. generate new reset code'
                raise Exception(error_message)
            password_details ={'user_password':hashed_password,
                               'updated_at' : datetime.now().strftime('%y-%m-%d %H:%M:%S')}
            
            UserLoginRepository.update_password(user_id, password_details)
        except Exception as e:
            raise e
        return {"message":"Password reset successful"}
    
        