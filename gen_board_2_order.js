

////////////////////////////////////////////////////

var ws;
received_data = "";
color_list = ["W", "R", "B", "Y", "G"];
game_log = '';
remaining_turns = 2;
var discard_list = new Array(5);
for (var i = 0; i < 5; i++) {
	discard_list[i] = new Array(5);
	discard_list[i] = [0, 0, 0, 0, 0];
}
var turn = 0;
var sum_points = 0;
var PLAYERNUMBER = 2;
var turn_id = new Array(PLAYERNUMBER)
var turn_id2 = new Array(PLAYERNUMBER)
var turn_id3 = new Array(PLAYERNUMBER)
var playername = { 1:'相手', 2:'あなた'}//change_2
var colornumbername ={W:'白(White)', R:'赤(Red)',B:'青(Blue)',Y:'黄(Yellow)',G:'緑(Green)',1:1, 2:2,3:3,4:4,5:5}//change_2
var act = ''
P1_hand = new Array(5);
P2_hand = new Array(5);
P1_buttons = new Array(5);
P2_buttons = new Array(5);

private_ip_addr = '192.168.1.21';
localhost = 'localhost';
/////////////////////////////////////////////////////


function init() {
	// Connect to Web Socket
	ws = new WebSocket("ws://"+ localhost +":9000/");
	// Set event handlers.


	ws.onopen = function () {
		//output("onopen");
	};

	ws.onmessage = function (e) {
		// e.data contains received string.
		//output("onmessage: " + e.data);
		console.log(e.data)
		received_data = e.data;

		if (received_data[0] == 'O'){
			if(received_data[1]=='2'){
				buttons_generate_order(received_data)
				return
			}else{
				received_data_O = received_data
				hint = received_data[2]
				document.getElementById('P2_'+received_data[3]).innerHTML = '<img src="pict/' + hint +'.png" width = "120" height = "150">'
				document.getElementById('P2N_'+received_data[3]).innerHTML = String(5-(received_data.match(/0/g)|| []).length)
				if(received_data.length==8){
					MyFlg = 0;
					hint = received_data_O[2]
					let tenmetsu = setInterval(function(){
						if (MyFlg%2 == 0){
							for (var i = 0; i < 4; i++) {
								place = received_data_O[i+3]
								if (place != '0'){
									document.getElementById('P2_'+place).innerHTML = '<img src="pict/' + hint +'.png" width = "120" height = "150">'
								}
							}
						}else{
							for (var i = 0; i < 4; i++) {
								place = received_data_O[i+3]
								if (place != '0'){
									document.getElementById('P2_'+place).innerHTML = ' <img src="pict/Hanabi_default.png" width = "120" height = "150">';
								}
							}
						}
						if(MyFlg > 5){
							clearInterval(tenmetsu);
						}
						MyFlg+=1
					}, 200);
				}
				return
			}
		}

		if (received_data[130] == '2'){
			for (var i = 0; i < 5; i++) {
				document.getElementById('P2N_'+String(i+1)).innerHTML = '　'
			}
		}


		b_token = received_data[6];
		r_token = received_data[7];
		numofdecks = received_data[8] + received_data[9];
		act = received_data[131] + received_data[132] + received_data[133]
		if ( act === "end") {
			gen_log(e.data)
			sum_points = calculate_points(e.data);
			window.alert("No decks remaining! \n You got " + sum_points + " points !");
			ws.close();
			return true;
		}


		var p = new Promise((resolve,reject) => {
			if(received_data[131] == null){
				console.log("initialization")
				resolve();
			}

			else {
				movement(e.data)
				setTimeout(() => {
					console.log("movement resolve");
					resolve()
				},1200);
			}
			
		});
		movement(e.data)

		p.then((resolve,reject) =>{
			console.log("then called");
			
			check_tokens(received_data);
			hands_generate(received_data);
			check_hand_PO(received_data);
			if(turn % PLAYERNUMBER == 0){//change
				buttons_generate(e.data);
			}else{
				buttons_erase();
			}
			gen_log(e.data);
			gen_turn(Number(received_data[130]));
			gen_turn2(Number(received_data[130]));		
			gen_decks_remaining(received_data[8] + received_data[9]);
			gen_discards();
			if(r_token == 3){
				exit_state();
				window.alert("You have 3 red tokens!! \n Game Over");
				window.close();
				ws.close();
			}
			// if(received_data[134] != null & received_data[131] == 't' & received_data[132] == '2'){
			// 	MyFlg = 0;
			// 	hint = received_data[133]
			// 	place = received_data[134]
			// 	let tenmetsu = setInterval(function(){
			// 		if (MyFlg%2 == 0){
			// 			P2_hand[Number(place)-1].innerHTML = '<img src="pict/' + hint +'.png" width = "120" height = "150">'
			// 		}else{
			// 			P2_hand[Number(place)-1].innerHTML = ' <img src="pict/Hanabi_default.png" width = "120" height = "150">';
			// 		}
			// 		if(MyFlg > 3){
			// 			clearInterval(tenmetsu);
			// 		}
			// 		MyFlg+=1
			// 	}, 500);
				
			// }
		});

		turn += 1
	};

	ws.onclose = function () {
		//output("onclose");
	};
	ws.onerror = function (e) {
		//output("onerror");
		console.log(e)
	};
}

function onSubmit() {

	var input = document.getElementById("input");
	// You can send message to the Web Socket using ws.send.
	ws.send(input.value);
	//output("send: " + input.value);
	//input.value = "";
	//input.focus();
}

function onCloseClick() {
	ws.close();
}

function output(str) {
	var log = document.getElementById("log");
	var escaped = str.replace(/&/, "&amp;").replace(/</, "&lt;").
		replace(/>/, "&gt;").replace(/"/, "&quot;"); // "
	log.innerHTML = escaped + "<br>" + log.innerHTML;
}

function check_fireworks(received_data) {
	var fireworks = new Array(5);
	fireworks[0] = document.getElementById('fw_W');
	fireworks[1] = document.getElementById('fw_R');
	fireworks[2] = document.getElementById('fw_B');
	fireworks[3] = document.getElementById('fw_Y');
	fireworks[4] = document.getElementById('fw_G');

	for (var i = 0; i < 5; i++) {
		for (var j = 0; j < 5; j++) {
			if (received_data[i + 1] == String(j + 1)) {
				fireworks[i].innerHTML = '<img src = "pict/' + color_list[i] + String(j + 1) + '.png" width = "120" height = "150">';
			}
		}
	}
}

function check_tokens(received_data) {
	var blue_token = document.getElementById('blue_token');
	var red_token = document.getElementById('red_token');
	blue_token.innerHTML = '';
	red_token.innerHTML = '';
	for (var i = 0; i < Number(received_data[6]); i++) {
		blue_token.innerHTML += '<img src = "pict/blue_token.png" style = "vertical-align: top;" width = "28" height = "28">';
	}
	for (var i = 0; i < Number(received_data[7]); i++) {
		red_token.innerHTML += '<img src = "pict/red_token.png" style = "vertical-align: bottom;" width = "28" height = "28">';
	}
}

function hands_generate(received_data) {
	for (var i = 0; i < 5; i++) {
		tmp_id = 'P1_' + String(i + 1);
		P1_hand[i] = document.getElementById(tmp_id);
	}
	for (var i = 0; i < 5; i++) {
		tmp_id = 'P2_' + String(i + 1);
		P2_hand[i] = document.getElementById(tmp_id);
	}
	if (received_data[0] == 1) {
		for (var i = 0; i < 5; i++) {
			P2_hand[i].innerHTML = '<img src = "pict/' + received_data[2 * i + 20] + received_data[2 * i + 21] + '.png" width = "120" height = "150">'
			P1_hand[i].innerHTML = '<img src="pict/Hanabi_default.png" width = "120" height = "150">'
		}
	}
	if (received_data[0] == 2) {
		for (var i = 0; i < 5; i++) {
			P1_hand[i].innerHTML = '<img src = "pict/' + received_data[2 * i + 10] + received_data[2 * i + 11] + '.png" width = "120" height = "150">'
			P2_hand[i].innerHTML = '<img src="pict/Hanabi_default.png" width = "120" height = "150">'
		}
	}
}

function check_hand_PO(received_data) {
	var P1_hand_PO = new Array(5);
	var P2_hand_PO = new Array(5);

	for (var i = 0; i < 5; i++) {
		tmp_id = 'P1_' + String(i + 1) + '_PO';
		P1_hand_PO[i] = document.getElementById(tmp_id);
		P1_hand_PO[i].innerHTML = ' ';
	}

	for (var i = 0; i < 5; i++) {
		for (var j = 0; j < 5; j++) {
			P1_hand_PO[i].innerHTML += received_data[2 * j + 10 * i + 30];
			P1_hand_PO[i].innerHTML += ' ';
		}//color
		P1_hand_PO[i].innerHTML += '<br> '
		for (var j = 0; j < 5; j++) {
			if (received_data[2 * j + 10 * i + 31] == '0') {
				P1_hand_PO[i].innerHTML += '_';
			}
			else {
				P1_hand_PO[i].innerHTML += received_data[2 * j + 10 * i + 31];
			}
			P1_hand_PO[i].innerHTML += ' ';
		}//number
		P1_hand_PO[i].innerHTML += '<br>';
	}

	for (var i = 0; i < 5; i++) {
		tmp_id = 'P2_' + String(i + 1) + '_PO';
		P2_hand_PO[i] = document.getElementById(tmp_id);
		P2_hand_PO[i].innerHTML = ' ';
	}

	for (var i = 0; i < 5; i++) {
		for (var j = 0; j < 5; j++) {
			P2_hand_PO[i].innerHTML += received_data[2 * j + 10 * i + 80];
			P2_hand_PO[i].innerHTML += ' ';
		}//color
		P2_hand_PO[i].innerHTML += '<br> '
		for (var j = 0; j < 5; j++) {
			if (received_data[2 * j + 10 * i + 81] == '0') {
				P2_hand_PO[i].innerHTML += '_';
			}
			else {
				P2_hand_PO[i].innerHTML += received_data[2 * j + 10 * i + 81];
			}
			P2_hand_PO[i].innerHTML += ' ';
		}//number
		P2_hand_PO[i].innerHTML += '<br>';
	}
}

function buttons_generate(received_data) {
	for (var h_i = 0; h_i < 5; h_i++) {
		tmp_id = 'P1b_' + String(h_i + 1);
		P1_buttons[h_i] = document.getElementById(tmp_id);
		tmp_id = 'P2b_' + String(h_i + 1);
		P2_buttons[h_i] = document.getElementById(tmp_id);
	}
	if (received_data[0] == 1) {
		for (h_i = 0; h_i < 5; h_i++) {
			P1_buttons[h_i].innerHTML = '<input type = "button" id = "P1_' + String(h_i + 1) + '_play" value = "プレイ" onclick = "gen_message(this)"> <input type = "button" id = "P1_' + String(h_i + 1) + '_discard" value = " 廃棄 " onclick = "gen_message(this)">';
			if (b_token == "0") {
				P2_buttons[h_i].innerHTML = "青トークン無し";
			}
			else {
				P2_buttons[h_i].innerHTML = '<input type = "button" id = "P2_' + String(h_i + 1) + '_color" value = "  色  " onclick = "gen_message(this)"> <input type = "button" id = "P2_' + String(h_i + 1) + '_number" value = " 数字 " onclick = "gen_message(this)">';
			}
		}
	}
	else if (received_data[0] == 2) {
		for (h_i = 0; h_i < 5; h_i++) {
			P2_buttons[h_i].innerHTML = '<input type = "button" id = "P2_' + String(h_i + 1) + '_play" value = "プレイ" onclick = "gen_message(this)"> <input type = "button" id = "P2_' + String(h_i + 1) + '_discard" value = " 廃棄 " onclick = "gen_message(this)">';
			if (b_token == "0") {
				P1_buttons[h_i].innerHTML = "青トークン無し";
			}
			else {
				P1_buttons[h_i].innerHTML = '<input type = "button" id = "P1_' + String(h_i + 1) + '_color" value = "　色　" onclick = "gen_message(this)"> <input type = "button" id = "P1_' + String(h_i + 1) + '_number" value = " 数字 " onclick = "gen_message(this)">';
			}
		}
	}
}

function buttons_erase() {
	for (var h_i = 0; h_i < 5; h_i++) {
		tmp_id = 'P1b_' + String(h_i + 1);
		P1_buttons[h_i] = document.getElementById(tmp_id);
		tmp_id = 'P2b_' + String(h_i + 1);
		P2_buttons[h_i] = document.getElementById(tmp_id);
	}
	for (h_i = 0; h_i < 5; h_i++) {
		P1_buttons[h_i].innerHTML = "相手ターン";
		P2_buttons[h_i].innerHTML = "相手ターン";
	}
}


function gen_message(button) {

	if (received_data[0] == 2) {//change_2
		for (h_i = 0; h_i < 5; h_i++) {
			P2_buttons[h_i].innerHTML = '<input type = "button" id = "P1_' + String(h_i + 1) + '_play" value = "プレイ" onclick = "gen_message(this)" disabled> <input type = "button" id = "P1_' + String(h_i + 1) + '_discard" value = " 廃棄 " onclick = "gen_message(this)" disabled>';
			P1_buttons[h_i].innerHTML = '<input type = "button" id = "P2_' + String(h_i + 1) + '_color" value = "  色  " onclick = "gen_message(this)" disabled> <input type = "button" id = "P2_' + String(h_i + 1) + '_number" value = " 数字 " onclick = "gen_message(this)" disabled>';
		}
	}
	for (var i = 1; i <= 2; i++) {
		for (var j = 1; j <= 5; j++) {
			if (button.id == "P" + String(i) + "_" + String(j) + "_play") {
				ws.send("p," + String(j));
			}
			else if (button.id == "P" + String(i) + "_" + String(j) + "_discard") {
				ws.send("d," + String(j));
			}
			else if (button.id == "P" + String(i) + "_" + String(j) + "_color") {
				ws.send("T," + String(i) + "," + received_data[10 * i + 2 * (j - 1)] + "," + String(j));//change 11/22
			}
			else if (button.id == "P" + String(i) + "_" + String(j) + "_number") {
				ws.send("T," + String(i) + "," + received_data[10 * i + 2 * (j - 1) + 1] + "," + String(j));// change 11/22
			}
		}
	}
}


function buttons_generate_order(received_data) {
	for (var h_i = 0; h_i < 5; h_i++) {
		tmp_id = 'P1b_' + String(h_i + 1);
		P1_buttons[h_i] = document.getElementById(tmp_id);
		tmp_id = 'P2b_' + String(h_i + 1);
		P2_buttons[h_i] = document.getElementById(tmp_id);
	}
	for (h_i = 0; h_i < 5; h_i++) {
		if (received_data.slice(9).includes(String(h_i+1))){
			if (received_data[8] == 'N'){
				P1_buttons[h_i].innerHTML = '<input type = "button" id = "P1_' + String(h_i + 1) + '_color" value = "  色  " onclick = "gen_message(this)" disabled> <input type = "button" id = "P1_' + String(h_i + 1) + '_number" value = " 数字 " onclick = "gen_message_order(this, received_data)">';
			}else{
				P1_buttons[h_i].innerHTML = '<input type = "button" id = "P1_' + String(h_i + 1) + '_color" value = "  色  " onclick = "gen_message_order(this, received_data)"> <input type = "button" id = "P1_' + String(h_i + 1) + '_number" value = " 数字 " onclick = "gen_message(this)" disabled>';
			}
		}
		else {
			P1_buttons[h_i].innerHTML = '';
		}
		P2_buttons[h_i].innerHTML = '';
	}
}

function gen_message_order(button, received_data) {
	ws.send("T," + String(3-Number(received_data[1])) + "," + received_data[2] + "," + button.id[3] +received_data.slice(3,7));
}



function gen_log(received_data) {
	var log_id = document.getElementById('game_log');
	//if(player[2].act_num==4){
	//	log_id.innerHTML = 'Agent is thinking..';
	//}	
	if(received_data[131] + received_data[132] + received_data[133] === 'end'){
		log_id.innerHTML = 'this game is terminated' + '<br>' + log_id.innerHTML;
	}
	for (var i = 1; i <= 2; i++) {

		if (received_data[130] == String(i)) {

			if (received_data[131] == 'p') {
				
				
				string = "" + String(turn - 1) + "ターン目:" + playername[i] + "は" + colornumbername[received_data[132]] +"の"+ received_data[133]+"をプレイしました";//change_2
				log_id.innerHTML = string + '<br>' + log_id.innerHTML;
				for (var j = 0; j < 5; j++) {
					if (color_list[j] == received_data[132]) {
						discard_list[j][Number(received_data[133]) - 1] += 1;
					}
				}
			}
			else if (received_data[131] == 'd') {
				string = "" + String(turn - 1) + "ターン目:" + playername[i] + "は" + received_data[132] +"の"+ received_data[133]+"を廃棄しました";//change_2
				log_id.innerHTML = string + '<br>' + log_id.innerHTML;
				for (var j = 0; j < 5; j++) {
					if (color_list[j] == received_data[132]) {
						discard_list[j][Number(received_data[133]) - 1] += 1;
					}
				}
			}
			else if (received_data[131] == 't') {
				string = "" + String(turn - 1) + "ターン目:" +playername[i] + "は" + colornumbername[received_data[133]] + "のヒントを" + playername[received_data[132]]+"に教えました";//change_2
				log_id.innerHTML = string + '<br>' + log_id.innerHTML;
			}
		}
	}
	// turn += 1
}

function gen_discards() {
	
	for (var i = 0; i < 5; i++) {
		for (var j = 0; j < 5; j++) {
			d_id = document.getElementById("discard_" + color_list[i] + String(j + 1));
			if (discard_list[i][j] > 0) {
				d_id.innerHTML = '';
				for (var k = 1; k <= discard_list[i][j]; k++) {
					d_id.innerHTML += '<img src = "pict/' + color_list[i] + String(j + 1) + '.png" width = "20" height = "28" >';
				}
			}
		}
	}
}

function gen_turn(acted_player){
	if(turn > 1){
		for (var i = 0; i < PLAYERNUMBER ; i++){
			turn_id[i] = document.getElementById("P"+String(i+1)+"_turn");
		}
		if((acted_player + 1) > PLAYERNUMBER){
			turn_id[0].innerHTML = ' <font color = "orangered"> <- TURN </font>';
			//turn_id[0].innerHTML += ' <img src ="pict/dot.gif">'
			for (var i = 1; i < PLAYERNUMBER ; i++){
				turn_id[i].innerHTML = '';
			}
		}
		else{
			turn_id[acted_player].innerHTML = ' <font color = "orangered"> <- TURN </font>';
			//turn_id[acted_player].innerHTML += ' <img src ="pict/dot.gif">'
			for (var i = 0; i < PLAYERNUMBER ; i++){
				if(i != acted_player){
					turn_id[i].innerHTML = '';
				}
			}		
		}
	}
}

function gen_turn2(acted_player){
	if(turn > 1){
		for (var i = 0; i < PLAYERNUMBER ; i++){
			turn_id2[i] = document.getElementById("P"+String(i+1)+"_turn2");
			turn_id3[i] = document.getElementById("P"+String(i+1)+"_turn3");
		}
		if((acted_player + 1) <= PLAYERNUMBER){//change
			// turn_id2[0].innerHTML = ' 考え中... ';
			turn_id3[0].innerHTML = '<img src="pict/playericon.png" width = "150" height = "150">';
			//turn_id[0].innerHTML += ' <img src ="pict/dot.gif">'
			for (var i = 1; i < PLAYERNUMBER ; i++){
				// turn_id2[i].innerHTML = '';
				turn_id3[i].innerHTML = '<img src="pict/agenticon.png" width = "150" height = "150">';
			}
		}
		else{
			// turn_id2[1].innerHTML = ' 考え中... ';
			turn_id3[1].innerHTML = '<img src="pict/agentnayamu2.gif" width = "150" height = "150">';

			// for (var i = 0; i < PLAYERNUMBER ; i++){
			// 	if(i != acted_player){
			// 		turn_id2[i].innerHTML = '';
			// 		turn_id3[i].innerHTML = '<img src="pict/playericon.png" width = "150" height = "150">';
			// 	}
			// }		
		}

	}
}

function gen_decks_remaining(sheets){
	decks = document.getElementById("decks");
	decks.innerHTML = '<img src="pict/Hanabi_default.png" style = "vertical-align: bottom;" width = "40" height = "55">';
	decks.innerHTML += '<span style = "font-size : 150%;"> x ' + sheets + '</span>';
}

function calculate_points(received_data){
	var p = 0;
	for ( var i = 1; i <= 5 ; i++ ){
		p += Number(received_data[i]);
	}
	return p;
}

function movement(received_data){
	if(received_data[131] == null){
		return
	}
	if(received_data[131] == 't'){

		if(received_data[132] == 1){
			for( var i = 0; i < 5 ; i++){
				if(received_data[133] == color_list[i]){
					for ( var j = 0; j < 5 ; j++ ){
						if(received_data[10 + 2*j] == color_list[i]){
							P1_hand[j].innerHTML = '<img src="pict/' + color_list[i] +'.png" width = "120" height = "150">'
						}
					}
				}else if (received_data[133] == String(i + 1)){
					for ( var j = 0 ; j < 5 ; j++ ){
						if(received_data[10 + 2*j + 1] == String(i + 1)){
							P1_hand[j].innerHTML = '<img src="pict/' + String(i + 1) +'.png" width = "120" height = "150">'
						}
					}
				}
			}
		}

		if(received_data[132] == 2){
			for( var i = 0; i < 5 ; i++){
				if(received_data[133] == color_list[i]){
					for ( var j = 0; j < 5 ; j++ ){
						if(received_data[20 + 2*j] == color_list[i]){
							P2_hand[j].innerHTML = '<img src="pict/' + color_list[i] +'.png" width = "120" height = "150">'
						}
					}
				}else if (received_data[133] == String(i + 1)){
					for ( var j = 0 ; j < 5 ; j++ ){
						if(received_data[20 + 2*j + 1] == String(i + 1)){
							P2_hand[j].innerHTML = '<img src="pict/' + String(i + 1) +'.png" width = "120" height = "150">'
						}
					}
				}
			}
		}
		return
	}
	function sleep (msec) {
		return new Promise(resolve => setTimeout(resolve, msec))
	  }



	if(received_data[131] == 'p'){
		fw_id = 'fw_' + received_data[132];
		var e_point_rect = document.getElementById(fw_id).getBoundingClientRect();
	}

	if(received_data[131] == 'd'){
		var e_point_rect = document.getElementById("discard_R3").getBoundingClientRect();
	}

	var hand_id = 'P' + received_data[130] + '_' + String(Number(received_data[134]));
	var hand_rect = document.getElementById(hand_id).getBoundingClientRect();
	var moving_card = document.getElementById('moving_card');
	
	var picture = received_data[132] + received_data[133]
	var dist_x = e_point_rect.left-hand_rect.left
	var dist_y = e_point_rect.top-hand_rect.top
	cos = dist_x/Math.sqrt(Math.pow(dist_x,2) + Math.pow(dist_y,2));
	//console.log(cos)
	sin = (dist_y)/Math.sqrt(Math.pow(dist_x,2) + Math.pow(dist_y,2));
	//console.log(sin);
	var x = hand_rect.left;
	var y = hand_rect.top
	moving_card.innerHTML = '<img  src = pict/' + picture + '.png style = "position:absolute; top:'+ y +'px; left:'+ x +'px; " width = "120" height = "150">'
	var speed = 60;
	var accel = 0.8;
	var time = 0;

	document.getElementById(hand_id).innerHTML = ' <img src="pict/Hanabi_default.png" width = "120" height = "150">';

	var move_card = setInterval(function(){
		time += speed
		x += cos*speed/1.5
		y += sin*speed/1.5
		moving_card.innerHTML = '<img  src = pict/' + picture + '.png style = "position:absolute; top:'+ y +'px; left:'+ x +'px; " width = "120" height = "150">'
		//moving_card.style.left -= stp_x;
			if(x < e_point_rect.left){
			moving_card.innerHTML = ''
			clearInterval(move_card);
			check_fireworks(received_data);
			
			console.log('move finish');
			return;
		}
	}, speed)

	return;

}

function exit_state(){
	for ( i = 0; i < 5 ; i++){
		P1_buttons[i].innerHTML = 'game finished';
		P2_buttons[i].innerHTML = 'game finished';
	}
}
