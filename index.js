const quiz = [
  {
    question: '選択した項目をコピーするコマンドはどれ？',
    answers: [ 
      'ctrl + b', 
      'ctrl + c', 
      'ctrl + v', 
      'ctrl + z'
    ],
    correct: 'ctrl + c'
  }, {
    question: 'コピーした項目を貼り付けるコマンドはどれ？',
    answers: [ 
      'ctrl + z', 
      'ctrl + x',
      'ctrl + v', 
      'ctrl + a'
    ],
    correct: 'ctrl + v'
  }, {
    question: '選択した項目を切り取るコマンドはどれ？',
    answers: [ 
     'ctrl + x',
     'ctrl + z',
     'ctrl + y', 
     'ctrl + s', 
    ],
    correct: 'ctrl + x'
  }, {
    question: 'すべての項目を選択するコマンドはどれ？',
    answers: [ 
     'ctrl + s',
     'ctrl + f',
     'ctrl + d', 
     'ctrl + a', 
    ],
    correct: 'ctrl + a'
  },{
    question: '行った操作を元に戻すコマンドはどれ？',
    answers: [ 
     'ctrl + z',
     'ctrl + s',
     'ctrl + d', 
     'ctrl + q', 
    ],
    correct: 'ctrl + z'
  },{
    question: '元に戻した操作をやり直すコマンドはどれ？',
    answers: [ 
     'ctrl + t',
     'ctrl + y',
     'ctrl + u', 
     'ctrl + i', 
    ],
    correct: 'ctrl + y'
  },{
    question: '実行中のファイルを保存するコマンドはどれ？',
    answers: [ 
     'ctrl + w',
     'ctrl + e',
     'ctrl + d', 
     'ctrl + s', 
    ],
    correct: 'ctrl + s'
  },{
    question: '新しいファイル、ウィンドウを開くコマンドはどれ？',
    answers: [ 
     'ctrl + b',
     'ctrl + n',
     'ctrl + f', 
     'ctrl + m', 
    ],
    correct: 'ctrl + n'
  },{
    question: '既に作成済みのファイルを開くコマンドはどれ？',
    answers: [ 
     'ctrl + p',
     'ctrl + o',
     'ctrl + i', 
     'ctrl + u', 
    ],
    correct: 'ctrl + o'
  },{
    question: 'デスクトップを表示するコマンドはどれ？',
    answers: [ 
     'Windows + e',
     'Windows + r',
     'Windows + d', 
     'Windows + f', 
    ],
    correct: 'Windows + d'
  }
];
const quizLength = quiz.length;
let quizIndex = 0;
let score = 0;

const corrects = quiz[quizIndex].correct;

const $button = document.getElementsByTagName("button");
const buttonLength = $button.length;


const setupQuiz = () => {
  document.getElementById('jsq').textContent = quiz[quizIndex].question;
  let buttonIndex = 0;
  while(buttonIndex < buttonLength){
    $button[buttonIndex].textContent = quiz[quizIndex].answers[buttonIndex];
    buttonIndex++;
  }
}
setupQuiz();

const clickHandler = (e) => {
  if(quiz[quizIndex].correct === e.target.textContent){
    window.alert("正解!");
    score++;
  }else{
    window.alert("不正解！\n正しくは" + corrects + "です。");
  }

  quizIndex++;

  if(quizIndex < quizLength){
    setupQuiz();
  }else{
    window.alert("終了！あなたの正解数は" + quizLength + "問中" + score + "問です。");
  }
};

let handlerIndex = 0;
while(handlerIndex < buttonLength){
  $button[handlerIndex].addEventListener("click", (e) => {
    clickHandler(e);
  });
  handlerIndex++;
}
