const takePhotoInput = document.getElementById('take-photo-input');
const initialScreen = document.getElementById('initial-screen');
const secondScreen = document.getElementById('second-screen');
const initialBtn = document.getElementById('initial-btn');
const captureBtn = document.getElementById('capture-btn');
const boardArea  = document.getElementById('board-area');
const blackboard = document.getElementById('blackboard');
const sendBtn = document.getElementById('send-btn');
const loader = document.getElementById('loader');
const board = document.getElementById('board');


initialBtn.addEventListener('click', () => {
  takePhotoInput.click();
});
captureBtn.addEventListener('click', () => {
  takePhotoInput.click();
});
sendBtn.addEventListener('click', () => {
  blackboard.style.display = 'flex';
})


takePhotoInput.addEventListener('change', () => {
  if (takePhotoInput.files.length) {
    initialScreen.style.display = 'none';
    secondScreen.style.display = 'block';
    let reader = new FileReader();
    reader.onload = (event) => {
      let dataURL = event.target.result,
      context = board.getContext('2d'),
      image = new Image();
      image.onload = () => {
        board.width = image.width;
        board.height = image.height;
        context.drawImage(image, 0, 0, board.width, board.height);
        blackboard.style.display = 'none';
        boardArea.style.visibility = 'visible';
      };
      image.src = dataURL;
    };
    reader.readAsDataURL(takePhotoInput.files[0]);
  }
});
