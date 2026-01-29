//alert("verify-captcha.js loaded");

console.log("verify-captcha.js loaded");

// Check that RECAPTCHA_SITE_KEY is defined
console.log("Site key is:", RECAPTCHA_SITE_KEY);

// Check that grecaptcha exists
if (typeof grecaptcha === 'undefined') {
  console.error("grecaptcha is not defined yet!");
}

function verifyCaptcha(){
  function bind() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      setTimeout(() => {
          grecaptcha.ready(function () {
          grecaptcha.execute(RECAPTCHA_SITE_KEY, { action: 'submit' }).then(function (token) {
            document.getElementById('g-recaptcha-response').value = token;
            console.log('Captcha token set:', token);
            form.submit();
          }).catch(function (error) {
            console.error('Error executing reCAPTCHA:', error);
          });
        });
      }, 1000);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }
};

verifyCaptcha();