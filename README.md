# AI Resume Builder

A full-featured Flask web application that allows users to create, manage, and download professional resumes with multiple templates and AI-powered content generation.

## Features

- **Create Resume**: Manually build a resume with all standard sections (objective, skills, education, projects, certifications, achievements, languages, hobbies, and profile photo)
- **AI Resume Builder**: Automatically generate resume content using OpenAI's GPT model. Just provide your name, email, target job title, and background summary
- **Multiple Resume Templates**: Choose from 5 professionally designed templates:
  - Modern
  - Classic
  - Professional
  - Minimal
  - Creative
- **View All Resumes**: Dashboard to browse all saved resumes
- **Search**: Search resumes by name
- **Edit & Delete**: Manage your resumes
- **PDF Download**: Export any resume as a PDF file
- **Responsive Design**: Mobile-friendly interface using Bootstrap

## Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy
- **Frontend**: HTML, Bootstrap 5, CSS
- **AI Integration**: OpenAI API (GPT-3.5 Turbo)
- **PDF Generation**: xhtml2pdf
- **Database**: SQLite

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-builder.git
cd resume-builder
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional, for AI features):
```bash
# On Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# On Windows CMD
set OPENAI_API_KEY=your-api-key-here
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

### Manual Resume Creation
1. Go to the dashboard and click **Create Resume**
2. Fill in all your details
3. Select a template style
4. Upload a profile photo (optional)
5. Click **Save Resume** to see a preview
6. Download as PDF from the resumes list

### AI Resume Builder
1. Go to the dashboard and click **AI Resume Builder**
2. Enter your name, email, phone, and address
3. Specify your target job title (e.g., Software Engineer)
4. Describe your experience and background
5. Select a template
6. Upload a profile photo (optional)
7. Click **Generate Resume with AI**
8. The AI will generate professional content for all sections
9. Preview and download your resume

**Note**: Without an OpenAI API key, the AI builder will use a built-in template. For best results, set the `OPENAI_API_KEY` environment variable.

## Project Structure

```
resume-builder/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html        # Landing page
│   ├── dashboard.html    # Dashboard with stats
│   ├── resume.html       # Manual resume creation form
│   ├── ai_resume.html    # AI resume builder form
│   ├── resumes.html      # List all resumes
│   ├── edit.html         # Edit existing resume
│   ├── modern.html       # Modern template
│   ├── classic.html      # Classic template
│   ├── professional.html # Professional template
│   ├── minimal.html      # Minimal template
│   ├── creative.html     # Creative template
│   └── pdf.html          # PDF generation template
├── static/
│   ├── css/style.css     # Custom styles
│   └── uploads/          # Uploaded profile photos
├── resume.db             # SQLite database (auto-generated)
├── requirements.txt      # Python dependencies
└── .gitignore           # Git ignore rules
```

## Database Schema

The application uses a single `Resume` model with the following fields:
- `id` - Primary key
- `name` - Full name
- `email` - Email address
- `phone` - Phone number
- `address` - Physical address
- `objective` - Career objective
- `skills` - Skills list
- `education` - Education details
- `projects` - Projects description
- `certifications` - Certifications
- `achievements` - Achievements
- `languages` - Languages known
- `hobbies` - Hobbies and interests
- `photo` - Profile photo filename
- `template` - Selected template style

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [OpenAI](https://openai.com/) - AI content generation
- [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf) - PDF generation

## Contact

Your Name - [@yourusername](https://github.com/yourusername)

Project Link: [https://github.com/yourusername/resume-builder](https://github.com/yourusername/resume-builder)
