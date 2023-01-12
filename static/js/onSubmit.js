async function onSubmit() {
  event.preventDefault();
  const form = event.target;
  const isLoadingElem = form.querySelector('#isLoading');
  const errorMsgElem = form.querySelector('#helpMsg');
  const submitBtn = form.querySelector('button[type="submit"]');
  const  url = location.pathname.includes('login') ? '\/login' : '\/';

  try {
    isLoadingElem.classList.remove('d-none');
    errorMsgElem.classList.add('d-none');
    submitBtn.setAttribute('disabled', true);

    const response = await fetch(url, {
      method: 'POST',
      body: new FormData(form),
    });

    if (!response.ok) {
      throw new Error();
    }

    if (form.querySelector('input[type="file"]')) {
      const fileName = form.querySelector('input').files[0].name + '_' + Date.now() + '.csv';

      const blob = await response.blob();

      const saveFile = document.querySelector('#saveFile');
      saveFile.setAttribute('href', URL.createObjectURL(blob));
      saveFile.setAttribute('download', fileName);
      saveFile.click();  
    } else {
      location.href = '/';
    }

    form.reset();
  } catch (err) {
    console.error(err);
    errorMsgElem.classList.remove('d-none');
  } finally {
    isLoadingElem.classList.add('d-none');
    submitBtn.removeAttribute('disabled');
  }
} 
