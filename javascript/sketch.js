


////////////////////////////////////////////////////////////
//Variables

let lines;
let current;
//let displayLittleWindow = false;
let windowMessage = "";


/////////////////////////////
//Button vars
let buttonFlag = 0;
const b_yNext = 1;
const b_yPrev = 2;
const b_mNext = 3;
const b_mPrev = 4;
const b_loadData = 5;
const b_lNext = 6;
const b_hNext = 7;
const b_hPrev = 8;


////////////////////////////


let d_year;
let d_month;
let d_hive = 1;


let loaded = false;

////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////
//Pictures


let flag_en, flag_fr, flag_es, flag_it, flag_ch, flag_jp, flag_rs;
let logo;




///////////////////////////////////////////////////////////////////////
//Languages

let fr_language = ["Janvier", "Février", "Mars", "Avril",
  "Mai", "Juin", "Juillet", "Août", "Septembre",
  "Octobre", "Novembre", "Décembre", "Humidité(%)",
  "Température (°C)", "Jours", "Charger", "Ruche ", "Jour : ",
  "Heure : "
];


let en_language = ["January", "February", "March", "April",
  "May", "June", "July", "August", "September",
  "October", "November", "December", "Humidity(%)",
  "Temperature(°C)", "Days", "Load Data", "Hive ", "Day : ",
  "Time : "
];


let es_language = ["Enero", "Febrero", "Marzo", "Abril",
  "Mayo", "Junio", "Julio", "Augosto", "Septiembre",
  "Octubre", "Noviembre", "Diciembre", "Humedad(%)",
  "Temperatura(°C)", "Dias", "Cargar", "Colmena ", "Día : ",
  "Hora : "
];

let it_language = ["Gennaio", "Febbraio", "Marzo", "Aprile",
  "Maggio", "Guigno", "Luglio", "Agosto", "Settembre",
  "Ottobre", "Novembre", "Dicembre", "Umidità(%)",
  "Temperatura(°C)", "Giorni", "Caricare", "Alveare ", "Giorno : ",
  "Tempo : "
];

let ch_language = ["一月", "二月", "行进", "四月",
  "能够", "六月", "七月", "八月", "九月",
  "十月", "十一月", "十二月", "湿度(%)",
  "温度(°C)", "天", "加载", "蜂巢 ", "天 : ",
  "时间 : "
];

let jp_language = ["1月", "2月", "行進", "4月",
  "できる", "六月", "7月", "8月", "9月",
  "10月", "11月", "12月", "湿度(%)",
  "温度(°C)", "日", "負荷", "ハイブ ", "日 : ",
  "時間 : "
];

let rs_language = ["Январь", "Февраль", "марш", "апреля",
  "Может", "июнь", "июль", "август", "сентябрь",
  "Октябрь", "Ноябрь", "Декабрь", "Влажность(%)",
  "Температура(°C)", "День", "Нагрузка", "Улей ", "день : ",
  "время : "
];








const en = 0;
const fr = 1;
const es = 2;
const it = 3;
const ch = 4;
const jp = 5;
const rs = 6;




let languages = [en_language, fr_language, es_language, it_language, ch_language, jp_language, rs_language];

let l_select = en;

///////////////////////////////////////////////////////////////////////


function preload()
{
  
   flag_en = loadImage('pictures/flag0.png');
   flag_fr = loadImage('pictures/flag1.png');
   flag_es = loadImage('pictures/flag2.png');
   flag_it = loadImage('pictures/flag3.png');
   flag_ch = loadImage('pictures/flag4.png');
   flag_jp = loadImage('pictures/flag5.png');
   flag_rs = loadImage('pictures/flag6.png');
   logo = loadImage('pictures/Logo.png');
  
}





function setup() {
  
  createCanvas(1600, 900); //define a const resolution
  

  //print(windowWidth);
  //print(windowHeight);
  
  
d_year = year();
d_month = month();

}

function draw() {

  background(220);

  image(logo, 0,0);
  
   
  
  //set a button to load data
  if(button(10,275,100,40, languages[l_select][15])){
    buttonFlag = b_loadData;
  }
  
  //set a buttons to set month / year
  if(button(125,210,30,40, "→")){
    buttonFlag = b_yNext;
  }
  
  if(button(10,210,30,40, "←")){
    buttonFlag = b_yPrev;
  }
  
  if(button(195,150,30,40, "→")){
    buttonFlag = b_mNext;
  }
  
  if(button(10,150,30,40, "←")){
    buttonFlag = b_mPrev;
  }
  
  if(button(10,75,62,42)){
    buttonFlag = b_lNext;
  }
  
  if(button(550,75,30,40, "→")){
    buttonFlag = b_hNext;
  }
  
  if(button(320,75,30,40, "←")){
    buttonFlag = b_hPrev;
  }
  
  switch(l_select){
      
    case en:
      image(flag_en, 10,75);
      break;
      
    case fr:
      image(flag_fr, 10,75);
      break;
      
    case es:
      image(flag_es, 10,75);
      break;
      
    case it:
      image(flag_it, 10,75);
      break;
      
    case ch:
      image(flag_ch, 10,75);
      break;
      
    case jp:
      image(flag_jp, 10,75);
      break;
      
    case rs:
      image(flag_rs, 10,75);
      break;
          
  }
  
  
  
  if(!mouseIsPressed){
    
    switch(buttonFlag){
        
      case b_loadData:
        
        let localTimer = millis();
        let localString = 'data/';
        
        //////////////////////////////////
        //Set year
        localString += 'Y' + d_year;
        
        if(d_month < 10)
        {
          localString += 'M0' + d_month;
        }else
        {
          localString += 'M' + d_month;
        }
        
        localString += '.txt'; // add fileformat
        
        //debug
        
        
        lines = loadStrings(localString);
        while(millis() - localTimer < 500); //Wait a little bit
        loaded = true;
        
        
        
        break;
        
      case b_yNext:
        
        d_year++;
        
        break;
        
      case b_yPrev:
        
        d_year--;
        
        break;
        
      case b_mNext:
        
        d_month++;
        
        if(d_month > 12){
          d_month = 1;
        }
        
        break;
        
      case b_mPrev:
        
        d_month--;
        
        if(d_month < 1){
          d_month = 12;
        }        
        
        break;
        
      
      case b_lNext:
        
        l_select++;
        if(l_select > 6)
          l_select = 0;
        break;
        
      case b_hNext:
        
        d_hive++;
        if(d_hive > 42)
          l_select = 42;
        break;
        
      case b_hPrev:
        
        d_hive--;
        if(d_hive < 1)
          d_hive = 1;
        break;
        
        
    }
    
    buttonFlag = 0; //reset flag
  }
  
  
  
  
  
  
  if(loaded == true){
  
  graph(lines, 'T', d_hive, 300, 150);
  
  graph(lines, 'H', d_hive, 300, 420);

  }

  textSize(30);
  fill(0, 102, 153);
  //text(current.R, 10, 30);
  //text(current.D, 10, 60);
  //text(current.T, 10, 90);
  //text(current.H, 10, 120);
  fill(0);
  noStroke();
  //text(day(), 10, 180);
  text(languages[l_select][d_month - 1], 50, 180);
  text(d_year, 50, 240);
  fill(0);
  //text(second(), 10, 350);
  //text(minute(), 10, 380);
  //text(hour(), 10, 410);

  text(languages[l_select][16] + d_hive, 380,107);
  
  //print(timer);

  //button(100, 200);

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
      index_line[i] == "6" || index_line[i] == "7" || index_line[i] == "8" || index_line[i] == "9" || index_line[i] == "." || index_line[i] == "-") {

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
  D = float(D);
  T = float(T);
  H = int(H);


  return {
    R,
    D,
    T,
    H
  }

}






/////////////////////////////////////////////////////////
//Button function

function button(x, y, w, h, txt) {

  let status = false;
  
  
  fill(255);
  stroke(1);  
  strokeWeight(1);
  if(mouseX > x && mouseX < x+w && mouseY > y && mouseY < y+h){
    fill(190);
    if(mouseIsPressed){
    fill(100);
      status = true;
    }
  }
  
  
  
  rect(x, y, w, h);
  
  fill(0);
  if(txt != null){
  noStroke();
  textSize(15);
  text(txt, x+10, y+5+(h/2));
  }

return status;

}



///////////////////////////////////////////////////////////////////////////////////////////////////
//graph





function graph(index_line, dataType, currentHive, posX = 0, posY = 0) {
  
  
  // set values
  let tempX, tempY, firstTime = true;
  let flag1 = false,
    flag2 = false;
  let readData;
  let local_h, local_m;
  
  fill(255);
  stroke(0);
  
  //draw rectangle in white background
  rect(posX,posY,320,204);
  
  fill(0);
  
  //display text of what we wan't to show
  textSize(15);
  text((dataType == 'H' ? languages[l_select][12] : languages[l_select][13]), posX - 30, posY-16);
  
  textSize(12);
  ///////////////////////////////////
  //draw grid now
  
  for(let i = 0; i < 21; i+=2){
    
    stroke(100);
    line(posX + 2, (posY+5) + (i*10), posX + 318, (posY+5) + (i*10));
    
    if(dataType == 'H')
    {
    text(100-(i*5), posX - (100-(i*5) >= 100 ? 30 : 100-(i*5) < 10 ? 17 : 23), (posY+10) + (i*10));
    }
    else
    {
      
      
    text(150-(i*10), posX - ((150-(i*10) < 100 && 150-(i*10)) > 0 ? 23 : 28), (posY+10) + (i*10));    
    }
    
  }
  
  ////////////////////////////////////////
  //Show the days on X axis
  
  textSize(15);
  text(languages[l_select][14], posX + 340, posY+220);
  textSize(12);
  for(let i = 0; i < 31; i+=2){
    
    stroke(100);
    line((posX + 10) + (i*10), posY+2, (posX + 10) + (i*10), posY+202);
    text((i+1), (posX + 5) + (i*10), posY+220);
    
  }
  
  
  //////////////////////////////////////////////////////
  
  fill(255);
  
  
  ////////////////////////////////////////////////////
  //Plot the data now
  
  for (let i = 0; i < index_line.length; i++) {
    
    
    
    current = parseData(index_line[i]);
    
    if(current.R == currentHive){ //check hive number

    switch (dataType) { //what data we wan't to have ?

      case 'H':
        readData = current.H; //humidity
        break;

      case 'T':
        readData = current.T; //temperature
        break;


    }

    stroke(0, 0, 0);
    
    if (firstTime) { // first time we plot ?
      
      tempX = (posX + 10) + ((current.D-1) * 10);
      
      if(dataType == 'T')
      {
      tempY = (posY + 155) - (readData);
      }else
      {
      tempY = (posY + 204) - (readData)*2;  
      }
      
      
      strokeWeight(5);
      
      
      //display value if user put mouse on it
      
      if (mouseX > tempX - 5 && mouseX < tempX + 5 && mouseY > tempY - 5 && mouseY < tempY + 5) {
        ////////////////////////////////////
        //Only for the first dot !
        //display the value box when user put the mouse on a dot (and display on the first layer !) !
        rect(mouseX + 10, mouseY + 10, 198, 48);
        textSize(16);
        //text(readData + "%", mouseX + 20, mouseY + 30);
        stroke(255, 0, 0);
        flag1 = true;
        local_h = map(current.D - int(current.D),0, 1, 0, 24); //get hour value (in float value, example : 12h30 → 12.5) //need an int value
        local_m = map(local_h - int(local_h), 0,1,0,60);//get hour value (in float value, example : 50m30 → 50.5 m) //need an int value
        windowMessage = readData + (dataType == 'H' ? "%" : "°C") + "\n" + languages[l_select][17] + int(current.D) + "   " + languages[l_select][18] + int(local_h) + "h" + (int(local_m) > 9 ? int(local_m) : "0" + int(local_m));
        
      }
    
      point(tempX, tempY); // draw the point
      firstTime = false;
    
    } else { // anothers plot ?
      
      
      
      /////////////////////////////////////////////////////////////
      // draw the rest depend on the data type we wan't(to draw in the right scale !)
      if(dataType == 'T')
      {
        
        //////////////////////////////////////////////////
        //Plot temperature values
      
      strokeWeight(1);
      line(tempX, tempY, posX + 10 + ((current.D-1) * 10), posY + 155 - (readData));//rely points values by a line -> so beautiful !!!
      strokeWeight(5);
        
        //display value if user put mouse on it (according to the right coordinates)
        
      if (mouseX > posX + 10 + ((current.D-1) * 10) - 5 && mouseX < posX + 10 + ((current.D-1) * 10) + 5 && mouseY > posY + 155 - (readData) - 5 && mouseY < posY + 155 - (readData) + 5) {
        
        ////////////////////////////////////
        //Only for the first dot !
        //display the value box when user put the mouse on a dot (and display on the first layer !) !
        rect(mouseX + 10, mouseY + 10, 198, 48); 
        textSize(16);
        //text(readData + "°C", mouseX + 20, mouseY + 30);
        stroke(255, 0, 0);
        flag2 = true;
        windowMessage = readData + "°C";
        local_h = map(current.D - int(current.D),0, 1, 0, 24);
        local_m = map(local_h - int(local_h), 0,1,0,60);
        windowMessage = readData + "°C" + "\n" + languages[l_select][17] + int(current.D) + "   " + languages[l_select][18] + int(local_h) + "h" + (int(local_m) > 9 ? int(local_m) : "0" + int(local_m));
        print(windowMessage);
        
      }
      
      point(posX + 10 + ((current.D-1) * 10), posY + 155 - (readData)); //draw points in right X coordinate according to the day

      
      
      }
      else
      {
        
        //////////////////////////////////////////////////
        //Plot humidity values
        
      strokeWeight(1);
      line(tempX, tempY, posX + 10 + ((current.D-1) * 10), posY + 204 - (readData)*2); //rely points values by a line -> so beautiful !!!
      strokeWeight(5);
        
      if (mouseX > posX + 10 + ((current.D-1) * 10) - 5 && mouseX < posX + 10 + ((current.D-1) * 10) + 5 && mouseY > posY + 204 - (readData)*2 - 5 && mouseY < posY + 204 - (readData)*2 + 5) {
        
        rect(mouseX + 10, mouseY + 10, 198, 48);
        textSize(16);
        //text(readData + "%", mouseX + 20, mouseY + 30);
        stroke(255, 0, 0);
        flag2 = true;
        //windowMessage = readData + "%";
        local_h = map(current.D - int(current.D),0, 1, 0, 24);
        local_m = map(local_h - int(local_h), 0,1,0,60);
        windowMessage = readData + "%" + "\n" + languages[l_select][17] + int(current.D) + "   " + languages[l_select][18] + int(local_h) + "h" + (int(local_m) > 9 ? int(local_m) : "0" + int(local_m));
        print(windowMessage);
        
      }
      
      point(posX + 10 + ((current.D-1) * 10), posY + 204 - (readData)*2);//draw points in right X coordinate according to the day
        
      }


      tempX = (posX + 10) + ((current.D-1) * 10);
      if(dataType == 'T')
      {
      tempY = (posY + 155) - (readData);
      }else
      {
      tempY = (posY + 204) - (readData)*2;  
      }
      
    }

    //point(300+(i*10),300-(current.T));  
    
  }//end ofcheck Hive number
    
    
  } // enf of for parse lines

  stroke(0);
  strokeWeight(1);

  ///////////////////////////////////////
  //Only for the others dots (not the first this time !)
  //display the value box when user put the mouse on a dot (and display on the first layer !) !
  if (flag1 || flag2) 
  { 

    rect(mouseX + 10, mouseY + 10, 198, 48);
    textSize(16);
    fill(0);
    text(windowMessage, mouseX + 20, mouseY + 30);
    fill(255);
  }
  //End of graph
  //////////////////////////////////////////////////////////////////////////////////////////////////
}