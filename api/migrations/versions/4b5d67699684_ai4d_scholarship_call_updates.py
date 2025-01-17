# -*- coding: utf-8 -*-

"""AI4D Scholarship Call Updates

Revision ID: 4b5d67699684
Revises: 49d55031108e
Create Date: 2020-11-06 21:08:35.496509

"""

# revision identifiers, used by Alembic.
revision = '4b5d67699684'
down_revision = '49d55031108e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import select
from sqlalchemy.orm import column_property
from app import db
import datetime
from enum import Enum

Base = declarative_base()

class Organisation(Base):

    __tablename__ = "organisation"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    system_name = db.Column(db.String(50), nullable=False)
    small_logo = db.Column(db.String(100), nullable=False)
    large_logo = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    email_from = db.Column(db.String(100), nullable=True)
    system_url = db.Column(db.String(100), nullable=False)

    def __init__(self, name, system_name, small_logo, large_logo, domain, url, email_from, system_url):
        self.name = name
        self.small_logo = small_logo
        self.large_logo = large_logo
        self.domain = domain
        self.system_name = system_name
        self.url = url
        self.email_from = email_from
        self.system_url = system_url

class Country(Base):
    __tablename__ = "country"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

class EventType(Enum):
    EVENT = 'event'
    AWARD = 'award'
    CALL = 'call'


class Event(Base):

    __tablename__ = "event"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)
    key = db.Column(db.String(255), nullable=False, unique=True)
    organisation_id = db.Column(db.Integer(), db.ForeignKey('organisation.id'), nullable=False)
    email_from = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    application_open = db.Column(db.DateTime(), nullable=False)
    application_close = db.Column(db.DateTime(), nullable=False)
    review_open = db.Column(db.DateTime(), nullable=False)
    review_close = db.Column(db.DateTime(), nullable=False)
    selection_open = db.Column(db.DateTime(), nullable=False)
    selection_close = db.Column(db.DateTime(), nullable=False)
    offer_open = db.Column(db.DateTime(), nullable=False)
    offer_close = db.Column(db.DateTime(), nullable=False)
    registration_open = db.Column(db.DateTime(), nullable=False)
    registration_close = db.Column(db.DateTime(), nullable=False)
    event_type = db.Column(db.Enum(EventType), nullable=False)
    travel_grant = db.Column(db.Boolean(), nullable=False)
    miniconf_url = db.Column(db.String(100), nullable=True)

    event_translations = db.relationship('EventTranslation', lazy='dynamic')

    def __init__(
        self,
        names,
        descriptions,
        start_date,
        end_date,
        key,
        organisation_id,
        email_from,
        url,
        application_open,
        application_close,
        review_open,
        review_close,
        selection_open,
        selection_close,
        offer_open,
        offer_close,
        registration_open,
        registration_close,
        event_type,
        travel_grant,
        miniconf_url=None
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.key = key
        self.organisation_id = organisation_id
        self.email_from = email_from
        self.url = url
        self.application_open = application_open
        self.application_close = application_close
        self.review_open = review_open
        self.review_close = review_close
        self.selection_open = selection_open
        self.selection_close = selection_close
        self.offer_open = offer_open
        self.offer_close = offer_close
        self.registration_open = registration_open
        self.registration_close = registration_close
        self.event_roles = []
        self.event_type = event_type
        self.travel_grant = travel_grant
        self.miniconf_url = miniconf_url

        self.add_event_translations(names, descriptions)

    def add_event_translations(self, names, descriptions):
        for language in names:
            name = names[language]
            description = descriptions[language]
            event_translation = EventTranslation(name, description, language)
            self.event_translations.append(event_translation)

class EventTranslation(Base):

    __tablename__ = "event_translation"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    event_id = db.Column(db.Integer(), db.ForeignKey("event.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(2))

    event = db.relationship('Event', foreign_keys=[event_id])

    def __init__(self, name, description, language):
        self.name = name
        self.description = description
        self.language = language

class ApplicationForm(Base):
    __tablename__ = 'application_form'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('event.id'), nullable=False)
    is_open = db.Column(db.Boolean(), nullable=False)
    nominations = db.Column(db.Boolean(), nullable=False)

    def __init__(self, event_id, is_open, nominations):
        self.event_id = event_id
        self.is_open = is_open
        self.nominations = nominations

class Question(Base):
    __tablename__ = 'question'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    application_form_id = db.Column(db.Integer(), db.ForeignKey('application_form.id'), nullable=False)
    section_id = db.Column(db.Integer(), db.ForeignKey('section.id'), nullable=False)
    type = db.Column(db.String(), nullable=False)
    order = db.Column(db.Integer(), nullable=False)
    is_required = db.Column(db.Boolean(), nullable=False)
    depends_on_question_id = db.Column(db.Integer(), db.ForeignKey('question.id'), nullable=True)
    key = db.Column(db.String(255), nullable=True)

    question_translations = db.relationship('QuestionTranslation', lazy='dynamic')

    def __init__(self, application_form_id, section_id, order, questionType, is_required=True):
        self.application_form_id = application_form_id
        self.section_id = section_id
        self.order = order
        self.type = questionType
        self.is_required = is_required

    def get_translation(self, language):
        question_translation = self.question_translations.filter_by(language=language).first()
        return question_translation


class Section(Base):
    __tablename__ = 'section'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    application_form_id = db.Column(db.Integer(), db.ForeignKey('application_form.id'), nullable=False)
    order = db.Column(db.Integer(), nullable=False)
    depends_on_question_id = db.Column(db.Integer(), db.ForeignKey('question.id', use_alter=True), nullable=True)
    key = db.Column(db.String(255), nullable=True)

    section_translations = db.relationship('SectionTranslation', lazy='dynamic')

    def __init__(self, application_form_id, order, depends_on_question_id=None, key=None):
        self.application_form_id = application_form_id
        self.order = order
        self.depends_on_question_id = depends_on_question_id
        self.key = key

    def get_translation(self, language):
        section_translation = self.section_translations.filter_by(language=language).first()
        return section_translation


class SectionTranslation(Base):
    __tablename__ = 'section_translation'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    section_id = db.Column(db.Integer(), db.ForeignKey('section.id'), nullable=False)
    language = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(), nullable=False)
    show_for_values = db.Column(db.JSON(), nullable=True)

    section = db.relationship('Section', foreign_keys=[section_id])

    def __init__(self, section_id, language, name, description, show_for_values=None):
        self.section_id = section_id
        self.language = language
        self.name = name
        self.description = description
        self.show_for_values = show_for_values


class QuestionTranslation(Base):
    __tablename__ = 'question_translation'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    question_id = db.Column(db.Integer(), db.ForeignKey('question.id'), nullable=False)
    language = db.Column(db.String(2), nullable=False)
    headline = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    placeholder = db.Column(db.String(), nullable=True)
    validation_regex = db.Column(db.String(), nullable=True)
    validation_text = db.Column(db.String(), nullable=True)
    options = db.Column(db.JSON(), nullable=True)
    show_for_values = db.Column(db.JSON(), nullable=True)

    question = db.relationship('Question', foreign_keys=[question_id])

    def __init__(
        self,
        question_id,
        language,
        headline,
        description=None,
        placeholder=None,
        validation_regex=None,
        validation_text=None,
        options=None,
        show_for_values=None
    ):
        self.question_id = question_id
        self.language = language
        self.headline = headline
        self.description = description
        self.placeholder = placeholder
        self.validation_regex = validation_regex
        self.validation_text = validation_text
        self.options = options
        self.show_for_values = show_for_values


def upgrade():
    Base.metadata.bind = op.get_bind()
    session = orm.Session(bind=Base.metadata.bind)

    event = session.query(Event).filter_by(key='prc').first()
    form = session.query(ApplicationForm).filter_by(event_id=event.id).first()

    en = (session.query(SectionTranslation)
        .filter_by(language='en', name='AI4D Call for Proposals: Scholarships program manager')
        .first())

    fr = (session.query(SectionTranslation)
        .filter_by(language='fr', name=u'Appel à propositions IAPD: Gestionnaire des programmes de bourses')
        .first())

    en.description = """The International Development Research Centre (IDRC) and the Swedish International Development Agency (Sida) invite proposals from qualified institutions to manage the African Artificial Intelligence for Development (AI4D) Scholarships program.  

**The goal of this call is to identify a program and financial manager for the AI4D Scholarships program**. The host institution (“scholarships manager”) will design and administer a scholarships program that will foster the talent needed to meet a growing demand for responsible Artificial Intelligence (“AI”) for development research and innovation in African public universities. The program will support two scholarship activities: (i) the African AI4D PhD Scholarships and (ii) the African AI4D Advanced Scholars Program. The African AI4D Scholarships program will provide support to the next generation of AI and related disciplines (such as machine learning) academics, practitioners and students who are focused on responsible AI innovation for sustainable development. Responsible AI strives to be inclusive, rights-based and sustainable in its development and implementation, ensuring that AI applications are leveraged for public benefit.1  

For eligibility criteria, please see [www.ai4d.ai/calls](www.ai4d.ai/calls)
For the Scholarships Manager Call for Proposals, see: [https://bit.ly/3l5OJfN](https://bit.ly/3l5OJfN)
For the full AI4D background document, see: [https://resources.ai4d.ai/files/AI4D_Proposal.pdf](https://resources.ai4d.ai/files/AI4D_Proposal.pdf)

For all questions, email social@ai4d.ai

**The deadline for submission of the proposal online is 23:59 EST on December 8, 2020.**

"""

    fr.description = u"""**Le présent appel a pour objectif de désigner un gestionnaire de programme et directeur financier pour le programme de bourses d’études en IAPD**. L’institution d’accueil (« gestionnaire de bourses ») concevra et administrera un programme de bourses d’études qui favorisera le développement des talents nécessaires pour répondre à une demande croissante en recherche et en innovation dans le domaine de l’intelligence artificielle (« IA ») responsable pour le développement dans les universités publiques africaines. Le programme soutiendra deux activités d’allocation de bourses : (i) les bourses de doctorat africaines en IAPD et (ii) le programme de bourses avancées africaines en IAPD. Le programme de bourses d’études africaines en IAPD apportera un soutien à la prochaine génération d’universitaires, de praticiens et d’étudiants en IA et dans les disciplines connexes (telles que l’apprentissage automatique) qui se concentrent sur l’innovation en IA responsable pour le développement durable. L’IA responsable s’efforce d’être inclusive, fondée sur les droits et durable dans son développement et sa mise en oeuvre, en veillant à ce que les applications d’IA soient exploitées au profit du public. 

Pour les critères d'éligibilité, veuillez consulter www.ai4d.ai/calls
Appel de propositions pour désigner un gestionnaire de programme et directeur financier pour le programme de bourses d’études en IAPD:https://resources.ai4d.ai/files/2020/scholarships-call/AI4D_Scholarships_CFP_FR.pdf 

Proposition de programme IAPD Afrique: https://resources.ai4d.ai/files/AI4D_Proposal.pdf

Pour toute question, veuillez envoyer un e-mail à social@ai4d.ai

**La proposition et tous les documents à l’appui demandés doivent être soumis par l’intermédiaire du site baobab.ai4d.ai au plus tard le 8 decembre 2020, à 23 h 59 (HNE).**
"""

    session.commit()

    q = session.query(QuestionTranslation).filter_by(language='en', headline='Telephone').first()
    if q:
        q_id = q.id
        op.execute("""DELETE FROM Answer WHERE question_id={}""".format(q_id))
        session.query(QuestionTranslation).filter_by(question_id=q_id).delete()
        session.query(Question).filter_by(id=q_id).delete()

    q = session.query(QuestionTranslation).filter_by(language='en', headline='Mobile (Optional)').first()
    if q:
        q_id = q.id
        op.execute("""DELETE FROM Answer WHERE question_id={}""".format(q_id))
        session.query(QuestionTranslation).filter_by(question_id=q_id).delete()
        session.query(Question).filter_by(id=q_id).delete()

    q = session.query(QuestionTranslation).filter_by(language='en', headline='Email Address').first()
    if q:
        q_id = q.id
        op.execute("""DELETE FROM Answer WHERE question_id={}""".format(q_id))
        session.query(QuestionTranslation).filter_by(question_id=q_id).delete()
        session.query(Question).filter_by(id=q_id).delete()
    
    en = session.query(QuestionTranslation).filter_by(language='en', headline='2. Summary of the proposed approach to the financial and administrative management of the AI4D scholarships')
    en.description = """Briefly outline your proposal to manage the AI4D scholarship program according to the requirements outlined in section 2.1 of the Call for Proposals Background Document. What approaches, disciplines and modalities will you draw upon to support this?"""

    session.commit()

    en = session.query(QuestionTranslation).filter_by(language='en', headline='2a.Communication strategies')
    en.description = """Discuss your plan for launching the African AI4D PhD Scholarship and the African AI4D Advanced Scholars Program. How does your plan ensure that the program will be as inclusive as possible?"""

    session.commit()

    en = session.query(QuestionTranslation).filter_by(language='en', headline='3a. Gender and Inclusion Considerations')
    en.description = """How will your proposed approach promote increased diversity and equity in AI research? What literature or experience will you draw upon to support gender equity and linguistic equity goals in the design and execution of the calls? How will your process integrate best practices in marketing and outreach, engagement, and support for recipients?"""

    session.commit()

    en = session.query(QuestionTranslation).filter_by(language='en', headline='3b. Selection process and evaluation')
    en.description = """Broadly discuss the evaluation process for the two scholarships activities. 
How will the evaluation process ensure that the projects funded will be relevant to the AI4D Africa program’s responsible AI mandate, address ethical concerns and gender dimensions, and assess the capacity of applicants to carry out the proposed research?"""

    session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
