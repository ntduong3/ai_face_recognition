const translations = window.APP_TRANSLATIONS.dashboard;
const formatMessage = (template, params) =>
  template.replace(/\{(\w+)\}/g, (_, key) => params[key] ?? "");

const langKey = (window.APP_CONFIG && window.APP_CONFIG.langStorageKey) || "lang";

$(function () {
  let currentLanguage = localStorage.getItem(langKey) || "vi";

  const applyLanguage = (lang) => {
    const dict = translations[lang] || translations.vi;
    currentLanguage = lang;
    document.documentElement.lang = lang === "en" ? "en" : "vi";
    document.title = dict.user_detail_title || document.title;
    $("[data-i18n]").each(function () {
      const key = $(this).data("i18n");
      if (dict[key]) {
        $(this).text(dict[key]);
      }
    });
  };

  applyLanguage(currentLanguage);

  const $missingSpan = $("[data-missing]");
  if ($missingSpan.length) {
    const missing = $missingSpan
      .data("missing")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
    const dict = translations[currentLanguage] || translations.vi;
    const labels = missing.map((angle) => dict[`angle_${angle}`] || angle);
    $missingSpan.text(labels.join(", "));
  }

  const $cardRoot = $(".card.primary[data-identity]");
  const identityId = $cardRoot.data("identity") || "";

  const updatePreview = ($card, file) => {
    if (!file) {
      return;
    }
    const reader = new FileReader();
    reader.onload = (event) => {
      let $img = $card.find(".angle-photo img");
      const $placeholder = $card.find(".angle-placeholder");
      if ($img.length === 0) {
        $img = $("<img />").attr("alt", $card.data("angle") || "");
        const $container = $card.find(".angle-photo");
        if ($container.length) {
          $container.empty().append($img);
        }
      }
      if ($placeholder.length) {
        $placeholder.remove();
      }
      $img.attr("src", event.target.result);
    };
    reader.readAsDataURL(file);
  };

  $("[data-angle-input]").on("change", function () {
    const $card = $(this).closest(".angle-card");
    if ($card.length === 0) {
      return;
    }
    updatePreview($card, this.files[0]);
  });

  $("[data-angle-save]").on("click", async function () {
    const angle = $(this).data("angleSave");
    const $card = $(this).closest(".angle-card");
    const $input = $card.find("[data-angle-input]");
    const file = $input.get(0)?.files?.[0];
    if (!file || !identityId) {
      alert(translations[currentLanguage].alert_need_photo);
      return;
    }

    const originalText = $(this).text();
    $(this).prop("disabled", true);
    $(this).text(translations[currentLanguage].updating_photo);

    const formData = new FormData();
    formData.append("identity_id", identityId);
    formData.append("images", file);
    formData.append("angles", angle);

    const response = await fetch("/v1/enroll", { method: "POST", body: formData });
    $(this).prop("disabled", false);
    $(this).text(originalText);

    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      alert(payload.error || translations[currentLanguage].alert_update_photo_fail);
      return;
    }

    alert(translations[currentLanguage].alert_update_photo_ok);
    location.reload();
  });
});
