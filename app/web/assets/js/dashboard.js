const translations = window.APP_TRANSLATIONS.dashboard;
const formatMessage = (template, params) =>
  template.replace(/\{(\w+)\}/g, (_, key) => params[key] ?? "");

const langKey = (window.APP_CONFIG && window.APP_CONFIG.langStorageKey) || "lang";

$(function () {
  const $createForm = $("#createForm");
  const $editForm = $("#editForm");
  const $editAngleWarning = $("#editAngleWarning");
  const $editMissingAngles = $("#editMissingAngles");
  const $editImagesLink = $("#editImagesLink");
  const $createAngleInputs = $("#createForm input[type='file'][data-angle]");
  const $searchInput = $("#searchInput");
  const $clearSearch = $("#clearSearch");
  const $rows = $(".table .row").not(".header");
  const $languageSelect = $("#languageSelect");
  const editModalEl = $("#editModal").get(0);
  const createModalEl = $("#createModal").get(0);
  const editModal = editModalEl ? new bootstrap.Modal(editModalEl) : null;
  const createModal = createModalEl ? new bootstrap.Modal(createModalEl) : null;

  let currentLanguage = localStorage.getItem(langKey) || "vi";

  const applyLanguage = (lang) => {
    const dict = translations[lang] || translations.vi;
    currentLanguage = lang;
    document.documentElement.lang = lang === "en" ? "en" : "vi";
    document.title = dict.title;
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
    $("[data-i18n-aria]").each(function () {
      const key = $(this).data("i18nAria");
      if (dict[key]) {
        $(this).attr("aria-label", dict[key]);
      }
    });
    $(".badge").each(function () {
      const isActive = $(this).data("active") === true || $(this).data("active") === "true";
      $(this).text(isActive ? dict.status_active : dict.status_inactive);
    });
  };

  $languageSelect.val(currentLanguage);
  applyLanguage(currentLanguage);

  $languageSelect.on("change", function () {
    const selected = $languageSelect.val();
    localStorage.setItem(langKey, selected);
    applyLanguage(selected);
  });

  const renderPreview = (file, $box, $image) => {
    if (!file) {
      $box.removeClass("active");
      $image.attr("src", "");
      return;
    }
    const reader = new FileReader();
    reader.onload = (event) => {
      $image.attr("src", event.target.result);
      $box.addClass("active");
    };
    reader.readAsDataURL(file);
  };

  const bindAngleInputs = ($inputs) => {
    $inputs.each(function () {
      const $input = $(this);
      const $card = $input.closest(".angle-card");
      if ($card.length === 0) {
        return;
      }
      const $previewBox = $card.find(".preview");
      const $previewImage = $card.find(".preview img");
      if ($previewBox.length === 0 || $previewImage.length === 0) {
        return;
      }
      $input.on("change", function () {
        renderPreview(this.files[0], $previewBox, $previewImage);
      });
    });
  };

  bindAngleInputs($createAngleInputs);

  $createForm.on("submit", async function (event) {
    event.preventDefault();
    const $submitButton = $createForm.find("button[type='submit']");
    $submitButton.prop("disabled", true);
    $submitButton.text(translations[currentLanguage].creating);

    const formData = new FormData(this);
    const angleFiles = [];
    $createAngleInputs.each(function () {
      if (this.files.length > 0) {
        angleFiles.push({ file: this.files[0], angle: $(this).data("angle") });
      }
    });

    let response;
    if (angleFiles.length === 0) {
      response = await fetch("/ui/users/", { method: "POST", body: formData });
    } else {
      angleFiles.forEach((item) => {
        formData.append("images", item.file);
        formData.append("angles", item.angle);
      });
      response = await fetch("/v1/enroll", { method: "POST", body: formData });
    }

    $submitButton.prop("disabled", false);
    $submitButton.text(translations[currentLanguage].create);
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      alert(payload.error || translations[currentLanguage].alert_create_fail);
      return;
    }
    this.reset();
    $createAngleInputs.each(function () {
      const $card = $(this).closest(".angle-card");
      if ($card.length === 0) {
        return;
      }
      const $previewBox = $card.find(".preview");
      const $previewImage = $card.find(".preview img");
      if ($previewBox.length && $previewImage.length) {
        $previewBox.removeClass("active");
        $previewImage.attr("src", "");
      }
    });
    if (createModal) {
      createModal.hide();
    }
    location.reload();
  });

  const applySearch = () => {
    const query = ($searchInput.val() || "").trim().toLowerCase();
    $rows.each(function () {
      const text = $(this).text().toLowerCase();
      $(this).toggle(text.includes(query));
    });
  };

  let searchTimer;
  $searchInput.on("input", function () {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(applySearch, 120);
  });

  $clearSearch.on("click", function () {
    $searchInput.val("");
    applySearch();
    $searchInput.trigger("focus");
  });

  $("[data-action='edit']").on("click", function () {
    const $row = $(this).closest(".row");
    const editFormEl = $editForm.get(0);
    editFormEl.identity_id.value = $row.data("id");
    editFormEl.name.value = $row.find(".name").text().trim();
    editFormEl.department.value = $row.find(".department").text().trim();
    editFormEl.email.value = $row.find(".email").text().trim();
    const $badge = $row.find(".badge").first();
    editFormEl.active.value = $badge.hasClass("active") ? "true" : "false";

    const imagesPayload = $row.attr("data-images") || "{}";
    let images = {};
    try {
      images = JSON.parse(imagesPayload);
    } catch (err) {
      images = {};
    }

    if ($editImagesLink.length) {
      $editImagesLink.attr("href", `/users/${$row.data("id")}`);
    }

    if (editModal) {
      editModal.show();
    }

    if ($editAngleWarning.length && $editMissingAngles.length) {
      const missing = [];
      ["front", "left", "right", "up", "down"].forEach((angle) => {
        if (!images?.[angle]?.image_url) {
          missing.push(angle);
        }
      });
      if (missing.length > 0) {
        const dict = translations[currentLanguage] || translations.vi;
        const labels = missing.map((angle) => dict[`angle_${angle}`] || angle);
        $editMissingAngles.text(labels.join(", "));
        $editAngleWarning.css("display", "flex");
      } else {
        $editMissingAngles.text("");
        $editAngleWarning.hide();
      }
    }
  });

  $editForm.on("submit", async function (event) {
    event.preventDefault();
    const editFormEl = $editForm.get(0);
    const identityId = editFormEl.identity_id.value;
    const $submitButton = $editForm.find("button[type='submit']");
    $submitButton.prop("disabled", true);
    $submitButton.text(translations[currentLanguage].saving);

    const payload = {
      name: editFormEl.name.value,
      department: editFormEl.department.value,
      email: editFormEl.email.value,
      active: editFormEl.active.value === "true",
    };
    const response = await fetch(`/ui/users/${identityId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    $submitButton.prop("disabled", false);
    $submitButton.text(translations[currentLanguage].save);

    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      alert(payload.error || translations[currentLanguage].alert_update_fail);
      return;
    }

    const $row = $(`.row[data-id='${identityId}']`);
    if ($row.length) {
      $row.find(".name").text(editFormEl.name.value || "-");
      $row.find(".department").text(editFormEl.department.value || "-");
      $row.find(".email").text(editFormEl.email.value || "-");
      const $badge = $row.find(".badge").first();
      const isActive = editFormEl.active.value === "true";
      $badge.text(isActive ? translations[currentLanguage].status_active : translations[currentLanguage].status_inactive);
      $badge.toggleClass("active", isActive);
      $badge.toggleClass("inactive", !isActive);
      $badge.attr("data-active", isActive ? "true" : "false");
    }

    if (editModal) {
      editModal.hide();
    }
  });

  $("[data-action='delete']").on("click", async function () {
    const $button = $(this);
    const $row = $button.closest(".row");
    const identityId = $row.data("id");
    const confirmMessage = formatMessage(translations[currentLanguage].confirm_delete, {
      id: identityId,
    });
    if (!confirm(confirmMessage)) {
      return;
    }
    $button.prop("disabled", true);
    const response = await fetch(`/ui/users/${identityId}`, { method: "DELETE" });
    $button.prop("disabled", false);
    if (!response.ok) {
      alert(translations[currentLanguage].alert_delete_fail);
      return;
    }
    $row.remove();
  });

  const $loginBtn = $("#loginBtn");
  const $signupBtn = $("#signupBtn");

  if ($loginBtn.length) {
    $loginBtn.on("click", function () {
      window.location.href = "/login";
    });
  }

  if ($signupBtn.length) {
    $signupBtn.on("click", function () {
      window.location.href = "/register";
    });
  }
});
