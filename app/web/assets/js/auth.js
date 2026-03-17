const translations = window.APP_TRANSLATIONS.auth;
const langKey = (window.APP_CONFIG && window.APP_CONFIG.langStorageKey) || "lang";

const applyLanguage = (lang) => {
  const dict = translations[lang] || translations.vi;
  document.documentElement.lang = lang === "en" ? "en" : "vi";
  $("[data-i18n]").each(function () {
    const key = $(this).data("i18n");
    if (dict[key]) {
      $(this).text(dict[key]);
    }
  });
  $("[data-i18n-placeholder]").each(function () {
    const key = $(this).data("i18nPlaceholder");
    if (dict[key]) {
      $(this).attr("placeholder", dict[key]);
    }
  });
  return dict;
};

const validateEmail = (value) => /.+@.+\..+/.test(value);

$(function () {
  const currentLanguage = localStorage.getItem(langKey) || "vi";
  const messages = applyLanguage(currentLanguage);

  const setError = ($input, message) => {
    const inputId = $input.attr("id");
    const $holder = $(`[data-error-for='${inputId}']`);
    if ($holder.length) {
      $holder.text(message || "");
    }
    $input.toggleClass("is-invalid", Boolean(message));
  };

  const attachLoginValidation = ($form) => {
    const $email = $form.find("#loginEmail");
    const $password = $form.find("#loginPassword");

    $form.on("submit", function (event) {
      event.preventDefault();
      let valid = true;

      if (!$email.val().trim()) {
        setError($email, messages.err_email_required);
        valid = false;
      } else if (!validateEmail($email.val().trim())) {
        setError($email, messages.err_email_invalid);
        valid = false;
      } else {
        setError($email, "");
      }

      if (!$password.val().trim()) {
        setError($password, messages.err_password_required);
        valid = false;
      } else if ($password.val().length < 8) {
        setError($password, messages.err_password_short);
        valid = false;
      } else {
        setError($password, "");
      }

      if (valid) {
        this.submit();
      }
    });

    $email.on("input", function () {
      setError($email, "");
    });
    $password.on("input", function () {
      setError($password, "");
    });
  };

  const attachRegisterValidation = ($form) => {
    const $name = $form.find("#registerName");
    const $email = $form.find("#registerEmail");
    const $password = $form.find("#registerPassword");
    const $confirm = $form.find("#registerConfirm");

    $form.on("submit", function (event) {
      event.preventDefault();
      let valid = true;

      if (!$name.val().trim()) {
        setError($name, messages.err_name_required);
        valid = false;
      } else {
        setError($name, "");
      }

      if (!$email.val().trim()) {
        setError($email, messages.err_email_required);
        valid = false;
      } else if (!validateEmail($email.val().trim())) {
        setError($email, messages.err_email_invalid);
        valid = false;
      } else {
        setError($email, "");
      }

      if (!$password.val().trim()) {
        setError($password, messages.err_password_required);
        valid = false;
      } else if ($password.val().length < 8) {
        setError($password, messages.err_password_short);
        valid = false;
      } else {
        setError($password, "");
      }

      if (!$confirm.val().trim()) {
        setError($confirm, messages.err_confirm_required);
        valid = false;
      } else if ($confirm.val() !== $password.val()) {
        setError($confirm, messages.err_confirm_mismatch);
        valid = false;
      } else {
        setError($confirm, "");
      }

      if (valid) {
        this.submit();
      }
    });

    $name.on("input", function () {
      setError($name, "");
    });
    $email.on("input", function () {
      setError($email, "");
    });
    $password.on("input", function () {
      setError($password, "");
    });
    $confirm.on("input", function () {
      setError($confirm, "");
    });
  };

  const $loginForm = $("#loginForm");
  if ($loginForm.length) {
    attachLoginValidation($loginForm);
  }

  const $registerForm = $("#registerForm");
  if ($registerForm.length) {
    attachRegisterValidation($registerForm);
  }
});
