# -*- coding: utf-8 -*-

import json
import os
import random
import unicodedata
import unittest
from datetime import datetime, timedelta
from sqlite3 import Connection as SQLite3Connection

import six
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ProgrammingError

from app import LOGGER, app, db
from app.applicationModel.models import (ApplicationForm, Question, QuestionTranslation, Section,
                                         SectionTranslation)
from app.events.models import Event, EventType
from app.invitedGuest.models import InvitedGuest
from app.organisation.models import Organisation
from app.registration.models import Offer, RegistrationForm
from app.responses.models import Answer, Response, ResponseReviewer, ResponseTag
from app.users.models import AppUser, Country, UserCategory
from app.email_template.models import EmailTemplate
from app.reviews.models import ReviewConfiguration, ReviewForm, ReviewResponse, ReviewQuestion, ReviewQuestionTranslation, ReviewScore
from app.tags.models import Tag, TagTranslation


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

titles = ('Mr', "Ms", 'Mrs', 'Dr', 'Prof', 'Rev', 'Mx')

def strip_accents(text):
    """
    Strip accents from input.
    Helper function to create 'clean' emails
        see https://stackoverflow.com/a/518232/5209000

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = six.ensure_text(text)
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    return str(text)

class ApiTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ApiTestCase, self).__init__(*args, **kwargs)
        self.test_users = []
        self.firstnames = []
        self.lastnames = []

    def _get_names(self):
        """Retrieve a list of names from a text file for testing"""
        if len(self.firstnames):
            return self.firstnames, self.lastnames

        if os.path.exists("/code/api/app/utils/names.txt"):
            with open("/code/api/app/utils/names.txt") as file_with_names:
                names = file_with_names.readlines()
            names = [n.decode('utf-8', 'replace') for n in names]
        else:
            # why yes, these are names of African Hollywood actors (according to Wikipedia)
            names = ["Mehcad Brooks", "Malcolm Barrett", "Nick Cannon", "Lamorne Morris", "Neil Brown Jr.",
                     "William Jackson Harper", "Marques Houston", "Jennifer Hudson", "Alicia Keys", "Meghan Markle",
                     "Beyonce Knowles", "Jesse Williams", "Lance Gross", "Hosea Chanchez", "Daveed Diggs",
                     "Damon Wayans Jr.", "Columbus Short", "Terrence Jenkins", "Ron Funches", "Jussie Smollett",
                     "Donald Glover", "Brian Tyree Henry", "Gabourey Sidibe", "Trai Byers", "Robert Ri'chard",
                     "Arjay Smith", "Tessa Thompson", "J.Lee", "Lauren London", "DeVaughn Nixon", "Rob Brown", ]
        for _name in names:
            split_name = _name.strip().split(" ")
            self.firstnames.append(split_name[0])
            lastname = " ".join(split_name[1:]) if len(split_name) > 1 else ""
            self.lastnames.append(lastname)
        return self.firstnames, self.lastnames

    def add_user(self, 
                 email='user@user.com', 
                 firstname='User', 
                 lastname='Lastname', 
                 user_title='Mrs',
                 password='abc',
                 organisation_id=1,
                 is_admin=False,
                 post_create_fn=lambda x: None):
        user = AppUser(email,
                 firstname,
                 lastname,
                 user_title,
                 password,
                 organisation_id,
                 is_admin)
        user.verify()

        post_create_fn(user)

        db.session.add(user)
        db.session.commit()
        self.test_users.append(user)
        return user

    def add_n_users(self, n,
                    password='abcd',
                    organisation_id=1,
                    is_admin=False,
                    post_create_fn=lambda x: None):
        firstnames, lastnames = self._get_names()
        users = []

        for i in range(n):
            title = random.choice(titles)
            firstname = random.choice(firstnames)
            lastname = random.choice(lastnames)
            email = "{firstname}.{lastname}{num}@bestemail.com".format(firstname=firstname,
                                                                       lastname=lastname if lastname != "" else "x",
                                                                       num=len(self.test_users))
            email = strip_accents(email)
            user = self.add_user(email, firstname, lastname, title, password, organisation_id, is_admin, post_create_fn)
            users.append(user)

        return users

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.reflect()
        db.drop_all()
        db.create_all()
        LOGGER.setLevel('ERROR')

        # Add dummy metadata
        self.user_category = UserCategory('Postdoc')
        db.session.add(self.user_category)
        self.country = Country('South Africa')
        db.session.add(self.country)

        # Add a dummy organisation
        self.add_organisation(domain='org')
        db.session.flush()

    def add_organisation(self, name='My Org', system_name='Baobab', small_logo='org.png', 
                                    large_logo='org_big.png', icon_logo='org_icon.png', domain='com', url='www.org.com',
                                    email_from='contact@org.com', system_url='baobab.deeplearningindaba.com',
                                    privacy_policy='PrivacyPolicy.pdf', languages=[{"code": "en", "description": "English"}]):
        org = Organisation(name, system_name, small_logo, large_logo, icon_logo, domain, url, email_from, system_url, privacy_policy, languages)
        db.session.add(org)
        db.session.commit()
        return org

    def add_country(self):
        country = Country('South Africa')
        db.session.add(country)
        db.session.commit()
        return country
    
    def add_category(self):
        category = UserCategory('Student')
        db.session.add(category)
        db.session.commit()
        return category

    def add_event(self, 
                 name ={'en': 'Test Event'}, 
                 description = {'en': 'Event Description'}, 
                 start_date = datetime.now() + timedelta(days=30), 
                 end_date = datetime.now() + timedelta(days=60),
                 key = 'INDABA2025',
                 organisation_id = 1, 
                 email_from = 'abx@indaba.deeplearning', 
                 url = 'indaba.deeplearning',
                 application_open = datetime.now(),
                 application_close = datetime.now() + timedelta(days=10),
                 review_open = datetime.now() ,
                 review_close = datetime.now() + timedelta(days=15),
                 selection_open = datetime.now(),
                 selection_close = datetime.now() + timedelta(days=15),
                 offer_open = datetime.now(),
                 offer_close = datetime.now(),
                 registration_open = datetime.now(),
                 registration_close = datetime.now() + timedelta(days=15),
                 event_type = EventType.EVENT,
                 travel_grant = False):

        event = Event(name, description, start_date,  end_date, key,  organisation_id,  email_from,  url, 
                      application_open, application_close, review_open, review_close, selection_open, 
                      selection_close, offer_open,  offer_close, registration_open, registration_close, event_type,
                      travel_grant)
        db.session.add(event)
        db.session.commit()
        return event

    def add_review_config(self, review_form_id=1, num_reviews_required=1, num_optional_reviews=1):
        review_config = ReviewConfiguration(
            review_form_id=review_form_id, 
            num_reviews_required=num_reviews_required, 
            num_optional_reviews=num_optional_reviews)
        db.session.add(review_config)
        db.session.commit()
        return review_config

    def add_review_form(self, application_form_id=1, deadline=None):
        deadline = deadline or datetime.now()
        review_form = ReviewForm(application_form_id, deadline)
        db.session.add(review_form)
        db.session.commit()
        return review_form

    def add_review_question(self, review_form_id, headings=None, weight=0):
        headings = headings or {
            'en': 'Heading En',
            'fr': 'Heading Fr'
        }
        
        review_question = ReviewQuestion(review_form_id, None, type='short-text', is_required=True, order=1, weight=weight)
        db.session.add(review_question)
        db.session.commit()

        db.session.add_all([
            ReviewQuestionTranslation(review_question.id, k, headline=v)
            for k, v in headings.iteritems()
        ])
        db.session.commit()

        return review_question

    def add_email_template(self, template_key, template='This is an email', language='en', subject='Subject', event_id=None):
        email_template = EmailTemplate(template_key, event_id, subject, template, language)
        db.session.add(email_template)
        db.session.commit()
        return email_template

    def get_auth_header_for(self, email, password='abc'):
        body = {
            'email': email,
            'password': password
        }
        response = self.app.post('api/v1/authenticate', data=body)
        data = json.loads(response.data)
        header = {'Authorization': data['token']}
        return header

    def add_to_db(self, obj):
        db.session.add(obj)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.reflect()
        db.drop_all()

    def create_application_form(self,
                            event_id = 1,
                            is_open = True,
                            nominations = False):
                            
        application_form = ApplicationForm(event_id, is_open, nominations)
        db.session.add(application_form)
        db.session.commit()
        return application_form

    def create_registration_form(self, event_id=1):
        registration_form = RegistrationForm(event_id)
        db.session.add(registration_form)
        db.session.commit()
        return registration_form
    
    def add_section(self, application_form_id, order=1):
        section = Section(application_form_id, order)
        db.session.add(section)
        db.session.commit()
        return section
    
    def add_section_translation(
        self,
        section_id,
        language,
        name='Section Name',
        description='Section Description',
        show_for_values=None):
        section_translation = SectionTranslation(section_id, language, name, description, show_for_values)
        db.session.add(section_translation)
        db.session.commit()
        return section_translation

    def add_question(
        self,
        application_form_id,
        section_id,
        order=1,
        question_type='short-text'):
        question = Question(application_form_id, section_id, order, question_type)
        db.session.add(question)
        db.session.commit()
        return question

    def add_question_translation(self,
        question_id,
        language,
        headline='Question Headline',
        description=None,
        placeholder=None,
        validation_regex=None,
        validation_text=None,
        options=None,
        show_for_values=None):
        question_translation = QuestionTranslation(
            question_id,
            language,
            headline,
            description,
            placeholder,
            validation_regex,
            validation_text,
            options,
            show_for_values)
        db.session.add(question_translation)
        db.session.commit()
        return question_translation
    
    def add_response(self, application_form_id, user_id, is_submitted=False, is_withdrawn=False, language='en'):
        response = Response(application_form_id, user_id, language)
        if is_submitted:
            response.submit()
        if is_withdrawn:
            response.withdraw()

        db.session.add(response)
        db.session.commit()
        return response
    
    def add_response_reviewer(self, response_id, reviewer_user_id):
        rr = ResponseReviewer(response_id, reviewer_user_id)
        db.session.add(rr)
        db.session.commit()
        return rr

    def add_answer(self, response_id, question_id, answer_value):
        answer = Answer(response_id, question_id, answer_value)
        db.session.add(answer)
        db.session.commit()
        return answer

    def add_review_response(self, reviewer_user_id, response_id, review_form_id=1, language='en', is_submitted=False):
        rr = ReviewResponse(review_form_id, reviewer_user_id, response_id, language)
        if is_submitted:
            rr.submit()
        db.session.add(rr)
        db.session.commit()

        return rr

    def add_review_score(self, review_response_id, review_question_id, value):
        rs = ReviewScore(review_question_id, value)
        rs.review_response_id = review_response_id
        db.session.add(rs)
        db.session.commit()
        return rs

    def add_offer(self, user_id, event_id=1, offer_date=None, expiry_date=None, payment_required=False, travel_award=False, accommodation_award=False, candidate_response=None):
        offer_date = offer_date or datetime.now()
        expiry_date = expiry_date or datetime.now() + timedelta(10)

        offer = Offer(
            user_id=user_id, 
            event_id=event_id, 
            offer_date=offer_date, 
            expiry_date=expiry_date,
            payment_required=payment_required,
            travel_award=travel_award,
            accommodation_award=accommodation_award,
            candidate_response=candidate_response)

        db.session.add(offer)
        db.session.commit()
        return offer

    def add_invited_guest(self, user_id, event_id=1, role='Guest'):
        print('Adding invited guest for user: {}, event: {}, role: {}'.format(user_id, event_id, role))
        guest = InvitedGuest(event_id, user_id, role)
        db.session.add(guest)
        db.session.commit()
        return guest

    def add_tag(self, event_id=1, names={'en': 'Tag 1 en', 'fr': 'Tag 1 fr'}):
        tag = Tag(event_id)
        db.session.add(tag)
        db.session.commit()
        translations = [
            TagTranslation(tag.id, k, name) for k, name in names.iteritems()
        ]
        db.session.add_all(translations)
        db.session.commit()
        return tag

    def tag_response(self, response_id, tag_id):
        rt = ResponseTag(response_id, tag_id)
        db.session.add(rt)
        db.session.commit()
        return rt
