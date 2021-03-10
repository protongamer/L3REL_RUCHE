////////////////////////////////////////////////////////////
//Variables

let lines;
let current;
//let displayLittleWindow = false;
let windowMessage = "";


let phoneMode = false;

////////////////////////////////////////////////////////////







///////////////////////////////////////////////////////////////////////
//Languages

let fr_language = ["Janvier", "Février", "Mars", "Avril",
  "Mai", "Juin", "Juillet", "Août", "Septembre",
  "Octobre", "Novembre", "Décembre"
];


let en_language = ["January", "February", "March", "April",
  "May", "June", "July", "August", "September",
  "October", "November", "December"
];



///////////////////////////////////////////////////////////////////////





function setup() {
  createCanvas(windowWidth, windowHeight);
  lines = loadStrings('data/Y2021M04.txt');

  print(windowWidth);
  print(windowHeight);

}

function draw() {

  background(220);


  ///////////////////////////////////////////////////////////////////////////////////////////////////
  //graph
  let tempX, tempY, firstTime = true;
  let flag1 = false,
    flag2 = false;
  for (let i = 0; i < lines.length; i++) {
    current = parseData(lines[i]);
    stroke(0, 0, 0);
    if (firstTime) {
      tempX = 300 + (i * 10);
      tempY = 300 - (current.T);
      strokeWeight(5);
      if (mouseX > tempX - 5 && mouseX < tempX + 5 && mouseY > tempY - 5 && mouseY < tempY + 5) {
        rect(mouseX + 10, mouseY + 10, 125, 30);
        textSize(16);
        text(current.T + "%", mouseX + 20, mouseY + 30);
        stroke(255, 0, 0);
        flag1 = true;
        windowMessage = current.T + "%";
      }
      point(tempX, tempY);
      firstTime = false;
    } else {
      strokeWeight(1);
      line(tempX, tempY, 300 + (i * 10), 300 - (current.T));
      strokeWeight(5);
      if (mouseX > 300 + (i * 10) - 5 && mouseX < 300 + (i * 10) + 5 && mouseY > 300 - (current.T) - 5 && mouseY < 300 - (current.T) + 5) {
        rect(mouseX + 10, mouseY + 10, 125, 30);
        textSize(16);
        text(current.T + "%", mouseX + 20, mouseY + 30);
        stroke(255, 0, 0);
        flag2 = true;
        windowMessage = current.T + "%";
        print(windowMessage);
      }
      point(300 + (i * 10), 300 - (current.T));



      tempX = 300 + (i * 10);
      tempY = 300 - (current.T);
    }

    //point(300+(i*10),300-(current.T));  
  }
  
  stroke(0);
  strokeWeight(1);

  if (flag1 || flag2) {
   
    rect(mouseX + 10, mouseY + 10, 125, 30);
    textSize(16);
    fill(0);
    text(windowMessage, mouseX + 20, mouseY + 30);
     fill(255);
  }
  //End of graph
  //////////////////////////////////////////////////////////////////////////////////////////////////

  textSize(30);
  fill(0, 102, 153);
  //text(current.R, 10, 30);
  //text(current.D, 10, 60);
  //text(current.T, 10, 90);
  //text(current.H, 10, 120);
  fill(100, 102, 153);
  text(day(), 10, 180);
  text(en_language[month() - 1], 10, 210);
  text(year(), 10, 240);
  fill(100, 102, 0);
  text(second(), 10, 300);
  text(minute(), 10, 330);
  text(hour(), 10, 360);

  //print(timer);

  button(100, 200);

}







///////////////////////////////////////////////////////////////////
//Functions


//Godlike function -> The parser
function parseData(index_line) {

  let R = "";
  let D = "";
  let T = "";
  let H = "";
  let state = 0;

  //print(index_line.length);

  //start read line
  for (let i = 0; i < index_line.length; i++) {


    //Check if we have a code Character
    if (index_line[i] == " ") {
      state = 0;
    } else if (index_line[i] == "R") {
      state = 1;
    } else if (index_line[i] == "D") {
      state = 2;
    } else if (index_line[i] == "T") {
      state = 3;
    } else if (index_line[i] == "H") {
      state = 4;
    }

    //then read numbers
    else if (index_line[i] == "0" || index_line[i] == "1" || index_line[i] == "2" || index_line[i] == "3" || index_line[i] == "4" || index_line[i] == "5" ||
      index_line[i] == "6" || index_line[i] == "7" || index_line[i] == "8" || index_line[i] == "9" || index_line[i] == ".") {

      //then the state value

      switch (state) {

        case 1:
          R = R + index_line[i];
          break;

        case 2:
          D = D + index_line[i];
          break;

        case 3:
          T = T + index_line[i];
          break;

        case 4:
          H = H + index_line[i];
          break;

      }

    }





  }


  R = int(R);
  D = int(D);
  T = float(T);
  H = int(H);


  return {
    R,
    D,
    T,
    H
  }

}







function button(x, y) {


  fill(250);
  strokeWeight(1);
  rect(x, y, 100, 100);



}