from time import time
import traceback
from flask import make_response, render_template
from flask_restful import Resource
from libs.mailgun import MailgunException
from libs.strings import get_text
from models.confirmation import ConfirmationModel
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        '''Returns html page confirming registeration/ account activation'''
        confirmation = ConfirmationModel.find_by_id(confirmation_id)

        if not confirmation:
            return {"message": get_text("confirmation_not_found")}, 404

        if confirmation.expired:
            return {"message": get_text("confirmation_link_expired")}, 400

        if confirmation.confirmed:
            return {"message": get_text("confirmation_already_confirmed")}, 400

        confirmation.confirmed = True
        confirmation.save_to_database()

        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email = confirmation.user.email),
            200,
            headers
        )
    

class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        '''Returns confirmations for a given user. Used for testing api.'''
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': get_text("user_not_found")}, 404
        
        return (
            {
                "current_time": int(time()),
                "confirmation": [
                    confirmation_schema.dump(each) for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )

    @classmethod
    def post(cls, user_id: int):
        '''Resends confirmation email to a user if required'''
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': get_text("user_not_found")}, 404

        try:
            confirmation = user.most_recent_confirmation
            #if confirmation model already exists, make sure it's invalid and return already confirmed
            if confirmation:
                if confirmation.confirmed:
                    return {'message': get_text("confirmation_already_confirmed")}, 400
                #if not confirmed yet, expire the existing link forcefully before creating a fresh link
                #force_to_expire validates the latest confirmation and forces the prev one to expire 
                confirmation.force_to_expire()
                
            #create a new confirmation -> save it to database -> send new confirmation email to user
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_database()
            user.send_confirmation_email()
            return {'message': get_text("confirmation_resend_successful")}, 201
        
        except MailgunException as e:
            return {'message': str(e)}, 500
        except:
            traceback.print_exc()
            return {'message': get_text("confirmation_resend_fail")}, 500

        
        
    