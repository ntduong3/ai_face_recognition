const translations = {
  vi: {
    app_name: "Face Attendance",
    login_title: "Đăng nhập",
    login_subtitle: "Chào mừng bạn trở lại. Vui lòng nhập thông tin để tiếp tục.",
    register_title: "Đăng ký",
    register_subtitle: "Tạo tài khoản mới để bắt đầu quản lý dữ liệu nhận diện.",
    label_name: "Họ tên",
    label_email: "Email",
    label_password: "Mật khẩu",
    label_confirm: "Xác nhận mật khẩu",
    placeholder_name: "Nguyễn Văn A",
    placeholder_email: "email@congty.vn",
    placeholder_password: "Tối thiểu 8 ký tự",
    placeholder_confirm: "Nhập lại mật khẩu",
    login_btn: "Đăng nhập",
    register_btn: "Đăng ký",
    no_account: "Bạn chưa có tài khoản?",
    have_account: "Đã có tài khoản?",
    go_register: "Đăng ký",
    go_login: "Đăng nhập",
    footer_rights: "© 2026. All rights reserved.",
    footer_terms: "Điều khoản",
    footer_privacy: "Chính sách",
    footer_support: "Hỗ trợ",
    err_email_required: "Vui lòng nhập email.",
    err_email_invalid: "Email không hợp lệ.",
    err_password_required: "Vui lòng nhập mật khẩu.",
    err_password_short: "Mật khẩu tối thiểu 8 ký tự.",
    err_name_required: "Vui lòng nhập họ tên.",
    err_confirm_required: "Vui lòng xác nhận mật khẩu.",
    err_confirm_mismatch: "Mật khẩu xác nhận không khớp."
  },
  en: {
    app_name: "Face Attendance",
    login_title: "Sign in",
    login_subtitle: "Welcome back. Please enter your details to continue.",
    register_title: "Sign up",
    register_subtitle: "Create a new account to start managing recognition data.",
    label_name: "Full name",
    label_email: "Email",
    label_password: "Password",
    label_confirm: "Confirm password",
    placeholder_name: "Jane Doe",
    placeholder_email: "email@company.com",
    placeholder_password: "Minimum 8 characters",
    placeholder_confirm: "Re-enter password",
    login_btn: "Sign in",
    register_btn: "Sign up",
    no_account: "Don't have an account?",
    have_account: "Already have an account?",
    go_register: "Sign up",
    go_login: "Sign in",
    footer_rights: "© 2026. All rights reserved.",
    footer_terms: "Terms",
    footer_privacy: "Privacy",
    footer_support: "Support",
    err_email_required: "Please enter your email.",
    err_email_invalid: "Invalid email address.",
    err_password_required: "Please enter your password.",
    err_password_short: "Password must be at least 8 characters.",
    err_name_required: "Please enter your name.",
    err_confirm_required: "Please confirm your password.",
    err_confirm_mismatch: "Passwords do not match."
  }
};

const applyLanguage = (lang) => {
  const dict = translations[lang] || translations.vi;
  document.documentElement.lang = lang === "en" ? "en" : "vi";
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
  return dict;
};

const currentLanguage = localStorage.getItem("lang") || "vi";
const messages = applyLanguage(currentLanguage);

const setError = (input, message) => {
  const holder = document.querySelector(`[data-error-for='${input.id}']`);
  if (holder) {
    holder.textContent = message || "";
  }
  input.classList.toggle("is-invalid", Boolean(message));
};

const validateEmail = (value) => /.+@.+\..+/.test(value);

const attachLoginValidation = (form) => {
  const email = form.querySelector("#loginEmail");
  const password = form.querySelector("#loginPassword");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    let valid = true;

    if (!email.value.trim()) {
      setError(email, messages.err_email_required);
      valid = false;
    } else if (!validateEmail(email.value.trim())) {
      setError(email, messages.err_email_invalid);
      valid = false;
    } else {
      setError(email, "");
    }

    if (!password.value.trim()) {
      setError(password, messages.err_password_required);
      valid = false;
    } else if (password.value.length < 8) {
      setError(password, messages.err_password_short);
      valid = false;
    } else {
      setError(password, "");
    }

    if (valid) {
      form.submit();
    }
  });

  [email, password].forEach((input) => {
    input.addEventListener("input", () => setError(input, ""));
  });
};

const attachRegisterValidation = (form) => {
  const name = form.querySelector("#registerName");
  const email = form.querySelector("#registerEmail");
  const password = form.querySelector("#registerPassword");
  const confirm = form.querySelector("#registerConfirm");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    let valid = true;

    if (!name.value.trim()) {
      setError(name, messages.err_name_required);
      valid = false;
    } else {
      setError(name, "");
    }

    if (!email.value.trim()) {
      setError(email, messages.err_email_required);
      valid = false;
    } else if (!validateEmail(email.value.trim())) {
      setError(email, messages.err_email_invalid);
      valid = false;
    } else {
      setError(email, "");
    }

    if (!password.value.trim()) {
      setError(password, messages.err_password_required);
      valid = false;
    } else if (password.value.length < 8) {
      setError(password, messages.err_password_short);
      valid = false;
    } else {
      setError(password, "");
    }

    if (!confirm.value.trim()) {
      setError(confirm, messages.err_confirm_required);
      valid = false;
    } else if (confirm.value !== password.value) {
      setError(confirm, messages.err_confirm_mismatch);
      valid = false;
    } else {
      setError(confirm, "");
    }

    if (valid) {
      form.submit();
    }
  });

  [name, email, password, confirm].forEach((input) => {
    input.addEventListener("input", () => setError(input, ""));
  });
};

const loginForm = document.getElementById("loginForm");
if (loginForm) {
  attachLoginValidation(loginForm);
}

const registerForm = document.getElementById("registerForm");
if (registerForm) {
  attachRegisterValidation(registerForm);
}
