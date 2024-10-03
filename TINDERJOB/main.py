from flask import Flask, render_template, redirect, url_for, request, flash, session, get_flashed_messages
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = '0b7b48e6def3779af1fe3b0a0c888b69cf1d4ec316a11a36811a0e8e0a3d46bf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tinderjob.db'
db = SQLAlchemy(app)
Bootstrap5(app)

class Developer(db.Model):
    __tablename__ = 'developer' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cel = db.Column(db.String(100), nullable=False)
    habilidades = db.Column(db.Text, nullable=False)
    
    matches = db.relationship('Match', back_populates='developer')


class Company(db.Model):
    __tablename__ = 'company'  
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    matches = db.relationship('Match', back_populates='company')


class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    dev_match = db.Column(db.Boolean, default=False)
    com_match = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')
    
    developer = db.relationship('Developer', back_populates='matches')
    company = db.relationship('Company', back_populates='matches')

class DevRegForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    cel = StringField('Celular', validators=[DataRequired()])
    habilidades = TextAreaField('Habilidades', validators=[DataRequired()])
    submit= SubmitField('Cadastrar')
    
class DevLoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class EmpRegForm(FlaskForm):
    company_name = StringField('Nome da Empresa', validators=[DataRequired()])
    company_email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class EmpLoginForm(FlaskForm):
    company_email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session)
        if 'developer_id' not in session and 'company_id' not in session:
            flash('Você precisa estar logado para acessar essa página.', 'warning')
            return redirect(url_for('home')) 
        return f(*args, **kwargs)
    return decorated_function



def get_current_logged_in_developer():
    developer_id = session.get('developer_id')
    if developer_id:
        return Developer.query.get(developer_id)
    return None

def get_current_logged_in_company():
    company_id = session.get('company_id')
    if company_id:
        return Company.query.get(company_id)
    return None

# Rotas
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dev/login", methods=["GET", "POST"])
def dev_login():
    form = DevLoginForm()
    if form.validate_on_submit():
        developer = Developer.query.filter_by(email=form.email.data.lower(), password=form.password.data).first()
        if developer:
            get_flashed_messages()
            session['developer_id'] = developer.id 
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('dev_home'))
        else:
            flash("E-mail ou senha inválidos", "danger")
    return render_template("dev_login.html", form=form)


@app.route("/dev/register", methods=["GET", "POST"])
def dev_register():
    form = DevRegForm()
    if form.validate_on_submit():
        new_dev = Developer(
            name=form.name.data,
            email=form.email.data.lower(),
            password=form.password.data,
            cel=form.cel.data,
            habilidades=form.habilidades.data
        )
        db.session.add(new_dev)
        db.session.commit()
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('dev_login'))
    return render_template("dev_register.html", form=form)


@app.route("/emp/login", methods=["GET", "POST"])
def emp_login():
    form = EmpLoginForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(company_email=form.company_email.data.lower(), password=form.password.data).first()
        if company:
            get_flashed_messages()
            session['company_id'] = company.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('emp_home'))
        else:
            flash("E-mail ou senha inválidos", "danger")
    return render_template("emp_login.html", form=form)

@app.route("/emp/register", methods=["GET", "POST"])
def emp_register():
    form = EmpRegForm()
    if form.validate_on_submit():
        new_company = Company(
            company_name=form.company_name.data,
            company_email=form.company_email.data.lower(),
            password=form.password.data,
            description=form.description.data
        )
        db.session.add(new_company)
        db.session.commit()
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('emp_login'))
    return render_template("emp_register.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for('home'))

@app.route("/dev/home", methods=["GET"])
@login_required
def dev_home():
    developer = get_current_logged_in_developer()
    if developer:
        developer.matches = Match.query.filter_by(developer_id=developer.id).all()
        return render_template("dev_home.html", developer=developer)
    else:
        flash("Você precisa estar logado!", "danger")
        return redirect(url_for('dev_login'))



@app.route("/emp/home", methods=["GET"])
@login_required
def emp_home():
    company = get_current_logged_in_company()
    if company:
        company.matches = Match.query.filter_by(company_id=company.id).all() 
        return render_template("emp_home.html", company=company)
    else:
        flash("Você precisa estar logado!", "danger")
        return redirect(url_for('emp_login'))

@app.route("/dev/browse_companies", methods=["GET", "POST"])
@login_required
def browse_companies():
    developer = get_current_logged_in_developer() 
    matched_companies_ids = db.session.query(Match.company_id).filter_by(developer_id=developer.id, dev_match=True).all()
    matched_company_ids = [company_id for (company_id,) in matched_companies_ids]

    companies = Company.query.filter(Company.id.notin_(matched_company_ids)).all()

    if not companies:
        flash("Não há novas empresas para dar match.", "info")
        return redirect(url_for('dev_home')) 

    return render_template("browse_companies.html", companies=companies)


@app.route("/emp/browse_developers", methods=["GET", "POST"])
@login_required
def browse_developers():
    company = get_current_logged_in_company()
    matched_developers_ids = db.session.query(Match.developer_id).filter_by(company_id=company.id, com_match=True).all()
    matched_developer_ids = [developer_id for (developer_id,) in matched_developers_ids]

    developers = Developer.query.filter(Developer.id.notin_(matched_developer_ids)).all()

    if not developers: 
        flash("Não há novos desenvolvedores para dar match.", "info")
        return redirect(url_for('emp_home')) 

    return render_template("browse_developers.html", developers=developers)


@app.route("/dev/match/<int:company_id>")
@login_required
def dev_match_company(company_id):
    developer = get_current_logged_in_developer()
    match = Match.query.filter_by(developer_id=developer.id, company_id=company_id).first()

    if not match:
        match = Match(developer_id=developer.id, company_id=company_id, dev_match=True)
        db.session.add(match)
        db.session.commit()
        flash("Match aguardando confirmação!", "info")
    else:
        flash("Você já deu match com esta empresa!", "warning")

    return redirect(url_for('browse_companies'))

@app.route("/dev/accept_match/<int:match_id>")
@login_required
def dev_accept_match(match_id):
    match = Match.query.get(match_id)
    if match and match.developer_id == session.get('developer_id'):
        match.dev_match = True
        db.session.commit()
        flash("Match aceito com sucesso!", "success")

        if match.com_match:
            match.status = "accepted"  
            db.session.commit()
            flash("Parabéns! O match foi aceito por ambas as partes!", "success")
    else:
        flash("Você não pode aceitar este match.", "danger")

    return redirect(url_for('dev_home'))

@app.route("/dev/cancel_match/<int:match_id>")
@login_required
def dev_cancel_match(match_id):
    match = Match.query.get(match_id)
    if match:
        db.session.delete(match)
        db.session.commit()
        flash("Match cancelado com sucesso!", "success")
    else:
        flash("Match não encontrado.", "danger")

    return redirect(url_for('dev_home'))

@app.route("/emp/match/<int:developer_id>")
@login_required
def emp_match_developer(developer_id):
    company = get_current_logged_in_company()
    match = Match.query.filter_by(developer_id=developer_id, company_id=company.id).first()

    if not match:
        match = Match(developer_id=developer_id, company_id=company.id, com_match=True)
        db.session.add(match)
        db.session.commit()
        flash("Match aguardando confirmação!", "info")
    else:
        flash("Você já deu match com este desenvolvedor!", "warning")

    return redirect(url_for('browse_developers'))

@app.route("/emp/accept_match/<int:match_id>")
@login_required
def emp_accept_match(match_id):
    match = Match.query.get(match_id)
    if match and match.company_id == session.get('company_id'):
        match.com_match = True
        db.session.commit()
        flash("Match aceito com sucesso!", "success")

        if match.dev_match:
            match.status = "accepted"
            db.session.commit()
            flash("Parabéns! O match foi aceito por ambas as partes!", "success")
    else:
        flash("Você não pode aceitar este match.", "danger")

    return redirect(url_for('emp_home'))

@app.route("/emp/cancel_match/<int:match_id>")
@login_required
def emp_cancel_match(match_id):
    match = Match.query.get(match_id)
    if match:
        db.session.delete(match)
        db.session.commit()
        flash("Match cancelado com sucesso!", "success")
    else:
        flash("Match não encontrado.", "danger")

    return redirect(url_for('emp_home'))


if __name__ == '__main__':
    app.run(debug=True, port=6001)