import os
from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from sqlalchemy.sql import text
from dotenv import load_dotenv
from datetime import datetime
import json


load_dotenv()
print("DB URL:", os.getenv("MYSQL_DB_URL"))

app = Flask(__name__)
app.secret_key = 'suvidha-802'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'Uploads'

def allowed_file(filename, file_type='document'):
    """
    Check if a file is allowed based on its extension.
    Args:
        filename: The name of the file to check
        file_type: Type of file ('image' or 'document')
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    ALLOWED_EXTENSIONS = {
        'image': {'png', 'jpg', 'jpeg', 'gif'},
        'document': {'pdf', 'doc', 'docx'}
    }
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS.get(file_type, set())

# Ensure upload directory exists and has proper permissions
def ensure_upload_dir():
    upload_dir = os.path.join(app.static_folder, 'Uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir

# Update the UPLOAD_FOLDER configuration
app.config['UPLOAD_FOLDER'] = ensure_upload_dir()

db = SQLAlchemy(app)

# ------------------ Models ------------------ #
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Matches updated schema
    password_hash = db.Column(db.String(128), nullable=False)  # Matches updated schema
    role = db.Column(db.String(20), nullable=False)  # student, employee, or tpo

    __table_args__ = (
        db.UniqueConstraint('username', name='unique_username'),
        db.UniqueConstraint('email', name='unique_email'),
    )

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    resume_path = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    full_name = db.Column(db.String(100))
    course_year = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    country = db.Column(db.String(100))
    college = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    about = db.Column(db.Text)
    designation = db.Column(db.String(100))
    company_website = db.Column(db.String(255))
    department = db.Column(db.String(100))
    company = db.Column(db.String(100))  # Add this field
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    from_user = db.relationship('User', foreign_keys=[from_id])
    to_user = db.relationship('User', foreign_keys=[to_id])

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    certification_name = db.Column(db.String(100))  # Matches schema
    issuer = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    credential_id = db.Column(db.String(100))
    filename = db.Column(db.String(255))  # For file path

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_name = db.Column(db.String(255))  # Matches schema
    project_type = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    description = db.Column(db.Text)
    github_link = db.Column(db.String(200))

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    degree = db.Column(db.String(100))
    institution = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    grade = db.Column(db.String(20))

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    position = db.Column(db.String(100))
    company = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    description = db.Column(db.Text)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_name = db.Column(db.String(100))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, hired, rejected
    
    # Update relationships with proper back_populates
    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    internship = db.relationship('Internship', backref=db.backref('applications', lazy=True))

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    stipend = db.Column(db.Integer)
    category = db.Column(db.String(100))
    start_day = db.Column(db.Date)
    company = db.relationship('User', backref='posted_internships')

# ------------------ Database Initialization ------------------ #
def init_db():
    with app.app_context():
        db.create_all()

# Initialize database during app setup
init_db()

# ------------------ Helper Functions ------------------ #
def save_uploaded_file(file, filename, file_type='document'):
    """
    Save an uploaded file with proper error handling and logging.
    Args:
        file: The uploaded file object
        filename: The name to save the file as
        file_type: Type of file ('image' or 'document')
    Returns:
        str: The relative path where the file was saved
    """
    try:
        if not file:
            print(f"No file provided for {file_type}")
            return None
            
        if not allowed_file(filename, file_type):
            print(f"Invalid file type for {filename}")
            return None
            
        # Ensure the Uploads directory exists
        upload_dir = os.path.join(app.static_folder, 'Uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            print(f"Created Uploads directory at {upload_dir}")
            
        secure_name = secure_filename(filename)
        file_path = os.path.join(upload_dir, secure_name)
        print(f"Attempting to save {file_type} to {file_path}")
        
        # Save the file
        file.save(file_path)
        print(f"Successfully saved {file_type} to {file_path}")
        
        # Return the relative path for database storage
        return os.path.join('Uploads', secure_name)
    except Exception as e:
        print(f"Error saving {file_type}: {str(e)}")
        return None

# ------------------ Routes ------------------ #
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role='student'):
    if role not in ['student', 'employee', 'tpo']:
        return render_template('login.html', error="Invalid role")

    template_map = {
        'student': 'student_registration.html',
        'employee': 'employee_registration.html',
        'tpo': 'tpo_registration.html'
    }

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')

            # Validate input
            if not all([username, email, password, confirm_password, full_name, phone]):
                return render_template(template_map[role], error="All fields are required")
            if password != confirm_password:
                return render_template(template_map[role], error="Passwords do not match")
            if len(password) < 8:
                return render_template(template_map[role], error="Password must be at least 8 characters")

            # Check if username or email exists
            if User.query.filter(or_(User.username == username, User.email == email)).first():
                return render_template(template_map[role], error="Username or email already taken")

            # Create new user
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Get user.id

            # Create profile
            profile_data = {
                'user_id': user.id,
                'full_name': full_name,
                'email': email,
                'phone': phone
            }

            if role == 'student':
                profile_data.update({
                    'course_year': request.form.get('course_year'),
                    'college': request.form.get('college'),
                    'branch': request.form.get('branch')
                })
            elif role == 'tpo':
                verification_doc = request.files.get('verification_doc')
                if verification_doc and allowed_file(verification_doc.filename, 'document'):
                    filename = secure_filename(verification_doc.filename)
                    verification_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    verification_doc.save(verification_path)
                    profile_data['resume_path'] = verification_path
                profile_data.update({
                    'college': request.form.get('college'),
                    'designation': request.form.get('designation')
                })
            elif role == 'employee':
                verification_doc = request.files.get('verification_doc')
                if verification_doc and allowed_file(verification_doc.filename, 'document'):
                    filename = secure_filename(verification_doc.filename)
                    verification_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    verification_doc.save(verification_path)
                    profile_data['resume_path'] = verification_path
                profile_data.update({
                    'company': request.form.get('company_name'),
                    'company_website': request.form.get('company_website'),
                    'designation': request.form.get('designation'),
                    'department': request.form.get('department')
                })

            profile = Profile(**profile_data)
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return render_template(template_map[role], error=f"Registration failed: {str(e)}")
    
    return render_template(template_map[role])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            role = request.form.get('role', 'student')
            identifier = request.form.get('username')  # Could be username or email
            password = request.form.get('password')

            # Query user by username or email, and role
            user = User.query.filter(
                or_(User.username == identifier, User.email == identifier),
                User.role == role
            ).first()

            # Check if user exists and password matches
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['role'] = user.role
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Invalid username/email, password, or role")
        except Exception as e:
            return render_template('login.html', error=f"Login failed: {str(e)}")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or 'role' not in session:
        return redirect(url_for('login'))
    try:
        user = db.session.get(User, session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        dashboard_map = {
            'student': 'stu_dash.html',
            'employee': 'employee_dash.html',
            'tpo': 'tpo_dash.html'
        }
        
        template = dashboard_map.get(user.role, 'stu_dash.html')
        
        if user.role == 'student':
            try:
                others = User.query.filter(User.id != user.id).all()
                received = Rating.query.filter_by(to_id=user.id).all()
                internships = Internship.query.order_by(Internship.posted_on.desc()).all()
                return render_template(template, user=user, others=others, received=received, internships=internships)
            except Exception as e:
                print(f"Error in student dashboard: {str(e)}")
                return render_template(template, user=user, others=[], received=[], internships=[])
                
        elif user.role == 'employee':
            try:
                # Get internships count for this employee
                internships = Internship.query.filter_by(company_id=user.id).all()
                internships_count = len(internships)
                print(f"Found {internships_count} internships for company_id {user.id}")  # Debug log
                
                # Get applications for this employee's internships
                applications = []
                for internship in internships:
                    apps = Application.query.filter_by(internship_id=internship.id).all()
                    applications.extend(apps)
                
                applications_count = len(applications)
                hired_count = sum(1 for app in applications if app.status == 'hired')
                
                return render_template(template, user=user, 
                                     students_count=hired_count,  # Show hired students instead of total
                                     internships_count=internships_count, 
                                     applications_count=applications_count,
                                     applications=applications)
            except Exception as e:
                print(f"Error in employee dashboard: {str(e)}")
                return render_template(template, user=user, students_count=0, 
                                     internships_count=0, applications_count=0, applications=[])
                
        elif user.role == 'tpo':
            try:
                students = User.query.filter_by(role='student').all()
                students_count = len(students) if students else 0
                internships_count = Internship.query.count()
                applications_count = Application.query.count()
                
                return render_template(template, user=user, students_count=students_count, 
                                     internships_count=internships_count, applications_count=applications_count, 
                                     students=students)
            except Exception as e:
                print(f"Error in tpo dashboard: {str(e)}")
                return render_template(template, user=user, students_count=0, 
                                     internships_count=0, applications_count=0, students=[])
    
    except Exception as e:
        print(f"General dashboard error: {str(e)}")
        return render_template('login.html', error=f"Error loading dashboard: {str(e)}")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session or 'role' not in session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Please log in to continue'}), 401
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user:
        session.clear()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'User not found'}), 404
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            print(f"Processing profile update for user {user.id}")
            
            # Initialize or update profile
            if not user.profile:
                profile = Profile(user_id=user.id)
                db.session.add(profile)
                db.session.flush()
                print(f"Created new profile for user {user.id}")
            
            # Update profile fields
            profile_data = {
                'full_name': request.form.get('full_name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'address': request.form.get('address'),
                'city': request.form.get('city'),
                'state': request.form.get('state'),
                'pincode': request.form.get('pincode'),
                'country': request.form.get('country'),
                'college': request.form.get('college'),
                'branch': request.form.get('branch'),
                'course_year': request.form.get('course_year'),
                'graduation_year': request.form.get('graduation_year'),
                'linkedin_url': request.form.get('linkedin_url'),
                'github_url': request.form.get('github_url'),
                'about': request.form.get('about')
            }
            
            print("Profile data received:", profile_data)
            
            for key, value in profile_data.items():
                if value is not None:
                    setattr(user.profile, key, value)
                    print(f"Updated {key} to {value}")
            
            # Handle profile photo upload
            profile_photo = request.files.get('profile_photo')
            if profile_photo:
                print(f"Processing profile photo: {profile_photo.filename}")
                photo_path = save_uploaded_file(
                    profile_photo,
                    f"{user.id}_profile_{profile_photo.filename}",
                    'image'
                )
                if photo_path:
                    user.profile.profile_photo = photo_path
                    print(f"Updated profile photo path to {photo_path}")
            
            # Handle resume upload
            resume = request.files.get('resume')
            if resume:
                print(f"Processing resume: {resume.filename}")
                resume_path = save_uploaded_file(
                    resume,
                    f"{user.id}_resume_{resume.filename}",
                    'document'
                )
                if resume_path:
                    user.profile.resume_path = resume_path
                    print(f"Updated resume path to {resume_path}")
            
            # Handle skills
            skills = request.form.getlist('skills[]')
            if skills:
                print("Processing skills:", skills)
                if len(skills) == 1 and skills[0].startswith('['):
                    import json
                    skills = json.loads(skills[0])
                
                Skill.query.filter_by(user_id=user.id).delete()
                print(f"Deleted existing skills for user {user.id}")
                
                for skill in skills:
                    if isinstance(skill, str) and skill.strip():
                        db.session.add(Skill(user_id=user.id, skill_name=skill.strip()))
                        print(f"Added skill: {skill.strip()}")
            
            # Handle projects
            projects = request.form.getlist('projects[]')
            if projects:
                # Convert string representation of list to actual list if necessary
                if len(projects) == 1 and projects[0].startswith('['):
                    import json
                    projects = json.loads(projects[0])
                
                # Delete existing projects
                Project.query.filter_by(user_id=user.id).delete()
                
                # Add new projects
                for project_data in projects:
                    if isinstance(project_data, dict):
                        db.session.add(Project(
                            user_id=user.id,
                            project_name=project_data.get('project_name', '').strip(),
                            project_type=project_data.get('project_type', '').strip(),
                            duration=project_data.get('duration', '').strip(),
                            description=project_data.get('description', '').strip(),
                            github_link=project_data.get('github_link', '').strip()
                        ))
            
            # Handle certifications
            certifications = request.form.getlist('certifications[]')
            if certifications:
                # Convert string representation of list to actual list if necessary
                if len(certifications) == 1 and certifications[0].startswith('['):
                    import json
                    certifications = json.loads(certifications[0])
                
                # Delete existing certifications
                Certificate.query.filter_by(user_id=user.id).delete()
                
                # Add new certifications
                for cert_data in certifications:
                    if isinstance(cert_data, dict):
                        cert = Certificate(
                            user_id=user.id,
                            certification_name=cert_data.get('certification_name', '').strip(),
                            issuer=cert_data.get('issuer', '').strip(),
                            duration=cert_data.get('duration', '').strip(),
                            credential_id=cert_data.get('credential_id', '').strip()
                        )
                        db.session.add(cert)
            
            # Handle certificate files
            for key in request.files:
                if key.startswith('certificate_files_'):
                    cert_file = request.files[key]
                    if cert_file and allowed_file(cert_file.filename, 'document'):
                        filename = secure_filename(cert_file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        cert_file.save(file_path)
                        # Update the corresponding certification with the file path
                        index = int(key.split('_')[-1])
                        if index < len(certifications):
                            cert = Certificate.query.filter_by(
                                user_id=user.id,
                                certification_name=certifications[index].get('certification_name')
                            ).first()
                            if cert:
                                cert.filename = f'Uploads/{filename}'
            
            db.session.commit()
            print(f"Successfully committed all changes for user {user.id}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Profile updated successfully',
                    'redirect': url_for('resume_edit')
                })
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('resume_edit'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating profile for user {user.id}: {str(e)}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
            
            flash(f'Error updating profile: {str(e)}', 'error')
            return redirect(url_for('profile'))
    
    skills = Skill.query.filter_by(user_id=user.id).all()
    projects = Project.query.filter_by(user_id=user.id).all()
    certificates = Certificate.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, skills=skills, projects=projects, certificates=certificates)

@app.route('/post_internship', methods=['GET', 'POST'])
def post_internship():
    if 'user_id' not in session or session['role'] not in ['employee', 'tpo']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            description = request.form.get('description')
            location = request.form.get('location')
            duration = request.form.get('duration')
            stipend = request.form.get('stipend')
            category = request.form.get('category')
            start_day = request.form.get('start_day')
            
            # Validate required fields
            if not all([title, description, location, category, duration, stipend, start_day]):
                flash('All fields are required', 'error')
                return redirect(url_for('post_internship'))
            
            try:
                duration = int(duration)
                if duration <= 0:
                    raise ValueError("Duration must be a positive integer")
            except ValueError:
                flash('Duration must be a positive number', 'error')
                return redirect(url_for('post_internship'))
                
            try:
                stipend = int(stipend)
                if stipend < 0:
                    raise ValueError("Stipend cannot be negative")
            except ValueError:
                flash('Stipend must be a non-negative number', 'error')
                return redirect(url_for('post_internship'))
                
            try:
                start_day = datetime.strptime(start_day, '%Y-%m-%d').date()
                today = datetime.utcnow().date()
                if start_day < today:
                    flash('Start date cannot be in the past', 'error')
                    return redirect(url_for('post_internship'))
            except ValueError:
                flash('Invalid start date format', 'error')
                return redirect(url_for('post_internship'))
                
            internship = Internship(
                title=title,
                description=description,
                company_id=session['user_id'],
                location=location,
                duration=duration,
                stipend=stipend,
                category=category,
                start_day=start_day
            )
            db.session.add(internship)
            db.session.commit()
            flash('Internship posted successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error posting internship: {str(e)}', 'error')
            return redirect(url_for('post_internship'))
    return render_template('post_internship.html')

@app.route('/apply/<int:internship_id>', methods=['GET'])
def apply_to_internship(internship_id):
    if 'user_id' not in session or session['role'] != 'student':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Please log in as a student to apply'}), 401
        return redirect(url_for('login'))
    
    try:
        # Check if already applied
        existing = Application.query.filter_by(user_id=session['user_id'], internship_id=internship_id).first()
        if existing:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'error': 'You have already applied to this internship!'}), 400
            flash('You have already applied to this internship!', 'warning')
            return redirect(url_for('dashboard'))
            
        # Create new application
        application = Application(user_id=session['user_id'], internship_id=internship_id)
        db.session.add(application)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Application submitted successfully!'})
            
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        db.session.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': str(e)}), 500
        flash(f'Application failed: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/applications')
def applications():
    if 'user_id' not in session or session['role'] not in ['employee', 'tpo']:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    # Explicitly define the join condition
    applications = (db.session.query(Application)
                    .join(Internship, Application.internship_id == Internship.id)
                    .filter(Internship.company_id == user.id)
                    .all())
    
    return render_template('applications.html', applications=applications)

@app.route('/students')
def students():
    if 'user_id' not in session or session['role'] != 'tpo':
        return redirect(url_for('login'))
    students = User.query.filter_by(role='student').all()
    return render_template('students.html', students=students)

@app.route('/internships')
def internships():
    try:
        # Get filter parameters
        location = request.args.get('location')
        category = request.args.get('category')
        duration = request.args.get('duration')
        stipend = request.args.get('stipend')
        search = request.args.get('search', '').lower()
        sort = request.args.get('sort', 'recent')

        # Base query
        query = Internship.query

        # Apply filters
        if location:
            query = query.filter(Internship.location == location)
        if category:
            query = query.filter(Internship.category == category)
        if duration:
            query = query.filter(Internship.duration == int(duration))
        if stipend:
            query = query.filter(Internship.stipend >= int(stipend))
        if search:
            query = query.filter(Internship.title.ilike(f'%{search}%'))

        # Apply sorting
        if sort == 'stipend':
            query = query.order_by(Internship.stipend.desc())
        else:  # sort by recent
            query = query.order_by(Internship.posted_on.desc())

        internships = query.all()

        # Get current user if logged in
        user = None
        user_applications = set()  # Store just the internship IDs that user has applied to
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            if user and user.role == 'student':
                # Get list of internship IDs that user has applied to
                applications = Application.query.filter_by(user_id=user.id).all()
                user_applications = {app.internship_id for app in applications}

        # Format internships data
        internships_data = []
        for internship in internships:
            company = db.session.get(User, internship.company_id)
            days_ago = (datetime.utcnow() - internship.posted_on).days
            
            internship_data = {
                'id': internship.id,
                'title': internship.title,
                'company': company.username if company else 'Unknown',
                'location': internship.location,
                'duration': internship.duration,
                'stipend': internship.stipend,
                'category': internship.category,
                'startDate': internship.start_day.strftime('%B %d, %Y') if internship.start_day else 'Flexible',
                'postedDaysAgo': days_ago,
                'description': internship.description,
                'hasApplied': internship.id in user_applications if user and user.role == 'student' else False
            }
            internships_data.append(internship_data)

        # If it's an AJAX request, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'internships': internships_data,
                'isStudent': user.role == 'student' if user else False
            })

        # Otherwise render the template
        return render_template('internship_listing.html', 
                            internships=internships_data, 
                            user=user,
                            error=None)
    except Exception as e:
        print(f"Error in internships route: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': str(e)}), 500
        return render_template('internship_listing.html', 
                            internships=[], 
                            user=None,
                            error=f"Error loading internships: {str(e)}")

# Routes (only showing updated resume_edit route)
@app.route('/resume_edit', methods=['GET', 'POST'])
def resume_edit():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            # Handle profile photo
            profile_photo = request.files.get('profile_photo')
            if profile_photo:
                print(f"Processing profile photo: {profile_photo.filename}")
                photo_path = save_uploaded_file(
                    profile_photo,
                    f"{user.id}_photo_{profile_photo.filename}",
                    'image'
                )
                if photo_path:
                    print(f"Setting profile photo path to: {photo_path}")
                    user.profile.profile_photo = photo_path

            # Update profile fields
            profile_data = {
                'full_name': request.form.get('full_name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'address': request.form.get('address'),
                'city': request.form.get('city'),
                'state': request.form.get('state'),
                'pincode': request.form.get('pincode'),
                'country': request.form.get('country'),
                'college': request.form.get('college'),
                'branch': request.form.get('branch'),
                'course_year': request.form.get('course_year'),
                'graduation_year': int(request.form.get('graduation_year')) if request.form.get('graduation_year') else None,
                'linkedin_url': request.form.get('linkedin_url'),
                'github_url': request.form.get('github_url'),
                'about': request.form.get('about')
            }
            for key, value in profile_data.items():
                if value is not None:
                    setattr(user.profile, key, value)

            # Handle resume file
            resume = request.files.get('resume')
            if resume and allowed_file(resume.filename, 'document'):
                resume_path = save_uploaded_file(resume, f"{user.id}_resume_{resume.filename}", 'document')
                if resume_path:
                    user.profile.resume_path = resume_path

            # Handle skills
            skills_json = request.form.get('skills')
            if skills_json:
                skills = json.loads(skills_json)
                Skill.query.filter_by(user_id=user.id).delete()
                for skill in skills:
                    if skill.strip():
                        db.session.add(Skill(user_id=user.id, skill_name=skill.strip()))

            # Handle projects
            projects_json = request.form.get('projects')
            if projects_json:
                projects = json.loads(projects_json)
                Project.query.filter_by(user_id=user.id).delete()
                for project in projects:
                    if project.get('project_name') and project.get('duration'):
                        db.session.add(Project(
                            user_id=user.id,
                            project_name=project['project_name'].strip(),
                            project_type=project['project_type'].strip(),
                            duration=project['duration'].strip(),
                            description=project.get('description', '').strip(),
                            github_link=project.get('github_link', '').strip()
                        ))

            # Handle certifications
            certifications_json = request.form.get('certifications')
            if certifications_json:
                certifications = json.loads(certifications_json)
                Certificate.query.filter_by(user_id=user.id).delete()
                for index, cert in enumerate(certifications):
                    if cert.get('certification_name') and cert.get('duration'):
                        cert_file = request.files.get(f'certificate_files[{index}]')
                        cert_path = None
                        if cert_file and allowed_file(cert_file.filename, 'document'):
                            cert_path = save_uploaded_file(cert_file, f"cert_{user.id}_{index}_{cert_file.filename}", 'document')
                        db.session.add(Certificate(
                            user_id=user.id,
                            certification_name=cert['certification_name'].strip(),
                            issuer=cert['issuer'].strip(),
                            duration=cert['duration'].strip(),
                            credential_id=cert.get('credential_id', '').strip(),
                            filename=cert_path
                        ))

            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Resume updated successfully',
                'redirect': url_for('resume_edit')
            })
        except Exception as e:
            db.session.rollback()
            print(f"Error saving resume: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

    skills = Skill.query.filter_by(user_id=user.id).all()
    projects = Project.query.filter_by(user_id=user.id).all()
    certificates = Certificate.query.filter_by(user_id=user.id).all()
    return render_template('Resume_edit.html', user=user, skills=skills, projects=projects, certificates=certificates)

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/rate/<int:to_id>', methods=['GET', 'POST'])
def rate(to_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            rating_value = int(request.form['rating'])
            comment_text = request.form['comment']
            existing = Rating.query.filter_by(from_id=session['user_id'], to_id=to_id).first()
            if existing:
                existing.rating = rating_value
                existing.comment = comment_text
            else:
                rating = Rating(
                    from_id=session['user_id'],
                    to_id=to_id,
                    rating=rating_value,
                    comment=comment_text
                )
                db.session.add(rating)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            to_user = User.query.get(to_id)
            return render_template('rate.html', to_user=to_user, error=f"Rating failed: {str(e)}")
    try:
        to_user = User.query.get(to_id)
        return render_template('rate.html', to_user=to_user)
    except Exception as e:
        return redirect(url_for('dashboard'), error=f"Error loading rate page: {str(e)}")

@app.route('/application_page')
def application_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        user = User.query.get(session['user_id'])
        applications = Application.query.filter_by(user_id=user.id).all()
        return render_template('application_page.html', user=user, applications=applications)
    except Exception as e:
        return render_template('login.html', error=f"Error loading application page: {str(e)}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/initdb')
def initdb():
    init_db()
    return "Database initialized!"

@app.route('/update_application_status/<int:application_id>', methods=['POST'])
def update_application_status(application_id):
    if 'user_id' not in session or session['role'] not in ['employee', 'tpo']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        status = request.form.get('status')
        if status not in ['pending', 'hired', 'rejected']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
            
        application = Application.query.get(application_id)
        if not application:
            return jsonify({'success': False, 'error': 'Application not found'}), 404
            
        # Verify the employee owns this internship
        internship = Internship.query.get(application.internship_id)
        if internship.company_id != session['user_id']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
            
        application.status = status
        db.session.commit()
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ------------------ Main ------------------ #
if __name__ == '__main__':
    app.run(debug=True)