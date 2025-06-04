document.addEventListener("DOMContentLoaded", () => {
    let isEditMode = false
    let originalPhotoSrc = null
  
    const resumeForm = document.getElementById("resume-form")
    const editBtn = document.getElementById("edit-btn")
    const saveBtn = document.getElementById("save-btn")
    const downloadBtn = document.getElementById("download-btn")
    const photoPreview = document.getElementById("photo-preview")
    const profilePhotoInput = document.getElementById("profile-photo")
    const photoBtn = document.querySelector(".photo-btn")
    const skillInput = document.getElementById("skill-input")
    const skillsContainer = document.getElementById("skills-container")
    const loadingOverlay = document.getElementById("loading-overlay")
    const notification = document.getElementById("notification")
    const notificationMessage = document.getElementById("notification-message")
    const collapseBtns = document.querySelectorAll(".collapse-btn")
    const menuToggle = document.querySelector(".menu-toggle")
    const mainNav = document.querySelector(".main-nav")
  
    // Initialize original photo source
    const img = photoPreview.querySelector("img")
    originalPhotoSrc = img ? img.src : null
  
    // Mobile menu toggle
    if (menuToggle) {
      menuToggle.addEventListener("click", () => {
        mainNav.classList.toggle("active")
      })
    }
  
    // Section collapse functionality
    collapseBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-target")
        const targetSection = document.getElementById(targetId)
  
        if (targetSection) {
          const isCollapsed = targetSection.style.display === "none"
  
          // Toggle section visibility with animation
          if (isCollapsed) {
            targetSection.style.display = "block"
            targetSection.style.maxHeight = "0"
            setTimeout(() => {
              targetSection.style.maxHeight = targetSection.scrollHeight + "px"
            }, 10)
            setTimeout(() => {
              targetSection.style.maxHeight = ""
            }, 300)
          } else {
            targetSection.style.maxHeight = targetSection.scrollHeight + "px"
            setTimeout(() => {
              targetSection.style.maxHeight = "0"
            }, 10)
            setTimeout(() => {
              targetSection.style.display = "none"
            }, 300)
          }
  
          // Toggle button icon
          btn.classList.toggle("collapsed")
        }
      })
    })
  
    // Make photo preview clickable in edit mode
    photoPreview.addEventListener("click", () => {
      if (isEditMode) {
        profilePhotoInput.click()
      }
    })
  
    // Preview profile photo with animation
    profilePhotoInput.addEventListener("change", (e) => {
      const file = e.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (event) => {
          // Create new image element
          const newImg = document.createElement("img")
          newImg.src = event.target.result
          newImg.alt = "Profile Photo"
          newImg.style.opacity = "0"
  
          // Clear photo preview and add new image
          photoPreview.innerHTML = ""
          photoPreview.appendChild(newImg)
  
          // Fade in animation
          setTimeout(() => {
            newImg.style.transition = "opacity 0.3s ease"
            newImg.style.opacity = "1"
          }, 50)
        }
        reader.readAsDataURL(file)
      }
    })
  
    // Initialize form state
    function initializeFormState() {
      // Disable all form inputs
      resumeForm.querySelectorAll('input:not([type="file"]), textarea, select').forEach((element) => {
        element.readOnly = true
        element.classList.remove("editable")
      })
  
      // Disable all file inputs and buttons
      resumeForm
        .querySelectorAll('input[type="file"], button.btn-primary, button.remove-btn, button.remove-skill')
        .forEach((element) => {
          element.disabled = true
          element.style.display = "none"
        })
  
      // Hide photo upload button
      photoBtn.style.display = "none"
      photoPreview.style.cursor = "default"
  
      // Disable skill input
      if (skillInput) {
        skillInput.readOnly = true
        skillInput.style.display = "none"
      }
  
      // Disable select elements
      resumeForm.querySelectorAll("select").forEach((select) => {
        select.disabled = true
      })
  
      // Hide all remove buttons
      resumeForm.querySelectorAll(".remove-btn").forEach((btn) => {
        btn.style.display = "none"
      })
    }
  
    // Toggle edit mode with animations
    function toggleEditMode() {
      isEditMode = !isEditMode
  
      // Update edit button with animation
      if (isEditMode) {
        editBtn.innerHTML = '<i class="fas fa-times"></i> Cancel'
        editBtn.classList.add("btn-danger")
        editBtn.classList.remove("btn-secondary")
      } else {
        editBtn.innerHTML = '<i class="fas fa-edit"></i> Edit'
        editBtn.classList.remove("btn-danger")
        editBtn.classList.add("btn-secondary")
      }
  
      saveBtn.disabled = !isEditMode
  
      // Toggle input fields with animation
      resumeForm.querySelectorAll('input:not([type="file"]), textarea').forEach((element) => {
        element.readOnly = !isEditMode
  
        if (isEditMode) {
          element.classList.add("editable")
          element.style.transition = "all 0.3s ease"
          element.style.backgroundColor = "#fff"
          element.style.borderColor = "#f4b400"
        } else {
          element.classList.remove("editable")
          element.style.transition = "all 0.3s ease"
          element.style.backgroundColor = "#f8f9fa"
          element.style.borderColor = "#e2e8f0"
        }
      })
  
      // Toggle select elements
      resumeForm.querySelectorAll("select").forEach((select) => {
        select.disabled = !isEditMode
  
        if (isEditMode) {
          select.classList.add("editable")
          select.style.transition = "all 0.3s ease"
          select.style.backgroundColor = "#fff"
          select.style.borderColor = "#f4b400"
        } else {
          select.classList.remove("editable")
          select.style.transition = "all 0.3s ease"
          select.style.backgroundColor = "#f8f9fa"
          select.style.borderColor = "#e2e8f0"
        }
      })
  
      // Toggle file inputs and buttons with animation
      resumeForm
        .querySelectorAll('input[type="file"], button.btn-primary, button.remove-btn, button.remove-skill')
        .forEach((element) => {
          element.disabled = !isEditMode
  
          if (isEditMode) {
            element.style.display = ""
            element.style.opacity = "0"
            setTimeout(() => {
              element.style.transition = "opacity 0.3s ease"
              element.style.opacity = "1"
            }, 50)
          } else {
            element.style.transition = "opacity 0.3s ease"
            element.style.opacity = "0"
            setTimeout(() => {
              element.style.display = "none"
            }, 300)
          }
        })
  
      // Update photo preview cursor and interaction state
      photoPreview.style.cursor = isEditMode ? "pointer" : "default"
  
      // Show/hide photo button with animation
      if (isEditMode) {
        photoBtn.style.display = ""
        photoBtn.style.opacity = "0"
        setTimeout(() => {
          photoBtn.style.transition = "opacity 0.3s ease"
          photoBtn.style.opacity = "1"
        }, 50)
      } else {
        photoBtn.style.transition = "opacity 0.3s ease"
        photoBtn.style.opacity = "0"
        setTimeout(() => {
          photoBtn.style.display = "none"
        }, 300)
      }
  
      // Show/hide skill input with animation
      if (skillInput) {
        if (isEditMode) {
          skillInput.readOnly = false
          skillInput.style.display = ""
          skillInput.style.opacity = "0"
          setTimeout(() => {
            skillInput.style.transition = "opacity 0.3s ease"
            skillInput.style.opacity = "1"
          }, 50)
        } else {
          skillInput.readOnly = true
          skillInput.style.transition = "opacity 0.3s ease"
          skillInput.style.opacity = "0"
          setTimeout(() => {
            skillInput.style.display = "none"
          }, 300)
        }
      }
  
      if (!isEditMode) {
        // Reset form to original state
        resumeForm.reset()
        // Restore original photo with animation
        if (!originalPhotoSrc) {
          photoPreview.innerHTML = '<i class="fas fa-camera"></i><span>No Photo Available</span>'
        } else {
          const currentImg = photoPreview.querySelector("img")
          if (currentImg) {
            currentImg.style.transition = "opacity 0.3s ease"
            currentImg.style.opacity = "0"
  
            setTimeout(() => {
              photoPreview.innerHTML = `<img src="${originalPhotoSrc}" alt="Profile Photo" style="opacity: 0;">`
              const newImg = photoPreview.querySelector("img")
  
              setTimeout(() => {
                newImg.style.transition = "opacity 0.3s ease"
                newImg.style.opacity = "1"
              }, 50)
            }, 300)
          } else {
            photoPreview.innerHTML = `<img src="${originalPhotoSrc}" alt="Profile Photo">`
          }
        }
      }
    }
  
    // Add skill tag
    function addSkillTag(skill) {
      if (!skill) return
  
      // Check if skill already exists
      const existingSkills = Array.from(skillsContainer.querySelectorAll(".skill-tag")).map((tag) =>
        tag.dataset.skill.toLowerCase(),
      )
  
      if (existingSkills.includes(skill.toLowerCase())) {
        showNotification("This skill already exists!", "error")
        return
      }
  
      const skillTag = document.createElement("div")
      skillTag.className = "skill-tag"
      skillTag.dataset.skill = skill
      skillTag.style.opacity = "0"
      skillTag.style.transform = "translateY(10px)"
  
      skillTag.innerHTML = `
              <span>${skill}</span>
              <button type="button" class="remove-skill" onclick="removeSkillTag(this)">×</button>
          `
  
      skillsContainer.appendChild(skillTag)
  
      // Animate the new skill tag
      setTimeout(() => {
        skillTag.style.transition = "all 0.3s ease"
        skillTag.style.opacity = "1"
        skillTag.style.transform = "translateY(0)"
      }, 10)
    }
  
    // Remove skill tag
    window.removeSkillTag = (button) => {
      const skillTag = button.closest(".skill-tag")
  
      // Animate removal
      skillTag.style.transition = "0.3s ease"
      skillTag.style.opacity = "0"
      skillTag.style.transform = "translateY(-10px)"
  
      setTimeout(() => {
        skillTag.remove()
      }, 300)
    }
  
    // Skill input handling
    if (skillInput) {
      skillInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && isEditMode) {
          e.preventDefault()
          const skill = skillInput.value.trim()
          if (skill) {
            addSkillTag(skill)
            skillInput.value = ""
          }
        }
      })
    }
  
    // Save resume with loading animation
    function saveResume() {
      if (!isEditMode) return
  
      // Show loading overlay
      showLoading()
  
      const formData = new FormData(resumeForm)
  
      // Collect skills
      const skills = Array.from(skillsContainer.querySelectorAll(".skill-tag")).map((tag) => tag.dataset.skill)
      formData.append("skills", JSON.stringify(skills))
  
      // Collect projects
      const projects = []
      document.querySelectorAll(".project-card").forEach((card) => {
        const project = {
          project_name: card.querySelector('input[name="projects[][project_name]"]').value,
          project_type: card.querySelector('select[name="projects[][project_type]"]').value,
          duration: `${card.querySelector('input[name="projects[][duration_start]"]').value}-${card.querySelector('input[name="projects[][duration_end]"]').value}`,
          github_link: card.querySelector('input[name="projects[][github_link]"]').value,
          description: card.querySelector('textarea[name="projects[][description]"]').value,
        }
        projects.push(project)
      })
      formData.append("projects", JSON.stringify(projects))
  
      // Collect certifications
      const certifications = []
      document.querySelectorAll(".certification-card").forEach((card) => {
        const cert = {
          certification_name: card.querySelector('input[name="certifications[][certification_name]"]').value,
          issuer: card.querySelector('input[name="certifications[][issuer]"]').value,
          duration: `${card.querySelector('input[name="certifications[][duration_start]"]').value}-${card.querySelector('input[name="certifications[][duration_end]"]').value}`,
          credential_id: card.querySelector('input[name="certifications[][credential_id]"]').value,
        }
        certifications.push(cert)
      })
      formData.append("certifications", JSON.stringify(certifications))
  
      fetch("/resume_edit", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          hideLoading()
  
          if (data.success) {
            // Update original photo source after successful save
            const img = photoPreview.querySelector("img")
            if (img) {
              originalPhotoSrc = img.src
            }
  
            showNotification(data.message, "success")
  
            // Reload the page after a short delay
            setTimeout(() => {
              window.location.reload()
            }, 1500)
          } else {
            showNotification("Error: " + data.error, "error")
          }
        })
        .catch((error) => {
          hideLoading()
          console.error("Error saving resume:", error)
          showNotification("Error saving resume: " + error.message, "error")
        })
    }
  
    // Show loading overlay
    function showLoading() {
      loadingOverlay.classList.add("active")
    }
  
    // Hide loading overlay
    function hideLoading() {
      loadingOverlay.classList.remove("active")
    }
  
    // Show notification
    function showNotification(message, type = "success") {
      notificationMessage.textContent = message
      notification.className = `notification ${type}`
      notification.style.display = "block"
  
      // Auto hide after 3 seconds
      setTimeout(() => {
        notification.style.animation = "fadeOut 0.3s ease-out"
        setTimeout(() => {
          notification.style.display = "none"
          notification.style.animation = ""
        }, 300)
      }, 3000)
    }
  
    // Add project card
    window.addProjectCard = () => {
      const projectsContainer = document.getElementById("projects-container")
      const projectCard = document.createElement("div")
      projectCard.className = "item-card project-card"
      projectCard.style.opacity = "0"
      projectCard.style.transform = "translateY(20px)"
  
      projectCard.innerHTML = `
              <div class="form-grid">
                  <div class="form-group">
                      <label>Project Name</label>
                      <div class="input-wrapper">
                          <input type="text" name="projects[][project_name]" required>
                          <span class="focus-border"></span>
                      </div>
                  </div>
                  <div class="form-group">
                      <label>Project Type</label>
                      <div class="select-wrapper">
                          <select name="projects[][project_type]" required>
                              <option value="academic">Academic</option>
                              <option value="personal">Personal</option>
                              <option value="professional">Professional</option>
                          </select>
                          <span class="focus-border"></span>
                      </div>
                  </div>
                  <div class="form-group">
                      <label>Duration</label>
                      <div class="duration-inputs">
                          <div class="input-wrapper">
                              <input type="month" name="projects[][duration_start]" required>
                              <span class="focus-border"></span>
                          </div>
                          <span>to</span>
                          <div class="input-wrapper">
                              <input type="month" name="projects[][duration_end]" required>
                              <span class="focus-border"></span>
                          </div>
                      </div>
                  </div>
                  <div class="form-group">
                      <label>GitHub Link</label>
                      <div class="input-wrapper">
                          <input type="url" name="projects[][github_link]">
                          <span class="focus-border"></span>
                      </div>
                  </div>
                  <div class="form-group full-width">
                      <label>Description</label>
                      <div class="input-wrapper">
                          <textarea name="projects[][description]" rows="3" required></textarea>
                          <span class="focus-border"></span>
                      </div>
                  </div>
              </div>
              <button type="button" class="remove-btn" onclick="removeCard(this)">
                  <i class="fas fa-trash"></i> Remove Project
              </button>
          `
  
      projectsContainer.appendChild(projectCard)
  
      // Animate the new card
      setTimeout(() => {
        projectCard.style.transition = "all 0.3s ease"
        projectCard.style.opacity = "1"
        projectCard.style.transform = "translateY(0)"
      }, 10)
    }
  
    // Add certification card
    window.addCertificationCard = () => {
      const certificationsContainer = document.getElementById("certifications-container")
      const certCard = document.createElement("div")
      certCard.className = "item-card certification-card"
      certCard.style.opacity = "0"
      certCard.style.transform = "translateY(20px)"
  
      certCard.innerHTML = `
              <div class="form-grid">
                  <div class="form-group">
                      <label>Certification Name</label>
                      <div class="input-wrapper">
                          <input type="text" name="certifications[][certification_name]" required>
                          <span class="focus-border"></span>
                      </div>
                  </div>
                  <div class="form-group">
                      <label>Issuing Organization</label>
                      <div class="input-wrapper">
                          <input type="text" name="certifications[][issuer]" required>
                          <span class="focus-border"></span>
                      </div>
                  </div>
                  <div class="form-group">
                      <label>Duration</label>
                      <div class="duration-inputs">
                          <div class="input-wrapper">
                              <input type="month" name="certifications[][duration_start]" required>
                              <span class="focus-border"></span>
                          </div>
                          <span>to</span>
                          <div class="input-wrapper">
                              <input type="month" name="certifications[][duration_end]" required>
                              <span class="focus-border"></span>
                          </div>
                      </div>
                  </div>
                  <div class="form-group">
                      <label>Credential ID</label>
                      <div class="input-wrapper">
                          <input type="text" name="certifications[][credential_id]">
                          <span class="focus-border"></span>
                      </div>
                  </div>
                  <div class="form-group">
                      <label>Certificate File</label>
                      <div class="file-upload-wrapper">
                          <input type="file" name="certificate_files[]" accept=".pdf,.doc,.docx">
                      </div>
                  </div>
              </div>
              <button type="button" class="remove-btn" onclick="removeCard(this)">
                  <i class="fas fa-trash"></i> Remove Certificate
              </button>
          `
  
      certificationsContainer.appendChild(certCard)
  
      // Animate the new card
      setTimeout(() => {
        certCard.style.transition = "all 0.3s ease"
        certCard.style.opacity = "1"
        certCard.style.transform = "translateY(0)"
      }, 10)
    }
  
    // Remove card
    window.removeCard = (button) => {
      const card = button.closest(".item-card")
  
      // Animate removal
      card.style.transition = "all 0.3s ease"
      card.style.opacity = "0"
      card.style.transform = "translateY(-20px)"
  
      setTimeout(() => {
        card.remove()
      }, 300)
    }
  
    // Add smooth section collapse
    function toggleSection(targetId) {
      const section = document.getElementById(targetId);
      const content = section.querySelector('.section-content');
      
      if (content.style.maxHeight) {
        content.style.maxHeight = null;
        setTimeout(() => {
          content.style.display = 'none';
        }, 300);
      } else {
        content.style.display = 'block';
        content.style.maxHeight = content.scrollHeight + "px";
      }
    }
  
    // Enhanced image preview loading
    function previewImage(input) {
      if (input.files && input.files[0]) {
        const preview = document.getElementById('photo-preview');
        const loadingState = preview.querySelector('.loading-state');
        
        loadingState.style.display = 'block';
        
        const reader = new FileReader();
        reader.onload = function(e) {
          const img = preview.querySelector('img');
          img.style.opacity = '0';
          
          setTimeout(() => {
            img.src = e.target.result;
            img.style.transition = 'opacity 0.3s ease';
            img.style.opacity = '1';
            loadingState.style.display = 'none';
          }, 500);
        };
        
        reader.readAsDataURL(input.files[0]);
      }
    }
  
    // Add input focus animations
    document.querySelectorAll('input, textarea').forEach(input => {
      input.addEventListener('focus', () => {
        if (!input.readOnly) {
          input.parentElement.classList.add('focused');
        }
      });
      
      input.addEventListener('blur', () => {
        input.parentElement.classList.remove('focused');
      });
      
      // Handle floating labels
      input.addEventListener('input', () => {
        if (input.value) {
          input.classList.add('has-value');
        } else {
          input.classList.remove('has-value');
        }
      });
    });
  
    // Enhance card animations
    document.querySelectorAll('.item-card').forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-5px)';
      });
      
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
      });
    });
  
    // Add download progress animation
    downloadBtn.addEventListener('click', () => {
      const progress = document.createElement('div');
      progress.className = 'download-progress';
      downloadBtn.appendChild(progress);
      
      progress.style.width = '100%';
      
      setTimeout(() => {
        progress.remove();
      }, 2000);
    });
  
    // Optionally, set the body background for extra safety
    document.body.style.background = "#fffbe6";
  
    // Initialize the form state
    initializeFormState()
  
    // Event listeners
    editBtn.addEventListener("click", toggleEditMode)
    saveBtn.addEventListener("click", saveResume)
    downloadBtn.addEventListener("click", () => {
      showLoading()
  
      const element = document.querySelector(".resume-builder")
      // Check if html2pdf is defined before using it
      if (typeof html2pdf !== "undefined") {
        html2pdf()
          .from(element)
          .save("resume.pdf")
          .then(() => {
            hideLoading()
            showNotification("Resume downloaded successfully!", "success")
          })
          .catch((error) => {
            hideLoading()
            showNotification("Error downloading resume: " + error.message, "error")
          })
      } else {
        hideLoading()
        showNotification("Error: html2pdf is not defined. Please ensure it is properly loaded.", "error")
      }
    })
  
    // Add smooth scrolling to sections
    document.querySelectorAll(".section-header").forEach((header) => {
      header.addEventListener("click", (e) => {
        if (e.target.closest(".collapse-btn")) return
  
        header.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      })
    })
  
    // Add input focus animations
    document.querySelectorAll("input, textarea, select").forEach((input) => {
      input.addEventListener("focus", () => {
        if (!input.readOnly && !input.disabled) {
          input.style.transform = "scale(1.02)"
        }
      })
  
      input.addEventListener("blur", () => {
        input.style.transform = "scale(1)"
      })
    })
  
    // Add button click animations
    document.querySelectorAll("button").forEach((button) => {
      button.addEventListener("click", () => {
        if (!button.disabled) {
          button.style.transform = "scale(0.95)"
          setTimeout(() => {
            button.style.transform = ""
          }, 150)
        }
      })
    })
  })
