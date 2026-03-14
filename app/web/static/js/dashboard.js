const translations = {
  vi: {
    title: "Dashboard - Face Attendance",
    app_name: "Face Attendance",
    dashboard_title: "Dashboard người dùng",
    total_users_label: "Tổng user",
    updated_label: "Cập nhật",
    export_list: "Xuất danh sách",
    add_user: "Thêm user",
    list_title: "Danh sách user",
    list_subtitle: "Quản lý nhận diện và điểm danh nhanh, sạch, chính xác.",
    search_placeholder: "Tìm theo ID, tên, phòng ban, email...",
    search_clear: "Xóa tìm kiếm",
    hint_client: "Tìm kiếm chạy trên trình duyệt để giảm tải server.",
    th_image: "Ảnh",
    th_id: "ID",
    th_name: "Họ tên",
    th_department: "Phòng ban",
    th_email: "Email",
    th_status: "Trạng thái",
    th_actions: "Hành động",
    action_edit: "Sửa",
    action_delete: "Xóa",
    guide_title: "Hướng dẫn ảnh chuẩn",
    guide_li1: "Mặt nhìn thẳng, đủ trán và cằm, không che mặt.",
    guide_li2: "Ánh sáng đều, nền sáng/đơn giản, không bị ngược sáng.",
    guide_li3: "Khuôn mặt chiếm ~60-70% khung hình, ảnh rõ nét, không mờ.",
    guide_tip: "Ưu tiên ảnh góc từ camera, hạn chế filter hoặc ảnh nén mạnh.",
    footer_text: "Quản trị hệ thống nhận diện",
    help: "Trợ giúp",
    settings: "Cài đặt",
    edit_title: "Chỉnh sửa user",
    create_title: "Thêm user + enroll",
    field_id: "Mã nhân viên",
    field_name: "Họ tên",
    field_department: "Phòng ban",
    field_email: "Email",
    field_status: "Trạng thái",
    field_avatar: "Ảnh đại diện",
    status_active: "Hoạt động",
    status_inactive: "Ngưng hoạt động",
    choose_new_photo: "Chọn ảnh mới",
    choose_photo: "Chọn ảnh",
    preview: "Preview",
    edit_upload_hint: "Nếu không chọn ảnh, hệ thống chỉ cập nhật thông tin.",
    create_upload_hint: "Ảnh rõ mặt, nhìn thẳng, không che mặt, nền sáng.",
    cancel: "Hủy",
    save: "Lưu",
    create: "Tạo + enroll",
    creating: "Đang tạo...",
    saving: "Đang lưu...",
    placeholder_id: "VD: NV001",
    placeholder_name: "Nguyễn Văn A",
    placeholder_department: "Kỹ thuật",
    placeholder_email: "email@congty.vn",
    alert_create_fail: "Không thể tạo/enroll user. Kiểm tra ảnh và ID đã tồn tại.",
    alert_update_fail: "Không thể cập nhật user.",
    alert_delete_fail: "Không thể xóa user.",
    confirm_delete: "Xóa user {id}?"
  },
  en: {
    title: "Dashboard - Face Attendance",
    app_name: "Face Attendance",
    dashboard_title: "User Dashboard",
    total_users_label: "Total users",
    updated_label: "Updated",
    export_list: "Export list",
    add_user: "Add user",
    list_title: "User list",
    list_subtitle: "Manage recognition and attendance quickly, cleanly, accurately.",
    search_placeholder: "Search by ID, name, department, email...",
    search_clear: "Clear search",
    hint_client: "Search runs in the browser to reduce server load.",
    th_image: "Photo",
    th_id: "ID",
    th_name: "Full name",
    th_department: "Department",
    th_email: "Email",
    th_status: "Status",
    th_actions: "Actions",
    action_edit: "Edit",
    action_delete: "Delete",
    guide_title: "Photo guidelines",
    guide_li1: "Face forward, include forehead and chin, no obstruction.",
    guide_li2: "Even light, bright/simple background, avoid backlight.",
    guide_li3: "Face fills ~60-70% of the frame, sharp and clear.",
    guide_tip: "Prefer straight camera shots, limit filters or heavy compression.",
    footer_text: "Recognition system admin",
    help: "Help",
    settings: "Settings",
    edit_title: "Edit user",
    create_title: "Add user + enroll",
    field_id: "Employee ID",
    field_name: "Full name",
    field_department: "Department",
    field_email: "Email",
    field_status: "Status",
    field_avatar: "Avatar",
    status_active: "Active",
    status_inactive: "Inactive",
    choose_new_photo: "Choose new photo",
    choose_photo: "Choose photo",
    preview: "Preview",
    edit_upload_hint: "If no photo is selected, only details will be updated.",
    create_upload_hint: "Clear face, looking forward, no obstruction, bright background.",
    cancel: "Cancel",
    save: "Save",
    create: "Create + enroll",
    creating: "Creating...",
    saving: "Saving...",
    placeholder_id: "e.g. EMP001",
    placeholder_name: "Jane Doe",
    placeholder_department: "Engineering",
    placeholder_email: "email@company.com",
    alert_create_fail: "Unable to create/enroll user. Check the photo and if the ID already exists.",
    alert_update_fail: "Unable to update user.",
    alert_delete_fail: "Unable to delete user.",
    confirm_delete: "Delete user {id}?",
    login: "Login",
    signup: "Sign up",
    footer_terms: "Terms of use",
    footer_privacy: "Privacy policy",
    footer_cookies: "Cookies",
    footer_rss: "RSS",
    footer_headline: "Leading Vietnamese digital outlet",
    footer_owner: "Under the Ministry of Science and Technology",
    footer_license: "License: 548/GP-BTTTT",
    footer_editor: "Editor-in-chief: Pham Van Hieu",
    footer_address: "Floor 10, Tower A, FPT Tower, 10 Pham Van Bach, Hanoi",
    footer_contact: "Phone: 024 7300 8899 ? Email: webmaster@faceattendance.vn",
    footer_copyright: "? 2026 Face Attendance. All rights reserved.",
    social_facebook: "Facebook",
    social_x: "X",
    social_youtube: "YouTube",
    social_instagram: "Instagram",
    social_rss: "RSS",
    social_facebook: "Facebook",
    social_x: "X",
    social_youtube: "YouTube",
    social_instagram: "Instagram",
    social_rss: "RSS",
    total_users_inline: "Total users:"
  }
};

const formatMessage = (template, params) =>
  template.replace(/\{(\w+)\}/g, (_, key) => params[key] ?? "");

const createForm = document.getElementById("createForm");
const editModalEl = document.getElementById("editModal");
const editModal = new bootstrap.Modal(editModalEl);
const editForm = document.getElementById("editForm");
const imageInput = document.getElementById("imageInput");
const previewBox = document.getElementById("previewBox");
const previewImage = document.getElementById("previewImage");
const editImageInput = document.getElementById("editImageInput");
const editPreviewBox = document.getElementById("editPreviewBox");
const editPreviewImage = document.getElementById("editPreviewImage");
const createModalEl = document.getElementById("createModal");
const createModal = new bootstrap.Modal(createModalEl);
const searchInput = document.getElementById("searchInput");
const clearSearch = document.getElementById("clearSearch");
const rows = Array.from(document.querySelectorAll(".table .row")).filter(
  (row) => !row.classList.contains("header")
);
const languageSelect = document.getElementById("languageSelect");
let currentLanguage = localStorage.getItem("lang") || "vi";

const applyLanguage = (lang) => {
  const dict = translations[lang] || translations.vi;
  currentLanguage = lang;
  document.documentElement.lang = lang === "en" ? "en" : "vi";
  document.title = dict.title;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.dataset.i18nPlaceholder;
    if (dict[key]) {
      el.setAttribute("placeholder", dict[key]);
    }
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((el) => {
    const key = el.dataset.i18nAria;
    if (dict[key]) {
      el.setAttribute("aria-label", dict[key]);
    }
  });
  document.querySelectorAll(".badge").forEach((badge) => {
    const isActive = badge.dataset.active === "true";
    badge.textContent = isActive ? dict.status_active : dict.status_inactive;
  });
};

languageSelect.value = currentLanguage;
applyLanguage(currentLanguage);

languageSelect.addEventListener("change", () => {
  const selected = languageSelect.value;
  localStorage.setItem("lang", selected);
  applyLanguage(selected);
});

const renderPreview = (file, box, image) => {
  if (!file) {
    box.classList.remove("active");
    image.src = "";
    return;
  }
  const reader = new FileReader();
  reader.onload = (event) => {
    image.src = event.target.result;
    box.classList.add("active");
  };
  reader.readAsDataURL(file);
};

imageInput.addEventListener("change", () => {
  renderPreview(imageInput.files[0], previewBox, previewImage);
});

editImageInput.addEventListener("change", () => {
  renderPreview(editImageInput.files[0], editPreviewBox, editPreviewImage);
});

createForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const submitButton = createForm.querySelector("button[type='submit']");
  submitButton.disabled = true;
  submitButton.textContent = translations[currentLanguage].creating;
  const formData = new FormData(createForm);
  const response = await fetch("/v1/enroll", { method: "POST", body: formData });
  submitButton.disabled = false;
  submitButton.textContent = translations[currentLanguage].create;
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    alert(payload.error || translations[currentLanguage].alert_create_fail);
    return;
  }
  createForm.reset();
  previewBox.classList.remove("active");
  previewImage.src = "";
  createModal.hide();
  location.reload();
});

const applySearch = () => {
  const query = searchInput.value.trim().toLowerCase();
  rows.forEach((row) => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(query) ? "" : "none";
  });
};

let searchTimer;
searchInput.addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(applySearch, 120);
});

clearSearch.addEventListener("click", () => {
  searchInput.value = "";
  applySearch();
  searchInput.focus();
});

document.querySelectorAll("[data-action='edit']").forEach((button) => {
  button.addEventListener("click", () => {
    const row = button.closest(".row");
    editForm.identity_id.value = row.dataset.id;
    editForm.name.value = row.querySelector(".name").textContent.trim();
    editForm.department.value = row.querySelector(".department").textContent.trim();
    editForm.email.value = row.querySelector(".email").textContent.trim();
    const badge = row.querySelector(".badge");
    editForm.active.value = badge.classList.contains("active") ? "true" : "false";

    const imageUrl = row.dataset.image;
    editImageInput.value = "";
    if (imageUrl) {
      editPreviewImage.src = imageUrl;
      editPreviewBox.classList.add("active");
    } else {
      editPreviewImage.src = "";
      editPreviewBox.classList.remove("active");
    }
    editModal.show();
  });
});

editForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const identityId = editForm.identity_id.value;
  const submitButton = editForm.querySelector("button[type='submit']");
  submitButton.disabled = true;
  submitButton.textContent = translations[currentLanguage].saving;

  const shouldUpdateImage = editImageInput.files.length > 0;
  let response;

  if (shouldUpdateImage) {
    const formData = new FormData();
    formData.append("identity_id", identityId);
    formData.append("name", editForm.name.value);
    formData.append("department", editForm.department.value);
    formData.append("email", editForm.email.value);
    formData.append("active", editForm.active.value);
    formData.append("image", editImageInput.files[0]);
    response = await fetch("/v1/enroll", { method: "POST", body: formData });
  } else {
    const payload = {
      name: editForm.name.value,
      department: editForm.department.value,
      email: editForm.email.value,
      active: editForm.active.value === "true",
    };
    response = await fetch(`/ui/users/${identityId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  }

  submitButton.disabled = false;
  submitButton.textContent = translations[currentLanguage].save;

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    alert(payload.error || translations[currentLanguage].alert_update_fail);
    return;
  }

  const row = document.querySelector(`.row[data-id='${identityId}']`);
  if (row) {
    row.querySelector(".name").textContent = editForm.name.value || "-";
    row.querySelector(".department").textContent = editForm.department.value || "-";
    row.querySelector(".email").textContent = editForm.email.value || "-";
    const badge = row.querySelector(".badge");
    const isActive = editForm.active.value === "true";
    badge.textContent = isActive
      ? translations[currentLanguage].status_active
      : translations[currentLanguage].status_inactive;
    badge.classList.toggle("active", isActive);
    badge.classList.toggle("inactive", !isActive);
    badge.dataset.active = isActive ? "true" : "false";
  }

  editModal.hide();
  if (shouldUpdateImage) {
    location.reload();
  }
});

document.querySelectorAll("[data-action='delete']").forEach((button) => {
  button.addEventListener("click", async () => {
    const row = button.closest(".row");
    const identityId = row.dataset.id;
    const confirmMessage = formatMessage(translations[currentLanguage].confirm_delete, {
      id: identityId,
    });
    if (!confirm(confirmMessage)) {
      return;
    }
    button.disabled = true;
    const response = await fetch(`/ui/users/${identityId}`, { method: "DELETE" });
    button.disabled = false;
    if (!response.ok) {
      alert(translations[currentLanguage].alert_delete_fail);
      return;
    }
    row.remove();
  });
});


const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");

if (loginBtn) {
  loginBtn.addEventListener("click", () => {
    window.location.href = "/login";
  });
}

if (signupBtn) {
  signupBtn.addEventListener("click", () => {
    window.location.href = "/register";
  });
}
