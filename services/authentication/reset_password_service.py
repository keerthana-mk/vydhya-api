import os
from passlib.totp import TOTP
import logging


class ResetPasswordServices:
    
    @staticmethod
    def generate_email_otp(email):
        otp = generate_otp(user_id, role)
        generate_reset_password_email(user_id, role, otp, email)
        
    @staticmethod
    def generate_otp(user_id, role):
        
        otp = TOTP('s3jdvb7qd2r7jpxx', digits=int(os.getenv("SECRET_CODE_LEN")))
        token = otp.generate()
        logging.info("token generated=",token.token)
        return token.token
    
    @staticmethod
    def generate_reset_password_email(user_id, role, email, reset_code):
        
        reset_code = ResetPasswordServices().generate_otp(user_id, role)
        
        
    
        