window.onload = function() {
    fetch('/templates').then(response => response.json()).then(data => {
        let templateSelect = document.getElementById('template');
        data.forEach(template => {
            let option = document.createElement('option');
            option.value = Object.keys(template)[0];
            option.text = template[Object.keys(template)[0]];
            templateSelect.appendChild(option);
        });
    });
};

document.getElementById('pptForm').onsubmit = function(event) {
    event.preventDefault();
    const formData = {
        template: document.getElementById('template').value,
        title: document.getElementById('title').value,
        subtitle: document.getElementById('subtitle').value,
        slides: JSON.parse(document.getElementById('slides').value)
    };

    fetch('/generate_presentation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    }).then(response => response.blob())
      .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'output.pptx';
          document.body.appendChild(a);
          a.click();
          a.remove();
      });
};
