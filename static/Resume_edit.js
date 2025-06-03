document.addEventListener('DOMContentLoaded', () => {
    let isEditMode = false;
    let originalPhotoSrc = null;

    const resumeForm = document.getElementById('resume-form');
    const editBtn = document.getElementById('edit-btn');
    const saveBtn = document.getElementById('save-btn');
    const downloadBtn = document.getElementById('download-btn');
    const photoPreview = document.getElementById('photo-preview');
    const profilePhotoInput = document.getElementById('profile-photo');
    const photoBtn = document.querySelector('.photo-btn');
    const skillInput = document.getElementById('skill-input');
    const skillsContainer = document.getElementById('skills-container');

    // Initialize original photo source
    const img = photoPreview.querySelector('img');
    originalPhotoSrc = img ? img.src : null;

    // Make photo preview clickable in edit mode
    photoPreview.addEventListener('click', () => {
        if (isEditMode) {
            profilePhotoInput.click();
        }
    });

    // Preview profile photo
    profilePhotoInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                photoPreview.innerHTML = `<img src="${event.target.result}" alt="Profile Photo">`;
            };
            reader.readAsDataURL(file);
        }
    });

    // Initialize form state
    function initializeFormState() {
        // Disable all form inputs
        resumeForm.querySelectorAll('input:not([type="file"]), textarea, select').forEach(element => {
            element.readOnly = true;
        });

        // Disable all file inputs and buttons
        resumeForm.querySelectorAll('input[type="file"], button.btn-primary, button.remove-btn, button.remove-skill').forEach(element => {
            element.disabled = true;
            element.style.display = 'none';
        });

        // Hide photo upload button
        photoBtn.style.display = 'none';
        photoPreview.style.cursor = 'default';

        // Disable skill input
        if (skillInput) {
            skillInput.readOnly = true;
            skillInput.style.display = 'none';
        }

        // Disable select elements
        resumeForm.querySelectorAll('select').forEach(select => {
            select.disabled = true;
        });

        // Hide all remove buttons
        resumeForm.querySelectorAll('.remove-btn').forEach(btn => {
            btn.style.display = 'none';
        });
    }

    // Toggle edit mode
    function toggleEditMode() {
        isEditMode = !isEditMode;
        editBtn.innerHTML = isEditMode ? '<i class="fas fa-times"></i> Cancel' : '<i class="fas fa-edit"></i> Edit';
        saveBtn.disabled = !isEditMode;

        // Toggle input fields
        resumeForm.querySelectorAll('input:not([type="file"]), textarea').forEach(element => {
            element.readOnly = !isEditMode;
        });

        // Toggle select elements
        resumeForm.querySelectorAll('select').forEach(select => {
            select.disabled = !isEditMode;
        });

        // Toggle file inputs and buttons
        resumeForm.querySelectorAll('input[type="file"], button.btn-primary, button.remove-btn, button.remove-skill').forEach(element => {
            element.disabled = !isEditMode;
            element.style.display = isEditMode ? '' : 'none';
        });

        // Update photo preview cursor and interaction state
        photoPreview.style.cursor = isEditMode ? 'pointer' : 'default';

        // Show/hide skill input
        if (skillInput) {
            skillInput.readOnly = !isEditMode;
            skillInput.style.display = isEditMode ? '' : 'none';
        }

        if (!isEditMode) {
            // Reset form to original state
            resumeForm.reset();
            // Restore original photo
            if (!originalPhotoSrc) {
                photoPreview.innerHTML = '<i class="fas fa-camera"></i><span>No Photo Available</span>';
            } else {
                photoPreview.innerHTML = `<img src="${originalPhotoSrc}" alt="Profile Photo">`;
            }
        }
    }

    // Save resume
    function saveResume() {
        if (!isEditMode) return;

        const formData = new FormData(resumeForm);

        // Collect skills
        const skills = Array.from(skillsContainer.querySelectorAll('.skill-tag')).map(tag => tag.dataset.skill);
        formData.append('skills', JSON.stringify(skills));

        // Collect projects
        const projects = [];
        document.querySelectorAll('.project-card').forEach(card => {
            const project = {
                project_name: card.querySelector('input[name="projects[][project_name]"]').value,
                project_type: card.querySelector('select[name="projects[][project_type]"]').value,
                duration: `${card.querySelector('input[name="projects[][duration_start]"]').value}-${card.querySelector('input[name="projects[][duration_end]"]').value}`,
                github_link: card.querySelector('input[name="projects[][github_link]"]').value,
                description: card.querySelector('textarea[name="projects[][description]"]').value
            };
            projects.push(project);
        });
        formData.append('projects', JSON.stringify(projects));

        // Collect certifications
        const certifications = [];
        document.querySelectorAll('.certification-card').forEach(card => {
            const cert = {
                certification_name: card.querySelector('input[name="certifications[][certification_name]"]').value,
                issuer: card.querySelector('input[name="certifications[][issuer]"]').value,
                duration: `${card.querySelector('input[name="certifications[][duration_start]"]').value}-${card.querySelector('input[name="certifications[][duration_end]"]').value}`,
                credential_id: card.querySelector('input[name="certifications[][credential_id]"]').value
            };
            certifications.push(cert);
        });
        formData.append('certifications', JSON.stringify(certifications));

        fetch('/resume_edit', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update original photo source after successful save
                const img = photoPreview.querySelector('img');
                if (img) {
                    originalPhotoSrc = img.src;
                }
                alert(data.message);
                // Reload the page to show updated data
                window.location.reload();
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error saving resume:', error);
            alert('Error saving resume: ' + error.message);
        });
    }

    // Initialize the form state
    initializeFormState();

    // Event listeners
    editBtn.addEventListener('click', toggleEditMode);
    saveBtn.addEventListener('click', saveResume);
    downloadBtn.addEventListener('click', () => {
        const element = document.querySelector('.resume-builder');
        html2pdf().from(element).save('resume.pdf');
    });
});